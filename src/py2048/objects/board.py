import random
from typing import Optional

import pygame
from loguru import logger

from py2048 import Config
from py2048.utils import Direction, Position

from .tile import Tile


class Board(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, *Config.BOARD.size)
        self.score: int = 0
        self.rect.x, self.rect.y = Config.BOARD.pos
        self._initiate_game()

    def _initiate_game(self) -> None:
        """Initiate the game."""
        self.generate_initial_tiles()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the board."""
        self._draw_background(surface)
        super().draw(surface)

    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw the board background."""
        pygame.draw.rect(
            surface,
            Config.COLORSCHEME.BOARD_BG,
            self.rect,
            border_radius=Config.TILE.border.radius,
        )  # background
        pygame.draw.rect(
            surface,
            Config.COLORSCHEME.BOARD_BG,
            self.rect,
            width=Config.TILE.border.width,
            border_radius=Config.TILE.border.radius,
        )  # border

    def move(self, direction: Direction) -> None:
        """Move the tiles in the specified direction."""
        tiles = self.sprites()
        tile: Tile

        match direction:
            case Direction.UP:
                tiles.sort(key=lambda tile: tile.rect.y)
            case Direction.DOWN:
                tiles.sort(key=lambda tile: tile.rect.y, reverse=True)
            case Direction.LEFT:
                tiles.sort(key=lambda tile: tile.rect.x)
            case Direction.RIGHT:
                tiles.sort(key=lambda tile: tile.rect.x, reverse=True)

        for tile in tiles:
            self.score += tile.move(direction)

        if not self._is_full():
            self.generate_random_tile()

    def generate_initial_tiles(self) -> None:
        """Generate the initial tiles."""
        self.generate_tile(Config.TILE.initial_count)

    def generate_tile(self, amount: int = 1, *pos: Position) -> None:
        """Generate `amount` number of tiles or at the specified positions."""
        if pos:
            for coords in pos:
                x, y = coords.x * Config.TILE.size, coords.y * Config.TILE.size
                self.add(Tile(Position(x, y), self))
            return

        for _ in range(amount):
            self.generate_random_tile()

    def generate_random_tile(self) -> None:
        """Generate a tile with random coordinates aligned with the grid."""
        while True:
            # Generate random coordinates aligned with the grid
            x = random.randint(0, 3) * Config.TILE.size + Config.BOARD.pos.x
            y = random.randint(0, 3) * Config.TILE.size + Config.BOARD.pos.y
            tile = Tile(Position(x, y), self)

            colliding_tiles = pygame.sprite.spritecollide(
                tile, self, False
            )  # check for collisions

            if not colliding_tiles:
                self.add(tile)
                return

    def _is_full(self) -> bool:
        """Check if the board is full."""
        return len(self.sprites()) == Config.BOARD.len**2

    def _can_move(self) -> bool:
        """Check if any movement is possible on the board."""
        tile: Tile
        for tile in self.sprites():
            if tile.can_move():
                return True
        return False

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self._is_full() and not self._can_move()

    def reset(self) -> None:
        """Reset the board."""
        self.empty()
        self._initiate_game()

    def max_val(self) -> int:
        """Return the maximum value of the tiles."""
        tile: Tile
        return int(max(tile.value for tile in self.sprites()))

    def get_tile(self, position: Position) -> Optional[Tile]:
        """Return the tile at the specified position."""
        tile: Tile
        for tile in self.sprites():
            if tile.pos == position:
                return tile
        return None

    def matrix(self) -> list[int]:
        """Return a 1d matrix of values of the tiles."""
        matrix: list[int] = []

        for i in range(1, Config.BOARD.len + 1):
            for j in range(1, Config.BOARD.len + 1):
                tile = self.get_tile(Position(j, i))
                if tile:
                    matrix.append(tile.value)
                else:
                    matrix.append(0)

        return matrix
