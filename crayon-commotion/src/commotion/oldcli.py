from pathlib import Path

from commotion.models import ClassroomPlan
from commotion.palettes.loader import load_palette
from commotion.planning.dimensions import suggest_dimensions
from commotion.imaging.resize import load_and_resize_image
from commotion.imaging.quantize import quantize_image
from commotion.encoders.decimal import DecimalEncoder
from commotion.encoders.grid import encode_grid
from commotion.worksheets.builder import build_worksheet
from commotion.renderers.csv_renderer import write_csv
from commotion.planning.sheets import suggest_sheet_dimensions
from commotion.worksheets.splitter import split_into_student_sheets
from commotion.models import DimensionOption

def main():
    project_root = Path(__file__).resolve().parents[2]

    palette_path = project_root / "palettes" / "crayola24.csv"
    palette = load_palette(palette_path, palette_name="Crayola 24")

    print(f"Loaded palette: {palette.name}")
    print(f"Colors: {len(palette.colors)}")
    print()

    plan = ClassroomPlan(
        students=24,
        sheets_per_student=2,
        cells_per_sheet=10,
    )

    print(
        f"Dimension suggestions for {plan.students} students, "
        f"{plan.sheets_per_student} sheets each, "
        f"{plan.cells_per_sheet} cells per sheet:"
    )

    options = suggest_dimensions(plan)

    for option in options:
        print(f"  {option.rows} x {option.cols} = {option.cells} cells")
        
    project_root = Path(__file__).resolve().parents[2]

    # Palette test
    palette_path = project_root / "palettes" / "crayola24.csv"
    palette = load_palette(palette_path, palette_name="Crayola 24")

    print(f"Loaded palette: {palette.name}")
    print(f"Colors: {len(palette.colors)}")
    print()

    # Planning test
    plan = ClassroomPlan(students=24, sheets_per_student=2, cells_per_sheet=10)
    options = suggest_dimensions(plan)

    print("Dimension suggestions:")
    for option in options:
        print(f"  {option.rows} x {option.cols} = {option.cells} cells")
    print()

    # Image test
    image_path = project_root / "images" / "test_image.png"
    chosen = options[0]   # just pick the first suggestion for now

    pixels = load_and_resize_image(image_path, rows=chosen.rows, cols=chosen.cols)

    print(f"Loaded image for grid {chosen.rows} x {chosen.cols}")
    print(f"Top-left pixel: {pixels[0][0]}")
    print(f"Bottom-right pixel: {pixels[-1][-1]}")
    
    grid = quantize_image(pixels, palette)

    cell = grid[0][0]

    print()
    print("First cell")
    print(f"RGB: {cell.rgb}")
    print(f"Nearest crayon: {cell.color.name}")
    
    encoded = encode_grid(
    grid,
    DecimalEncoder(),
    )

    cell = encoded[0][0]

    print(encoded[0][0].value)
    
    worksheet = build_worksheet(
        title="Rainbow Test",
        cells=encoded,
        encoder_name="Decimal",
        palette_name=palette.name,
    )

    print(worksheet)
    
    output = project_root / "output"

    output.mkdir(exist_ok=True)

    write_csv(
        worksheet,
        output / "rainbow.csv",
    )

    print("CSV written.")
    
    print("\nSheet dimensions for 10 cells:")
    for option in suggest_sheet_dimensions(10):
        print(option)

    print("\nSheet dimensions for 12 cells:")
    for option in suggest_sheet_dimensions(12):
        print(option)

    print("\nSheet dimensions for 16 cells:")
    for option in suggest_sheet_dimensions(16):
        print(option)
        
    sheet_size = DimensionOption(rows=4, cols=4)
        
    print(f"Worksheet: {worksheet.rows} x {worksheet.cols}")
    print(f"Sheet: {sheet_size.rows} x {sheet_size.cols}")
        
    

    student_sheets = split_into_student_sheets(
        worksheet,
        sheet_size,
    )

    print(f"Created {len(student_sheets)} student sheets")

    first = student_sheets[0]

    print("First sheet cell locations:")

    for r in range(first.rows):
        for c in range(first.cols):
            cell = first.cells[r * first.cols + c]
            print(f"({cell.row}, {cell.col})", end=" ")
        print()
        
    second = student_sheets[1]

    print("\nSecond sheet cell locations:")

    for r in range(second.rows):
        for c in range(second.cols):
            cell = second.cells[r * second.cols + c]
            print(f"({cell.row}, {cell.col})", end=" ")
        print()


if __name__ == "__main__":
    main()
    
    