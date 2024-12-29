import os
from django.core.management.base import BaseCommand
from aggregator.services.collect_data import CollectData

class Command(BaseCommand):
    help = "Collect currency data for multiple banks using the CollectData service."

    def get_last_processed_bank(self):
        """Retrieve the last processed bank from a file or database."""
        try:
            with open('last_processed_bank.txt', 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            return None

    def set_last_processed_bank(self, bank_name):
        """Set the last processed bank in a file."""
        with open('last_processed_bank.txt', 'w') as file:
            file.write(bank_name)

    def get_next_bank(self, current_bank):
        """Get the next bank in the list after the current one."""
        banks = ["NCBA", "EQUITY", "IM", "Africa", "Prime"]
        try:
            current_index = banks.index(current_bank)
            return banks[current_index + 1] if current_index + 1 < len(banks) else banks[0]  # Start over after last bank
        except ValueError:
            return banks[0]  # Default to the first bank if current_bank is None

    def handle(self, *args, **options):
        self.stdout.write("Starting data collection for multiple banks...")

        # Get the last processed bank (if any)
        last_processed_bank = self.get_last_processed_bank()

        # Determine the next bank to process
        next_bank = self.get_next_bank(last_processed_bank)

        self.stdout.write(f"Starting data collection for {next_bank}...")
        collector = CollectData(next_bank)
        collector()  # Run the collection process for the current bank

        # After processing, update the last processed bank
        self.set_last_processed_bank(next_bank)

        self.stdout.write(self.style.SUCCESS(f"Data collection successful for {next_bank}."))
