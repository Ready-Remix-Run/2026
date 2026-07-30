from pathlib import Path
import csv

from commotion.models import Worksheet


def write_csv(
    worksheet: Worksheet,
    output_path: str | Path,
) -> None:

    output_path = Path(output_path)

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        writer.writerow(["Title", worksheet.title])
        writer.writerow(["Palette", worksheet.palette_name])
        writer.writerow(["Encoder", worksheet.encoder_name])
        writer.writerow([])

        for row in worksheet.cells:
            row_values = []
            for cell in row:
                row_values.append(cell.value)
            writer.writerow(row_values)