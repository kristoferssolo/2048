import pygame

from py2048 import Config
from py2048.objects import Label
from py2048.utils import Position, Size


class Header:
    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, *Config.HEADER.size)
        self.labels = self._create_labels()

    def _create_labels(self) -> pygame.sprite.Group:
        score = Label(
            text=f"SCORE\n{0}",
            size=Size(50, 50),
            position=Position(0, 0),
            bg_color=Config.COLORSCHEME.BOARD_BG,
            font_color=Config.COLORSCHEME.LIGHT_TEXT,
            font_size=16,
        )
        highscore = Label(
            text=f"HIGHSCORE\n{2048}",
            size=Size(50, 50),
            position=Position(200, 0),
            bg_color=Config.COLORSCHEME.BOARD_BG,
            font_color=Config.COLORSCHEME.LIGHT_TEXT,
            font_size=16,
        )
        return pygame.sprite.Group(score, highscore)

    def draw(self, screen: pygame.Surface, score: int) -> None:
        """Draw the header."""
        self.labels.draw(screen)

    def update(self, score: int) -> None:
        """Update the header."""
        # self.labels. = f"SCORE\n{score}"
        self.labels.update()
