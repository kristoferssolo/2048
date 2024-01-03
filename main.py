#!/usr/bin/env python

import argparse

from game import play

# from ai import train
from loguru import logger
from utils import BASE_PATH


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


def setup_logger(debug_level: str) -> None:
    logger.add(
        BASE_PATH / ".logs" / "game.log",
        format="{time} | {level} | {message}",
        level=debug_level.upper(),
        rotation="10 MB",
        compression="zip",
    )


@logger.catch
def main(args: argparse.ArgumentParser) -> None:
    if args.debug:
        setup_logger("debug")
    elif args.verbose:
        setup_logger("debug")
    else:
        setup_logger("warning")

    if args.train is not None:
        # train(args.train)
        logger.debug("Train")
    elif args.noui:
        logger.debug("Run game in CLI")
        play()
    else:
        logger.debug("Run app")
        # play()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
