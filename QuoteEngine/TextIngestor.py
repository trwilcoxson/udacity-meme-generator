"""Ingestor for plain-text (.txt) quote files."""

import logging
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .exceptions import FileIngestError

logger = logging.getLogger(__name__)


class TextIngestor(IngestorInterface):
    """Parse quotes from a plain-text file.

    Expected format: one quote per line as  "body" - author
    """

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a .txt file and return QuoteModel objects.

        :param path: Path to the .txt file.
        :return: List of QuoteModel instances.
        :raises FileIngestError: If the file cannot be read.
        """
        if not cls.can_ingest(path):
            raise FileIngestError(f"TextIngestor cannot ingest '{path}'")

        logger.info("Parsing text file: %s", path)
        quotes: List[QuoteModel] = []

        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    quote = cls._parse_quote_line(line)
                    if quote is not None:
                        quotes.append(quote)
        except FileNotFoundError as exc:
            raise FileIngestError(f"File not found: {path}") from exc
        except PermissionError as exc:
            raise FileIngestError(f"Permission denied: {path}") from exc
        except UnicodeDecodeError as exc:
            raise FileIngestError(
                f"Cannot decode file (not valid UTF-8): {path}"
            ) from exc

        logger.info("Parsed %d quotes from %s", len(quotes), path)
        return quotes
