"""Abstract base class for quote ingestors."""

from abc import ABC, abstractmethod
from typing import List

from .QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """Define the interface for all file ingestors."""

    allowed_extensions: List[str] = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check whether this ingestor can handle the given file.

        :param path: Path to the file to check.
        :return: True if the file extension is supported.
        """
        ext = path.rsplit('.', 1)[-1].lower() if '.' in path else ''
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the given file and return a list of QuoteModel objects.

        :param path: Path to the file to parse.
        :return: List of QuoteModel instances.
        """
