import sys

import pygame
from loguru import logger

from .board import Board
from .config import Config
from .logger import setup_logger
from .screens.header import Header
from .utils import Direction


class Game:
    def __init__(self) -> None:
        setup_logger()
        logger.info("Initializing game")

        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode(Config.SCREEN_SIZE)
        pygame.display.set_caption("2048")
        self.board = Board()
        self.header = Header()
        self.score = 0

    def run(self) -> None:
        """Run the game loop."""
        while True:
            self._hande_events()
            self._update()
            self._render()

    def _update(self) -> None:
        """Update the game."""
        self.board.update()

    def _render(self) -> None:
        """Render the game."""
        self.screen.fill(Config.COLORSCHEME.BG)
        self.board.draw(self.screen)
        self.header.draw(self.screen, self.score)
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
        self.score += self.board.move(Direction.UP)

    def move_down(self) -> None:
        self.score += self.board.move(Direction.DOWN)

    def move_left(self) -> None:
        self.score += self.board.move(Direction.LEFT)

    def move_right(self) -> None:
        self.score += self.board.move(Direction.RIGHT)

    def exit(self) -> None:
        """Exit the game."""
        pygame.quit()
        sys.exit()
