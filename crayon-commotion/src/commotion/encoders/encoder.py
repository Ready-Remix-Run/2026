from abc import ABC, abstractmethod

from commotion.models import GridCell


class Encoder(ABC):
    """
    Base class for all worksheet encoders.
    """

    @abstractmethod
    def encode(self, cell: GridCell) -> str:
        """
        Return the string that should appear in the worksheet cell.
        """
        pass