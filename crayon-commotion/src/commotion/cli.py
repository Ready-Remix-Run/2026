from __future__ import annotations

from pathlib import Path

from PIL import Image

from commotion.models import ClassroomPlan, DimensionOption, Palette, StudentSheet, Worksheet
from commotion.palettes.loader import load_palette
from commotion.planning.dimensions import suggest_dimensions
from commotion.planning.sheets import suggest_sheet_dimensions
from commotion.imaging.resize import load_and_resize_image
from commotion.imaging.quantize import quantize_image
from commotion.imaging.variety import count_monochrome_blocks, ensure_block_variety
from commotion.encoders.decimal import DecimalEncoder
from commotion.encoders.binary import BinaryEncoder, bits_needed_for_palette
from commotion.encoders.rgb_binary import RGBBinaryEncoder
from commotion.encoders.hexadecimal import RGBHexEncoder
from commotion.encoders.encoder import Encoder
from commotion.encoders.grid import encode_grid
from commotion.worksheets.builder import build_worksheet
from commotion.worksheets.splitter import split_into_student_sheets
from commotion.renderers.csv_renderer import write_csv
from commotion.renderers.pdf import (
    render_blank_block_sheet,
    render_cheat_sheet,
    render_encoding_sheets,
    render_reference_sheet,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PALETTE_PATH = PROJECT_ROOT / "palettes" / "crayola24.csv"
PALETTE_16_PATH = PROJECT_ROOT / "palettes" / "crayola16.csv"
IMAGE_PATH = PROJECT_ROOT / "images" / "test_image.png"
CSTA_IMAGE_PATH = PROJECT_ROOT / "images" / "csta2027.png"
OUTPUT_DIR = PROJECT_ROOT / "output"


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def test_palette() -> Palette:
    section("Palette")

    palette = load_palette(PALETTE_PATH, palette_name="Crayola 24")
    print(f"Loaded '{palette.name}' with {len(palette.colors)} colors")
    for color in palette.colors[:3]:
        print(f"  {color.id}: {color.name} rgb({color.r}, {color.g}, {color.b})")
    print("  ...")

    return palette


def test_palette_16() -> Palette:
    section("Palette (Crayola 16)")

    palette = load_palette(PALETTE_16_PATH, palette_name="Crayola 16")
    print(f"Loaded '{palette.name}' with {len(palette.colors)} colors -> {bits_needed_for_palette(palette)}-bit binary")
    for color in palette.colors:
        print(f"  {color.id}: {color.name} rgb({color.r}, {color.g}, {color.b})")

    return palette


def test_dimensions(plan: ClassroomPlan) -> DimensionOption:
    section("Worksheet dimensions")

    print(
        f"Plan: {plan.students} students x {plan.sheets_per_student} sheets x "
        f"{plan.cells_per_sheet} cells/sheet = {plan.total_cells} cells"
    )

    options = suggest_dimensions(plan)
    for option in options:
        print(f"  {option.rows} x {option.cols} = {option.cells} cells")

    chosen = options[0]
    print(f"Chosen worksheet size: {chosen.rows} x {chosen.cols}")

    return chosen


def test_image(dims: DimensionOption) -> list[list[tuple[int, int, int]]]:
    section("Image load + resize")

    pixels = load_and_resize_image(IMAGE_PATH, rows=dims.rows, cols=dims.cols)
    print(f"Loaded '{IMAGE_PATH.name}' resized to {dims.rows} x {dims.cols}")
    print(f"  top-left:     {pixels[0][0]}")
    print(f"  bottom-right: {pixels[-1][-1]}")

    return pixels


def test_quantize(pixels: list[list[tuple[int, int, int]]], palette: Palette):
    section("Quantize")

    grid = quantize_image(pixels, palette)
    cell = grid[0][0]
    print(f"Top-left pixel {cell.rgb} -> nearest crayon '{cell.color.name}' (id {cell.color.id})")

    return grid


def test_encode(grid):
    section("Encode")

    encoded = encode_grid(grid, DecimalEncoder())
    print(f"Top-left cell encoded value: '{encoded[0][0].value}'")

    return encoded


def test_encode_binary(grid, palette: Palette):
    section("Encode (binary)")

    bit_width = bits_needed_for_palette(palette)
    encoded = encode_grid(grid, BinaryEncoder(bit_width))
    print(f"Palette has {len(palette.colors)} colors -> {bit_width}-bit binary values")
    print(f"Top-left cell encoded value: '{encoded[0][0].value}'")

    return encoded


def test_worksheet(encoded, palette: Palette) -> Worksheet:
    section("Worksheet")

    worksheet = build_worksheet(
        title="Rainbow Test",
        cells=encoded,
        encoder_name="Decimal",
        palette_name=palette.name,
    )
    print(
        f"Worksheet '{worksheet.title}': {worksheet.rows} x {worksheet.cols}, "
        f"palette={worksheet.palette_name}, encoder={worksheet.encoder_name}"
    )

    return worksheet


def pick_compatible_sheet_size(worksheet: Worksheet, cells_per_sheet: int) -> DimensionOption:
    """
    suggest_sheet_dimensions only knows about cells_per_sheet, and
    suggest_dimensions only knows about the classroom plan -- neither checks
    the other, so a suggested sheet size isn't guaranteed to evenly tile the
    chosen worksheet. Try each suggestion (and its transpose) until one fits.
    """
    for option in suggest_sheet_dimensions(cells_per_sheet):
        for rows, cols in ((option.rows, option.cols), (option.cols, option.rows)):
            if worksheet.rows % rows == 0 and worksheet.cols % cols == 0:
                return DimensionOption(rows=rows, cols=cols)

    raise ValueError(
        f"No {cells_per_sheet}-cell layout evenly divides a "
        f"{worksheet.rows} x {worksheet.cols} worksheet"
    )


def test_sheet_size(worksheet: Worksheet, cells_per_sheet: int) -> DimensionOption:
    section("Sheet dimensions")

    options = suggest_sheet_dimensions(cells_per_sheet)
    print(f"Layout options for {cells_per_sheet} cells per sheet:")
    for option in options:
        print(f"  {option.rows} x {option.cols}")

    sheet_size = pick_compatible_sheet_size(worksheet, cells_per_sheet)
    print(f"Chosen sheet size (fits {worksheet.rows} x {worksheet.cols} worksheet): "
          f"{sheet_size.rows} x {sheet_size.cols}")

    return sheet_size


def test_split(worksheet: Worksheet, sheet_size: DimensionOption):
    section("Split into student sheets")

    sheets = split_into_student_sheets(worksheet, sheet_size)
    print(
        f"Worksheet {worksheet.rows} x {worksheet.cols} split into "
        f"{len(sheets)} sheets of {sheet_size.rows} x {sheet_size.cols}"
    )

    first = sheets[0]
    print(f"Sheet {first.number}/{first.total} cell locations:")
    for r in range(first.rows):
        row_cells = [
            f"({first.cells[r * first.cols + c].row},{first.cells[r * first.cols + c].col})"
            for c in range(first.cols)
        ]
        print("  " + " ".join(row_cells))

    return sheets


def test_csv(worksheet: Worksheet) -> Path:
    section("CSV export")

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / "rainbow.csv"
    write_csv(worksheet, out_path)
    print(f"Wrote {out_path}")

    return out_path


def build_encoder(encoder_name: str, palette: Palette) -> Encoder:
    if encoder_name == "Decimal":
        return DecimalEncoder()
    if encoder_name == "Binary":
        return BinaryEncoder(bits_needed_for_palette(palette))
    if encoder_name == "RGB Binary":
        return RGBBinaryEncoder()
    if encoder_name == "RGB Hex":
        return RGBHexEncoder()
    raise ValueError(f"Unknown encoder: {encoder_name!r}")


def reference_label_fn(encoder_name: str):
    """
    RGBBinaryEncoder/RGBHexEncoder don't use palette ids, so their
    reference chart has to show RGB decimal values instead (e.g.
    "255,255,255") -- everything else still looks up a palette id, so it
    keeps the id label.
    """
    if encoder_name in ("RGB Binary", "RGB Hex"):
        return lambda color: f"{color.r},{color.g},{color.b}"
    return lambda color: str(color.id)


def test_csta_worksheet(
    palette: Palette,
    ensure_variety: bool = False,
    encoder_name: str = "Binary",
) -> tuple[Worksheet, list[StudentSheet], DimensionOption]:
    """
    Build the full 1-pixel-per-cell worksheet for csta2027.png and split it
    into 6 (wide) x 4 (tall) pixel blocks -- no resizing needed since the
    source image already divides evenly.

    Defaults to binary encoding: CS teacher participants decode binary to
    decimal first, then look up the color on the (decimal-keyed) reference
    chart. Pass encoder_name="Decimal" for a simpler, elementary-friendly
    version that skips the binary-to-decimal step entirely.
    """
    section("CSTA image: worksheet + blocks")

    with Image.open(CSTA_IMAGE_PATH) as img:
        width, height = img.size
    print(f"Source image '{CSTA_IMAGE_PATH.name}': {width} x {height} px")

    block_cols, block_rows = 6, 4
    if width % block_cols or height % block_rows:
        raise ValueError(
            f"{width}x{height} image doesn't divide evenly into "
            f"{block_cols}x{block_rows} blocks"
        )

    pixels = load_and_resize_image(CSTA_IMAGE_PATH, rows=height, cols=width)
    grid = quantize_image(pixels, palette)

    mono_before, total_blocks = count_monochrome_blocks(grid, block_rows, block_cols)
    print(f"Monochrome blocks before variety pass: {mono_before}/{total_blocks}")

    if ensure_variety:
        grid = ensure_block_variety(grid, palette, block_rows, block_cols)
        mono_after, _ = count_monochrome_blocks(grid, block_rows, block_cols)
        print(f"Monochrome blocks after variety pass:  {mono_after}/{total_blocks}")

    encoder = build_encoder(encoder_name, palette)
    encoded = encode_grid(grid, encoder)
    worksheet = build_worksheet(
        title="CSTA 2027",
        cells=encoded,
        encoder_name=encoder_name,
        palette_name=palette.name,
    )
    print(f"Worksheet: {worksheet.rows} x {worksheet.cols} (1 cell per pixel, no resize needed)")
    print(f"Encoding: {encoder_name} (e.g. top-left cell = '{encoded[0][0].value}')")

    sheet_size = DimensionOption(rows=block_rows, cols=block_cols)
    sheets = split_into_student_sheets(worksheet, sheet_size)
    print(f"Split into {len(sheets)} blocks of {sheet_size.rows} x {sheet_size.cols} pixels each")

    return worksheet, sheets, sheet_size


def test_blank_sheet(sheet_size: DimensionOption) -> Path:
    section("PDF: blank student sheet")

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / "blank_sheet.pdf"
    per_page = render_blank_block_sheet(sheet_size.rows, sheet_size.cols, out_path)
    print(f"Wrote {out_path} ({per_page} blank blocks fit on the page)")

    return out_path


def test_encoding_sheets(sheets: list[StudentSheet]) -> Path:
    section("PDF: encoding instructions")

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / "encoding_sheets.pdf"
    pages = render_encoding_sheets(sheets, out_path)
    print(f"Wrote {out_path} ({pages} pages for {len(sheets)} blocks)")

    return out_path


def test_reference_sheet(palette: Palette, encoder_name: str = "Decimal") -> Path:
    section("PDF: reference chart")

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / "reference_sheet.pdf"
    render_reference_sheet(palette, out_path, label_fn=reference_label_fn(encoder_name))
    print(f"Wrote {out_path}")

    return out_path


def test_cheat_sheet(worksheet: Worksheet, sheet_size: DimensionOption, cell_size_cm: float = 0.5) -> Path:
    section("PDF: teacher cheat sheet")

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / "cheat_sheet.pdf"
    pages = render_cheat_sheet(
        worksheet, out_path,
        block_rows=sheet_size.rows, block_cols=sheet_size.cols,
        cell_size_cm=cell_size_cm,
    )
    print(f"Wrote {out_path} ({pages} pages, {cell_size_cm:g} cm cells)")

    return out_path


def main():
    palette = test_palette()
    test_palette_16()

    plan = ClassroomPlan(students=24, sheets_per_student=2, cells_per_sheet=10)
    dims = test_dimensions(plan)

    pixels = test_image(dims)
    grid = test_quantize(pixels, palette)
    encoded = test_encode(grid)
    test_encode_binary(grid, palette)
    worksheet = test_worksheet(encoded, palette)

    sheet_size = test_sheet_size(worksheet, plan.cells_per_sheet)
    test_split(worksheet, sheet_size)

    test_csv(worksheet)

    csta_encoder_name = "RGB Hex"
    csta_worksheet, csta_sheets, csta_sheet_size = test_csta_worksheet(
        palette, ensure_variety=True, encoder_name=csta_encoder_name,
    )
    test_blank_sheet(csta_sheet_size)
    test_encoding_sheets(csta_sheets)
    test_reference_sheet(palette, encoder_name=csta_encoder_name)
    test_cheat_sheet(csta_worksheet, csta_sheet_size)


if __name__ == "__main__":
    main()
