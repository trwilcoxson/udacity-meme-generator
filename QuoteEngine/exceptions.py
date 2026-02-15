"""Custom exceptions for the QuoteEngine module."""


class QuoteEngineError(Exception):
    """Base exception for QuoteEngine errors."""

    pass


class UnsupportedFileTypeError(QuoteEngineError):
    """Raised when a file type is not supported by any ingestor."""

    def __init__(self, path: str) -> None:
        """Create exception with the unsupported file path."""
        ext = path.rsplit('.', 1)[-1] if '.' in path else 'unknown'
        super().__init__(
            f"Unsupported file type '.{ext}' for file: {path}"
        )


class FileIngestError(QuoteEngineError):
    """Raised when a file cannot be parsed by its ingestor."""

    pass
