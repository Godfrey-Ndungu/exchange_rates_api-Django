import logging
from django.utils import timezone
import importlib

from domain.models import Bank, Currency, Record, AggregatorLog

logger = logging.getLogger(__name__)


class CollectData:
    def __init__(self, bank_name):
        self.bank_name_lower = self.bank_name.lower()
        self.module_name = f'aggregator.scrapers.spiders.{self.bank_name_lower}_spider'# noqa
        self.class_name = f'{self.bank_name.capitalize()}Spider'

    def get_bank(self):
        # Retrieve the bank by name, return None if it doesn't exist
        try:
            return Bank.objects.get(name=self.bank_name)
        except Bank.DoesNotExist:
            logger.error(f"Bank with name '{self.bank_name}' does not exist.")
            return None

    def run_spider(self):
        try:
            # Dynamically import the module
            spider_module = importlib.import_module(self.module_name)
            # Get the spider class dynamically
            spider_class = getattr(spider_module, self.class_name)
            # Instantiate the spider class and call start_requests
            return spider_class().start_requests()
        except ModuleNotFoundError:
            logger.error(f"No spider module found for bank: {self.bank_name}")
        except AttributeError:
            logger.error(
                f"Spider class '{self.class_name}' not found in module: {self.module_name}") # noqa
        return None

    def save_record(self, currency_code, buy_value, sell_value):
        try:
            currency = Currency.objects.get(short_name=currency_code)
            Record.objects.create(
                bank=self.bank,
                currency=currency,
                type="buy",
                value=buy_value
            )
            Record.objects.create(
                bank=self.bank,
                currency=currency,
                type="sell",
                value=sell_value
            )
            return True
        except Currency.DoesNotExist:
            logger.error(
                f"Currency '{currency_code}' does not exist")
            return False

    def save_aggregator_log(self, status):
        AggregatorLog.objects.create(
            bank=self.bank,
            type="scrape",
            status=status
        )

    def update_last_checked(self):
        self.bank.last_checked = timezone.now()
        self.bank.save()

    def process_data(self):
        # Make sure the bank exists
        if not self.bank:
            logger.error(
                f"Cannot proceed without a valid bank: {self.bank_name}")
            return

        # Run the spider to get the data
        scraped_data = self.run_spider()
        if not scraped_data:
            logger.error(f"Scraping failed for bank: {self.bank_name}")
            self.save_aggregator_log("failure")
            return

        # Process each row of scraped data
        all_success = True
        for data in scraped_data:
            currency = data.get("currency")
            buy = data.get("buy")
            sell = data.get("sell")

            # Save the records to the database
            success = self.save_record(currency, buy, sell)
            if not success:
                all_success = False
        # Log the outcome
        if all_success:
            self.save_aggregator_log("success")
        else:
            self.save_aggregator_log("failure")

        # Update the last_checked timestamp
        self.update_last_checked()
