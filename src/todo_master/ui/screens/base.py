"""
Base screen class for all application screens
"""

from abc import ABC, abstractmethod
from typing import Optional
import curses

from todo_master.utils.keybindings import KEY_HELP, KEY_QUIT


class BaseScreen(ABC):
    """
    Abstract base class for all screens

    Provides common functionality for navigation, help, and status bar.
    """

    def __init__(self, stdscr, title: str):
        """
        Initialize screen

        Args:
            stdscr: Main curses window
            title: Screen title
        """
        self.stdscr = stdscr
        self.title = title
        self.active = False

    @abstractmethod
    def draw(self) -> None:
        """Draw the screen content"""
        pass

    @abstractmethod
    def handle_key(self, key: int) -> Optional[str]:
        """
        Handle keyboard input

        Args:
            key: Key code

        Returns:
            Action string or None
        """
        pass

    def activate(self):
        """Called when screen becomes active"""
        self.active = True

    def deactivate(self):
        """Called when screen becomes inactive"""
        self.active = False

    def draw_title(self):
        """Draw screen title at top"""
        height, width = self.stdscr.getmaxyx()
        title_text = f" {self.title} "
        try:
            self.stdscr.addstr(0, (width - len(title_text)) // 2, title_text,
                             curses.A_BOLD)
        except curses.error:
            pass

    def draw_status_bar(self, text: str):
        """
        Draw status bar at bottom

        Args:
            text: Status text to display
        """
        height, width = self.stdscr.getmaxyx()
        try:
            self.stdscr.addstr(height - 1, 0, text[:width - 1].ljust(width - 1),
                             curses.A_REVERSE)
        except curses.error:
            pass

    def show_message(self, message: str):
        """
        Show a message at the bottom of the screen

        Args:
            message: Message to display
        """
        self.draw_status_bar(message)
        self.stdscr.refresh()


__all__ = ["BaseScreen"]
