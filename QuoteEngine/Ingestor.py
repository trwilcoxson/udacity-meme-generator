"""Facade ingestor that delegates to the appropriate file-type ingestor."""

import logging
from typing import List

from .CSVIngestor import CSVIngestor
from .DocxIngestor import DocxIngestor
from .IngestorInterface import IngestorInterface
from .PDFIngestor import PDFIngestor
from .QuoteModel import QuoteModel
from .TextIngestor import TextIngestor
from .exceptions import UnsupportedFileTypeError

logger = logging.getLogger(__name__)


class Ingestor(IngestorInterface):
    """Select and delegate to the correct ingestor for a given file."""

    ingestors = [CSVIngestor, DocxIngestor, PDFIngestor, TextIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a file by delegating to the matching ingestor.

        :param path: Path to the quote file.
        :return: List of QuoteModel instances.
        :raises UnsupportedFileTypeError: If no ingestor supports the file.
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                logger.info(
                    "Delegating '%s' to %s",
                    path, ingestor.__name__
                )
                return ingestor.parse(path)

        raise UnsupportedFileTypeError(path)
