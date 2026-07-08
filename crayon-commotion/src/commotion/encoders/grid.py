from commotion.encoders.encoder import Encoder
from commotion.models import EncodedCell, GridCell


def encode_grid(
    grid: list[list[GridCell]],
    encoder: Encoder,
) -> list[list[EncodedCell]]:

    encoded_grid = []

    for row in grid:
        encoded_row = []

        for cell in row:
            encoded_row.append(
                EncodedCell(
                    row=cell.row,
                    col=cell.col,
                    color=cell.color,
                    value=encoder.encode(cell),
                )
            )

        encoded_grid.append(encoded_row)

    return encoded_grid