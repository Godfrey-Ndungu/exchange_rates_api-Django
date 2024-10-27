import importlib
import logging

from django.utils import timezone

from domain.models import AggregatorLog, Bank, Currency, Record

logger = logging.getLogger(__name__)


class CollectData:
    """
    A service class to collect currency data for a specific bank,
    run a designated spider,and save the resulting records into the database.
    This class handles errors, logging,and updating of currency values for
    buy and sell records.

    Attributes:
        bank_name (str): The name of the bank for which data is collected.
        bank_name_lower (str): Lowercase version of the bank name, used to
        locate the spider module.module_name (str): Full path of the spider
        module based on bank name.
        class_name (str): Expected class name of the spider based on bank name.
    """

    def __init__(self, bank_name):
        """
        Initializes the CollectData instance.

        Args:
            bank_name (str): The name of the bank to collect data for.
        """
        self.bank_name = bank_name
        self.bank_name_lower = bank_name.lower()
        self.module_name = f"aggregator.scrapers.spiders.{
            self.bank_name_lower}_spider"
        self.class_name = f"{self.bank_name.capitalize()}Spider"

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
        """
        Imports and initiates the spider class for the bank
        to collect currency data.

        Returns:
            list[dict]: List of dictionaries with scraped data if successful;
            None otherwise.
        """
        try:
            spider_module = importlib.import_module(self.module_name)
            spider_class = getattr(spider_module, self.class_name)
            return spider_class().start_requests()
        except ModuleNotFoundError:
            logger.error(f"No spider module found for bank: {self.bank_name}")
        except AttributeError:
            logger.error(
                f"Spider class '{
                    self.class_name}' not found in module: {self.module_name}"
            )
        return None

    def save_record(self, currency_code, buy_value, sell_value):
        """
        Saves buy and sell records for a given currency,
        only if values have changed.

        Args:
            currency_code (str): The code of the currency to save (e.g."USD").
            buy_value (Decimal): The buy value for the currency.
            sell_value (Decimal): The sell value for the currency.

        Returns:
            bool: True if record is created or updated,
            False if an error occurs.
        """
        try:
            currency = Currency.objects.get(short_name=currency_code)
            last_record_buy = (
                Record.objects.filter(
                    bank=self.bank, currency=currency, type="buy")
                .order_by("-created_at")
                .first()
            )
            last_record_sell = (
                Record.objects.filter(
                    bank=self.bank, currency=currency, type="sell")
                .order_by("-created_at")
                .first()
            )

            if (last_record_buy and last_record_buy.value == buy_value) and (
                last_record_sell and last_record_sell.value == sell_value
            ):
                logger.info(
                    f"Skipping record creation for {
                        currency_code} as values have not changed."
                )
                return True

            Record.objects.create(
                bank=self.bank, currency=currency, type="buy", value=buy_value
            )
            Record.objects.create(
                bank=self.bank,
                currency=currency,
                type="sell",
                value=sell_value
            )
            return True
        except Currency.DoesNotExist:
            logger.error(f"Currency '{currency_code}' does not exist")
            return False

    def save_aggregator_log(self, status):
        """
        Creates an aggregator log entry for the bank with the provided status.

        Args:
            status (str): The status of the scraping operation
            ('success' or 'failure').
        """
        AggregatorLog.objects.create(bank=self.bank,
                                     type="scrape",
                                     status=status)

    def update_last_checked(self):
        """
        Updates the 'last_checked' field of the bank to the current time.
        """
        self.bank.last_checked = timezone.now()
        self.bank.save()

    def process_data(self):
        """
        Main method to run the entire data collection process:
        - Retrieves the bank.
        - Runs the spider to collect data.
        - Saves records for each currency with updated buy and sell values.
        - Logs the scraping operation's success or failure.
        - Updates the bank's last_checked field.

        Logs errors and updates the aggregator log in case of failure.
        """
        self.bank = self.get_bank()
        if not self.bank:
            logger.error(f"Cannot proceed without a valid bank: {
                self.bank_name}")
            return

        scraped_data = self.run_spider()
        if not scraped_data:
            logger.error(f"Scraping failed for bank: {self.bank_name}")
            self.save_aggregator_log("failure")
            return

        all_success = True
        for data in scraped_data:
            currency = data.get("currency")
            buy = data.get("buy")
            sell = data.get("sell")

            success = self.save_record(currency, buy, sell)
            if not success:
                all_success = False

        if all_success:
            self.save_aggregator_log("success")
        else:
            self.save_aggregator_log("failure")

        self.update_last_checked()
