from abc import ABC, ABCMeta, abstractmethod

import pygame

from py2048.utils import Direction, Position


class MovableUIElement(ABC, metaclass=ABCMeta):
    @abstractmethod
    def move(self, direction: Direction) -> None:
        """Move the element in the given direction."""

    @abstractmethod
    def update(self) -> None:
        """Update the element."""

    @abstractmethod
    def __hash__(self) -> int:
        """Return a hash of the sprite."""

    @property
    @abstractmethod
    def pos(self) -> Position:
        """Return the position of the element."""
