"""
Theme and color management for curses UI

Handles color pair initialization and theme switching (FR-046, FR-074).
"""

import curses
from typing import Dict, Optional

from todo_master.utils.constants import (
    COLOR_NORMAL, COLOR_SELECTED, COLOR_PRIORITY_LOW, COLOR_PRIORITY_MEDIUM,
    COLOR_PRIORITY_HIGH, COLOR_PRIORITY_URGENT, COLOR_PROJECT_RED,
    COLOR_PROJECT_GREEN, COLOR_PROJECT_YELLOW, COLOR_PROJECT_BLUE,
    COLOR_PROJECT_MAGENTA, COLOR_PROJECT_CYAN, COLOR_PROJECT_WHITE,
    COLOR_OVERDUE, COLOR_STATUS_BAR, COLOR_MODAL_BORDER
)


class ThemeManager:
    """
    Manages color schemes and themes for the application (FR-046, FR-074)

    Initializes curses color pairs and provides theme switching between
    dark, light, and auto modes. Supports 256-color terminals with fallback
    to 8-color ANSI.
    """

    def __init__(self):
        """Initialize theme manager"""
        self.current_theme = "dark"
        self.has_colors = False
        self.color_count = 0
        self.initialized = False

    def initialize(self):
        """
        Initialize curses colors and color pairs

        Called after curses.initscr() to setup color support.
        Detects terminal capabilities and initializes appropriate color scheme.
        """
        if not curses.has_colors():
            self.has_colors = False
            self.initialized = True
            return

        curses.start_color()
        curses.use_default_colors()
        self.has_colors = True
        self.color_count = curses.COLORS

        # Initialize color pairs based on terminal capability
        if self.color_count >= 256:
            self._init_256_colors()
        else:
            self._init_8_colors()

        self.initialized = True

    def _init_256_colors(self):
        """Initialize 256-color palette"""
        # Normal and selected
        curses.init_pair(COLOR_NORMAL, curses.COLOR_WHITE, -1)
        curses.init_pair(COLOR_SELECTED, curses.COLOR_BLACK, curses.COLOR_CYAN)

        # Priority colors
        curses.init_pair(COLOR_PRIORITY_LOW, 244, -1)      # Gray
        curses.init_pair(COLOR_PRIORITY_MEDIUM, curses.COLOR_BLUE, -1)
        curses.init_pair(COLOR_PRIORITY_HIGH, curses.COLOR_YELLOW, -1)
        curses.init_pair(COLOR_PRIORITY_URGENT, curses.COLOR_RED, -1)

        # Project colors
        curses.init_pair(COLOR_PROJECT_RED, curses.COLOR_RED, -1)
        curses.init_pair(COLOR_PROJECT_GREEN, curses.COLOR_GREEN, -1)
        curses.init_pair(COLOR_PROJECT_YELLOW, curses.COLOR_YELLOW, -1)
        curses.init_pair(COLOR_PROJECT_BLUE, curses.COLOR_BLUE, -1)
        curses.init_pair(COLOR_PROJECT_MAGENTA, curses.COLOR_MAGENTA, -1)
        curses.init_pair(COLOR_PROJECT_CYAN, curses.COLOR_CYAN, -1)
        curses.init_pair(COLOR_PROJECT_WHITE, curses.COLOR_WHITE, -1)

        # Special colors
        curses.init_pair(COLOR_OVERDUE, curses.COLOR_RED, -1)
        curses.init_pair(COLOR_STATUS_BAR, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(COLOR_MODAL_BORDER, curses.COLOR_CYAN, -1)

    def _init_8_colors(self):
        """Initialize 8-color ANSI palette (fallback)"""
        # Same as 256-color but with basic ANSI colors
        curses.init_pair(COLOR_NORMAL, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_SELECTED, curses.COLOR_BLACK, curses.COLOR_CYAN)

        curses.init_pair(COLOR_PRIORITY_LOW, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PRIORITY_MEDIUM, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PRIORITY_HIGH, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PRIORITY_URGENT, curses.COLOR_RED, curses.COLOR_BLACK)

        curses.init_pair(COLOR_PROJECT_RED, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PROJECT_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PROJECT_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PROJECT_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PROJECT_MAGENTA, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PROJECT_CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PROJECT_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)

        curses.init_pair(COLOR_OVERDUE, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(COLOR_STATUS_BAR, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(COLOR_MODAL_BORDER, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def get_priority_color(self, priority: str) -> int:
        """Get color pair for priority level"""
        priority_colors = {
            "low": COLOR_PRIORITY_LOW,
            "medium": COLOR_PRIORITY_MEDIUM,
            "high": COLOR_PRIORITY_HIGH,
            "urgent": COLOR_PRIORITY_URGENT,
        }
        return curses.color_pair(priority_colors.get(priority, COLOR_PRIORITY_MEDIUM))

    def get_project_color(self, color: str) -> int:
        """Get color pair for project color"""
        project_colors = {
            "red": COLOR_PROJECT_RED,
            "green": COLOR_PROJECT_GREEN,
            "yellow": COLOR_PROJECT_YELLOW,
            "blue": COLOR_PROJECT_BLUE,
            "magenta": COLOR_PROJECT_MAGENTA,
            "cyan": COLOR_PROJECT_CYAN,
            "white": COLOR_PROJECT_WHITE,
        }
        return curses.color_pair(project_colors.get(color, COLOR_PROJECT_WHITE))

    def get_color(self, color_id: int) -> int:
        """Get color pair by ID"""
        if not self.has_colors:
            return 0
        return curses.color_pair(color_id)

    def set_theme(self, theme: str):
        """
        Switch theme (dark/light/auto)

        Args:
            theme: Theme name ("dark", "light", "auto")
        """
        self.current_theme = theme
        # Theme switching would reinitialize colors here
        # For MVP, we'll just track the preference


__all__ = ["ThemeManager"]
