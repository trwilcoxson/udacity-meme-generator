"""Ingestor for Word (.docx) quote files."""

import logging
from typing import List

from docx import Document

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .exceptions import FileIngestError

logger = logging.getLogger(__name__)


class DocxIngestor(IngestorInterface):
    """Parse quotes from a .docx file.

    Expected format: one quote per paragraph as  "body" - author
    """

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a .docx file and return QuoteModel objects.

        :param path: Path to the .docx file.
        :return: List of QuoteModel instances.
        :raises FileIngestError: If the file cannot be read.
        """
        if not cls.can_ingest(path):
            raise FileIngestError(f"DocxIngestor cannot ingest '{path}'")

        logger.info("Parsing DOCX file: %s", path)

        try:
            doc = Document(path)
        except FileNotFoundError as exc:
            raise FileIngestError(f"File not found: {path}") from exc
        except Exception as exc:
            raise FileIngestError(
                f"Failed to open DOCX file: {path} — {exc}"
            ) from exc

        quotes: List[QuoteModel] = []
        for para in doc.paragraphs:
            quote = cls._parse_quote_line(para.text)
            if quote is not None:
                quotes.append(quote)

        logger.info("Parsed %d quotes from %s", len(quotes), path)
        return quotes
