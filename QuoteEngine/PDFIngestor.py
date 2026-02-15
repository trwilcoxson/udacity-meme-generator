"""Ingestor for PDF quote files."""

import os
import subprocess
import tempfile
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class PDFIngestor(IngestorInterface):
    """Parse quotes from PDF files using the pdftotext CLI tool."""

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a PDF file and return a list of QuoteModel objects.

        Uses subprocess to call pdftotext, then parses the text output.
        Each line should be in the format: "body" - author

        :param path: Path to the PDF file.
        :return: List of QuoteModel instances.
        """
        if not cls.can_ingest(path):
            raise ValueError(f'Cannot ingest file: {path}')

        tmp_file = tempfile.NamedTemporaryFile(
            suffix='.txt', delete=False
        )
        tmp_path = tmp_file.name
        tmp_file.close()

        try:
            subprocess.run(
                ['pdftotext', path, tmp_path],
                check=True,
                capture_output=True,
            )

            quotes = []
            with open(tmp_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if ' - ' in line and len(line) > 3:
                        parts = line.rsplit(' - ', 1)
                        body = parts[0].strip().strip('"')
                        author = parts[1].strip()
                        if body and author:
                            quotes.append(QuoteModel(body, author))
            return quotes
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
