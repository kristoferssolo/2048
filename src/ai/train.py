import neat
from loguru import logger
from path import BASE_PATH
from py2048 import Menu


def _get_config() -> neat.Config:
    config_path = BASE_PATH / "config.txt"
    return neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )


def train() -> None:
    config = _get_config()
    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-0")
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)

    logger.info(f"\nBest genome:\n{winner}")


def eval_genomes(genomes, config: neat.Config):
    for genome_id, genome in genomes:
        genome.fitness = 4.0
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

            if app.game.board._is_full() or app.game.board.score > 10_000:
                calculate_fitness(genome, app.game.board.score)
                logger.info(
                    f"Genome: {genome_id} fitness: {genome.fitness} score: {app.game.board.score}"
                )
                app.game.restart()
                break


def calculate_fitness(genome, score: int):
    genome.fitness += score
