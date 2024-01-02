import pygame

from py2048 import Config
from py2048.objects import Label
from py2048.utils import Position, Size


class Header:
    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, *Config.HEADER.size)

    def draw(self, screen: pygame.Surface, score: int) -> None:
        """Draw the header."""
        self.label = Label(
            text=f"{score}",
            size=Size(50, 50),
            position=Position(0, 0),
            bg_color=Config.COLORSCHEME.BOARD_BG,
            font_color=Config.COLORSCHEME.DARK_TEXT,
            font_size=16,
        )
        self.label.draw(screen)

    def update(self, score: int) -> None:
        """Update the header."""
        self.label.text = f"SCORE\n{score}"
        self.label.update()
