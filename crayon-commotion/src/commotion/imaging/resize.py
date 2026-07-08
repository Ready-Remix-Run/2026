from __future__ import annotations

from pathlib import Path

from PIL import Image


def load_and_resize_image(image_path: str | Path, rows: int, cols: int) -> list[list[tuple[int, int, int]]]:
    """
    Load an image, resize it to (cols, rows), and return a 2D list of RGB tuples.
    """
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    with Image.open(path) as img:
        img = img.convert("RGB")
        img = img.resize((cols, rows))

        pixels: list[list[tuple[int, int, int]]] = []

        for y in range(rows):
            row: list[tuple[int, int, int]] = []
            for x in range(cols):
                row.append(img.getpixel((x, y)))
            pixels.append(row)

    return pixels