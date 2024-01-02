import pygame
from loguru import logger
from py2048.config import Config

from .elements.button import Button


class Menu:
    def __init__(self):
        self.buttons = [
            Button(
                "Play",
                Config.FONT_FAMILY,
                Config.FONT_SIZE,
                Config.COLORSCHEME.LIGHT_TEXT,
                (Config.SCREEN_WIDTH / 2 - 50, Config.SCREEN_HEIGHT / 2 - 100),
                100,
                50,
                self.play,
                Config.COLORSCHEME.BOARD_BG,
                Config.COLORSCHEME.BLOCK_0,
            ),
            Button(
                "Exit",
                Config.FONT_FAMILY,
                Config.FONT_SIZE,
                Config.COLORSCHEME.LIGHT_TEXT,
                (Config.SCREEN_WIDTH / 2 - 50, Config.SCREEN_HEIGHT / 2),
                100,
                50,
                self.exit,
                Config.COLORSCHEME.BOARD_BG,
                Config.COLORSCHEME.BLOCK_0,
            ),
        ]

    def _handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.check_click(event.pos)

    def draw(self, surface: pygame.Surface) -> None:
        for button in self.buttons:
            button.draw(surface)

    def play(self) -> None:
        logger.debug("Play")

    def exit(self) -> None:
        logger.debug("Exit")
