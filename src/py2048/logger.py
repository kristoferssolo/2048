from pathlib import Path

from loguru import logger

BASE_PATH = Path(__file__).resolve().parent.parent.parent


def setup_logger() -> None:
    logger.add(
        BASE_PATH.joinpath(".logs", "game.log"),
        format="{time} | {level} | {message}",
        level="DEBUG" if BASE_PATH.joinpath("debug").exists() else "INFO",
        rotation="1 MB",
        compression="zip",
    )
