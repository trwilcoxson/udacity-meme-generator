"""CLI tool for generating memes with random or user-supplied quotes."""

import argparse
import logging
import os
import random

from MemeEngine import MemeEngine
from QuoteEngine import Ingestor, QuoteModel
from QuoteEngine.exceptions import QuoteEngineError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s — %(name)s — %(levelname)s — %(message)s'
)
logger = logging.getLogger(__name__)


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an image path and a quote.

    :param path: Path to a source image (random if None).
    :param body: Quote body text (random if None).
    :param author: Quote author (required when body is given).
    :return: File path of the generated meme.
    """
    if path is None:
        images_dir = './_data/photos/dog/'
        imgs = []
        for root, dirs, files in os.walk(images_dir):
            imgs.extend(
                os.path.join(root, name)
                for name in files
                if name.lower().endswith(('.jpg', '.jpeg', '.png'))
            )
        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = [
            './_data/DogQuotes/DogQuotesTXT.txt',
            './_data/DogQuotes/DogQuotesDOCX.docx',
            './_data/DogQuotes/DogQuotesPDF.pdf',
            './_data/DogQuotes/DogQuotesCSV.csv',
        ]
        quotes = []
        for f in quote_files:
            try:
                quotes.extend(Ingestor.parse(f))
            except QuoteEngineError as exc:
                logger.warning("Could not parse '%s': %s", f, exc)
        if not quotes:
            raise QuoteEngineError("No quotes could be loaded from any file")
        quote = random.choice(quotes)
    else:
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    out = meme.make_meme(img, quote.body, quote.author)
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a meme image.')
    parser.add_argument('--path', type=str, default=None,
                        help='Path to an image file')
    parser.add_argument('--body', type=str, default=None,
                        help='Quote body to add to the image')
    parser.add_argument('--author', type=str, default=None,
                        help='Quote author to add to the image')
    args = parser.parse_args()

    if args.body and not args.author:
        parser.error('--author is required when --body is provided')

    print(generate_meme(args.path, args.body, args.author))
