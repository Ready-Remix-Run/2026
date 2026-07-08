from __future__ import annotations

import csv
from pathlib import Path

from commotion.models import Palette, PaletteColor


def load_palette(csv_path: str | Path, palette_name: str | None = None) -> Palette:
    """
    Load a palette from a CSV file with columns:
    id,name,r,g,b
    """
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"Palette file not found: {path}")

    colors: list[PaletteColor] = []

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        required_columns = {"id","name", "r", "g", "b"}
        if reader.fieldnames is None or not required_columns.issubset(set(reader.fieldnames)):
            raise ValueError(
                f"Palette CSV must contain columns: {sorted(required_columns)}"
            )

        for row in reader:
            color = PaletteColor(
                id=int(row["id"].strip()),
                name=row["name"].strip(),
                r=int(row["r"]),
                g=int(row["g"]),
                b=int(row["b"]),
            )
            colors.append(color)

    if palette_name is None:
        palette_name = path.stem

    return Palette(name=palette_name, colors=colors)