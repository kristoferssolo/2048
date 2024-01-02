import pygame
from loguru import logger

from py2048 import Config
from py2048.utils import Position, Size

from .abc import UIElement


class Label(UIElement, pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs) -> None:
        pygame.sprite.Sprite.__init__(self)
        super().__init__(*args, **kwargs)

        self.image = self._create_surface()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.update()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the element on the given surface."""
        self._draw_background(surface)
        self._draw_text()
        self.image.blit(self.image, (0, 0))

    def update(self) -> None:
        """Update the sprite."""
        self._draw_background(self.image)
        self._draw_text()
        self.image.blit(self.image, (0, 0))

    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw a background for the given surface."""
        if self.size:
            pygame.draw.rect(
                surface,
                self.bg_color,
                (0, 0, *self.size),
                border_radius=Config.TILE.border.radius,
            )

    def _draw_text(self) -> None:
        """Draw the text of the element."""
        self.rendered_text = self.font.render(self.text, True, self.font_color)
        self.image.blit(
            self.rendered_text,
            self.rendered_text.get_rect(center=self.image.get_rect().center),
        )

    def _create_surface(self) -> pygame.Surface:
        """Create a surface for the element."""
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self._draw_background(surface)
        return surface
