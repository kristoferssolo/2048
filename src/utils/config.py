from attr import define, field

from .collections import Board, Font, Header, Position, Screen, Size, Tile
from .color import ColorScheme
from .enums import Direction


@define
class Config:
    font = Font()

    colorscheme = ColorScheme.ORIGINAL.value

    tile = Tile()
    board = Board()
    header = Header()
    screen = Screen()
