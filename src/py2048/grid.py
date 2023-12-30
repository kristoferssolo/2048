import random

import pygame

from .block import Block
from .config import Config
from .utils import Direction


class Grid(pygame.sprite.Group):
    def move(self, direction: Direction):
        blocks = list(self.sprites())

        match direction:
            case Direction.DOWN:
                blocks.sort(key=lambda block: block.rect.y, reverse=True)
            case Direction.RIGHT:
                blocks.sort(key=lambda block: block.rect.x, reverse=True)

        for block in blocks:
            block.move(direction)

    def generate_block(self, amount: int = 1, *pos: tuple[int, int]) -> None:
        """Generate `amount` number of blocks."""
        if pos:
            for coords in pos:
                self.add(Block(coords[0] * Config.BLOCK_SIZE, coords[1] * Config.BLOCK_SIZE))
            return

        for _ in range(amount):
            while True:
                x = random.randint(0, 3) * Config.BLOCK_SIZE  # random column position
                y = random.randint(0, 3) * Config.BLOCK_SIZE  # random row position
                block = Block(x, y)

                colliding_blocks = self.spritecollide(block, self, False)  # check collision

                if not colliding_blocks:
                    self.add(block)
                    break
