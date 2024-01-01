import random
from typing import Union

import pygame

from .color import ColorScheme
from .config import Config
from .utils import Direction, grid_pos


class Block(pygame.sprite.Sprite):
    def __init__(
        self, x: int, y: int, group: pygame.sprite.Group, value: int | None = 2
    ):
        """Initialize a block"""
        super().__init__()

        self.value: int = (
            value
            if value is not None
            else 2
            if random.random() <= Config.BLOCK_VALUE_PROBABILITY
            else 4
        )
        self.image = self._create_block_surface()
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.font = pygame.font.SysFont(Config.FONT_FAMILY, Config.FONT_SIZE)
        self.group = group
        self.update()

    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw a rounded rectangle with borders on the given surface."""
        rect = (0, 0, Config.BLOCK_SIZE, Config.BLOCK_SIZE)
        pygame.draw.rect(
            surface, self._get_color(), rect, border_radius=Config.BLOCK_BORDER_RADIUS
        )  # background
        pygame.draw.rect(
            surface,
            (0, 0, 0, 0),
            rect,
            border_radius=Config.BLOCK_BORDER_RADIUS,
            width=Config.BLOCK_BORDER_WIDTH,
        )  # border

    def _create_block_surface(self) -> pygame.Surface:
        """Create a surface for the block."""
        block_surface = pygame.Surface(
            (Config.BLOCK_SIZE, Config.BLOCK_SIZE), pygame.SRCALPHA
        )
        self._draw_background(block_surface)
        return block_surface

    def draw(self) -> None:
        """Draw the value of the block"""
        text = self.font.render(str(self.value), True, Config.COLORSCHEME.DARK_TEXT)
        block_surface = self._create_block_surface()

        block_center: tuple[int, int] = (Config.BLOCK_SIZE // 2, Config.BLOCK_SIZE // 2)

        text_rect: pygame.Rect = text.get_rect(center=self.image.get_rect().center)
        block_surface.blit(text, text_rect)

        self.image.blit(block_surface, (0, 0))

    def move(self, direction: Direction) -> int:
        """Move the block by `dx` and `dy`."""
        score = 0
        while True:
            new_x, new_y = self._calc_new_pos(direction)

            if self._is_out_if_bounds(new_x, new_y):
                return score

            if self._has_collision(new_x, new_y):
                collided_block = self._get_collided_block(new_x, new_y)
                if collided_block and self._can_merge(collided_block):
                    score += self._merge(collided_block)
                else:
                    return score

            self.group.remove(self)
            self.rect.topleft = new_x, new_y
            self.group.add(self)

    def _calc_new_pos(self, direction: Direction) -> tuple[int, int]:
        """Calculate the new position of the block."""
        dx, dy = direction * Config.BLOCK_SIZE
        return self.rect.x + dx, self.rect.y + dy

    def _is_out_if_bounds(self, x: int, y: int) -> bool:
        """Return whether the block is out of bounds."""
        board_left = Config.BOARD_X
        board_right = Config.BOARD_X + Config.BOARD_WIDTH - Config.BLOCK_SIZE
        board_top = Config.BOARD_Y
        board_bottom = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BLOCK_SIZE
        return not (board_left <= x <= board_right and board_top <= y <= board_bottom)

    def _has_collision(self, x: int, y: int) -> bool:
        """Checks whether the block has a collision with any other block."""
        return any(
            block.rect.collidepoint(x, y) for block in self.group if block != self
        )

    def _get_collided_block(self, x: int, y: int) -> Union["Block", None]:
        """Get the block that collides with the given block."""

        return next(
            (
                block
                for block in self.group
                if block != self and block.rect.collidepoint(x, y)
            ),
            None,
        )

    def _can_merge(self, other: "Block") -> bool:
        """Check if the block can merge with another block."""
        return self.value == other.value

    def _merge(self, other: "Block") -> int:
        """Merge the block with another block."""
        self.group.remove(other)
        self.group.remove(self)
        self.value += other.value
        self.update()
        self.group.add(self)
        return self.value

    def update(self) -> None:
        """Update the block"""
        self.draw()

    def can_move(self) -> bool:
        """Check if the block can move"""
        for direction in Direction:
            new_x, new_y = self._calc_new_pos(direction)
            if not self._is_out_if_bounds(new_x, new_y) and self._has_collision(
                new_x, new_y
            ):
                collided_block = self._get_collided_block(new_x, new_y)
                if collided_block and self._can_merge(collided_block):
                    return True
        return False

    def _get_color(self) -> ColorScheme:
        """Change the color of the block based on its value"""
        color_map = {
            2: Config.COLORSCHEME.BLOCK_2,
            4: Config.COLORSCHEME.BLOCK_4,
            8: Config.COLORSCHEME.BLOCK_8,
            16: Config.COLORSCHEME.BLOCK_16,
            32: Config.COLORSCHEME.BLOCK_32,
            64: Config.COLORSCHEME.BLOCK_64,
            128: Config.COLORSCHEME.BLOCK_128,
            256: Config.COLORSCHEME.BLOCK_256,
            512: Config.COLORSCHEME.BLOCK_512,
            1024: Config.COLORSCHEME.BLOCK_1024,
            2048: Config.COLORSCHEME.BLOCK_2048,
        }
        return color_map.get(self.value, Config.COLORSCHEME.BLOCK_ELSE)

    def __repr__(self) -> str:
        """Return a string representation of the block"""
        return f"Block({id(self)}): {self.pos} num={self.value}"

    def __str__(self) -> str:
        """Return a string representation of the block"""
        return self.__repr__()

    def __hash__(self) -> int:
        """Return a hash of the block"""
        return hash((self.rect.x, self.rect.y, self.value))

    @property
    def pos(self) -> tuple[int, int]:
        """Return the position of the block"""
        return grid_pos(self.rect.x), grid_pos(self.rect.y)
