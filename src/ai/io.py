import pickle
from pathlib import Path

import neat
from path import BASE_PATH


def read_genome(filename: Path) -> neat.DefaultGenome:
    with open(filename, "rb") as f:
        return pickle.load(f)


def save_genome(genome, filename: Path) -> None:
    with open(filename, "wb") as f:
        pickle.dump(genome, f)
