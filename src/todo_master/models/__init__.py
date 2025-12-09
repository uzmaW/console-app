"""
Data models for Todo Master application

Includes enums for task status, priority, and project colors, as well as
data classes for Task, Project, Tag, Filter, and Settings.
"""

from enum import Enum
from typing import List

# FR-008: Task status values
class TaskStatus(str, Enum):
    """Task status enumeration (FR-008)"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"

    def __str__(self) -> str:
        return self.value

    @property
    def display_name(self) -> str:
        """Get human-readable status name"""
        return self.value.replace("_", " ").title()

    @property
    def symbol(self) -> str:
        """Get status symbol for UI display"""
        symbols = {
            TaskStatus.TODO: "○",
            TaskStatus.IN_PROGRESS: "◐",
            TaskStatus.DONE: "●",
            TaskStatus.ARCHIVED: "◌",
        }
        return symbols.get(self, "○")


# FR-009: Priority levels
class Priority(str, Enum):
    """Task priority enumeration (FR-009)"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

    def __str__(self) -> str:
        return self.value

    @property
    def display_name(self) -> str:
        """Get human-readable priority name"""
        return self.value.capitalize()

    @property
    def symbol(self) -> str:
        """Get priority symbol for UI display"""
        symbols = {
            Priority.LOW: "↓",
            Priority.MEDIUM: "−",
            Priority.HIGH: "↑",
            Priority.URGENT: "‼",
        }
        return symbols.get(self, "−")

    @property
    def sort_value(self) -> int:
        """Get numeric value for sorting (higher = more urgent)"""
        values = {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
            Priority.URGENT: 4,
        }
        return values.get(self, 2)

    @classmethod
    def from_number(cls, number: int) -> "Priority":
        """
        Convert number (1-5) to Priority enum

        Args:
            number: Priority number (1=low, 2=medium, 3=high, 4=urgent, 5=urgent)

        Returns:
            Priority enum value
        """
        mapping = {
            1: cls.LOW,
            2: cls.MEDIUM,
            3: cls.HIGH,
            4: cls.URGENT,
            5: cls.URGENT,  # Both 4 and 5 map to URGENT for 1-5 keyboard shortcuts
        }
        return mapping.get(number, cls.MEDIUM)


# FR-014: Project colors
class ProjectColor(str, Enum):
    """Project color enumeration (FR-014)"""
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"

    def __str__(self) -> str:
        return self.value

    @property
    def display_name(self) -> str:
        """Get human-readable color name"""
        return self.value.capitalize()

    @property
    def curses_color(self) -> int:
        """Get curses color constant"""
        import curses
        colors = {
            ProjectColor.RED: curses.COLOR_RED,
            ProjectColor.GREEN: curses.COLOR_GREEN,
            ProjectColor.YELLOW: curses.COLOR_YELLOW,
            ProjectColor.BLUE: curses.COLOR_BLUE,
            ProjectColor.MAGENTA: curses.COLOR_MAGENTA,
            ProjectColor.CYAN: curses.COLOR_CYAN,
            ProjectColor.WHITE: curses.COLOR_WHITE,
        }
        return colors.get(self, curses.COLOR_WHITE)


__all__ = [
    "TaskStatus",
    "Priority",
    "ProjectColor",
]
