from __future__ import annotations

import math
from pathlib import Path
from typing import Callable

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from commotion.models import Palette, PaletteColor, Run, StudentSheet, Worksheet

MARGIN = 1.27 * cm  # 0.5"
GUTTER = 1.0 * cm
LABEL_HEIGHT = 0.6 * cm
HEADER_HEIGHT = 1.5 * cm


def _column_label(index: int) -> str:
    """0 -> 'A', 25 -> 'Z', 26 -> 'AA', ... (spreadsheet-style column labels)."""
    index += 1
    label = ""
    while index > 0:
        remainder = (index - 1) % 26
        index = (index - 1) // 26
        label = chr(ord("A") + remainder) + label
    return label


def _default_reference_label(color: PaletteColor) -> str:
    return str(color.id)


def _text_color_for_background(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Black text on light backgrounds, white text on dark ones."""
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    if luminance > 0.5:
        return (0, 0, 0)
    return (1, 1, 1)


def _fit_grid(usable: float, pitch: float) -> int:
    """How many repeats of `pitch` (including one trailing gutter) fit in `usable`."""
    return max(1, int((usable + GUTTER) // pitch))


def _fit_font_size(
    canvas: Canvas,
    text: str,
    font_name: str,
    max_size: float,
    max_width: float,
    min_size: float = 4,
) -> float:
    """The largest font size (up to max_size) that fits `text` within max_width."""
    size = max_size
    while size > min_size and canvas.stringWidth(text, font_name, size) > max_width:
        size -= 1
    return size


def _draw_grid_value(canvas: Canvas, x: float, y: float, cell: float, value: str, font_size: float = 8) -> None:
    """
    Draw a cell's encoded value, centered in the cell_size x cell_size box
    whose bottom-left corner is (x, y). A value with embedded newlines
    (e.g. one line per RGB component) is drawn as stacked rows instead of
    a single line, with the font shrunk to fit all of them in the cell.
    """
    lines = value.split("\n")
    cx = x + cell / 2
    cy = y + cell / 2

    if len(lines) == 1:
        canvas.setFont("Helvetica", font_size)
        canvas.drawCentredString(cx, cy - font_size * 0.35, lines[0])
        return

    line_height = cell / len(lines)
    line_font_size = max(4, line_height * 0.55)
    canvas.setFont("Helvetica", line_font_size)
    top = cy + cell / 2 - line_height / 2
    for i in range(len(lines)):
        line = lines[i]
        ly = top - i * line_height
        canvas.drawCentredString(cx, ly - line_font_size * 0.35, line)


def render_blank_block_sheet(
    block_rows: int,
    block_cols: int,
    path: str | Path,
    cell_size_cm: float = 1.0,
    page_size: tuple[float, float] = letter,
    title: str = "Crayon Commotion - Blank Sheet",
) -> int:
    """
    Fill a page with as many identical blank block_rows x block_cols grids
    (of cell_size_cm cells each) as comfortably fit. Returns the number of
    blocks placed per page.
    """
    cell = cell_size_cm * cm
    block_w = block_cols * cell
    block_h = block_rows * cell

    page_w, page_h = page_size
    usable_w = page_w - 2 * MARGIN
    usable_h = page_h - 2 * MARGIN - HEADER_HEIGHT

    cols_per_page = _fit_grid(usable_w, block_w + GUTTER)
    rows_per_page = _fit_grid(usable_h, block_h + LABEL_HEIGHT + GUTTER)

    canvas = Canvas(str(path), pagesize=page_size)

    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(MARGIN, page_h - MARGIN - 0.35 * cm, title)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(
        MARGIN, page_h - MARGIN - 0.9 * cm,
        f"{block_rows} x {block_cols} cells, {cell_size_cm:g} cm each",
    )

    top = page_h - MARGIN - HEADER_HEIGHT

    for r in range(rows_per_page):
        block_top = top - r * (block_h + LABEL_HEIGHT + GUTTER)
        for c in range(cols_per_page):
            block_left = MARGIN + c * (block_w + GUTTER)

            canvas.setLineWidth(0.3)
            canvas.setStrokeColorRGB(0.6, 0.6, 0.6)
            for row in range(block_rows):
                for col in range(block_cols):
                    canvas.rect(
                        block_left + col * cell,
                        block_top - block_h + row * cell,
                        cell, cell,
                        stroke=1, fill=0,
                    )

            canvas.setLineWidth(1.2)
            canvas.setStrokeColorRGB(0, 0, 0)
            canvas.rect(block_left, block_top - block_h, block_w, block_h, stroke=1, fill=0)

            canvas.setFont("Helvetica", 7)
            canvas.setFillColorRGB(0, 0, 0)
            canvas.drawString(block_left, block_top - block_h - 0.4 * cm, "Block: ______")

    canvas.save()
    return rows_per_page * cols_per_page


def render_encoding_sheets(
    sheets: list[StudentSheet],
    path: str | Path,
    cell_size_cm: float = 1.0,
    page_size: tuple[float, float] = letter,
) -> int:
    """
    Render one entry per StudentSheet showing its encoded values in a grid,
    labeled with its position (e.g. "C4") so it can be matched to a spot on
    the blank sheet / easel. Packs as many entries per page as comfortably
    fit. Returns the number of pages written.
    """
    if not sheets:
        raise ValueError("sheets must not be empty")

    block_rows = sheets[0].rows
    block_cols = sheets[0].cols

    cell = cell_size_cm * cm
    block_w = block_cols * cell
    block_h = block_rows * cell

    page_w, page_h = page_size
    usable_w = page_w - 2 * MARGIN
    usable_h = page_h - 2 * MARGIN - HEADER_HEIGHT

    cols_per_page = _fit_grid(usable_w, block_w + GUTTER)
    rows_per_page = _fit_grid(usable_h, block_h + LABEL_HEIGHT + GUTTER)
    per_page = rows_per_page * cols_per_page

    canvas = Canvas(str(path), pagesize=page_size)
    pages = 0

    for page_start in range(0, len(sheets), per_page):
        page_sheets = sheets[page_start:page_start + per_page]
        pages += 1

        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(MARGIN, page_h - MARGIN - 0.35 * cm, "Crayon Commotion - Encoding Instructions")
        canvas.setFont("Helvetica", 9)
        canvas.drawString(
            MARGIN, page_h - MARGIN - 0.9 * cm,
            f"Page {pages} - blocks {page_start + 1}-{page_start + len(page_sheets)} of {len(sheets)}",
        )

        top = page_h - MARGIN - HEADER_HEIGHT

        for i in range(len(page_sheets)):
            sheet = page_sheets[i]
            r = i // cols_per_page
            c = i % cols_per_page
            block_top = top - r * (block_h + LABEL_HEIGHT + GUTTER)
            block_left = MARGIN + c * (block_w + GUTTER)

            block_row = sheet.start_row // sheet.rows
            block_col = sheet.start_col // sheet.cols
            label = f"{_column_label(block_col)}{block_row + 1}"

            canvas.setLineWidth(0.3)
            canvas.setStrokeColorRGB(0.6, 0.6, 0.6)
            canvas.setFillColorRGB(0, 0, 0)
            for row in range(sheet.rows):
                for col in range(sheet.cols):
                    x = block_left + col * cell
                    y = block_top - block_h + (sheet.rows - 1 - row) * cell
                    canvas.rect(x, y, cell, cell, stroke=1, fill=0)
                    value = sheet.cells[row * sheet.cols + col].value
                    _draw_grid_value(canvas, x, y, cell, value)

            canvas.setLineWidth(1.2)
            canvas.setStrokeColorRGB(0, 0, 0)
            canvas.rect(block_left, block_top - block_h, block_w, block_h, stroke=1, fill=0)

            canvas.setFont("Helvetica-Bold", 7)
            canvas.setFillColorRGB(0, 0, 0)
            canvas.drawString(
                block_left, block_top - block_h - 0.4 * cm,
                f"Block {label}  ({sheet.number}/{sheet.total})",
            )

        canvas.showPage()

    canvas.save()
    return pages


def render_run_length_encoding_sheets(
    sheets: list[StudentSheet],
    runs_by_sheet: list[list[Run]],
    path: str | Path,
    page_size: tuple[float, float] = letter,
    columns: int = 2,
) -> int:
    """
    Render one card per StudentSheet showing its color sequence as an
    ordered "count x palette id" list instead of a grid of per-cell values
    -- no grid, and no color shown (kept blind like the other encoding
    sheets; the color only appears on the teacher's cheat sheet).

    runs_by_sheet must line up with sheets (each StudentSheet's cells
    already run-length-encoded via run_length_encode -- computing that here
    would make this renderer depend on the encoders package, unlike every
    other render_* function, which only draws data it's handed).

    Card height varies with how many runs a block happens to have, so
    cards flow down `columns` side-by-side columns -- each new card goes
    into whichever column currently has the least ink on it -- wrapping to
    a new page once neither column has room left, rather than assuming a
    uniform grid of same-size boxes like the other sheet renderers do.
    """
    if not sheets:
        raise ValueError("sheets must not be empty")
    if len(runs_by_sheet) != len(sheets):
        raise ValueError("runs_by_sheet must have one entry per sheet")

    page_w, page_h = page_size
    usable_w = page_w - 2 * MARGIN
    usable_h = page_h - 2 * MARGIN - HEADER_HEIGHT

    col_w = (usable_w - (columns - 1) * GUTTER) / columns
    card_pad = 0.25 * cm
    line_h = 0.42 * cm
    header_h = 0.5 * cm
    footer_h = 0.38 * cm

    def card_height(n_runs: int) -> float:
        return header_h + n_runs * line_h + footer_h + 2 * card_pad

    canvas = Canvas(str(path), pagesize=page_size)
    pages = 0
    col_used = [0.0] * columns

    def start_page() -> None:
        nonlocal pages, col_used
        if pages > 0:
            canvas.showPage()
        pages += 1
        col_used = [0.0] * columns
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(MARGIN, page_h - MARGIN - 0.35 * cm, "Crayon Commotion - Encoding Instructions (Run-Length)")
        canvas.setFont("Helvetica", 9)
        canvas.drawString(MARGIN, page_h - MARGIN - 0.9 * cm, f"Page {pages}")

    start_page()

    for sheet_index in range(len(sheets)):
        sheet = sheets[sheet_index]
        runs = runs_by_sheet[sheet_index]
        height = card_height(len(runs))

        col = 0
        for candidate in range(1, columns):
            if col_used[candidate] < col_used[col]:
                col = candidate
        if col_used[col] > 0 and col_used[col] + height > usable_h:
            # A card taller than a whole empty column would otherwise
            # trigger a fresh (still-too-small) page every iteration
            # forever. Only bail to a new page if this column already has
            # something on it -- an oversized card on an empty column just
            # overflows the bottom margin instead of looping.
            start_page()
            col = 0

        block_row = sheet.start_row // sheet.rows
        block_col = sheet.start_col // sheet.cols
        label = f"{_column_label(block_col)}{block_row + 1}"

        x = MARGIN + col * (col_w + GUTTER)
        top = page_h - MARGIN - HEADER_HEIGHT - col_used[col]

        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawString(x, top - header_h + 0.12 * cm, f"Block {label}  ({sheet.number}/{sheet.total})")

        canvas.setFont("Helvetica", 9)
        y = top - header_h - card_pad
        for run in runs:
            canvas.drawString(x, y - line_h * 0.75, f"{run.count} x {run.color.id}")
            y -= line_h

        canvas.setFont("Helvetica-Oblique", 7)
        canvas.setFillColorRGB(0.35, 0.35, 0.35)
        canvas.drawString(
            x, y - footer_h * 0.6,
            f"{len(runs)} runs, {len(sheet.cells)} cells ({sheet.rows}x{sheet.cols}), "
            "fill left to right, wrap down",
        )

        col_used[col] += height + GUTTER

    canvas.save()
    return pages


def render_reference_sheet(
    palette: Palette,
    path: str | Path,
    page_size: tuple[float, float] = letter,
    title: str = "Color Reference Chart",
    label_fn: Callable[[PaletteColor], str] = _default_reference_label,
) -> None:
    """
    One page, single palette, swatches sized as large as will fit so the
    chart is readable from across a room.

    label_fn controls what's printed on each swatch -- the default prints
    the palette id (matching Decimal/Binary encoding), but e.g. a function
    that returns f"{c.r},{c.g},{c.b}" matches RGBBinaryEncoder, which
    doesn't use palette ids at all.
    """
    page_w, page_h = page_size
    usable_w = page_w - 2 * MARGIN
    usable_h = page_h - 2 * MARGIN - HEADER_HEIGHT

    n = len(palette.colors)

    best = None
    for cols in range(1, n + 1):
        rows = math.ceil(n / cols)
        cell_w = usable_w / cols
        cell_h = usable_h / rows
        swatch_side = min(cell_w, cell_h * 0.72)
        if best is None or swatch_side > best[0]:
            best = (swatch_side, cols, rows)

    _, cols, rows = best
    cell_w = usable_w / cols
    cell_h = usable_h / rows
    swatch_side = min(cell_w, cell_h * 0.72) * 0.9

    canvas = Canvas(str(path), pagesize=page_size)

    canvas.setFont("Helvetica-Bold", 20)
    canvas.drawCentredString(page_w / 2, page_h - MARGIN - 0.9 * cm, title)

    top = page_h - MARGIN - HEADER_HEIGHT

    for i in range(len(palette.colors)):
        color = palette.colors[i]
        r = i // cols
        c = i % cols
        cell_left = MARGIN + c * cell_w
        cell_top = top - r * cell_h

        swatch_x = cell_left + (cell_w - swatch_side) / 2
        swatch_y = cell_top - swatch_side

        canvas.setFillColorRGB(color.r / 255, color.g / 255, color.b / 255)
        canvas.setStrokeColorRGB(0, 0, 0)
        canvas.setLineWidth(1)
        canvas.rect(swatch_x, swatch_y, swatch_side, swatch_side, stroke=1, fill=1)

        label = label_fn(color)
        text_r, text_g, text_b = _text_color_for_background(color.r, color.g, color.b)
        canvas.setFillColorRGB(text_r, text_g, text_b)
        label_font_size = _fit_font_size(
            canvas, label, "Helvetica-Bold",
            max_size=max(8, swatch_side * 0.55), max_width=swatch_side * 0.85,
        )
        canvas.setFont("Helvetica-Bold", label_font_size)
        canvas.drawCentredString(swatch_x + swatch_side / 2, swatch_y + swatch_side * 0.3, label)

        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont("Helvetica", max(6, swatch_side * 0.16))
        canvas.drawCentredString(cell_left + cell_w / 2, swatch_y - swatch_side * 0.16 - 8, color.name)

    canvas.save()


def render_cheat_sheet(
    worksheet: Worksheet,
    path: str | Path,
    block_rows: int,
    block_cols: int,
    cell_size_cm: float = 1.0,
) -> int:
    """
    Tile the fully-colored worksheet across as many Letter pages as needed,
    auto-choosing portrait or landscape (whichever needs fewer pages).

    Draws a bold line at every mini-page boundary and labels each one with
    its position (e.g. "C7", matching the same labels used on the encoding
    instructions), so a teacher who's told "block C7 is wrong" can find
    that exact rectangle of pixels instead of counting cells by hand.

    Returns the number of pages written.
    """
    cell = cell_size_cm * cm
    row_label_w = 1.0 * cm
    col_label_h = 0.5 * cm

    def page_count(page_size: tuple[float, float]) -> tuple[int, int, int]:
        page_w, page_h = page_size
        usable_w = page_w - 2 * MARGIN - row_label_w
        usable_h = page_h - 2 * MARGIN - HEADER_HEIGHT - col_label_h
        cols_per_page = max(1, int(usable_w // cell))
        rows_per_page = max(1, int(usable_h // cell))
        pages_across = math.ceil(worksheet.cols / cols_per_page)
        pages_down = math.ceil(worksheet.rows / rows_per_page)
        return pages_across * pages_down, rows_per_page, cols_per_page

    portrait_size = letter
    landscape_size = landscape(letter)

    portrait_result = page_count(portrait_size)
    portrait_total = portrait_result[0]
    landscape_result = page_count(landscape_size)
    landscape_total = landscape_result[0]

    if landscape_total <= portrait_total:
        page_size = landscape_size
    else:
        page_size = portrait_size

    total_pages, rows_per_page, cols_per_page = page_count(page_size)
    page_w, page_h = page_size
    pages_across = math.ceil(worksheet.cols / cols_per_page)
    pages_down = math.ceil(worksheet.rows / rows_per_page)

    grid_left = MARGIN + row_label_w
    top = page_h - MARGIN - HEADER_HEIGHT - col_label_h

    canvas = Canvas(str(path), pagesize=page_size)

    page_num = 0
    for page_row in range(pages_down):
        row_start = page_row * rows_per_page
        row_end = min(row_start + rows_per_page, worksheet.rows)

        for page_col in range(pages_across):
            col_start = page_col * cols_per_page
            col_end = min(col_start + cols_per_page, worksheet.cols)
            page_num += 1

            first_block_col = col_start // block_cols
            last_block_col = (col_end - 1) // block_cols
            first_block_row = row_start // block_rows
            last_block_row = (row_end - 1) // block_rows
            block_range = (
                f"{_column_label(first_block_col)}{first_block_row + 1}-"
                f"{_column_label(last_block_col)}{last_block_row + 1}"
            )

            canvas.setFont("Helvetica-Bold", 14)
            canvas.setFillColorRGB(0, 0, 0)
            canvas.drawString(MARGIN, page_h - MARGIN - 0.35 * cm, f"Teacher Cheat Sheet - '{worksheet.title}'")
            canvas.setFont("Helvetica", 9)
            canvas.drawString(
                MARGIN, page_h - MARGIN - 0.9 * cm,
                f"Page {page_num}/{total_pages}  (sheet row {page_row + 1}/{pages_down}, "
                f"col {page_col + 1}/{pages_across})  blocks {block_range}  "
                f"rows {row_start}-{row_end - 1}, cols {col_start}-{col_end - 1}",
            )

            grid_w = (col_end - col_start) * cell
            grid_h = (row_end - row_start) * cell

            canvas.setLineWidth(0.2)
            for row in range(row_start, row_end):
                for col in range(col_start, col_end):
                    cell_obj = worksheet.cells[row][col]
                    color = cell_obj.color
                    x = grid_left + (col - col_start) * cell
                    y = top - (row - row_start) * cell - cell
                    canvas.setFillColorRGB(color.r / 255, color.g / 255, color.b / 255)
                    canvas.setStrokeColorRGB(0.3, 0.3, 0.3)
                    canvas.rect(x, y, cell, cell, stroke=1, fill=1)

            canvas.setLineWidth(1.2)
            canvas.setStrokeColorRGB(0, 0, 0)
            for boundary_col in range(0, worksheet.cols + 1, block_cols):
                if col_start <= boundary_col <= col_end:
                    x = grid_left + (boundary_col - col_start) * cell
                    canvas.line(x, top - grid_h, x, top)
            for boundary_row in range(0, worksheet.rows + 1, block_rows):
                if row_start <= boundary_row <= row_end:
                    y = top - (boundary_row - row_start) * cell
                    canvas.line(grid_left, y, grid_left + grid_w, y)

            canvas.setFont("Helvetica-Bold", 8)
            canvas.setFillColorRGB(0, 0, 0)
            for block_col_index in range(first_block_col, last_block_col + 1):
                block_start = block_col_index * block_cols
                block_end = min(block_start + block_cols, worksheet.cols)
                visible_start = max(block_start, col_start)
                visible_end = min(block_end, col_end)
                if visible_end <= visible_start:
                    continue
                center_x = grid_left + ((visible_start - col_start) + (visible_end - col_start)) / 2 * cell
                canvas.drawCentredString(center_x, top + 0.12 * cm, _column_label(block_col_index))

            for block_row_index in range(first_block_row, last_block_row + 1):
                block_start = block_row_index * block_rows
                block_end = min(block_start + block_rows, worksheet.rows)
                visible_start = max(block_start, row_start)
                visible_end = min(block_end, row_end)
                if visible_end <= visible_start:
                    continue
                center_y = top - ((visible_start - row_start) + (visible_end - row_start)) / 2 * cell
                canvas.drawRightString(grid_left - 0.15 * cm, center_y - 3, str(block_row_index + 1))

            canvas.showPage()

    canvas.save()
    return total_pages
