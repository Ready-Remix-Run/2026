from __future__ import annotations

import math
from pathlib import Path

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from commotion.models import Palette, StudentSheet, Worksheet

MARGIN = 1.27 * cm  # 0.5"
GUTTER = 1.0 * cm
LABEL_HEIGHT = 0.6 * cm
HEADER_HEIGHT = 1.5 * cm


def _column_label(index: int) -> str:
    """0 -> 'A', 25 -> 'Z', 26 -> 'AA', ... (spreadsheet-style column labels)."""
    index += 1
    label = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        label = chr(ord("A") + remainder) + label
    return label


def _text_color_for_background(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Black text on light backgrounds, white text on dark ones."""
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return (0, 0, 0) if luminance > 0.5 else (1, 1, 1)


def _fit_grid(usable: float, pitch: float) -> int:
    """How many repeats of `pitch` (including one trailing gutter) fit in `usable`."""
    return max(1, int((usable + GUTTER) // pitch))


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

        for i, sheet in enumerate(page_sheets):
            r, c = divmod(i, cols_per_page)
            block_top = top - r * (block_h + LABEL_HEIGHT + GUTTER)
            block_left = MARGIN + c * (block_w + GUTTER)

            block_row = sheet.start_row // sheet.rows
            block_col = sheet.start_col // sheet.cols
            label = f"{_column_label(block_col)}{block_row + 1}"

            canvas.setLineWidth(0.3)
            canvas.setStrokeColorRGB(0.6, 0.6, 0.6)
            canvas.setFont("Helvetica", 8)
            for row in range(sheet.rows):
                for col in range(sheet.cols):
                    x = block_left + col * cell
                    y = block_top - block_h + (sheet.rows - 1 - row) * cell
                    canvas.rect(x, y, cell, cell, stroke=1, fill=0)
                    value = sheet.cells[row * sheet.cols + col].value
                    canvas.drawCentredString(x + cell / 2, y + cell / 2 - 3, value)

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


def render_reference_sheet(
    palette: Palette,
    path: str | Path,
    page_size: tuple[float, float] = letter,
    title: str = "Color Reference Chart",
) -> None:
    """
    One page, single palette, swatches sized as large as will fit so the
    chart is readable from across a room.
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

    for i, color in enumerate(palette.colors):
        r, c = divmod(i, cols)
        cell_left = MARGIN + c * cell_w
        cell_top = top - r * cell_h

        swatch_x = cell_left + (cell_w - swatch_side) / 2
        swatch_y = cell_top - swatch_side

        canvas.setFillColorRGB(color.r / 255, color.g / 255, color.b / 255)
        canvas.setStrokeColorRGB(0, 0, 0)
        canvas.setLineWidth(1)
        canvas.rect(swatch_x, swatch_y, swatch_side, swatch_side, stroke=1, fill=1)

        text_r, text_g, text_b = _text_color_for_background(color.r, color.g, color.b)
        canvas.setFillColorRGB(text_r, text_g, text_b)
        canvas.setFont("Helvetica-Bold", max(8, swatch_side * 0.55))
        canvas.drawCentredString(swatch_x + swatch_side / 2, swatch_y + swatch_side * 0.3, str(color.id))

        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont("Helvetica", max(6, swatch_side * 0.16))
        canvas.drawCentredString(cell_left + cell_w / 2, swatch_y - swatch_side * 0.16 - 8, color.name)

    canvas.save()


def render_cheat_sheet(
    worksheet: Worksheet,
    path: str | Path,
    cell_size_cm: float = 1.0,
) -> int:
    """
    Tile the fully-colored worksheet across as many Letter pages as needed,
    auto-choosing portrait or landscape (whichever needs fewer pages).
    Returns the number of pages written.
    """
    cell = cell_size_cm * cm

    def page_count(page_size: tuple[float, float]) -> tuple[int, int, int]:
        page_w, page_h = page_size
        usable_w = page_w - 2 * MARGIN
        usable_h = page_h - 2 * MARGIN - HEADER_HEIGHT
        cols_per_page = max(1, int(usable_w // cell))
        rows_per_page = max(1, int(usable_h // cell))
        pages_across = math.ceil(worksheet.cols / cols_per_page)
        pages_down = math.ceil(worksheet.rows / rows_per_page)
        return pages_across * pages_down, rows_per_page, cols_per_page

    portrait_size = letter
    landscape_size = landscape(letter)

    portrait_total, *_ = page_count(portrait_size)
    landscape_total, *_ = page_count(landscape_size)

    if landscape_total <= portrait_total:
        page_size = landscape_size
    else:
        page_size = portrait_size

    total_pages, rows_per_page, cols_per_page = page_count(page_size)
    page_w, page_h = page_size
    pages_across = math.ceil(worksheet.cols / cols_per_page)
    pages_down = math.ceil(worksheet.rows / rows_per_page)

    canvas = Canvas(str(path), pagesize=page_size)
    top = page_h - MARGIN - HEADER_HEIGHT

    page_num = 0
    for page_row in range(pages_down):
        row_start = page_row * rows_per_page
        row_end = min(row_start + rows_per_page, worksheet.rows)

        for page_col in range(pages_across):
            col_start = page_col * cols_per_page
            col_end = min(col_start + cols_per_page, worksheet.cols)
            page_num += 1

            canvas.setFont("Helvetica-Bold", 14)
            canvas.setFillColorRGB(0, 0, 0)
            canvas.drawString(MARGIN, page_h - MARGIN - 0.35 * cm, f"Teacher Cheat Sheet - '{worksheet.title}'")
            canvas.setFont("Helvetica", 9)
            canvas.drawString(
                MARGIN, page_h - MARGIN - 0.9 * cm,
                f"Page {page_num}/{total_pages}  (sheet row {page_row + 1}/{pages_down}, "
                f"col {page_col + 1}/{pages_across})  rows {row_start}-{row_end - 1}, "
                f"cols {col_start}-{col_end - 1}",
            )

            canvas.setLineWidth(0.2)
            for row in range(row_start, row_end):
                for col in range(col_start, col_end):
                    cell_obj = worksheet.cells[row][col]
                    color = cell_obj.color
                    x = MARGIN + (col - col_start) * cell
                    y = top - (row - row_start) * cell - cell
                    canvas.setFillColorRGB(color.r / 255, color.g / 255, color.b / 255)
                    canvas.setStrokeColorRGB(0.3, 0.3, 0.3)
                    canvas.rect(x, y, cell, cell, stroke=1, fill=1)

            canvas.showPage()

    canvas.save()
    return total_pages
