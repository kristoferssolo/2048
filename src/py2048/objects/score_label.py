from typing import Optional

import pygame
from loguru import logger

from py2048 import Config
from py2048.utils import Position, Size

from .abc import UIElement


class ScoreLabel(UIElement, pygame.sprite.Sprite):
    def __init__(self, value: int, *args, **kwargs) -> None:
        pygame.sprite.Sprite.__init__(self)
        super().__init__(*args, **kwargs)
        self.value = value
        self.image = self._create_surface()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.update()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the element on the given surface."""
        self._draw_background(surface)
        self._draw_text()

    def update(self) -> None:
        """Update the sprite."""
        self._draw_background(self.image)
        self._draw_text()

    def update_score(self, score: int) -> None:
        """Update the score value."""
        self.value = score
        self.update()

    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw a background for the given surface."""
        if self.size:
            pygame.draw.rect(
                surface,
                self.bg_color,
                (0, 0, *self.size),
                border_radius=self.border_radius,
            )

    def _draw_text(self) -> None:
        """Draw the text of the element."""
        centerx, centery = self.image.get_rect().center

        # Render text
        label_text = self.font.render(self.text, True, self.font_color)
        label_rect = label_text.get_rect(center=(centerx, centery - 10))
        self.image.blit(label_text, label_rect)

        # Render value
        score_text = self.font.render(f"{self.value}", True, self.font_color)
        score_rect = score_text.get_rect(center=(centerx, centery + 10))
        self.image.blit(score_text, score_rect)

    def _create_surface(self) -> pygame.Surface:
        """Create a surface for the element."""
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self._draw_background(surface)
        return surface
