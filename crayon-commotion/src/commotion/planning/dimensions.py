from __future__ import annotations

from math import isqrt

from commotion.models import ClassroomPlan, DimensionOption


def suggest_dimensions(
    plan: ClassroomPlan,
    max_options: int = 8,
) -> list[DimensionOption]:
    """
    Suggest image grid dimensions based on classroom needs.
    """
    if plan.students <= 0:
        raise ValueError("students must be > 0")
    if plan.sheets_per_student <= 0:
        raise ValueError("sheets_per_student must be > 0")
    if plan.cells_per_sheet <= 0:
        raise ValueError("cells_per_sheet must be > 0")

    total_cells = plan.total_cells
    options: list[DimensionOption] = []

    for rows in range(1, isqrt(total_cells) + 1):
        if total_cells % rows == 0:
            cols = total_cells // rows
            options.append(DimensionOption(rows=rows, cols=cols))

    options.sort(key=lambda opt: abs(opt.rows - opt.cols))
    return options[:max_options]

