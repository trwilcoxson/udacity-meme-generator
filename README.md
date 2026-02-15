# Motivational Meme Generator

A multimedia application that dynamically generates memes by overlaying quotes on images. Interact with it through the command line or a Flask web interface.

## Setup

### Prerequisites

- Python 3.6+
- `pdftotext` CLI tool (from xpdf or poppler-utils)

Install the system dependency:

```bash
# macOS
brew install xpdf
# or
brew install poppler

# Ubuntu/Debian
sudo apt-get install -y xpdf
```

### Install Python Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Generate a random meme:

```bash
python3 meme.py
```

Generate a meme with specific arguments:

```bash
python3 meme.py --path "./_data/photos/dog/xander_1.jpg" --body "To be or not to be" --author "Shakespeare"
```

Arguments:
- `--path`: Path to an image file (optional; random if not given)
- `--body`: Quote body text (optional; random if not given)
- `--author`: Quote author (required if `--body` is provided)

### Flask Web Application

```bash
python3 app.py
```

Then visit [http://localhost:5000](http://localhost:5000).

- **Home page** (`/`): Displays a randomly generated meme
- **Create page** (`/create`): Form to create a custom meme from an image URL, quote, and author

## Project Structure

### QuoteEngine Package

Handles ingesting quotes from multiple file formats using the strategy design pattern.

- **QuoteModel** (`QuoteModel.py`): Data class encapsulating a quote's `body` and `author`.
- **IngestorInterface** (`IngestorInterface.py`): Abstract base class defining `can_ingest` and `parse` class methods. All ingestors inherit from this.
- **CSVIngestor** (`CSVIngestor.py`): Parses CSV files using pandas. Expects `body` and `author` columns.
- **DocxIngestor** (`DocxIngestor.py`): Parses DOCX files using python-docx. Each paragraph should be `"body" - author`.
- **PDFIngestor** (`PDFIngestor.py`): Parses PDF files using subprocess calls to the `pdftotext` CLI tool. Temporary files are cleaned up after parsing.
- **TextIngestor** (`TextIngestor.py`): Parses plain text files. Each line should be `"body" - author`.
- **Ingestor** (`Ingestor.py`): Facade class implementing the strategy pattern. Selects the appropriate ingestor based on file extension.

### MemeEngine Package

Handles image manipulation for meme generation.

- **MemeEngine** (`MemeEngine.py`): Loads images with Pillow, resizes to a max width of 500px (maintaining aspect ratio), draws the quote text and author with a shadow effect for readability, and saves the result.

### Application Files

- **meme.py**: CLI tool using argparse for generating memes from the command line.
- **app.py**: Flask web application with routes for random meme generation and custom meme creation.

## Dependencies

- Flask - Web framework
- Pillow - Image manipulation
- pandas - CSV parsing
- python-docx - DOCX file parsing
- requests - Downloading images from URLs
- pdftotext (system tool) - PDF text extraction
