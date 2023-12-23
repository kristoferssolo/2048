import sys

import pygame


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("2048")
        self.bg_color = (230, 230, 230)

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(self.bg_color)
            pygame.display.flip()

    def update(self) -> None:
        pass

    def render(self) -> None:
        self.screen.fill((255, 255, 255))
        pygame.display.flip()
