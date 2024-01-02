import random

import pygame
from loguru import logger

from py2048 import Config, Direction

from .tile import Tile


class Board(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, Config.BOARD_WIDTH, Config.BOARD_HEIGHT)
        self.rect.x = Config.BOARD_X
        self.rect.y = Config.BOARD_Y
        self.initiate_game()

    def initiate_game(self) -> None:
        """Initiate the game."""
        self.generate_initial_tiles()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the board."""
        tile: Tile
        self._draw_background(surface)

        super().draw(surface)

    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw the board background."""
        pygame.draw.rect(
            surface,
            Config.COLORSCHEME.BOARD_BG,
            self.rect,
            border_radius=Config.TILE_BORDER_RADIUS,
        )  # background
        pygame.draw.rect(
            surface,
            Config.COLORSCHEME.BOARD_BG,
            self.rect,
            width=Config.TILE_BORDER_WIDTH,
            border_radius=Config.TILE_BORDER_RADIUS,
        )  # border

    def move(self, direction: Direction) -> int:
        """Move the tiles in the specified direction."""
        score = 0
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
            score += tile.move(direction)

        if not self._is_full():
            self.generate_random_tile()

        return score

    def generate_initial_tiles(self) -> None:
        """Generate the initial tiles."""
        self.generate_tile(Config.INITIAL_TILE_COUNT)

    def generate_tile(self, amount: int = 1, *pos: tuple[int, int]) -> None:
        """Generate `amount` number of tiles or at the specified positions."""
        if pos:
            for coords in pos:
                x, y = coords[0] * Config.TILE_SIZE, coords[1] * Config.TILE_SIZE
                self.add(Tile(x, y, self))
            return

        for _ in range(amount):
            self.generate_random_tile()

    def generate_random_tile(self) -> None:
        """Generate a tile with random coordinates aligned with the grid."""
        while True:
            # Generate random coordinates aligned with the grid
            x = random.randint(0, 3) * Config.TILE_SIZE + Config.BOARD_X
            y = random.randint(0, 3) * Config.TILE_SIZE + Config.BOARD_Y
            tile = Tile(x, y, self)

            colliding_tiles = pygame.sprite.spritecollide(
                tile, self, False
            )  # check for collisions

            if not colliding_tiles:
                self.add(tile)
                return

    def _is_full(self) -> bool:
        """Check if the board is full."""
        return len(self.sprites()) == Config.BOARD_SIZE**2

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
        self.initiate_game()
