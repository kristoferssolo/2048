import pygame
from attrs import define, field
from py2048.color import ColorScheme
from py2048.config import Config


@define
class Label:
    text: str
    position: tuple[int, int]
    bg_color: ColorScheme
    font_family: str
    font_color: ColorScheme
    font_size: int
    font: pygame.font.Font = field(init=False)
    rendered_text: pygame.Surface = field(init=False)
    rect: pygame.Rect = field(init=False)

    def __attrs_post_init__(self):
        self.font = pygame.font.SysFont(self.font_family, self.font_size)
        self._draw_text()

    def _draw_text(self) -> None:
        self.rendered_text = self.font.render(
            self.text, True, self.font_color, self.bg_color
        )
        self.rect = self.rendered_text.get_rect(topleft=self.position)

    def update(self, new_text: str) -> None:
        self.text = new_text
        self._draw_text()

    def draw(self, screen):
        screen.blit(self.rendered_text, self.position)
