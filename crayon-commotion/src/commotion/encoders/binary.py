from commotion.encoders.encoder import Encoder
from commotion.models import GridCell, Palette


def bits_needed_for_palette(palette: Palette) -> int:
    """
    The minimum number of bits needed to represent every color id in the
    palette. A 24-color palette has ids 0-23, and 23 needs 5 bits to write
    in binary (2**4 = 16 isn't enough, 2**5 = 32 is), so every color in
    that palette gets encoded using 5 bits.
    """
    largest_id = palette.colors[0].id
    for color in palette.colors[1:]:
        if color.id > largest_id:
            largest_id = color.id

    return max(1, largest_id.bit_length())


class BinaryEncoder(Encoder):
    """
    Encodes each cell's color id as binary, padded with leading zeros so
    every value in the worksheet uses the same number of digits (e.g.
    "00101" instead of "101"). Real binary encoding uses a fixed number of
    bits per value, so this keeps the worksheet honest about that -- and
    the fixed width is exactly what makes the "how many bits do you need
    for N colors" discussion visible in the printed materials themselves.
    """

    def __init__(self, bit_width: int):
        self.bit_width = bit_width

    def encode(self, cell: GridCell) -> str:
        return format(cell.color.id, f"0{self.bit_width}b")
