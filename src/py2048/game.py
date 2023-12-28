import random
import sys

import pygame
from loguru import logger

from .block import Block
from .colors import COLORS
from .config import Config
from .logger import setup_logger


class Game:
    def __init__(self) -> None:
        setup_logger()
        logger.info("Initializing game")

        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption("2048")
        self.sprites = pygame.sprite.Group()
        self._generate_random_block(Config.INITIAL_BLOCK_COUNT)

    def run(self) -> None:
        """Run the game loop."""
        while True:
            self._hande_events()
            self._update()
            self._render()

    def _update(self) -> None:
        """Update the game."""
        self.sprites.update()

    def _render(self) -> None:
        """Render the game."""
        self.screen.fill(COLORS.BG)
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def _hande_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_h):
                    self.move_left()
                elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_l):
                    self.move_right()
                elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_k):
                    self.move_up()
                elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_j):
                    self.move_down()
                elif event.key == pygame.K_q:
                    self.exit()

    def move_up(self) -> None:
        """Move all blocks up"""
        logger.debug("Move up")
        self._move_blocks(0, -Config.BLOCK_SIZE)

    def move_down(self) -> None:
        """Move all blocks down"""
        logger.debug("Move down")
        self._move_blocks(0, Config.BLOCK_SIZE)

    def move_left(self) -> None:
        """Move all blocks left"""
        logger.debug("Move left")
        self._move_blocks(-Config.BLOCK_SIZE, 0)

    def move_right(self) -> None:
        """Move all blocks right"""
        logger.debug("Move right")
        self._move_blocks(Config.BLOCK_SIZE, 0)

    def _move_blocks(self, dx: int, dy: int) -> None:
        """Move all the blocks by `dx` and `dy`."""
        moved_blocks = pygame.sprite.Group()  # Keep track of moved blocks to avoid double merging
        blocks_to_remove = []

        for block in self.sprites:
            block.move(dx, dy)

        for block in self.sprites:
            colliding_blocks = pygame.sprite.spritecollide(block, self.sprites, False)

            for other_block in colliding_blocks:
                if block != other_block and block.value == other_block.value and other_block not in moved_blocks:
                    new_block = block + other_block
                    moved_blocks.add(new_block)
                    blocks_to_remove.extend([block, other_block])

        for block in blocks_to_remove:
            self.sprites.remove(block)

        self._generate_random_block()

    def _generate_random_block(self, count: int = 1) -> None:
        """Generate `count` number of random blocks."""
        for _ in range(count):
            while True:
                x = random.randint(0, 2) * Config.BLOCK_SIZE  # random column position
                y = random.randint(0, 2) * Config.BLOCK_SIZE  # random row position
                block = Block(x, y)

                colliding_blocks = pygame.sprite.spritecollide(block, self.sprites, False)  # check collision

                if not colliding_blocks:
                    self.sprites.add(block)
                    break

    def exit(self) -> None:
        """Exit the game."""
        pygame.quit()
        sys.exit()
