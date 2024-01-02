from enum import Enum


class Original:
    TILE_0 = "#cdc1b4"
    TILE_2 = "#eee4da"
    TILE_4 = "#eee1c9"
    TILE_8 = "#f3b27a"
    TILE_16 = "#f69664"
    TILE_32 = "#f77c5f"
    TILE_64 = "#f75f3b"
    TILE_128 = "#edcf72"
    TILE_256 = "#edcc61"
    TILE_512 = "#edc850"
    TILE_1024 = "#edc53f"
    TILE_2048 = "#edc22e"
    TILE_ELSE = "#ff0000"
    LIGHT_TEXT = "#f9f6f2"
    DARK_TEXT = "#776e65"
    OTHER = "#000000"
    BG = "#faf8ef"
    BOARD_BG = "#bbada0"


class ColorScheme(Enum):
    ORIGINAL = Original
    DARK = ...  # TODO: Implement dark color scheme
