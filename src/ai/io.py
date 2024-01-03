import pickle
from pathlib import Path

import neat
from path import BASE_PATH


def read_genome() -> neat.DefaultGenome:
    with open(BASE_PATH / "best_genome", "rb") as f:
        return pickle.load(f)


def save_genome(genome) -> None:
    with open(BASE_PATH / "best_genome", "wb") as f:
        pickle.dump(genome, f)
