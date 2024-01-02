import random
from typing import Union

import pygame
from loguru import logger

from py2048 import Config
from py2048.utils import ColorScheme, Direction, Position, Size

from .abc import MovableUIElement, UIElement


def _grid_pos(pos: int) -> int:
    """Return the position in the grid."""
    return pos // Config.TILE.size + 1


class Tile(MovableUIElement, pygame.sprite.Sprite):
    def __init__(
        self,
        position: Position,
        group: pygame.sprite.Group,
    ):
        pygame.sprite.Sprite.__init__(self)
        self.value = 2 if random.random() <= Config.TILE.value_probability else 4

        super().__init__(
            position=position,
            text=f"{self.value}",
            bg_color=Config.COLORSCHEME.TILE_0,
            font_color=Config.COLORSCHEME.DARK_TEXT,
            size=Size(Config.TILE.size, Config.TILE.size),
            border_radius=Config.TILE.border.radius,
            border_width=Config.TILE.border.width,
        )
        self.score: int = 0
        self.group = group

        self.image = self._create_surface()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.update()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the value of the tile."""
        self._draw_background(surface)
        self._draw_text()
        self.image.blit(self.image, (0, 0))

    def update(self) -> None:
        """Update the sprite."""
        self._draw_background(self.image)
        self.text = f"{self.value}"
        self._draw_text()
        self.image.blit(self.image, (0, 0))

    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw a rounded rectangle on the given surface."""
        if self.size:
            pygame.draw.rect(
                surface,
                self._get_color(),
                (0, 0, *self.size),
                border_radius=Config.TILE.border.radius,
            )
            self._draw_border(surface)

    def _draw_border(self, surface: pygame.Surface) -> None:
        """Draw a rounded border on the given surface."""
        if self.size:
            pygame.draw.rect(
                surface,
                (0, 0, 0, 0),
                (0, 0, *self.size),
                border_radius=Config.TILE.border.radius,
                width=Config.TILE.border.width,
            )

    def _draw_text(self) -> None:
        """Draw the text of the sprite."""
        self.rendered_text = self.font.render(self.text, True, self.font_color)
        self.image.blit(
            self.rendered_text,
            self.rendered_text.get_rect(center=self.image.get_rect().center),
        )

    def _create_surface(self) -> pygame.Surface:
        """Create a surface for the sprite."""
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self._draw_background(surface)
        return surface

    def move(self, direction: Direction) -> None:
        """
        Move the tile by `dx` and `dy`.
        If the tile collides with another tile, it will merge with it if possible.
        Before moving, reset the score of the tile.
        """
        while True:
            new_x, new_y = self._calc_new_pos(direction)

            if self._is_out_if_bounds(new_x, new_y):
                return

            if self._has_collision(new_x, new_y):
                collided_tile = self._get_collided_tile(new_x, new_y)
                if collided_tile and self._can_merge(collided_tile):
                    self._merge(collided_tile)
                else:
                    return

            self.group.remove(self)
            self.rect.topleft = new_x, new_y
            self.group.add(self)

    def get_score(self) -> int:
        """Return the score of the tile."""
        return self.score

    def _calc_new_pos(self, direction: Direction) -> tuple[int, int]:
        """Calculate the new position of the tile."""
        dx, dy = direction * Config.TILE.size
        return self.rect.x + dx, self.rect.y + dy

    def _is_out_if_bounds(self, x: int, y: int) -> bool:
        """Return whether the tile is out of bounds."""
        board_left = Config.BOARD.pos.x
        board_right = Config.BOARD.pos.x + Config.BOARD.size.width - Config.TILE.size
        board_top = Config.BOARD.pos.y
        board_bottom = Config.BOARD.pos.y + Config.BOARD.size.height - Config.TILE.size
        return not (board_left <= x <= board_right and board_top <= y <= board_bottom)

    def _has_collision(self, x: int, y: int) -> bool:
        """Checks whether the tile has a collision with any other tile."""
        return any(tile.rect.collidepoint(x, y) for tile in self.group if tile != self)

    def _get_collided_tile(self, x: int, y: int) -> Union["Tile", None]:
        """Get the tile that collides with the given tile."""

        return next(
            (
                tile
                for tile in self.group
                if tile != self and tile.rect.collidepoint(x, y)
            ),
            None,
        )

    def _can_merge(self, other: "Tile") -> bool:
        """Check if the tile can merge with another tile."""
        return self.value == other.value

    def _merge(self, other: "Tile") -> None:
        """Merge the tile with another tile."""
        self.group.remove(other)
        self.group.remove(self)
        self.value += other.value
        self.update()
        self.group.add(self)

    def can_move(self) -> bool:
        """Check if the tile can move"""
        for direction in Direction:
            new_x, new_y = self._calc_new_pos(direction)
            if not self._is_out_if_bounds(new_x, new_y) and self._has_collision(
                new_x, new_y
            ):
                collided_tile = self._get_collided_tile(new_x, new_y)
                if collided_tile and self._can_merge(collided_tile):
                    return True
        return False

    def _get_color(self) -> str:
        """Change the color of the tile based on its value."""
        color_map = {
            2: Config.COLORSCHEME.TILE_2,
            4: Config.COLORSCHEME.TILE_4,
            8: Config.COLORSCHEME.TILE_8,
            16: Config.COLORSCHEME.TILE_16,
            32: Config.COLORSCHEME.TILE_32,
            64: Config.COLORSCHEME.TILE_64,
            128: Config.COLORSCHEME.TILE_128,
            256: Config.COLORSCHEME.TILE_256,
            512: Config.COLORSCHEME.TILE_512,
            1024: Config.COLORSCHEME.TILE_1024,
            2048: Config.COLORSCHEME.TILE_2048,
        }
        return color_map.get(self.value, Config.COLORSCHEME.TILE_ELSE)

    def __repr__(self) -> str:
        """Return a string representation of the tile."""
        return f"Tile({id(self)}): {self.pos} num={self.value}"

    def __str__(self) -> str:
        """Return a string representation of the tile."""
        return self.__repr__()

    def __hash__(self) -> int:
        """Return a hash of the tile."""
        return hash((self.rect.x, self.rect.y, self.value))

    @property
    def pos(self) -> Position:
        """Return the position of the tile."""
        return Position(_grid_pos(self.rect.x), _grid_pos(self.rect.y))
