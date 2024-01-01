import random
from typing import Union

import pygame

from .color import Color
from .config import Config
from .utils import Direction, grid_pos


class Block(pygame.sprite.Sprite):
    def __init__(
        self, x: int, y: int, group: pygame.sprite.Group, value: int | None = 2
    ):
        """Initialize a block"""
        super().__init__()
        self.image = pygame.Surface((Config.BLOCK_SIZE, Config.BLOCK_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.value: int = (
            value
            if value is not None
            else 2
            if random.random() <= Config.BLOCK_VALUE_PROBABILITY
            else 4
        )
        self.font = pygame.font.SysFont(Config.FONT_FAMILY, Config.FONT_SIZE)
        self.group = group
        self.update()

    def _draw_value(self) -> None:
        """Draw the value of the block"""
        text = self.font.render(str(self.value), True, Color.FG)
        text_rect = text.get_rect(center=self.image.get_rect().center)
        self.image.blit(text, text_rect)

    def move(self, direction: Direction) -> None:
        """Move the block by `dx` and `dy`."""
        while True:
            new_x, new_y = self._calc_new_pos(direction)

            if self._is_out_if_bounds(new_x, new_y):
                return

            if self._has_collision(new_x, new_y):
                collided_block = self._get_collided_block(new_x, new_y)
                if collided_block and self._can_merge(collided_block):
                    self._merge(collided_block)
                else:
                    return

            self.group.remove(self)
            self.rect.topleft = new_x, new_y
            self.group.add(self)

    def _calc_new_pos(self, direction: Direction) -> tuple[int, int]:
        """Calculate the new position of the block."""
        dx, dy = direction * Config.BLOCK_SIZE
        return self.rect.x + dx, self.rect.y + dy

    def _is_out_if_bounds(self, x: int, y: int) -> bool:
        """Return whether the block is out of bounds."""
        return not (
            0 <= x <= Config.GRID_WIDTH - Config.BLOCK_SIZE
            and 0 <= y <= Config.GRID_HEIGHT - Config.BLOCK_SIZE
        )

    def _has_collision(self, x: int, y: int) -> bool:
        """Checks whether the block has a collision with any other block."""
        return any(
            block.rect.collidepoint(x, y) for block in self.group if block != self
        )

    def _get_collided_block(self, x: int, y: int) -> Union["Block", None]:
        """Get the block that collides with the given block."""

        return next(
            (
                block
                for block in self.group
                if block != self and block.rect.collidepoint(x, y)
            ),
            None,
        )

    def _can_merge(self, other: "Block") -> bool:
        """Check if the block can merge with another block."""
        return self.value == other.value

    def _merge(self, other: "Block") -> None:
        """Merge the block with another block."""
        self.group.remove(other)
        self.group.remove(self)
        self.value += other.value
        self.update()
        self.group.add(self)

    def update(self) -> None:
        """Update the block"""
        self._change_color()
        self._draw_value()

    def can_move(self) -> bool:
        """Check if the block can move"""
        for direction in Direction:
            new_x, new_y = self._calc_new_pos(direction)
            if not self._is_out_if_bounds(new_x, new_y) and self._has_collision(
                new_x, new_y
            ):
                collided_block = self._get_collided_block(new_x, new_y)
                if collided_block and self._can_merge(collided_block):
                    return True
        return False

    def _change_color(self) -> None:
        """Change the color of the block based on its value"""
        color_map = {
            2: Color.BLUE,
            4: Color.BLUE0,
            8: Color.BLUE1,
            16: Color.BLUE2,
            32: Color.DARK3,
            64: Color.BORDER_HIGHLIGHT,
            128: Color.BLUE5,
            256: Color.BLUE6,
            512: Color.BLUE7,
            1024: Color.ORANGE,
            2048: Color.RED,
        }
        self.image.fill(color_map.get(self.value, Color.ERROR))

    def __repr__(self) -> str:
        """Return a string representation of the block"""
        return f"Block({id(self)}): {self.pos} num={self.value}"

    def __str__(self) -> str:
        """Return a string representation of the block"""
        return self.__repr__()

    def __hash__(self) -> int:
        """Return a hash of the block"""
        return hash((self.rect.x, self.rect.y, self.value))

    @property
    def pos(self) -> tuple[int, int]:
        """Return the position of the block"""
        return grid_pos(self.rect.x), grid_pos(self.rect.y)
