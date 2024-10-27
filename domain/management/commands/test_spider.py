from django.core.management.base import BaseCommand
from aggregator.services.collect_data import CollectData


class Command(BaseCommand):
    help = "Collect currency data for NCBA Bank using the CollectData service."

    def handle(self, *args, **options):
        self.stdout.write("Starting data collection for NCBA Bank...")

        collector = CollectData("NCBA")
        collector()  # Run the data collection process using __call__

        self.stdout.write(self.style.SUCCESS(
            "Data collection for NCBA Bank completed successfully."))
