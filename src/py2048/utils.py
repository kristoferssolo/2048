from enum import Enum

from .config import Config


def grid_pos(pos: int) -> int:
    """Return the position in the grid."""
    return pos // Config.BLOCK_SIZE + 1


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __mul__(self, num: int) -> tuple[int, int]:
        """Multiply the direction by a constant."""
        return self.value[0] * num, self.value[1] * num

    def __imul__(self, num: int) -> tuple[int, int]:
        """Multiply the direction by a constant."""
        return self.value[0] * num, self.value[1] * num
