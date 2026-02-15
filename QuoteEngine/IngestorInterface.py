"""Abstract base class for all file ingestors."""

import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from .QuoteModel import QuoteModel

logger = logging.getLogger(__name__)


class IngestorInterface(ABC):
    """Abstract base class defining the ingestor interface.

    Subclasses must set ``allowed_extensions`` and implement
    ``parse``.  Shared helpers such as ``_parse_quote_line``
    live here so that child classes stay DRY.
    """

    allowed_extensions: List[str] = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check whether this ingestor can handle the given file.

        :param path: Path to the file.
        :return: True if the file extension is supported.
        """
        ext = path.rsplit('.', 1)[-1].lower() if '.' in path else ''
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the file and return a list of QuoteModel objects.

        :param path: Path to the file to parse.
        :return: List of QuoteModel instances.
        """
        ...

    # ---------------------------------------------------------------
    # Shared helpers available to all child ingestors
    # ---------------------------------------------------------------

    @staticmethod
    def _parse_quote_line(line: str) -> Optional[QuoteModel]:
        """Parse a single ``"body" - author`` line into a QuoteModel.

        Returns ``None`` when the line is blank or malformed so
        callers can simply filter.

        :param line: Raw text line.
        :return: A QuoteModel or None.
        """
        line = line.strip()
        if not line or ' - ' not in line:
            if line:
                logger.warning("Skipping malformed line: %s", line)
            return None
        body, author = line.rsplit(' - ', 1)
        body = body.strip().strip('"')
        return QuoteModel(body, author)
