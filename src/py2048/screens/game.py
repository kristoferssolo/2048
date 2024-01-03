import pygame
from loguru import logger

from py2048 import Config
from py2048.objects import Board, Button, ScoreLabel
from py2048.utils import Direction, Position, Size, setup_logger


class Game:
    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, *Config.HEADER.size)
        self.labels = self._create_labels()
        self.buttons = self._create_buttons()
        self.board = Board()

    def update_score(self, new_score: int) -> None:
        """Updates the score to `new_score`."""
        self.score.update_score(new_score)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(Config.COLORSCHEME.BG)
        self.board.draw(surface)
        self.labels.draw(surface)
        self.buttons.draw(surface)
        pygame.display.flip()

    def handle_events(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.on_click(Position(*event.pos))
        elif event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.on_hover(Position(*event.pos))
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_h):
                self.move_left()
            elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_l):
                self.move_right()
            elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_k):
                self.move_up()
            elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_j):
                self.move_down()

    def move(self, direction: Direction) -> None:
        """Moved the board in the given direction and updates the score."""
        self.board.move(direction)
        self.update_score(self.board.score)
        if self.board.is_game_over():
            logger.info("Game over!")
            self.restart()

    def move_up(self) -> None:
        self.move(Direction.UP)

    def move_down(self) -> None:
        self.move(Direction.DOWN)

    def move_left(self) -> None:
        self.move(Direction.LEFT)

    def move_right(self) -> None:
        self.move(Direction.RIGHT)

    def restart(self) -> None:
        self.board.reset()
        self.board.score = 0
        self.update_score(0)

    def _create_labels(self) -> pygame.sprite.Group:
        size = Size(60, 40)

        self.score = ScoreLabel(
            value=0,
            text="Score",
            size=size,
            position=Position(
                Config.SCREEN.size.width - Config.TILE.size // 2 - size.width * 2 - 10,
                10,
            ),
            bg_color=Config.COLORSCHEME.BOARD_BG,
            font_color=Config.COLORSCHEME.LIGHT_TEXT,
            font_size=16,
            border_radius=2,
        )
        highscore = ScoreLabel(
            value=2048,
            text="Best",
            size=size,
            position=Position(
                Config.SCREEN.size.width - Config.TILE.size // 2 - size.width, 10
            ),
            bg_color=Config.COLORSCHEME.BOARD_BG,
            font_color=Config.COLORSCHEME.LIGHT_TEXT,
            font_size=16,
            border_radius=2,
        )

        return pygame.sprite.Group(self.score, highscore)

    def _create_buttons(self) -> pygame.sprite.Group:
        reset = Button(
            position=(10, 10),
            bg_color=Config.COLORSCHEME.BOARD_BG,
            font_color=Config.COLORSCHEME.LIGHT_TEXT,
            hover_color=Config.COLORSCHEME.TILE_0,
            size=(100, 30),
            text="New Game",
            border_radius=Config.TILE.border.radius,
            action=self.restart,
            font_size=16,
            border_width=2,
        )
        return pygame.sprite.Group(reset)
