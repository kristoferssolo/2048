import random

import numpy as np
from loguru import logger
from utils import Config, Direction


class Game2048:
    def __init__(self, size: int = 4):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.score = 0
        self.game_over = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self) -> None:
        """Add a random tile to the board."""
        empty_cells: np.ndarray = np.argwhere(self.board == 0)
        if empty_cells.shape[0] > 0:
            row, col = random.choice(empty_cells)
            self.board[row, col] = random.choices(
                [2, 4], weights=Config.tile.probability
            )[0]

    def move(self, direction: Direction) -> None:
        pass

    def merge(self, row: np.ndarray) -> np.ndarray:
        pass

    def display(self) -> None:
        for row in self.board:
            for val in row:
                print(f"{val:^3}", end="")
            print()
