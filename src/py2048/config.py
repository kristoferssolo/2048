from .utils import Board, ColorScheme, Font, Header, Position, Screen, Size, Tile


class Config:
    FONT = Font()

    COLORSCHEME = ColorScheme.ORIGINAL.value

    TILE = Tile()
    BOARD = Board()
    HEADER = Header()
    SCREEN = Screen()
