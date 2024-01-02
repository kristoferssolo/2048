#!/usr/bin/env python


from loguru import logger
from py2048 import Game


@logger.catch
def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()
