"""Main ingestor that implements the strategy pattern."""

from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .CSVIngestor import CSVIngestor
from .DocxIngestor import DocxIngestor
from .PDFIngestor import PDFIngestor
from .TextIngestor import TextIngestor


class Ingestor(IngestorInterface):
    """Select the appropriate ingestor based on file extension.

    This class implements the strategy pattern, acting as a single
    entry point for ingesting quotes from any supported file type.
    """

    ingestors = [CSVIngestor, DocxIngestor, PDFIngestor, TextIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a file by delegating to the appropriate ingestor.

        :param path: Path to the quote file.
        :return: List of QuoteModel instances.
        :raises ValueError: If no suitable ingestor is found.
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f'No ingestor found for file: {path}')
