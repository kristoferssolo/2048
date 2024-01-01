from enum import Enum


class Original:
    BLOCK_0 = "#ccc0b3"
    BLOCK_2 = "#eee4da"
    BLOCK_4 = "#ede0c8"
    BLOCK_8 = "#f2b179"
    BLOCK_16 = "#f59563"
    BLOCK_32 = "#f67c5f"
    BLOCK_64 = "#f65e3b"
    BLOCK_128 = "#edcf72"
    BLOCK_256 = "#edcc61"
    BLOCK_512 = "#edc850"
    BLOCK_1024 = "#edc53f"
    BLOCK_2048 = "#edc22e"
    BLOCK_ELSE = "#ff0000"
    LIGHT_TEXT = "#f9f6f2"
    DARK_TEXT = "#776e65"
    OTHER = "#000000"
    BG = "#bbada0"


class ColorScheme(Enum):
    ORIGINAL = Original
    DARK = ...  # TODO: Implement dark color scheme
