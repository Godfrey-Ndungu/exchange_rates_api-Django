from django.core.management.base import BaseCommand
from domain.models import Bank


class Command(BaseCommand):
    help = "Seeds the Bank model with a list of banks data."

    def handle(self, *args, **kwargs):
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
