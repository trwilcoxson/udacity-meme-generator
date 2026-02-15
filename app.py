"""Flask web application for generating memes."""

import logging
import os
import random
import tempfile

import requests
from flask import Flask, render_template, request

from MemeEngine import MemeEngine
from MemeEngine.exceptions import MemeGenerationError
from QuoteEngine import Ingestor
from QuoteEngine.exceptions import QuoteEngineError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s — %(name)s — %(levelname)s — %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """Load all resources."""
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

    images_path = './_data/photos/dog/'
    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs.extend(
            os.path.join(root, name)
            for name in files
            if name.lower().endswith(('.jpg', '.jpeg', '.png'))
        )

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user-defined meme."""
    image_url = request.form.get('image_url')
    body = request.form.get('body', '')
    author = request.form.get('author', '')

    tmp_fd, tmp_path = tempfile.mkstemp(suffix='.jpg')
    os.close(tmp_fd)

    try:
        response = requests.get(image_url, timeout=15)
        response.raise_for_status()
        with open(tmp_path, 'wb') as f:
            f.write(response.content)

        path = meme.make_meme(tmp_path, body, author)
    except requests.RequestException as exc:
        logger.error("Failed to download image: %s", exc)
        return render_template('meme_form.html'), 400
    except MemeGenerationError as exc:
        logger.error("Meme generation failed: %s", exc)
        return render_template('meme_form.html'), 400
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return render_template('meme.html', path=path)


if __name__ == '__main__':
    app.run()
