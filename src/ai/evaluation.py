import time

import neat
from loguru import logger
from py2048 import Menu


def eval_genomes(genomes, config: neat.Config):
    app = Menu()
    app.play()
    app._game_active = False
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        start_time = time.perf_counter()

        while True:
            output = net.activate(
                (
                    *app.game.board.matrix(),
                    app.game.board.score,
                )
            )

            decision = output.index(max(output))

            decisions = {
                0: app.game.move_up,
                1: app.game.move_down,
                2: app.game.move_left,
                3: app.game.move_right,
            }

            decisions[decision]()

            app._hande_events()
            app.game.draw(app._surface)
            max_val = app.game.board.max_val()

            time_passed = time.perf_counter() - start_time
            score = app.game.board.score
            if max_val >= 32:
                calculate_fitness(genome, max_val)
                logger.info(f"{max_val=}\t{score=:_}\t{genome_id=}")
                app.game.restart()
                break
            elif app.game.board.is_game_over() or (
                app.game.board._is_full() and time_passed >= 0.1
            ):
                calculate_fitness(genome, -max_val)
                logger.info(f"{max_val=}\t{score=:_}\t{genome_id=}")
                app.game.restart()
                break


def calculate_fitness(genome: neat.DefaultGenome, score: int):
    genome.fitness += score
