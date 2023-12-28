import random

import pygame

from .block import Block
from .config import Config
from .utils import Direction


class Grid(pygame.sprite.Group):
    def move(self, direction: Direction):
        for block in self:
            block.move(direction)

    def generate_random_block(self, count: int = 1) -> None:
        """Generate `count` number of random blocks."""
        for _ in range(count):
            while True:
                x = random.randint(0, 2) * Config.BLOCK_SIZE  # random column position
                y = random.randint(0, 2) * Config.BLOCK_SIZE  # random row position
                block = Block(x, y)

                colliding_blocks = pygame.sprite.spritecollide(block, self, False)  # check collision

                if not colliding_blocks:
                    self.add(block)
                    break
