import pygame
from loguru import logger

from py2048 import Config
from py2048.objects import Button
from py2048.utils import Position


class Menu(pygame.sprite.AbstractGroup):
    def __init__(self):
        super().__init__()

        buttons_data = {
            "Play": self.play,
            "AI": self.ai,
            "Settings": self.settings,
            "Exit": self.exit,
        }
        button_width, button_height = 120, 50

        for index, (text, action) in enumerate(buttons_data.items(), start=1):
            self.add(
                Button(
                    position=Position(
                        Config.SCREEN.size.width / 2 - button_width / 2,
                        Config.SCREEN.size.height / len(buttons_data) * index
                        - button_height,
                    ),
                    bg_color=Config.COLORSCHEME.BOARD_BG,
                    font_color=Config.COLORSCHEME.LIGHT_TEXT,
                    hover_color=Config.COLORSCHEME.TILE_0,
                    size=(button_width, button_height),
                    text=text,
                    border_radius=Config.TILE.border.radius,
                    action=action,
                )
            )

    def _handle_events(self, event: pygame.event.Event) -> None:
        """Handle the event."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.sprites():
                button.on_click(Position(*event.pos))
        elif event.type == pygame.MOUSEMOTION:
            for button in self.sprites():
                button.on_hover(Position(*event.pos))

    def play(self) -> None:
        logger.debug("Play")

    def ai(self) -> None:
        logger.debug("AI")

    def settings(self) -> None:
        logger.debug("Settings")

    def exit(self) -> None:
        logger.debug("Exit")
