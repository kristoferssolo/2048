import random

import pygame

from .block import Block
from .config import Config
from .utils import Direction


class Board(pygame.sprite.Group):
    def move(self, direction: Direction):
        blocks = self.sprites()
        block: Block

        if direction in {Direction.DOWN, Direction.RIGHT}:
            blocks.sort(key=lambda block: (block.rect.x, block.rect.y), reverse=True)

        for block in blocks:
            block.move(direction)

        self.generate_block()

    def generate_block(self, amount: int = 1, *pos: tuple[int, int]) -> None:
        """Generate `amount` number of blocks."""
        if pos:
            for coords in pos:
                x, y = coords[0] * Config.BLOCK_SIZE, coords[1] * Config.BLOCK_SIZE
                self.add(Block(x, y, self))
            return

        for _ in range(amount):
            while True:
                # Generate random coordinates aligned with the grid
                x = random.randint(0, 3) * Config.BLOCK_SIZE
                y = random.randint(0, 3) * Config.BLOCK_SIZE
                block = Block(x, y, self)

                colliding_blocks = pygame.sprite.spritecollide(block, self, False)  # check for collisions

                if not colliding_blocks:
                    self.add(block)
                    break
