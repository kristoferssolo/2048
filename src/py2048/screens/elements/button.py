import sys

import pygame
from attrs import define, field
from py2048.color import ColorScheme
from py2048.config import Config


@define
class Button:
    text: str = field()
    font_family: str = field()
    font_size: int = field()
    font_color: ColorScheme = field()
    position: tuple[int, int] = field()
    width: int = field()
    height: int = field()
    action = field()
    bg_color: ColorScheme = field()
    hover_color: ColorScheme = field()
    font: pygame.Font = field(init=False)
    rendered_text: pygame.Surface = field(init=False)
    rect: pygame.Rect = field(init=False)
    is_hovered: bool = field(init=False, default=False)

    def __attrs_post_init__(self) -> None:
        """Initialize the button."""
        self.font = pygame.font.SysFont(self.font_family, self.font_size)
        self._draw_text()

    def _draw_text(self) -> None:
        """Draw the text on the button."""
        self.rendered_text = self.font.render(
            self.text, True, self.font_color, self.bg_color
        )
        self.rect = pygame.Rect(
            self.position[0], self.position[1], self.width, self.height
        )

    def check_hover(self, mouse_pos: tuple[int, int]) -> None:
        """Check if the mouse is hovering over the button."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos: tuple[int, int]) -> None:
        """Check if the button is clicked."""
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button on the given surface."""
        if self.is_hovered:
            self._draw_rect(surface, self.hover_color)
        else:
            self._draw_rect(surface, self.bg_color)

        surface.blit(self.rendered_text, self.position)

    def _draw_rect(self, surface: pygame.Surface, color: ColorScheme) -> None:
        """Draw the button rectangle."""
        pygame.draw.rect(surface, self.bg_color, self.rect)
