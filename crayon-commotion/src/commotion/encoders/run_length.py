from dataclasses import replace

from commotion.models import EncodedCell, Run


def run_length_encode(cells: list[EncodedCell]) -> list[Run]:
    """
    Group a block's cells, in reading order, into runs of consecutive
    identical colors (e.g. 11 Cerulean, 1 White, 3 Cerulean, ...).

    Unlike the other encoders, this isn't a per-cell Encoder -- a single
    cell's color doesn't have a meaningful "run-length value" on its own,
    only a sequence of cells does. Runs never cross a block boundary: call
    this once per StudentSheet.cells (already one block, already in
    reading order), not on a whole worksheet at once.
    """
    runs: list[Run] = []

    for cell in cells:
        if runs and runs[-1].color.id == cell.color.id:
            runs[-1] = replace(runs[-1], count=runs[-1].count + 1)
        else:
            runs.append(Run(count=1, color=cell.color))

    return runs
