"""MemeEngine module for generating meme images."""

import os
import random
import string
import textwrap

from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Generate meme images with text overlaid on photos."""

    def __init__(self, output_dir: str):
        """Create a new MemeEngine.

        :param output_dir: Directory where generated memes are saved.
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def make_meme(self, img_path: str, text: str, author: str,
                  width: int = 500) -> str:
        """Generate a meme by overlaying a quote on an image.

        :param img_path: Path to the source image.
        :param text: Quote body text.
        :param author: Quote author.
        :param width: Maximum width in pixels (default 500).
        :return: Path to the generated meme image.
        """
        width = min(width, 500)

        img = Image.open(img_path)

        # Resize maintaining aspect ratio
        ratio = width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((width, new_height), Image.LANCZOS)

        draw = ImageDraw.Draw(img)

        # Try to use a nice font, fall back to default
        font_size = max(16, width // 25)
        try:
            font = ImageFont.truetype(
                '/System/Library/Fonts/Helvetica.ttc', font_size
            )
        except (OSError, IOError):
            try:
                font = ImageFont.truetype(
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                    font_size,
                )
            except (OSError, IOError):
                font = ImageFont.load_default()

        # Wrap long text
        max_chars = max(20, width // (font_size // 2))
        wrapped = textwrap.fill(text, width=max_chars)
        full_text = f'{wrapped}\n  - {author}'

        # Position text in lower portion of image
        margin = 10
        y_pos = new_height - margin - (full_text.count('\n') + 1) * (font_size + 4) - 20
        y_pos = max(margin, y_pos)
        x_pos = margin

        # Draw text shadow for readability
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-2, -2), (2, 2)]:
            draw.multiline_text(
                (x_pos + dx, y_pos + dy), full_text,
                font=font, fill='black',
            )
        draw.multiline_text(
            (x_pos, y_pos), full_text,
            font=font, fill='white',
        )

        # Save with random filename
        rand = ''.join(random.choices(string.ascii_lowercase, k=8))
        out_path = os.path.join(self.output_dir, f'meme_{rand}.jpg')
        img.save(out_path)
        return out_path
