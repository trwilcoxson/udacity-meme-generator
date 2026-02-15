"""MemeEngine generates meme images with overlaid quotes."""

import logging
import os
import random
import string

from PIL import Image, ImageDraw, ImageFont

from .exceptions import MemeGenerationError

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Font search paths — checked in order; first match wins.
# Covers macOS system fonts, Homebrew, and common Linux locations.
# ---------------------------------------------------------------------------
_FONT_PATHS = [
    '/System/Library/Fonts/Supplemental/Arial.ttf',
    '/Library/Fonts/Arial Unicode.ttf',
    '/Library/Fonts/Arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/TTF/DejaVuSans.ttf',
]


class MemeEngine:
    """Generate meme images by overlaying quotes on photographs."""

    def __init__(self, output_dir: str) -> None:
        """Create a MemeEngine that saves output to *output_dir*.

        :param output_dir: Directory to save generated memes.
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info("MemeEngine output directory: %s", output_dir)

    # -------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------

    def make_meme(
        self, img_path: str, text: str, author: str, width: int = 500
    ) -> str:
        """Generate a meme and return the path to the output file.

        Steps: load image -> resize -> add caption -> save.

        :param img_path: Path to the source image.
        :param text: Quote body text.
        :param author: Quote author.
        :param width: Maximum width in pixels (default 500).
        :return: Path to the saved meme image.
        :raises MemeGenerationError: If the image cannot be loaded or saved.
        """
        logger.info("Generating meme from %s", img_path)

        # Step 1 — Load image from disk
        img = self._load_image(img_path)

        # Step 2 — Resize to max width while maintaining aspect ratio
        img = self._resize_image(img, width)

        # Step 3 — Draw the caption at a random location
        self._add_caption(img, text, author)

        # Step 4 — Save to a randomly named output file
        out_path = self._save_image(img)

        logger.info("Meme saved to %s", out_path)
        return out_path

    # -------------------------------------------------------------------
    # Private helpers — each handles one discrete responsibility
    # -------------------------------------------------------------------

    @staticmethod
    def _load_image(img_path: str) -> Image.Image:
        """Load an image from disk.

        :param img_path: Path to the image file.
        :return: A PIL Image object.
        :raises MemeGenerationError: If the file cannot be opened.
        """
        try:
            img = Image.open(img_path)
            # Force load so errors surface here, not later
            img.load()
        except FileNotFoundError as exc:
            raise MemeGenerationError(
                f"Image not found: {img_path}"
            ) from exc
        except (OSError, ValueError) as exc:
            raise MemeGenerationError(
                f"Cannot open image '{img_path}': {exc}"
            ) from exc

        logger.debug(
            "Loaded image %s (%dx%d)", img_path, img.width, img.height
        )
        return img

    @staticmethod
    def _resize_image(img: Image.Image, max_width: int) -> Image.Image:
        """Resize an image to *max_width* while keeping the aspect ratio.

        If the image is already narrower than *max_width* it is
        returned unchanged.

        :param img: Source PIL Image.
        :param max_width: Maximum width in pixels.
        :return: Resized (or original) PIL Image.
        """
        if img.width <= max_width:
            return img

        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)

        logger.debug("Resized image to %dx%d", img.width, img.height)
        return img

    @staticmethod
    def _add_caption(img: Image.Image, text: str, author: str) -> None:
        """Draw a quote caption at a random position on the image.

        A thin shadow is rendered behind the white text to ensure
        readability over both light and dark backgrounds.

        :param img: PIL Image to draw on (modified in place).
        :param text: Quote body.
        :param author: Quote author.
        """
        draw = ImageDraw.Draw(img)
        caption = f'"{text}" - {author}'

        # Load font for the caption text
        font = MemeEngine._load_font(24)

        # --- Random caption placement ---
        # Estimate text bounding box to keep caption within image
        bbox = draw.textbbox((0, 0), caption, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Horizontal: allow the caption to start anywhere from 10px to
        # (image_width - text_width - 10), but always at least 10px in.
        max_x = max(img.width - text_w - 10, 10)
        x_pos = random.randint(10, max_x)

        # Vertical: full range from 10px to (image_height - text_height - 10)
        max_y = max(img.height - text_h - 10, 10)
        y_pos = random.randint(10, max_y)

        logger.debug("Caption position: (%d, %d)", x_pos, y_pos)

        # Shadow pass — offset by 2px in four directions for readability
        for dx, dy in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            draw.text((x_pos + dx, y_pos + dy), caption,
                      font=font, fill='black')

        # Main white text
        draw.text((x_pos, y_pos), caption, font=font, fill='white')

    def _save_image(self, img: Image.Image) -> str:
        """Save the image to the output directory with a random filename.

        :param img: PIL Image to save.
        :return: Path to the saved file.
        :raises MemeGenerationError: If saving fails.
        """
        out_name = ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=12)
        ) + '.png'
        out_path = os.path.join(self.output_dir, out_name)

        try:
            img.save(out_path)
        except (OSError, ValueError) as exc:
            raise MemeGenerationError(
                f"Failed to save meme to '{out_path}': {exc}"
            ) from exc

        return out_path

    # -------------------------------------------------------------------
    # Font loading
    # -------------------------------------------------------------------

    @staticmethod
    def _load_font(size: int) -> ImageFont.FreeTypeFont:
        """Try to load a TrueType font, falling back to the default.

        :param size: Desired font size in points.
        :return: A PIL ImageFont object.
        """
        for fp in _FONT_PATHS:
            if os.path.isfile(fp):
                try:
                    return ImageFont.truetype(fp, size)
                except (IOError, OSError):
                    continue

        logger.warning("No TrueType font found; using default bitmap font")
        return ImageFont.load_default()
