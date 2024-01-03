from typing import NamedTuple

from attr import Factory, define, field


class Position(NamedTuple):
    x: int | float
    y: int | float


class Size(NamedTuple):
    width: int
    height: int


@define
class Font:
    family: str = "Roboto"
    size: int = 32


@define
class Border:
    width: int
    radius: int


@define
class Tile:
    size: int = 75
    border: Border = Border(size // 20, size // 10)
    initial_count: int = 2
    probability: tuple[float, float] = 0.9, 0.1


@define
class Board:
    len: int = 4
    size: Size = Size(len * Tile().size, len * Tile().size)
    pos: Position = Position(Tile().size // 2, Tile().size + Tile().size // 2)


@define
class Header:
    size: Size = Size(Board().size.width + Tile().size, Tile().size)


@define
class Screen:
    size: Size = Size(
        Header().size.width, Board().size.height + Tile().size + Header().size.height
    )
