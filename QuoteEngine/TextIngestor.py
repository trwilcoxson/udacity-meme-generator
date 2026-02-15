"""Ingestor for plain text quote files."""

from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class TextIngestor(IngestorInterface):
    """Parse quotes from plain text files."""

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a text file and return a list of QuoteModel objects.

        Each line should be in the format: "body" - author

        :param path: Path to the text file.
        :return: List of QuoteModel instances.
        """
        if not cls.can_ingest(path):
            raise ValueError(f'Cannot ingest file: {path}')

        quotes = []
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if ' - ' in line and len(line) > 3:
                    parts = line.rsplit(' - ', 1)
                    body = parts[0].strip().strip('"')
                    author = parts[1].strip()
                    if body and author:
                        quotes.append(QuoteModel(body, author))
        return quotes
