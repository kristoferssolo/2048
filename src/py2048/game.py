import random
import sys

import pygame

from .block import Block
from .colors import COLORS
from .config import Config


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption("2048")
        self.sprites = pygame.sprite.Group()
        self.generate_random_block(Config.INITIAL_BLOCK_COUNT)

    def run(self) -> None:
        """Run the game loop."""
        while True:
            self.hande_events()
            self.update()
            self.render()

    def update(self) -> None:
        """Update the game."""
        self.sprites.update()

    def render(self) -> None:
        """Render the game."""
        self.screen.fill(COLORS.BG)
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def hande_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_h):
                    self.move_blocks(-Config.BLOCK_SIZE, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_l):
                    self.move_blocks(Config.BLOCK_SIZE, 0)
                elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_k):
                    self.move_blocks(0, -Config.BLOCK_SIZE)
                elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_j):
                    self.move_blocks(0, Config.BLOCK_SIZE)
                elif event.key == pygame.K_q:
                    self.exit()

    def move_blocks(self, dx: int, dy: int) -> None:
        """Move all the blocks by `dx` and `dy`."""
        moved_blocks = pygame.sprite.Group()  # Keep track of moved blocks to avoid double merging

        for block in self.sprites:
            block.move(dx, dy)

        for block in self.sprites:  # FIX: different value block merge
            collidin_blocks = pygame.sprite.spritecollide(block, self.sprites, False)

            for other_block in collidin_blocks:
                if block != other_block and block.value == other_block.value and other_block not in moved_blocks:
                    block.increase_value()
                    self.sprites.remove(other_block)
                    moved_blocks.add(block)
        self.generate_random_block()

    def generate_random_block(self, count: int = 1) -> None:
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
