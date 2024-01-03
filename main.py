#!/usr/bin/env python
import argparse

from loguru import logger
from utils import BASE_PATH, Config


def pos_int(string: str) -> int:
    try:
        value = int(string)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Expected integer, got {string!r}")
    if value < 0:
        raise argparse.ArgumentTypeError(f"Expected non negative number, got {value}")
    return value


parser = argparse.ArgumentParser(description="2048 game with AI")
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-d",
    "--debug",
    action="store_true",
    help="Debug",
)

group.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Verbose",
)

group2 = parser.add_mutually_exclusive_group()

group2.add_argument(
    "-t",
    "--train",
    type=pos_int,
    nargs="?",
    const=100,
    metavar="int",
    help="Trains the AI",
)
group2.add_argument(
    "-n",
    "--noui",
    action="store_true",
    help="Run app in the CLI",
)

group2.add_argument(
    "-g",
    "--graphic",
    action="store_true",
    help="Run app with GUI",
)

logger.add(
    BASE_PATH / ".logs" / "2048.log",
    format="{time} | {level} | {message}",
    level="WARNING",
    rotation="10 MB",
    compression="zip",
)


@logger.catch
def main(args: argparse.ArgumentParser) -> None:
    if args.debug:
        Config.log_level = "debug"
    elif args.verbose:
        Config.log_level = "info"

    import ai
    import game
    import gui

    if args.train is not None:
        # train(args.train)
        ai.log.debug("Training the AI")
    elif args.noui:
        game.log.debug("Running the game in CLI")
        game.play()
    else:
        gui.log.debug("Running the game in GUI")
        gui.launch()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
