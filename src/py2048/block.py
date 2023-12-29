import random

import pygame
from loguru import logger

from .colors import COLORS
from .config import Config

from .utils import Direction


def _show_pos(pos: int) -> int:
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
        dx, dy = direction.value

        while True:
            new_x = self.rect.x + dx * Config.BLOCK_SIZE
            new_y = self.rect.y + dy * Config.BLOCK_SIZE

            if not (0 <= new_x <= Config.WIDTH - Config.BLOCK_SIZE and 0 <= new_y <= Config.HEIGHT - Config.BLOCK_SIZE):
                # logger.debug(f"Block({id(self)}) stayed at {self} (out of bounds)")
                break

            collision = any(block.rect.collidepoint(new_x, new_y) for block in self.groups()[0] if block != self)

            if collision:
                logger.debug(f"Block({id(self)}) collided with another block, stopped at {self}")
                break

            self.rect.topleft = new_x, new_y
            logger.debug(f"Moving block({id(self)}): {self} => ({_show_pos(new_x)}, {_show_pos(new_y)})")

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
        logger.debug(f"Merging blocks ({id(self)}) and ({id(other)}) => ({id(self)}), {self}")
        self.value += other.value
        self.update()

    def __iadd__(self, other: "Block") -> None:
        """Add the value of two blocks and updae the current block"""
        logger.debug(f"Merging blocks ({id(self)}) and ({id(other)}) => ({id(self)}), {self}")
        self.value += other.value
        self.update()

    def __repr__(self) -> str:
        """Return a string representation of the block"""
        return f"({_show_pos(self.rect.x)}, {_show_pos(self.rect.y)})"

    def __str__(self) -> str:
        """Return a string representation of the block"""
        return self.__repr__()

    def __hash__(self) -> int:
        """Return a hash of the block"""
        return hash((self.rect.x, self.rect.y, self.value))
