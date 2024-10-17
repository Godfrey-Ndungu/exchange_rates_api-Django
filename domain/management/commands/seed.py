from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from domain.models import Bank
from domain.models import Currency


class Command(BaseCommand):
    help = "Seeds the Bank model with a list of banks data."

    def handle(self, *args, **kwargs):
        # -----------------------------------------------------------------------
        banks_data = [
            {
                "name": "NCBA",
                "forex_link": "https://ke.ncbagroup.com/forex-rates/",
                "logo": "https://x.com/NCBABankKenya/photo",
            },
        ]

        for bank_data in banks_data:
            name = bank_data.get('name')
            forex_link = bank_data.get('forex_link')
            logo = bank_data.get('logo')

            try:
                bank = Bank.objects.get(name=name)
                if (bank.forex_link != forex_link or bank.logo != logo):
                    bank.forex_link = forex_link
                    bank.logo = logo
                    bank.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated Bank: {name}'))
                else:
                    self.stdout.write(
                        self.style.NOTICE(f'No changes for Bank: {name}'))
            except Bank.DoesNotExist:
                Bank.objects.create(
                    name=name,
                    forex_link=forex_link,
                    logo=logo,
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created new Bank: {name}'))

        self.stdout.write(self.style.SUCCESS('Bank seeding completed!'))
        # -----------------------------------------------------------------------
        currencies = [
            {"country": "United States", "currency": "United States Dollar", "code": "USD"}, # noqa
            {"country": "European Union", "currency": "Euro", "code": "EUR"}, # noqa# noqa
            {"country": "United Kingdom", "currency": "Pound Sterling", "code": "GBP"},# noqa# noqa
            {"country": "Switzerland", "currency": "Swiss Franc", "code": "CHF"},# noqa
            {"country": "Japan", "currency": "Japanese Yen", "code": "JPY"},
            {"country": "South Africa", "currency": "South African Rand", "code": "ZAR"},# noqa
            {"country": "Norway", "currency": "Norwegian Krone", "code": "NOK"},# noqa
            {"country": "Denmark", "currency": "Danish Krone", "code": "DKK"},
            {"country": "Sweden", "currency": "Swedish Krona", "code": "SEK"},
            {"country": "Canada", "currency": "Canadian Dollar", "code": "CAD"},# noqa
            {"country": "Australia", "currency": "Australian Dollar", "code": "AUD"},# noqa# noqa
            {"country": "Uganda", "currency": "Ugandan Shilling", "code": "UGX"},# noqa
            {"country": "Tanzania", "currency": "Tanzanian Shilling", "code": "TZS"},# noqa# noqa
            {"country": "Hong Kong", "currency": "Hong Kong Dollar", "code": "HKD"},# noqa# noqa
            {"country": "Thailand", "currency": "Thai Baht", "code": "THB"},
            {"country": "United Arab Emirates", "currency": "UAE Dirham", "code": "AED"},# noqa
            {"country": "India", "currency": "Indian Rupee", "code": "INR"},
            {"country": "Rwanda", "currency": "Rwandan Franc", "code": "RWF"},
            {"country": "Burundi", "currency": "Burundian Franc", "code": "BIF"},# noqa
            {"country": "South Sudan", "currency": "South Sudanese Pound", "code": "SSP"}# noqa
        ]

        for currency_data in currencies:
            country = currency_data.get('country')
            name = currency_data.get('currency')
            short_name = currency_data.get('code')

            try:
                currency, created = Currency.objects.get_or_create(
                    country=country,
                    name=name,
                    short_name=short_name
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Created: {name} ({short_name}) for {country}'))
                else:
                    self.stdout.write(self.style.NOTICE(
                        f'Currency: {name} ({short_name}) for {country}'))

            except IntegrityError as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error creating currency for {country}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Currency seeding completed!'))
