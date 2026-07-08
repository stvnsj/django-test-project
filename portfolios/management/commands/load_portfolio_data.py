
from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from portfolios.etl import load_portfolio_data


class Command(BaseCommand):
    help = "Load portfolio data from Excel file."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("file_path", type=str)

    def handle(self, *_args: Any, **options: Any) -> None:
        file_path = options["file_path"]

        load_portfolio_data(file_path)

        self.stdout.write("Portfolio data loaded successfully.")
