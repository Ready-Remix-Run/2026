from commotion.models import (
    DimensionOption,
    StudentSheet,
    Worksheet,
)
from dataclasses import replace


def split_into_student_sheets(
    worksheet: Worksheet,
    sheet_size: DimensionOption,
) -> list[StudentSheet]:

    if worksheet.rows % sheet_size.rows != 0:
        raise ValueError(
            "Worksheet rows must be divisible by sheet rows."
        )

    if worksheet.cols % sheet_size.cols != 0:
        raise ValueError(
            "Worksheet columns must be divisible by sheet columns."
        )

    sheets: list[StudentSheet] = []
    sheet_number = 1

    for start_row in range(0, worksheet.rows, sheet_size.rows):
        for start_col in range(0, worksheet.cols, sheet_size.cols):

            sheet_cells = []

            for row in range(start_row, start_row + sheet_size.rows):
                for col in range(start_col, start_col + sheet_size.cols):
                    sheet_cells.append(
                        worksheet.cells[row][col]
                    )

            sheets.append(
                StudentSheet(
                    number=sheet_number,
                    total=0,          # temporary
                    rows=sheet_size.rows,
                    cols=sheet_size.cols,
                    start_row=start_row,
                    start_col=start_col,
                    cells=sheet_cells,
                )
            )

            sheet_number += 1

    total = len(sheets)

    sheets = [
        replace(sheet, total=total)
        for sheet in sheets
    ]

    return sheets