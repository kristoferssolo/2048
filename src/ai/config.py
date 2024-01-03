import neat
from path import BASE_PATH


def get_config() -> neat.Config:
    config_path = BASE_PATH / "config.txt"
    return neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
