import random
from django.core.management.base import BaseCommand
from faker import Faker
from domain.models import Bank, Currency, Record, AggregatorLog

fake = Faker()

STATUS_CHOICES = ['success', 'failure']
TYPE_CHOICES = ['buy', 'sell']


class Command(BaseCommand):
    help = 'Generate sample data for banks, currencies, and records'

    def handle(self, *args, **kwargs):
        self.generate_banks(10)
        self.generate_currencies(10)
        self.generate_records(1000)
        self.stdout.write(self.style.SUCCESS(
            'Successfully generated sample data'))

    def generate_banks(self, count):
        for _ in range(count):
            bank = Bank.objects.create(
                logo=fake.image_url(),
                name=fake.company(),
                buy_link=fake.url(),
                sell_link=fake.url(),
                last_checked=fake.date_time_this_year()
            )
            # Generate logs for each bank
            for _ in range(5):  # Generate 5 logs per bank
                AggregatorLog.objects.create(
                    bank=bank,
                    type=random.choice(TYPE_CHOICES),
                    status=random.choice(STATUS_CHOICES)
                )
        self.stdout.write(self.style.SUCCESS(f'{count} banks created'))

    def generate_currencies(self, count):
        for _ in range(count):
            Currency.objects.create(
                country_flag=fake.image_url(),
                name=fake.currency_name(),
                country=fake.country(),
                short_name=fake.currency_code()
            )
        self.stdout.write(self.style.SUCCESS(f'{count} currencies created'))

    def generate_records(self, count):
        banks = list(Bank.objects.all())
        currencies = list(Currency.objects.all())

        for _ in range(count):
            Record.objects.create(
                bank=random.choice(banks),
                currency=random.choice(currencies),
                type=random.choice(TYPE_CHOICES),
                value=fake.pydecimal(left_digits=4, right_digits=2,
                                     positive=True)
            )
        self.stdout.write(self.style.SUCCESS(f'{count} records created'))
