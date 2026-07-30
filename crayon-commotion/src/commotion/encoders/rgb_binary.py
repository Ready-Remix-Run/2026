from commotion.encoders.encoder import Encoder
from commotion.models import GridCell


class RGBBinaryEncoder(Encoder):
    """
    Encodes each cell as its actual red, green, and blue values, each as
    8-bit binary, one component per line (e.g. "11101110\\n00100000\\n01001101").
    Unlike DecimalEncoder/BinaryEncoder, this doesn't use the palette id at
    all -- decoding recovers the color directly from its RGB components, so
    the reference chart needs to show RGB values too, not palette ids.
    """

    def encode(self, cell: GridCell) -> str:
        color = cell.color
        return f"{color.r:08b}\n{color.g:08b}\n{color.b:08b}"
