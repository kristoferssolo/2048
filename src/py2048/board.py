import random

import pygame
from loguru import logger

from .block import Block
from .config import Config
from .utils import Direction


class Board(pygame.sprite.Group):
    def move(self, direction: Direction):
        blocks = self.sprites()
        block: Block

        match direction:
            case Direction.UP:
                blocks.sort(key=lambda block: block.rect.y)
            case Direction.DOWN:
                blocks.sort(key=lambda block: block.rect.y, reverse=True)
            case Direction.LEFT:
                blocks.sort(key=lambda block: block.rect.x)
            case Direction.RIGHT:
                blocks.sort(key=lambda block: block.rect.x, reverse=True)

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
                    logger.debug(f"Created block at {block.pos()}")
                    break
