import random
import sys

import pygame

from .block import Block
from .colors import COLORS
from .config import Config


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption("2048")
        self.sprites = pygame.sprite.Group()
        self.generate_random_block()

    def run(self) -> None:
        while True:
            self.hande_events()
            self.update()
            self.render()

    def update(self) -> None:
        self.sprites.update()

    def render(self) -> None:
        self.screen.fill(COLORS.BG)
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def hande_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def generate_random_block(self) -> None:
        for _ in range(Config.INITIAL_BLOCK_COUNT):
            while True:
                x = random.randint(0, 2) * Config.BLOCK_SIZE  # random column position
                y = random.randint(0, 2) * Config.BLOCK_SIZE  # random row position

                block = Block(x, y)
                colligin_blocks = pygame.sprite.spritecollide(block, self.sprites, False)

                if not colligin_blocks:
                    self.sprites.add(block)
                    break
