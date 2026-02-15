# Meme Generator

A multimedia application that dynamically generates memes by overlaying
quotes on images. The application ingests quotes from multiple file formats
(TXT, CSV, DOCX, PDF) and provides both a command-line interface and a
Flask web application.

## Prerequisites

- Python 3.9+
- **pdftotext** (part of Poppler) for PDF quote ingestion:
  - macOS: `brew install poppler`
  - Ubuntu/Debian: `sudo apt-get install poppler-utils`

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

Generate a random meme:

```bash
python meme.py
```

Generate a meme with a specific quote:

```bash
python meme.py --body "To be or not to be" --author "Shakespeare"
```

Generate a meme with a specific image and quote:

```bash
python meme.py --path ./_data/photos/dog/xander_1.jpg --body "Woof" --author "Dog"
```

### Flask Web Application

```bash
python app.py
```

Then open http://localhost:5000 in your browser. Use the homepage for random
memes or navigate to the "Create" page to supply a custom image URL and
quote.

## Project Structure

### QuoteEngine

Responsible for ingesting quotes from various file formats.

| Module | Description | Dependencies |
|---|---|---|
| `QuoteModel.py` | Data class representing a quote (body + author) | — |
| `IngestorInterface.py` | ABC defining the ingestor contract | — |
| `TextIngestor.py` | Parses `.txt` files | — |
| `CSVIngestor.py` | Parses `.csv` files | pandas |
| `DocxIngestor.py` | Parses `.docx` files | python-docx |
| `PDFIngestor.py` | Parses `.pdf` files via subprocess | pdftotext CLI |
| `Ingestor.py` | Facade that delegates to the correct ingestor | — |
| `exceptions.py` | Custom exception classes | — |

Example:

```python
from QuoteEngine import Ingestor

quotes = Ingestor.parse('./_data/DogQuotes/DogQuotesTXT.txt')
for q in quotes:
    print(q)  # "Bark like no one's listening" - Rex
```

### MemeEngine

Responsible for generating meme images.

| Module | Description | Dependencies |
|---|---|---|
| `MemeEngine.py` | Loads, resizes, and overlays text on images | Pillow |
| `exceptions.py` | Custom exception class | — |

Example:

```python
from MemeEngine import MemeEngine

m = MemeEngine('./tmp')
path = m.make_meme('./_data/photos/dog/xander_1.jpg', 'Hello', 'World')
print(path)  # ./tmp/abc123.png
```
