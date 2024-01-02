import pygame

from py2048 import Config
from py2048.objects import Label
from py2048.utils import Position


class Header:
    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, *Config.HEADER.size)

    def draw(self, screen: pygame.Surface, score: int) -> None:
        """Draw the header."""
        self.score = Label(
            text=f"{score}",
            position=Position(10, 10),
            bg_color=Config.COLORSCHEME.BOARD_BG,
            font_family=Config.FONT.family,
            font_color=Config.COLORSCHEME.DARK_TEXT,
            font_size=Config.FONT.size,
        ).draw(screen)

    def update(self, score: int) -> None:
        """Update the header."""
        self.Label.text = f"{score}"
