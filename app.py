"""Flask web application for generating motivational memes."""

import os
import random
import tempfile

import requests
from flask import Flask, render_template, request, send_from_directory

from QuoteEngine import Ingestor
from MemeEngine import MemeEngine

app = Flask(__name__)

meme_engine = MemeEngine('./tmp')


def setup():
    """Load all quotes and image paths from the sample data."""
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

    images_dir = './_data/photos/dog/'
    imgs = [
        os.path.join(images_dir, f)
        for f in os.listdir(images_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Display a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme_engine.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """Show the form for creating a custom meme."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a meme from user-submitted data."""
    image_url = request.form['image_url']
    body = request.form['body']
    author = request.form['author']

    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    tmp_path = tmp_file.name
    tmp_file.close()

    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        with open(tmp_path, 'wb') as f:
            f.write(response.content)

        path = meme_engine.make_meme(tmp_path, body, author)
        return render_template('meme.html', path=path)
    except Exception as e:
        return render_template(
            'meme_form.html',
            error=f'Could not create meme: {e}',
        )
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.route('/tmp/<path:filename>')
def serve_meme(filename):
    """Serve generated meme images from the tmp directory."""
    return send_from_directory('./tmp', filename)


if __name__ == '__main__':
    app.run(debug=False)
