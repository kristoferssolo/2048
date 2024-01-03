import neat
from py2048 import Menu
from py2048.utils import Position


def calculate_fitness(genome: neat.DefaultGenome, app: Menu) -> tuple[int, int]:
    board = app.game.board
    score = board.score
    max_tile = board.max_val()
    empty_cells = 16 - len(board.sprites())
    smoothness = calc_smoothness(app)
    monotonicity = calc_monotonicity(app)

    genome.fitness = score + max_tile**3 + smoothness + monotonicity

    return max_tile, score


def calc_smoothness(app: Menu) -> int:
    smoothness = 0

    for row in range(4):
        for col in range(4):
            current_value = app.game.board.get_tile_value(Position(row, col))
            if current_value:
                right_value = app.game.board.get_tile_value(Position(row, col + 1))
                if right_value:
                    smoothness -= abs(current_value - right_value)
                left_value = app.game.board.get_tile_value(Position(row, col - 1))
                if left_value:
                    smoothness -= abs(current_value - left_value)

    for col in range(4):
        for row in range(4):
            current_value = app.game.board.get_tile_value(Position(row, col))
            if current_value:
                up_value = app.game.board.get_tile_value(Position(row - 1, col))
                if up_value:
                    smoothness -= abs(current_value - up_value)

                down_value = app.game.board.get_tile_value(Position(row + 1, col))
                if down_value:
                    smoothness -= abs(current_value - down_value)

    return smoothness


def calc_monotonicity(app: Menu):
    monotonicity = 0
    for row in range(4):
        row_values = [
            app.game.board.get_tile_value(Position(row, col)) for col in range(4)
        ]

        monotonicity += sum(sorted(row_values))

    for col in range(4):
        col_values = [
            app.game.board.get_tile_value(Position(row, col)) for row in range(4)
        ]

        monotonicity += sum(sorted(col_values))

    return monotonicity
