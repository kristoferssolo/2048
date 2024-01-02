import random
from typing import Union

import pygame

from py2048 import ColorScheme, Config, Direction

from .sprite import Sprite


def _grid_pos(pos: int) -> int:
    """Return the position in the grid."""
    return pos // Config.TILE_SIZE + 1


class Tile(Sprite):
    def __init__(
        self, x: int, y: int, group: pygame.sprite.Group, value: int | None = 2
    ):
        super().__init__(x, y, group)

        self.value: int = (
            value
            if value is not None
            else 2
            if random.random() <= Config.TILE_VALUE_PROBABILITY
            else 4
        )
        self.image = self._create_surface()
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.font = pygame.font.SysFont(Config.FONT_FAMILY, Config.FONT_SIZE)
        self.group = group
        self.update()

    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw a rounded rectangle with borders on the given surface."""
        rect = (0, 0, Config.TILE_SIZE, Config.TILE_SIZE)
        pygame.draw.rect(
            surface, self._get_color(), rect, border_radius=Config.TILE_BORDER_RADIUS
        )  # background
        pygame.draw.rect(
            surface,
            (0, 0, 0, 0),
            rect,
            border_radius=Config.TILE_BORDER_RADIUS,
            width=Config.TILE_BORDER_WIDTH,
        )  # border

    def _create_surface(self) -> pygame.Surface:
        """Create a surface for the tile."""
        sprite_surface = pygame.Surface(
            (Config.TILE_SIZE, Config.TILE_SIZE), pygame.SRCALPHA
        )
        self._draw_background(sprite_surface)
        return sprite_surface

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the value of the tile."""
        text = self.font.render(str(self.value), True, Config.COLORSCHEME.DARK_TEXT)
        sprite_surface = self._create_surface()

        sprite_center: tuple[int, int] = (Config.TILE_SIZE // 2, Config.TILE_SIZE // 2)

        text_rect: pygame.Rect = text.get_rect(center=self.image.get_rect().center)
        sprite_surface.blit(text, text_rect)

        self.image.blit(sprite_surface, (0, 0))

    def move(self, direction: Direction) -> int:
        """Move the tile by `dx` and `dy`."""
        score = 0
        while True:
            new_x, new_y = self._calc_new_pos(direction)

            if self._is_out_if_bounds(new_x, new_y):
                return score

            if self._has_collision(new_x, new_y):
                collided_tile = self._get_collided_tile(new_x, new_y)
                if collided_tile and self._can_merge(collided_tile):
                    score += self._merge(collided_tile)
                else:
                    return score

            self.group.remove(self)
            self.rect.topleft = new_x, new_y
            self.group.add(self)

    def _calc_new_pos(self, direction: Direction) -> tuple[int, int]:
        """Calculate the new position of the tile."""
        dx, dy = direction * Config.TILE_SIZE
        return self.rect.x + dx, self.rect.y + dy

    def _is_out_if_bounds(self, x: int, y: int) -> bool:
        """Return whether the tile is out of bounds."""
        board_left = Config.BOARD_X
        board_right = Config.BOARD_X + Config.BOARD_WIDTH - Config.TILE_SIZE
        board_top = Config.BOARD_Y
        board_bottom = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.TILE_SIZE
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

    def _merge(self, other: "Tile") -> int:
        """Merge the tile with another tile."""
        self.group.remove(other)
        self.group.remove(self)
        self.value += other.value
        self.update()
        self.group.add(self)
        return self.value

    def update(self) -> None:
        """Update the sprite."""
        self.draw()

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

    def _get_color(self) -> ColorScheme:
        """Change the color of the tile based on its value"""
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
    def pos(self) -> tuple[int, int]:
        """Return the position of the tile."""
        return _grid_pos(self.rect.x), _grid_pos(self.rect.y)
