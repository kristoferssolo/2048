#!/usr/bin/env python


from ai import train
from loguru import logger
from py2048 import Menu


@logger.catch
def main() -> None:
    # Menu().run()
    train(100)


if __name__ == "__main__":
    main()
