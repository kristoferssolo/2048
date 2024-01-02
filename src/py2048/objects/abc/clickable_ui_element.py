from abc import abstractmethod
from typing import Callable, Optional

import pygame

from py2048.utils import Position

from .ui_element import UIElement


class ClickableUIElement(UIElement):
    def __init__(
        self,
        hover_color: str,
        action: Optional[Callable[[], None]] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.action = action
        self.hover_color = hover_color
        self.is_hovered = False

    @abstractmethod
    def on_click(self, mouse_pos: Position) -> None:
        """Handle the click event."""

    @abstractmethod
    def on_hover(self, mouse_pos: Position) -> None:
        """Handle the hover event."""

    @abstractmethod
    def _draw_hover_background(self, surface: pygame.Surface) -> None:
        """Draw the hover rectangle."""
