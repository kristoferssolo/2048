import random

import numpy as np
from loguru import logger
from utils import Config, Direction


def play() -> None:
    game = Game2048()

    while True:
        game.display()
        move = input("Enter direction: ")
        moves = {
            "w": game.move_up,
            "a": game.move_left,
            "s": game.move_down,
            "d": game.move_right,
        }

        if move == "q":
            break

        direction = moves.get(move, None)

        if direction:
            direction()

    game.display()


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
        tile_value = random.choices([2, 4], weights=Config.tile.probability)[0]
        tile_row_options, tile_col_options = np.nonzero(np.logical_not(self.board))
        tile_loc = np.random.randint(0, len(tile_row_options))
        self.board[tile_row_options[tile_loc], tile_col_options[tile_loc]] = tile_value

    def move(self, direction: Direction) -> None:
        match direction:
            case Direction.LEFT:
                self.move_left()
            case Direction.RIGHT:
                self.move_right()
            case Direction.UP:
                self.move_up()
            case Direction.DOWN:
                self.move_down()

    def move_left(self) -> None:
        pass

    def move_right(self) -> tuple[bool, int]:
        self.board, has_pushed = self._push_board_right()
        has_merged = self.merge()
        self.board, _ = self._push_board_right()
        move_made = has_pushed or has_merged
        if move_made:
            self.add_random_tile()
        return move_made, self.score

    def move_up(self) -> None:
        pass

    def move_down(self) -> None:
        pass

    def merge(self, row: np.ndarray) -> bool:
        done = False
        for row in range(self.size):
            for col in range(self.size - 1, 0, -1):
                if (
                    self.board[row, col] == self.board[row, col - 1]
                    and self.board[row, col] != 0
                ):
                    self.board[row, col] *= 2
                    self.score += self.board[row, col]
                    self.board[row, col - 1] = 0
                    done = True

        return done

    def display(self) -> None:
        for row in self.board:
            for val in row:
                print(f"{val:^3}", end="")
            print()
