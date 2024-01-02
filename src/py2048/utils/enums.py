from enum import Enum

from .collections import Position


class Direction(Enum):
    UP = Position(0, -1)
    DOWN = Position(0, 1)
    LEFT = Position(-1, 0)
    RIGHT = Position(1, 0)

    def __mul__(self, num: int) -> Position:
        """Multiply the direction by a constant."""
        return Position(self.value.x * num, self.value.y * num)

    def __imul__(self, num: int) -> tuple[int, int]:
        """Multiply the direction by a constant."""
        return Position(self.value.x * num, self.value.y * num)
