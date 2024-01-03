import sys

import neat
import pygame
from loguru import logger

from py2048 import Config
from py2048.objects import Button
from py2048.utils import Position

from .game import Game


class Menu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2048")
        self._surface: pygame.Surface = pygame.display.set_mode(Config.SCREEN.size)

        logger.info("Initializing game")

        self._buttons_data = {
            "Play": self.play,
            "AI": self.ai,
            "Settings": self.settings,
            "Exit": self.exit,
        }
        self._game_active = False
        self._ai_active = False
        self._setting_active = False
        self._buttons = self._create_buttons()

    def _create_buttons(self) -> pygame.sprite.Group:
        """Create the buttons."""
        width, height = 120, 50
        buttons = pygame.sprite.Group()
        for index, (text, action) in enumerate(self._buttons_data.items(), start=1):
            buttons.add(
                Button(
                    position=(
                        Config.SCREEN.size.width / 2 - width / 2,
                        Config.SCREEN.size.height / len(self._buttons_data) * index
                        - height,
                    ),
                    bg_color=Config.COLORSCHEME.BOARD_BG,
                    font_color=Config.COLORSCHEME.LIGHT_TEXT,
                    hover_color=Config.COLORSCHEME.TILE_0,
                    size=(width, height),
                    text=text,
                    border_radius=Config.TILE.border.radius,
                    action=action,
                )
            )

        return buttons

    def draw(self) -> None:
        self._surface.fill(Config.COLORSCHEME.BG)
        self._buttons.draw(self._surface)
        pygame.display.flip()

    def run(self) -> None:
        """Run the game loop."""

        while True:
            self._hande_events()

            if self._game_active:
                self.game.draw(self._surface)
            elif self._ai_active:
                pass
            elif self._setting_active:
                pass
            else:
                self.draw()

    def _hande_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self._buttons:
                    button.on_click(Position(*event.pos))
            elif event.type == pygame.MOUSEMOTION:
                for button in self._buttons:
                    button.on_hover(Position(*event.pos))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.exit()
            if self._game_active:
                self.game.handle_events(event)

    def play(self) -> None:
        logger.debug("Launching game")
        self._game_active = True
        self.game = Game()

    def ai(self) -> None:
        logger.debug("AI")

    def settings(self) -> None:
        logger.debug("Settings")

    def exit(self) -> None:
        """Exit the game."""
        logger.debug("Exiting")
        pygame.quit()
        sys.exit()
