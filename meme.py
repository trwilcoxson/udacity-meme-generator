"""CLI tool for generating motivational memes."""

import argparse
import os
import random

from QuoteEngine import Ingestor, QuoteModel
from MemeEngine import MemeEngine


def generate_meme(path=None, body=None, author=None):
    """Generate a meme from the given arguments.

    If no arguments are provided, a random image and quote are selected
    from the sample data.

    :param path: Path to an image file.
    :param body: Quote body text.
    :param author: Quote author.
    :return: Path to the generated meme image.
    """
    if path is None:
        images_dir = './_data/photos/dog/'
        imgs = [
            os.path.join(images_dir, f)
            for f in os.listdir(images_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        path = random.choice(imgs)

    if body is None:
        quote_files = [
            './_data/DogQuotes/DogQuotesTXT.txt',
            './_data/DogQuotes/DogQuotesCSV.csv',
            './_data/DogQuotes/DogQuotesDOCX.docx',
            './_data/DogQuotes/DogQuotesPDF.pdf',
            './_data/SimpleLines/SimpleLines.txt',
            './_data/SimpleLines/SimpleLines.csv',
            './_data/SimpleLines/SimpleLines.docx',
            './_data/SimpleLines/SimpleLines.pdf',
        ]
        quotes = []
        for qf in quote_files:
            if os.path.exists(qf):
                try:
                    quotes.extend(Ingestor.parse(qf))
                except Exception:
                    pass
        quote = random.choice(quotes)
        body = quote.body
        author = quote.author

    meme = MemeEngine('./tmp')
    output_path = meme.make_meme(path, body, author)
    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a motivational meme.'
    )
    parser.add_argument('--path', type=str, default=None,
                        help='Path to an image file.')
    parser.add_argument('--body', type=str, default=None,
                        help='Quote body text.')
    parser.add_argument('--author', type=str, default=None,
                        help='Quote author (required if --body is given).')

    args = parser.parse_args()

    if args.body is not None and args.author is None:
        parser.error('--author is required when --body is provided.')

    print(generate_meme(args.path, args.body, args.author))
