from commotion.encoders.encoder import Encoder
from commotion.models import GridCell


class DecimalEncoder(Encoder):

    def encode(self, cell: GridCell) -> str:
        return str(cell.color.id)