from django.core.management.base import BaseCommand
from aggregator.services.collect_data import CollectData

class Command(BaseCommand):
    help = "Collect currency data for NCBA Bank using the CollectData service."

    def handle(self, *args, **options):
        self.stdout.write("Starting data collection for NCBA Bank...")

        collector1 = CollectData("NCBA")
        collector2 = CollectData("EQUITY")
        collector3 = CollectData("IM")
        collector3()

        self.stdout.write(self.style.SUCCESS(
            "."))
