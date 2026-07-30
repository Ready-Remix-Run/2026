from commotion.models import Worksheet


def build_worksheet(
    title: str,
    cells,
    encoder_name: str,
    palette_name: str,
) -> Worksheet:

    rows = len(cells)
    if rows:
        cols = len(cells[0])
    else:
        cols = 0

    return Worksheet(
        title=title,
        rows=rows,
        cols=cols,
        encoder_name=encoder_name,
        palette_name=palette_name,
        cells=cells,
    )