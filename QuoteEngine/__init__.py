"""QuoteEngine package for ingesting quotes from various file formats."""

from .QuoteModel import QuoteModel
from .Ingestor import Ingestor
from .IngestorInterface import IngestorInterface
from .CSVIngestor import CSVIngestor
from .DocxIngestor import DocxIngestor
from .PDFIngestor import PDFIngestor
from .TextIngestor import TextIngestor
