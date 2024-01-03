from loguru import logger
from path import BASE_PATH

from .collections import Board, Font, Header, Position, Screen, Size, Tile
from .color import ColorScheme
from .enums import Direction


def setup_logger() -> None:
    logger.add(
        BASE_PATH.joinpath(".logs", "game.log"),
        format="{time} | {level} | {message}",
        level="DEBUG" if BASE_PATH.joinpath("debug").exists() else "INFO",
        rotation="10 MB",
        compression="zip",
    )


__all__ = [
    "Board",
    "ColorScheme",
    "Direction",
    "Font",
    "Position",
    "Size",
    "Tile",
    "setup_logger",
    "Header",
    "Screen",
]
