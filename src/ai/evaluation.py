import random
import time

import neat
from loguru import logger
from py2048 import Menu

from .fitness import calculate_fitness


def eval_genomes(genomes, config: neat.Config):
    app = Menu()
    app.play()
    app._game_active = False
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        start_time = time.perf_counter()
        while True:
            output = net.activate((*app.game.board.matrix(),))

            decision = output.index(max(output))

            decisions = {
                0: app.game.move_left,
                1: app.game.move_down,
                2: app.game.move_up,
                3: app.game.move_right,
            }

            decisions[decision]()

            app._hande_events()
            app.game.draw(app._surface)

            time_passed = time.perf_counter() - start_time

            if app.game.board.is_game_over():
                max_tile, score = calculate_fitness(genome, app)

                logger.info(f"{max_tile=}\t{score=:_}\t{genome_id=}")
                app.game.restart()
                break
            elif app.game.board._is_full() and time_passed >= 0.1:
                decisions[random.choice((0, 1, 2, 3))]()
                max_tile, score = calculate_fitness(genome, app)
