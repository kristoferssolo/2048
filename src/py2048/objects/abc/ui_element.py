from abc import ABC, ABCMeta, abstractmethod
from typing import Optional

import pygame
from loguru import logger

from py2048 import Config
from py2048.utils import Position, Size


class UIElement(ABC, metaclass=ABCMeta):
    def __init__(
        self,
        /,
        *,
        position: Position,
        bg_color: str,
        font_color: str,
        font_size: int = Config.FONT.size,
        font_family: str = Config.FONT.family,
        size: Size = Size(50, 50),
        text: str = "",
        border_radius: int = 0,
        border_width: int = 0,
    ):
        super().__init__()
        self.text = text
        self.size = size
        self.bg_color = bg_color
        self.font_color = font_color
        self.border_radius = border_radius
        self.border_width = border_width
        self.position = position
        self.x, self.y = self.position
        self.font = pygame.font.SysFont(font_family, font_size)

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the element."""

    @abstractmethod
    def update(self) -> None:
        """Update the element."""

    @abstractmethod
    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw a background for the given surface."""

    @abstractmethod
    def _draw_text(self) -> None:
        """Draw the text of the element."""

    @abstractmethod
    def _create_surface(self) -> pygame.Surface:
        """Create a surface for the element."""
