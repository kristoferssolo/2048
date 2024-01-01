import pygame
from py2048.config import Config

from .elements.label import Label


class Header:
    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, Config.HEADER_WIDTH, Config.HEADER_HEIGHT)

    def draw(self, screen: pygame.Surface, score: int) -> None:
        """Draw the header."""
        score = Label(
            text=f"{score}",
            position=(10, 10),
            bg_color=Config.COLORSCHEME.BOARD_BG,
            font_family=Config.FONT_FAMILY,
            font_color=Config.COLORSCHEME.DARK_TEXT,
            font_size=Config.FONT_SIZE,
        ).draw(screen)
