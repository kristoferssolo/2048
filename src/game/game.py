import random

import numpy as np
from utils import Config


class Game2048:
    def __init__(self, size: int = 4):
        self.size = size
        self.board = np.zeros((size, size), dtype=np.int)
        self.score = 0
        self.game_over = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self) -> None:
        """Add a random tile to the board."""
        empty_cells: np.ndarray = np.argwhere(self.board == 0)
        if empty_cells.shape(0) > 0:
            row, col = random.choice(empty_cells)
            self.board[row, col] = random.choices(
                [2, 4], weights=Config.tile.probability
            )[0]
