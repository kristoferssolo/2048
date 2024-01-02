import sys
from typing import Callable, Optional

import pygame
from attrs import define, field

from py2048 import Config
from py2048.utils import Direction, Position

from .abc import ClickableUIElement, UIElement


class Button(ClickableUIElement, pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(*args, **kwargs)

        self.image = self._create_surface()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.update()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button on the given surface."""
        self._draw_background(surface)
        self._draw_text()
        self.image.blit(self.image, (0, 0))

    def update(self) -> None:
        """Update the button."""
        self._draw_background(self.image)
        self._draw_text()
        self.image.blit(self.image, (0, 0))

    def on_click(self, mouse_pos: Position) -> None:
        """Handle the click event."""
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()

    def on_hover(self, mouse_pos: Position) -> None:
        pass

    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw a rectangle on the given surface."""
        if self.size:
            pygame.draw.rect(
                surface,
                self.bg_color,
                (0, 0, *self.size),
                border_radius=Config.TILE.border.radius,
            )

    def _draw_hover_background(self, surface: pygame.Surface) -> None:
        """Draw the hover rectangle."""
        pygame.draw.rect(
            surface,
            self.hover_color,
            self.rect,
            border_radius=self.border_radius,
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
