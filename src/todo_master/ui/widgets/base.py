"""
Base widget class for UI components
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple
import curses


class BaseWidget(ABC):
    """
    Abstract base class for all UI widgets

    Provides common functionality for position, dimensions, drawing, and focus.
    """

    def __init__(self, y: int, x: int, height: int, width: int):
        """
        Initialize widget

        Args:
            y: Y position (row)
            x: X position (column)
            height: Widget height
            width: Widget width
        """
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.focused = False
        self.visible = True

    @abstractmethod
    def draw(self, window) -> None:
        """
        Draw the widget on the given window

        Args:
            window: Curses window object
        """
        pass

    def set_focus(self, focused: bool):
        """Set widget focus state"""
        self.focused = focused

    def set_visible(self, visible: bool):
        """Set widget visibility"""
        self.visible = visible

    def is_visible(self) -> bool:
        """Check if widget is visible"""
        return self.visible

    def contains_point(self, y: int, x: int) -> bool:
        """Check if point is within widget bounds"""
        return (self.y <= y < self.y + self.height and
                self.x <= x < self.x + self.width)

    def handle_key(self, key: int) -> bool:
        """
        Handle keyboard input

        Args:
            key: Key code

        Returns:
            True if key was handled, False otherwise
        """
        return False


__all__ = ["BaseWidget"]
