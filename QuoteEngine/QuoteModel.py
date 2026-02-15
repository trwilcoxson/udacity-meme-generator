"""QuoteModel module for encapsulating quote data."""


class QuoteModel:
    """Represent a quote with a body and an author."""

    def __init__(self, body: str, author: str):
        """Create a new QuoteModel.

        :param body: The text of the quote.
        :param author: The author of the quote.
        """
        self.body = body
        self.author = author

    def __repr__(self) -> str:
        """Return a human-readable string representation."""
        return f'"{self.body}" - {self.author}'
