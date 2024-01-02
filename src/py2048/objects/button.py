import sys
from typing import Callable, Optional

import pygame
from attrs import define, field

from py2048 import Config
from py2048.utils import Direction, Position

from .abc import ClickableUIElement, UIElement


class Button(UIElement, ClickableUIElement):
    def __init__(
        self,
        /,
        *,
        hover_color: str,
        action: Optional[Callable[[], None]] = None,
        **kwargs,
    ):
        super().__init__(hover_color, action)
        Static.__init__(self, **kwargs)

    def on_click(self) -> None:
        pass

    def on_hover(self) -> None:
        pass

    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw a rectangle with borders on the given surface."""
        pygame.draw.rect(
            surface,
            self.bg_color,
            (*self.position, *self.size),
            border_radius=self.border_radius,
        )

    def _draw_text(self) -> None:
        """Draw the text of the element."""
        self.rendered_text = self.font.render(
            self.text, True, self.font_color, self.bg_color
        )
        self.rect = self.rendered_text.get_rect(topleft=self.position)

    def _create_surface(self) -> pygame.Surface:
        """Create a surface for the element."""
        sprite_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self._draw_background(sprite_surface)
        return sprite_surface

    def check_hover(self, mouse_pos: tuple[int, int]) -> None:
        """Check if the mouse is hovering over the button."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos: tuple[int, int]) -> None:
        """Check if the button is clicked."""
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button on the given surface."""

        self._draw_hover_background(
            surface
        ) if self.is_hovered else self._draw_background(surface)

        surface.blit(self.rendered_text, self.rect.topleft)

    def _draw_hover_background(self, surface: pygame.Surface) -> None:
        """Draw the hover rectangle."""
        pygame.draw.rect(
            surface,
            self.hover_color,
            self.rect,
            border_radius=self.border_radius,
        )
