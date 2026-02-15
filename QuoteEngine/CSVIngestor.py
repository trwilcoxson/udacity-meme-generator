"""Ingestor for CSV (.csv) quote files."""

import logging
from typing import List

import pandas as pd

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .exceptions import FileIngestError

logger = logging.getLogger(__name__)


class CSVIngestor(IngestorInterface):
    """Parse quotes from a CSV file with 'body' and 'author' columns."""

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a .csv file and return QuoteModel objects.

        :param path: Path to the .csv file.
        :return: List of QuoteModel instances.
        :raises FileIngestError: If the file cannot be read or is malformed.
        """
        if not cls.can_ingest(path):
            raise FileIngestError(f"CSVIngestor cannot ingest '{path}'")

        logger.info("Parsing CSV file: %s", path)

        try:
            df = pd.read_csv(path)
        except FileNotFoundError as exc:
            raise FileIngestError(f"File not found: {path}") from exc
        except pd.errors.EmptyDataError as exc:
            raise FileIngestError(f"CSV file is empty: {path}") from exc
        except pd.errors.ParserError as exc:
            raise FileIngestError(
                f"CSV file is malformed: {path}"
            ) from exc

        required = {'body', 'author'}
        if not required.issubset(df.columns):
            missing = required - set(df.columns)
            raise FileIngestError(
                f"CSV missing required columns {missing}: {path}"
            )

        quotes = [
            QuoteModel(str(row['body']), str(row['author']))
            for _, row in df.iterrows()
        ]
        logger.info("Parsed %d quotes from %s", len(quotes), path)
        return quotes
