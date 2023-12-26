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
        self.change_color()
        self.draw_value()

    def change_color(self) -> None:
        match self.value:
            case 2:
                self.image.fill(COLORS.BLUE)
            case 4:
                self.image.fill(COLORS.BLUE0)
            case 8:
                self.image.fill(COLORS.BLUE1)
            case 16:
                self.image.fill(COLORS.BLUE2)
            case 32:
                self.image.fill(COLORS.DARK3)
            case 64:
                self.image.fill(COLORS.BORDER_HIGHLIGHT)
            case 128:
                self.image.fill(COLORS.BLUE5)
            case 256:
                self.image.fill(COLORS.BLUE6)
            case 512:
                self.image.fill(COLORS.BLUE7)
            case 1024:
                self.image.fill(COLORS.ORANGE)
            case 2048:
                self.image.fill(COLORS.RED)
