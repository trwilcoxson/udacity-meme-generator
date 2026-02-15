"""Ingestor for CSV quote files."""

from typing import List

import pandas as pd

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class CSVIngestor(IngestorInterface):
    """Parse quotes from CSV files using pandas."""

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a CSV file and return a list of QuoteModel objects.

        Expected CSV columns: body, author.

        :param path: Path to the CSV file.
        :return: List of QuoteModel instances.
        """
        if not cls.can_ingest(path):
            raise ValueError(f'Cannot ingest file: {path}')

        quotes = []
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            body = str(row['body']).strip()
            author = str(row['author']).strip()
            if body and author:
                quotes.append(QuoteModel(body, author))
        return quotes
