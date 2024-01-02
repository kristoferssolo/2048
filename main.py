#!/usr/bin/env python


from loguru import logger
from py2048 import Menu


@logger.catch
def main() -> None:
    Menu().run()


if __name__ == "__main__":
    main()
