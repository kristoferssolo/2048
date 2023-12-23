import random

import pygame

from .colors import COLORS
from .config import Config


class Block(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((Config.BLOCK_SIZE, Config.BLOCK_SIZE))
        self.image.fill(COLORS.ERROR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.value = 2 if random.random() <= Config.BLOCK_VALUE_PROBABILITY else 4
        self.draw_value()

    def draw_value(self) -> None:
        font = pygame.font.SysFont(Config.FONT_FAMILY, Config.FONT_SIZE)
        text = font.render(str(self.value), True, COLORS.FG)
        text_rect = text.get_rect(center=self.image.get_rect().center)
        self.image.blit(text, text_rect)

    def move(self, dx: int, dy: int) -> None:
        self.rect.x += dx
        self.rect.y += dy
