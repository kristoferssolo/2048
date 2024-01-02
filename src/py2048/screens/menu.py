import pygame
from loguru import logger

from py2048 import Config
from py2048.objects import Button
from py2048.utils import Position


class Menu:
    def __init__(self):
        buttons_data = {
            "Play": self.play,
            "AI": self.ai,
            "Settings": self.settings,
            "Exit": self.exit,
        }
        buttons_width, button_height = 120, 50

        self.buttons = [
            Button(
                position=Position(
                    Config.SCREEN.size.width / 2 - button_height // 2,
                    Config.SCREEN.size.height / len(buttons_data) * index
                    - button_height // 2,
                ),
                bg_color=Config.COLORSCHEME.BOARD_BG,
                font_color=Config.COLORSCHEME.LIGHT_TEXT,
                hover_color=Config.COLORSCHEME.TILE_0,
                size=(buttons_width, button_height),
                text=text,
                border_radius=Config.TILE.border.radius,
                action=action,
            )
            for index, (text, action) in enumerate(buttons_data.items(), start=1)
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

    def ai(self) -> None:
        logger.debug("AI")

    def settings(self) -> None:
        logger.debug("Settings")

    def exit(self) -> None:
        logger.debug("Exit")
