"""QuoteEngine package — parse quotes from various file formats."""

from .Ingestor import Ingestor
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel

__all__ = ['Ingestor', 'IngestorInterface', 'QuoteModel']
