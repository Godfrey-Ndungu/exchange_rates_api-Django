import importlib
import logging
from django.utils import timezone
from domain.models import AggregatorLog, Bank, Currency, Record
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from decimal import Decimal, InvalidOperation

logger = logging.getLogger(__name__)


class CollectData:
    """
    A service class to collect currency data for a specific bank,
    run a designated spider, and save the resulting records into the database.
    This class handles errors, logging, and updating of currency values for
    buy and sell records.
    """

    def __init__(self, bank_name):
        """
        Initializes the CollectData instance.

        Args:
            bank_name (str): The name of the bank to collect data for.
        """
        self.bank_name = bank_name
        self.bank_name_lower = bank_name.lower()
        self.module_name = f"aggregator.scrapers.spiders.{self.bank_name_lower}_spider" # noqa
        self.class_name = f"{self.bank_name.capitalize()}Spider"
        self.bank = self.get_bank()

    def __call__(self):
        """
        Makes the instance callable, triggering the data collection process
        when the instance is called as a function.
        """
        if self.bank:
            self.collect_and_save_data()
        else:
            logger.error(
                f"Cannot proceed without a valid bank: {self.bank_name}")

    def get_bank(self):
        """
        Retrieves the Bank object by name.

        Returns:
            Bank: The bank instance if found; otherwise,
            logs an error and returns None.
        """
        try:
            return Bank.objects.get(name=self.bank_name)
        except Bank.DoesNotExist:
            logger.error(f"Bank with name '{self.bank_name}' does not exist.")
            return None

    def run_spider(self):
        try:
            spider_module = importlib.import_module(self.module_name)
            spider_class = getattr(spider_module, self.class_name)

            process = CrawlerProcess(get_project_settings())
            # Run the spider by passing the class, not an instance
            process.crawl(spider_class)
            process.start()  # This will block until the crawling is finished

            return getattr(spider_class, "scraped_data", [])
        except ModuleNotFoundError:
            logger.error(f"No spider module found for bank: {self.bank_name}")
        except AttributeError:
            logger.error(
                f"Spider class '{
                    self.class_name}' not found in module: {self.module_name}")
        return None

    def save_record(self, currency_code, buy_value, sell_value):
        """
        Saves buy and sell records for a given currency,
        only if values have changed.

        Args:
            currency_code (str): The code of the currency to save (e.g. "USD").
            buy_value (str): The buy value for the currency as a string.
            sell_value (str): The sell value for the currency as a string.

        Returns:
            bool: True if record is created or updated,
            False if an error occurs.
        """
        try:
            buy_value = Decimal(buy_value) if buy_value not in ["-", None] else None # noqa
            sell_value = Decimal(sell_value) if sell_value not in ["-", None] else None # noqa

            if buy_value is None or sell_value is None:
                logger.warning(
                    f"Skipping record for {
                        currency_code}: Invalid buy/sell values.")
                return False

            currency = Currency.objects.get(short_name=currency_code)
            last_record_buy = Record.objects.filter(bank=self.bank,
                                                    currency=currency,
                                                    type="buy").order_by(
                                                        "-created_at").first()
            last_record_sell = Record.objects.filter(bank=self.bank,
                                                     currency=currency,
                                                     type="sell").order_by(
                                                         "-created_at").first()

            if (last_record_buy and last_record_buy.value == buy_value) and (
                    last_record_sell and last_record_sell.value == sell_value):
                logger.info(f"Skipping record creation for {
                    currency_code} as values have not changed.")
                return True

            Record.objects.create(bank=self.bank,
                                  currency=currency,
                                  type="buy",
                                  value=buy_value)
            Record.objects.create(bank=self.bank, currency=currency,
                                  type="sell", value=sell_value)
            return True
        except InvalidOperation:
            logger.error(
                f"Failed to convert values for {currency_code} to Decimal.")
            return False
        except Currency.DoesNotExist:
            logger.error(f"Currency '{currency_code}' does not exist.")
            return False

    def save_aggregator_log(self, status):
        """
        Creates an aggregator log entry for the bank with the provided status.

        Args:
            status (str): The status of the scraping operation (
            'success' or 'failure').
        """
        AggregatorLog.objects.create(bank=self.bank, status=status)

    def update_last_checked(self):
        """
        Updates the 'last_checked' field of the bank to the current time.
        """
        self.bank.last_checked = timezone.now()
        self.bank.save()

    def collect_and_save_data(self):
        """
        Executes the data collection and saving process:
        - Runs the spider to collect data.
        - Saves records for each currency with valid buy and sell values.
        - Logs the scraping operation's success or failure.
        - Updates the bank's last_checked field.
        """
        scraped_data = self.run_spider()

        if not scraped_data:
            logger.error(f"Scraping failed for bank: {self.bank_name}")
            self.save_aggregator_log("failure")
            self.update_last_checked()
            return

        all_success = True

        for data in scraped_data:
            currency = data.get("currency")
            buy = data.get("buy")
            sell = data.get("sell")

            if buy == "-" or sell == "-" or buy is None or sell is None:
                logger.warning(f"Skipping record for {
                    currency}: Invalid buy/sell values.")
                continue

            if not self.save_record(currency, buy, sell):
                all_success = False

        if all_success:
            logger.info(
                f"Data collection and saving successful for bank: {
                    self.bank_name}")
            self.save_aggregator_log("success")
        else:
            logger.error(
                f"Data collection had failures for bank: {self.bank_name}")
            self.save_aggregator_log("failure")

        self.update_last_checked()
