"""Ingestor for PDF (.pdf) quote files using pdftotext."""

import logging
import os
import subprocess
import tempfile
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .exceptions import FileIngestError

logger = logging.getLogger(__name__)


class PDFIngestor(IngestorInterface):
    """Parse quotes from a PDF file via the pdftotext CLI tool.

    Requires the ``pdftotext`` utility (part of Poppler / Xpdf).
    Install with ``brew install poppler`` on macOS or
    ``sudo apt-get install poppler-utils`` on Ubuntu/Debian.
    """

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a .pdf file and return QuoteModel objects.

        :param path: Path to the .pdf file.
        :return: List of QuoteModel instances.
        :raises FileIngestError: If the file cannot be read or
            pdftotext is not installed.
        """
        if not cls.can_ingest(path):
            raise FileIngestError(f"PDFIngestor cannot ingest '{path}'")

        if not os.path.isfile(path):
            raise FileIngestError(f"File not found: {path}")

        logger.info("Parsing PDF file: %s", path)

        tmp_fd, tmp_path = tempfile.mkstemp(suffix='.txt')
        os.close(tmp_fd)

        try:
            result = subprocess.run(
                ['pdftotext', '-layout', path, tmp_path],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                raise FileIngestError(
                    f"pdftotext failed on '{path}': {result.stderr.strip()}"
                )

            with open(tmp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError as exc:
            raise FileIngestError(
                "pdftotext is not installed. Install with: "
                "brew install poppler (macOS) or "
                "sudo apt-get install poppler-utils (Linux)"
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise FileIngestError(
                f"pdftotext timed out on '{path}'"
            ) from exc
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        quotes: List[QuoteModel] = []
        for line in lines:
            quote = cls._parse_quote_line(line)
            if quote is not None:
                quotes.append(quote)

        logger.info("Parsed %d quotes from %s", len(quotes), path)
        return quotes
