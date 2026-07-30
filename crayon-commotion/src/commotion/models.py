from dataclasses import dataclass

#---------Palette-------------
@dataclass(frozen = True)
class PaletteColor:
    id: int
    name: str
    r: int
    g: int
    b: int


@dataclass(frozen = True)
class Palette:
    name: str
    colors: list[PaletteColor]

#-----------Planning---------
@dataclass
class ClassroomPlan:
    students: int
    sheets_per_student: int
    cells_per_sheet: int
    
    @property
    def total_cells(self) -> int:
        return self.students * self.sheets_per_student * self.cells_per_sheet
    
@dataclass(frozen=True)
class DimensionOption:
    rows: int
    cols: int

    @property
    def cells(self) -> int:
        return self.rows * self.cols
 
#------------Image-----------
@dataclass(frozen=True)
class GridImage:
    rows: int
    cols: int
    pixels: list[list[tuple[int, int, int]]]
    
@dataclass(frozen=True)
class GridCell:
    row: int
    col: int
    rgb: tuple[int, int, int]
    color: PaletteColor

#---------Encoding-----------
@dataclass(frozen=True)
class EncodedCell:
    row: int
    col: int
    color: PaletteColor
    value: str
 
#---------Worksheet----------
@dataclass(frozen=True)
class Worksheet:
    title: str
    rows: int
    cols: int
    encoder_name: str
    palette_name: str
    cells: list[list[EncodedCell]]
    
@dataclass(frozen=True)
class StudentSheet:
    number: int
    total: int

    rows: int
    cols: int

    start_row: int
    start_col: int

    cells: list[EncodedCell]

#--------Run-length-----------
@dataclass(frozen=True)
class Run:
    count: int
    color: PaletteColor
