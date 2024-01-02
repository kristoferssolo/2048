from enum import Enum
from pathlib import Path

from loguru import logger

from .config import Config

BASE_PATH = Path(__file__).resolve().parent.parent.parent


def _setup_logger() -> None:
    logger.add(
        BASE_PATH.joinpath(".logs", "game.log"),
        format="{time} | {level} | {message}",
        level="DEBUG" if BASE_PATH.joinpath("debug").exists() else "INFO",
        rotation="1 MB",
        compression="zip",
    )


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
