"""Ingestor for DOCX quote files."""

from typing import List

from docx import Document

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class DocxIngestor(IngestorInterface):
    """Parse quotes from DOCX files using python-docx."""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a DOCX file and return a list of QuoteModel objects.

        Each paragraph should contain a quote in the format:
        "body" - author

        :param path: Path to the DOCX file.
        :return: List of QuoteModel instances.
        """
        if not cls.can_ingest(path):
            raise ValueError(f'Cannot ingest file: {path}')

        quotes = []
        doc = Document(path)
        for para in doc.paragraphs:
            line = para.text.strip()
            if ' - ' in line:
                parts = line.rsplit(' - ', 1)
                body = parts[0].strip().strip('"')
                author = parts[1].strip()
                if body and author:
                    quotes.append(QuoteModel(body, author))
        return quotes
