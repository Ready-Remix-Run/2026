from commotion.encoders.encoder import Encoder
from commotion.models import GridCell


class RGBDecimalEncoder(Encoder):
    """
    Encodes each cell as its actual red, green, and blue values, each as a
    plain decimal number, one component per line (e.g. "255\\n162\\n0").
    The inverse practice of RGBBinaryEncoder/RGBHexEncoder: those hand
    students binary/hex to decode down to decimal, while this hands them
    decimal and has them encode up to binary themselves, checking their
    work against a reference chart that shows each color's binary triple
    instead of a decimal one.
    """

    def encode(self, cell: GridCell) -> str:
        color = cell.color
        return f"{color.r}\n{color.g}\n{color.b}"
