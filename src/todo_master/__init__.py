"""
Todo Master - Multi-screen terminal-based task management application

A powerful curses-based task manager with project organization, calendar views,
tags, filters, statistics, and customizable settings.
"""

__version__ = "1.0.0"
__author__ = "Todo Master Team"
__license__ = "MIT"

# Re-export commonly used components for convenience
from todo_master.models import TaskStatus, Priority, ProjectColor

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "TaskStatus",
    "Priority",
    "ProjectColor",
]
