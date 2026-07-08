from commotion.models import DimensionOption
from math import isqrt

def suggest_sheet_dimensions(
    cells: int,
) -> list[DimensionOption]:
    """
    Return reasonable rectangular layouts for a student sheet.
    """

    if cells <= 0:
        raise ValueError("cells must be > 0")

    options: list[DimensionOption] = []

    for rows in range(1, isqrt(cells) + 1):
        if cells % rows == 0:
            cols = cells // rows
            options.append(DimensionOption(rows=rows, cols=cols))

    options.sort(key=lambda opt: abs(opt.rows - opt.cols))

    return options