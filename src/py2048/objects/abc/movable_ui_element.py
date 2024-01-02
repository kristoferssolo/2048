from abc import abstractmethod

import pygame

from py2048.utils import Direction, Position

from .ui_element import UIElement


class MovableUIElement(UIElement):
    def __init__(self, *args, **kwargs) -> None:
        UIElement.__init__(self, *args, **kwargs)

    @abstractmethod
    def move(self, direction: Direction) -> None:
        """Move the element in the given direction."""

    @property
    @abstractmethod
    def pos(self) -> Position:
        """Return the position of the element."""
