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

    def move(self, direction: Direction) -> tuple[bool, int]:
        match direction:
            case Direction.LEFT:
                return self.move_left()
            case Direction.RIGHT:
                return self.move_right()
            case Direction.UP:
                return self.move_up()
            case Direction.DOWN:
                return self.move_down()

    def move_right(self) -> tuple[bool, int]:
        self.board, moved = self._move_and_merge(self.board)

        if moved:
            self.add_random_tile()
        return moved, self.score

    def move_left(self) -> tuple[bool, int]:
        board = np.rot90(self.board, 2)
        board, moved = self._move_and_merge(board)
        self.board = np.rot90(board, 2)

        if moved:
            self.add_random_tile()
        return moved, self.score

    def move_up(self) -> tuple[bool, int]:
        board = np.rot90(self.board, -1)
        board, moved = self._move_and_merge(board)
        self.board = np.rot90(board, 1)

        if moved:
            self.add_random_tile()
        return moved, self.score

    def move_down(self) -> tuple[bool, int]:
        pass

    def _move_and_merge(self, board: np.ndarray) -> tuple[np.ndarray, bool]:
        board, has_pushed = self._push_board_right(board)
        board, has_merged = self._merge(board)
        board, _ = self._push_board_right(board)
        return board, has_pushed or has_merged

    def _merge(self, board: np.ndarray) -> tuple[np.ndarray, bool]:
        done = False
        for row in range(self.size):
            for col in range(self.size - 1, 0, -1):
                if board[row, col] == board[row, col - 1] and board[row, col] != 0:
                    board[row, col] *= 2
                    self.score += board[row, col]
                    board[row, col - 1] = 0
                    done = True

        return board, done

    def display(self) -> None:
        print(f"Score: {self.score}")
        for row in self.board:
            for val in row:
                print(f"{val:^3}", end="")
            print()

    def _push_board_right(self, board: np.ndarray) -> tuple[np.ndarray, bool]:
        new_board = np.zeros((self.size, self.size), dtype=int)
        done = False
        for row in range(self.size):
            count = self.size - 1
            for col in range(self.size - 1, -1, -1):
                if board[row, col] != 0:
                    new_board[row, count] = board[row, col]
                    if col != count:
                        done = True
                    count -= 1
        return new_board, done
