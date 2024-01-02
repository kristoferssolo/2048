from pathlib import Path

from loguru import logger

from .collections import Board, Font, Header, Position, Screen, Size, Tile
from .color import ColorScheme
from .enums import Direction

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent


def setup_logger() -> None:
    logger.add(
        BASE_PATH.joinpath(".logs", "game.log"),
        format="{time} | {level} | {message}",
        level="DEBUG" if BASE_PATH.joinpath("debug").exists() else "INFO",
        rotation="1 MB",
        compression="zip",
    )


__all__ = [
    "BASE_PATH",
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
