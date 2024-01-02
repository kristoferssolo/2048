import pygame
from loguru import logger

from py2048 import Config
from py2048.objects import Board
from py2048.utils import Direction, setup_logger

from .header import Header


class Game:
    def __init__(self) -> None:
        self.header = Header()
        self.board = Board()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(Config.COLORSCHEME.BG)
        self.board.draw(surface)
        self.header.draw(surface)
        pygame.display.flip()

    def handle_events(self, event: pygame.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_h):
                self.move_left()
            elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_l):
                self.move_right()
            elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_k):
                self.move_up()
            elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_j):
                self.move_down()

    def move(self, direction: Direction) -> None:
        self.board.move(direction)
        self.header.update(self.board.score)

    def move_up(self) -> None:
        self.move(Direction.UP)

    def move_down(self) -> None:
        self.move(Direction.DOWN)

    def move_left(self) -> None:
        self.move(Direction.LEFT)

    def move_right(self) -> None:
        self.move(Direction.RIGHT)
