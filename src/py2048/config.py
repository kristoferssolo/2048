class Config:
    FONT_FAMILY = "Roboto"
    FONT_SIZE = 32

    BOARD_SIZE = 4
    BLOCK_SIZE = 50

    # WIDTH = BOARD_SIZE * BLOCK_SIZE + BLOCK_SIZE
    # HEIGHT = BOARD_SIZE * BLOCK_SIZE + BLOCK_SIZE * 2

    BOARD_WIDTH = BOARD_SIZE * BLOCK_SIZE
    BOARD_HEIGHT = BOARD_SIZE * BLOCK_SIZE

    HEADER_WIDTH = BOARD_WIDTH + BLOCK_SIZE
    HEADER_HEIGHT = BLOCK_SIZE

    BOARD_X = BLOCK_SIZE // 2
    BOARD_Y = HEADER_HEIGHT + BLOCK_SIZE // 2

    SCREEN_WIDTH = HEADER_WIDTH
    SCREEN_HEIGHT = BOARD_HEIGHT + BLOCK_SIZE + HEADER_HEIGHT
    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT

    INITIAL_BLOCK_COUNT = 2
    BLOCK_VALUE_PROBABILITY = 0.9
