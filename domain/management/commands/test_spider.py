from multiprocessing import Process
from django.core.management.base import BaseCommand
from aggregator.services.collect_data import CollectData


def run_collector(bank_name):
    """
    Runs the CollectData service for a specific bank in a separate process.
    """
    collector = CollectData(bank_name)
    collector()


class Command(BaseCommand):
    help = "Collect currency data for multiple banks using the CollectData service."

    def handle(self, *args, **options):
        self.stdout.write("Starting data collection for multiple banks...")

        # List of bank names
        banks = ["NCBA", "EQUITY", "IM", "Africa", "Prime"]

        # Create and start a separate process for each bank
        processes = []
        for bank_name in banks:
            process = Process(target=run_collector, args=(bank_name,))
            process.start()
            processes.append(process)

        # Wait for all processes to complete
        for process in processes:
            process.join()

        self.stdout.write(self.style.SUCCESS("Data collection completed."))
