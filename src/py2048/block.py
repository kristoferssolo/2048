import random

import pygame

from .colors import COLORS
from .config import Config


class Block(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        """Initialize a block"""
        super().__init__()
        self.image = pygame.Surface((Config.BLOCK_SIZE, Config.BLOCK_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.value: int = 2 if random.random() <= Config.BLOCK_VALUE_PROBABILITY else 4
        self.font = pygame.font.SysFont(Config.FONT_FAMILY, Config.FONT_SIZE)
        self.update()

    def _draw_value(self) -> None:
        """Draw the value of the block"""
        text = self.font.render(str(self.value), True, COLORS.FG)
        text_rect = text.get_rect(center=self.image.get_rect().center)
        self.image.blit(text, text_rect)

    def move(self, dx: int, dy: int) -> None:
        """Move the block by `dx` and `dy`."""
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        if 0 <= new_x <= Config.WIDTH - Config.BLOCK_SIZE and 0 <= new_y <= Config.HEIGHT - Config.BLOCK_SIZE:
            self.rect.x = new_x
            self.rect.y = new_y

    def increase_value(self, num: int = 2) -> None:
        """Increase the value of the block `num` times"""
        self.value *= num
        self.update()

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

    def __add__(self, other: "Block") -> "Block":
        """Add the value of two blocks and return a new block"""
        new_block = Block(self.rect.x, self.rect.y)
        new_block.value = self.value + other.value
        return new_block

    def __iadd__(self, other: "Block") -> "Block":
        """Add the value of two blocks and return a new block"""
        return self + other

    def __eq__(self, other: "Block") -> bool:
        """Check if two block values are equal"""
        return self.value == other.value

    def __repr__(self) -> str:
        """Return a string representation of the block"""
        return f"Block({self.rect.x}, {self.rect.y})"

    def __str__(self) -> str:
        """Return a string representation of the block"""
        self.__repr__()

    def __hash__(self) -> int:
        """Return a hash of the block"""
        return hash((self.rect.x, self.rect.y, self.value))
