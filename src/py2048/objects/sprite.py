from abc import ABC, ABCMeta, abstractmethod

import pygame

from py2048 import Config, Direction


class Sprite(ABC, pygame.sprite.Sprite, metaclass=ABCMeta):
    def __init__(self, x: int, y: int, group: pygame.sprite.Group):
        super().__init__()
        self.image = self._create_surface()
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.font = pygame.font.SysFont(Config.FONT_FAMILY, Config.FONT_SIZE)
        self.group = group
        self.update()

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the sprite on the given surface."""

    @abstractmethod
    def update(self) -> None:
        """Update the sprite."""

    @abstractmethod
    def move(self, direction: Direction) -> None:
        """Move the tile by `dx` and `dy`."""

    @abstractmethod
    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw a rounded rectangle with borders on the given surface."""

    @abstractmethod
    def _create_surface(self) -> pygame.Surface:
        """Create a surface for the sprite."""
        sprite_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        self._draw_background(sprite_surface)
        return sprite_surface
