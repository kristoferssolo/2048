import random

from typing import Union

import pygame
from loguru import logger

from .colors import COLORS
from .config import Config

from .utils import Direction


def _grid_pos(pos: int) -> int:
    """Return the position in the grid."""
    return pos // Config.BLOCK_SIZE + 1


class Block(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, value: int | None = 2):
        """Initialize a block"""
        super().__init__()
        self.image = pygame.Surface((Config.BLOCK_SIZE, Config.BLOCK_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        logger.debug(f"Generated block({id(self)}) at {self}")

        self.value: int = value if value is not None else 2 if random.random() <= Config.BLOCK_VALUE_PROBABILITY else 4
        self.font = pygame.font.SysFont(Config.FONT_FAMILY, Config.FONT_SIZE)
        self.update()

    def _draw_value(self) -> None:
        """Draw the value of the block"""
        text = self.font.render(str(self.value), True, COLORS.FG)
        text_rect = text.get_rect(center=self.image.get_rect().center)
        self.image.blit(text, text_rect)

    def move(self, direction: Direction) -> None:
        """Move the block by `dx` and `dy`."""
        dx, dy = direction * Config.BLOCK_SIZE

        while True:
            new_x, new_y = self._calc_new_pos(direction)

            if self._is_out_if_bounds(new_x, new_y):
                logger.debug(f"Block({id(self)}) stayed at {self.pos()} (out of bounds)")
                return

            if self._has_collision(new_x, new_y):
                logger.debug(f"Block({id(self)}) collided with another, stopped at {self.pos()}")
                return

            self.rect.topleft = new_x, new_y
            logger.debug(f"Moving block({id(self)}): {self.pos()} => ({_grid_pos(new_x)}, {_grid_pos(new_y)})")

    def _calc_new_pos(self, direction: Direction) -> tuple[int, int]:
        """Calculate the new position of the block."""
        dx, dy = direction * Config.BLOCK_SIZE
        return self.rect.x + dx, self.rect.y + dy

    def _is_out_if_bounds(self, x: int, y: int) -> bool:
        """Return whether the block is out of bounds."""
        return not (0 <= x <= Config.WIDTH - Config.BLOCK_SIZE and 0 <= y <= Config.HEIGHT - Config.BLOCK_SIZE)

    def _has_collision(self, x: int, y: int) -> bool:
        """Checks whether the block has a collision with any other block."""
        return any(block.rect.collidepoint(x, y) for block in self.groups()[0] if block != self)

    def _get_collided_block(self) -> Union["Block", None]:
        """Get the block that collides with the given rectangle."""

    def _merge(self, other: "Block") -> None:
        """Merge the block with another block."""

    def update(self) -> None:
        """Update the block"""
        self._change_color()
        self._draw_value()

    def _change_color(self) -> None:
        """Change the color of the block based on its value"""
        color_map = {
            2: COLORS.BLUE,
            4: COLORS.BLUE0,
            8: COLORS.BLUE1,
            16: COLORS.BLUE2,
            32: COLORS.DARK3,
            64: COLORS.BORDER_HIGHLIGHT,
            128: COLORS.BLUE5,
            256: COLORS.BLUE6,
            512: COLORS.BLUE7,
            1024: COLORS.ORANGE,
            2048: COLORS.RED,
        }
        self.image.fill(color_map.get(self.value, COLORS.ERROR))

    def __add__(self, other: "Block") -> None:
        """Add the value of two blocks and update the current block"""
        logger.debug(f"Merging blocks ({id(self)}) and ({id(other)}) => ({id(self)}), {self.pos()}")
        self.value += other.value
        self.update()

    def __iadd__(self, other: "Block") -> None:
        """Add the value of two blocks and updae the current block"""
        logger.debug(f"Merging blocks ({id(self)}) and ({id(other)}) => ({id(self)}), {self.pos()}")
        self.value += other.value
        self.update()

    def __repr__(self) -> str:
        """Return a string representation of the block"""
        return f"Block({id(self)}): ({self.pos()})"

    def __str__(self) -> str:
        """Return a string representation of the block"""
        return self.__repr__()

    def __hash__(self) -> int:
        """Return a hash of the block"""
        return hash((self.rect.x, self.rect.y, self.value))

    def pos(self) -> tuple[int, int]:
        """Return the position of the block"""
        return _grid_pos(self.rect.x), _grid_pos(self.rect.y)
