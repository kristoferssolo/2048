import neat
from loguru import logger
from py2048 import Menu


def eval_genomes(genomes, config: neat.Config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        app = Menu()
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        app.play()
        app._game_active = False

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

            if app.game.board._is_full() or max_val >= 2048:
                calculate_fitness(genome, max_val)
                logger.info(f"{max_val=}")
                app.game.restart()
                break


def calculate_fitness(genome: neat.DefaultGenome, score: int):
    genome.fitness += score
