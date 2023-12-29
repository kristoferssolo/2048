from enum import Enum


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
