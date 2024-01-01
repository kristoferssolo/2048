import random

import pygame
from loguru import logger

from .block import Block
from .color import Color
from .config import Config
from .utils import Direction


class Board(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, Config.BOARD_WIDTH, Config.BOARD_HEIGHT)
        self.rect.x = Config.BOARD_X
        self.rect.y = Config.BOARD_Y
        self.initiate_game()

    def initiate_game(self) -> None:
        """Initiate the game."""
        self.generate_initial_blocks()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the board."""
        block: Block
        pygame.draw.rect(screen, Color.YELLOW, self.rect, 2)

        super().draw(screen)

    def move(self, direction: Direction):
        """Move the blocks in the specified direction."""
        blocks = self.sprites()
        block: Block

        match direction:
            case Direction.UP:
                blocks.sort(key=lambda block: block.rect.y)
            case Direction.DOWN:
                blocks.sort(key=lambda block: block.rect.y, reverse=True)
            case Direction.LEFT:
                blocks.sort(key=lambda block: block.rect.x)
            case Direction.RIGHT:
                blocks.sort(key=lambda block: block.rect.x, reverse=True)

        for block in blocks:
            block.move(direction)

        if not self._is_full():
            self.generate_random_block()

    def generate_initial_blocks(self) -> None:
        """Generate the initial blocks."""
        self.generate_block(Config.INITIAL_BLOCK_COUNT)

    def generate_block(self, amount: int = 1, *pos: tuple[int, int]) -> None:
        """Generate `amount` number of blocks or at the specified positions."""
        if pos:
            for coords in pos:
                x, y = coords[0] * Config.BLOCK_SIZE, coords[1] * Config.BLOCK_SIZE
                self.add(Block(x, y, self))
            return

        for _ in range(amount):
            self.generate_random_block()

    def generate_random_block(self) -> None:
        """Generate a block with random coordinates aligned with the grid."""
        while True:
            # Generate random coordinates aligned with the grid
            x = random.randint(0, 3) * Config.BLOCK_SIZE + Config.BOARD_X
            y = random.randint(0, 3) * Config.BLOCK_SIZE + Config.BOARD_Y
            block = Block(x, y, self)

            colliding_blocks = pygame.sprite.spritecollide(
                block, self, False
            )  # check for collisions

            if not colliding_blocks:
                self.add(block)
                return

    def _is_full(self) -> bool:
        """Check if the board is full."""
        return len(self.sprites()) == Config.BOARD_SIZE**2

    def _can_move(self) -> bool:
        """Check if any movement is possible on the board."""
        block: Block
        for block in self.sprites():
            if block.can_move():
                return True
        return False

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self._is_full() and not self._can_move()

    def reset(self) -> None:
        """Reset the board."""
        self.empty()
        self.initiate_game()
