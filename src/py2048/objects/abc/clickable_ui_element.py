from abc import ABC, ABCMeta, abstractmethod
from typing import Callable, Optional

import pygame


class ClickableUIElement(ABC, metaclass=ABCMeta):
    def __init__(
        self,
        /,
        hover_color: str,
        action: Optional[Callable[[], None]] = None,
    ) -> None:
        self.action = action
        self.hover_color = hover_color
        self.is_hovered = False

    @abstractmethod
    def on_click(self) -> None:
        """Handle the click event."""

    @abstractmethod
    def on_hover(self) -> None:
        """Handle the hover event."""

    @abstractmethod
    def _draw_hover_background(self, surface: pygame.Surface) -> None:
        """Draw the hover rectangle."""
