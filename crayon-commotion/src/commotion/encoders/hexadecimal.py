from commotion.encoders.encoder import Encoder
from commotion.models import GridCell


class RGBHexEncoder(Encoder):
    """
    Encodes each cell as its actual red, green, and blue values, each as a
    2-digit uppercase hex byte, one component per line (e.g. "FF\\nA2\\n00").
    Like RGBBinaryEncoder, this is the literal color rather than a palette
    id, so the reference chart needs RGB decimal labels to match it, not
    palette ids.
    """

    def encode(self, cell: GridCell) -> str:
        color = cell.color
        return f"{color.r:02X}\n{color.g:02X}\n{color.b:02X}"
