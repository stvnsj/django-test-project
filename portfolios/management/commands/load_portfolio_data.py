
from django.core.management.base import BaseCommand

from portfolios.etl import load_portfolio_data


class Command(BaseCommand):
    help = "Load portfolio data from Excel file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        
        file_path = options["file_path"]
        load_portfolio_data(file_path)
        self.stdout.write(self.style.SUCCESS("Portfolio data loaded successfully."))
