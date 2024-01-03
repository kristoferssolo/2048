import neat
from loguru import logger
from path import BASE_PATH

from .config import get_config
from .evaluation import eval_genomes
from .io import save_genome


def train(generations: int) -> None:
    """Train the AI for a given number of generations."""
    config = get_config()
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(1))

    winner = population.run(eval_genomes, generations)

    logger.info(winner)
    save_genome(winner, BASE_PATH / "best_genome")
