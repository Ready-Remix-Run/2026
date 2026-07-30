from __future__ import annotations

import random
from dataclasses import replace

from commotion.imaging.quantize import color_distance
from commotion.models import GridCell, Palette


def _second_nearest_palette_color(rgb, palette: Palette, exclude_id: int):
    candidates = []
    for c in palette.colors:
        if c.id != exclude_id:
            candidates.append(c)

    best = candidates[0]
    best_distance = color_distance(rgb, (best.r, best.g, best.b))

    for c in candidates[1:]:
        distance = color_distance(rgb, (c.r, c.g, c.b))
        if distance < best_distance:
            best = c
            best_distance = distance

    return best


def _interior_starts(length: int, size: int) -> range:
    """
    Valid start positions for a `size`-cell run inside a `length`-cell line,
    preferring positions that don't touch either end -- so a nudge doesn't
    blend visually into a neighboring block. Falls back to the full range
    if the line is too short to have an interior.
    """
    max_start = length - size
    if max_start <= 0:
        return range(0, 1)

    interior_max = max_start - 1
    if interior_max >= 1:
        return range(1, interior_max + 1)

    return range(0, max_start + 1)


def count_monochrome_blocks(
    grid: list[list[GridCell]],
    block_rows: int,
    block_cols: int,
) -> tuple[int, int]:
    """
    Returns (monochrome_blocks, total_blocks) for a block_rows x block_cols
    tiling of the grid -- how many blocks would come out as a single
    repeated color.
    """
    total_rows = len(grid)
    if total_rows:
        total_cols = len(grid[0])
    else:
        total_cols = 0

    monochrome = 0
    total = 0

    for block_top in range(0, total_rows, block_rows):
        for block_left in range(0, total_cols, block_cols):
            block_bottom = min(block_top + block_rows, total_rows)
            block_right = min(block_left + block_cols, total_cols)

            color_ids = set()
            for r in range(block_top, block_bottom):
                for c in range(block_left, block_right):
                    color_ids.add(grid[r][c].color.id)

            total += 1
            if len(color_ids) == 1:
                monochrome += 1

    return monochrome, total


def ensure_block_variety(
    grid: list[list[GridCell]],
    palette: Palette,
    block_rows: int,
    block_cols: int,
    nudge_size: int = 1,
) -> list[list[GridCell]]:
    """
    Guarantee every block_rows x block_cols block has at least two colors,
    so no student ends up coloring a sheet of identical cells. Blocks that
    would otherwise be a single repeated color get a small square of cells
    nudged to each cell's second-nearest palette color. The nudge stays
    away from the block's own edges (so it doesn't blend into a
    neighboring block), and its exact position is staggered per block --
    otherwise every affected block nudges the same relative spot and large
    flat regions (e.g. a sky) end up with a visible repeating grid pattern.

    Opt-in: this trades a bit of color accuracy for guaranteed variety,
    which only matters for flat/vector-style source images. A photo
    quantized to a small palette rarely produces a monochrome block in the
    first place, so this shouldn't be run unconditionally.
    """
    total_rows = len(grid)
    if total_rows:
        total_cols = len(grid[0])
    else:
        total_cols = 0

    result = []
    for row in grid:
        result.append(row[:])

    for block_top in range(0, total_rows, block_rows):
        for block_left in range(0, total_cols, block_cols):
            block_bottom = min(block_top + block_rows, total_rows)
            block_right = min(block_left + block_cols, total_cols)

            color_ids = set()
            for r in range(block_top, block_bottom):
                for c in range(block_left, block_right):
                    color_ids.add(grid[r][c].color.id)
            if len(color_ids) != 1:
                continue

            main_id = None
            for color_id in color_ids:
                main_id = color_id
            height = block_bottom - block_top
            width = block_right - block_left
            square_rows = min(nudge_size, height)
            square_cols = min(nudge_size, width)

            block_row_index = block_top // block_rows
            block_col_index = block_left // block_cols
            rng = random.Random(f"{block_row_index},{block_col_index}")
            row_start = block_top + rng.choice(list(_interior_starts(height, square_rows)))
            col_start = block_left + rng.choice(list(_interior_starts(width, square_cols)))

            for r in range(row_start, row_start + square_rows):
                for c in range(col_start, col_start + square_cols):
                    cell = grid[r][c]
                    alt = _second_nearest_palette_color(cell.rgb, palette, main_id)
                    result[r][c] = replace(cell, color=alt)

    return result
