import pygame

from py2048 import Config
from py2048.objects import ScoreLabel
from py2048.utils import Position, Size


class Header:
    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, *Config.HEADER.size)
        self.labels = self._create_labels()

    def _create_labels(self) -> pygame.sprite.Group:
        size = Size(60, 40)

        self.score = ScoreLabel(
            value=0,
            text="Score",
            size=size,
            position=Position(
                Config.SCREEN.size.width - Config.TILE.size // 2 - size.width * 2 - 10,
                10,
            ),
            bg_color=Config.COLORSCHEME.BOARD_BG,
            font_color=Config.COLORSCHEME.LIGHT_TEXT,
            font_size=16,
            border_radius=2,
        )
        highscore = ScoreLabel(
            value=2048,
            text="Best",
            size=size,
            position=Position(
                Config.SCREEN.size.width - Config.TILE.size // 2 - size.width, 10
            ),
            bg_color=Config.COLORSCHEME.BOARD_BG,
            font_color=Config.COLORSCHEME.LIGHT_TEXT,
            font_size=16,
            border_radius=2,
        )

        return pygame.sprite.Group(self.score, highscore)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the header."""
        self.labels.draw(surface)

    def update(self, score: int) -> None:
        """Update the score."""
        self.score.update_score(score)
