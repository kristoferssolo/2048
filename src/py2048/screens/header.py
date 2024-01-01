import pygame

from ..color import Color
from ..config import Config


class Header:
    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, Config.HEADER_WIDTH, Config.HEADER_HEIGHT)
        self.score = 0  # TODO: Implement score

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the header."""
        pygame.draw.rect(screen, Color.MAGENTA, self.rect, 2)
