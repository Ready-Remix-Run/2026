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

    # Selection sort: put the most-square option (smallest rows/cols
    # difference) first, without needing a lambda sort key.
    for i in range(len(options)):
        closest_index = i
        for j in range(i + 1, len(options)):
            closest_diff = abs(options[closest_index].rows - options[closest_index].cols)
            current_diff = abs(options[j].rows - options[j].cols)
            if current_diff < closest_diff:
                closest_index = j
        options[i], options[closest_index] = options[closest_index], options[i]

    return options