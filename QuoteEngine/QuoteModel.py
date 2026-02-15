"""QuoteModel encapsulates a quote body and author."""


class QuoteModel:
    """Represent a quote with a body and an author."""

    def __init__(self, body: str, author: str) -> None:
        """Create a new QuoteModel.

        :param body: The text of the quote.
        :param author: The author of the quote.
        """
        self.body = body.strip()
        self.author = author.strip()

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return f'QuoteModel(body="{self.body}", author="{self.author}")'

    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return f'"{self.body}" - {self.author}'
