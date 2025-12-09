"""
Keyboard bindings for Todo Master application

Defines all keyboard shortcuts used across different screens (FR-061 to FR-070).
"""

import curses
from typing import Dict, Optional

# Navigation keys (FR-065)
KEY_UP = ord('k')
KEY_DOWN = ord('j')
KEY_PAGE_UP = ord('K')
KEY_PAGE_DOWN = ord('J')
KEY_TOP = ord('g')
KEY_BOTTOM = ord('G')
KEY_TAB = ord('\t')
KEY_SHIFT_TAB = curses.KEY_BTAB

# Screen switching (FR-063)
KEY_SCREEN_1 = ord('1')
KEY_SCREEN_2 = ord('2')
KEY_SCREEN_3 = ord('3')
KEY_SCREEN_4 = ord('4')
KEY_SCREEN_5 = ord('5')
KEY_SCREEN_6 = ord('6')

# Task operations (FR-001 to FR-007)
KEY_NEW_TASK = ord('n')
KEY_EDIT = ord('e')
KEY_DELETE = ord('x')
KEY_TOGGLE_DONE = ord('d')
KEY_TOGGLE_DONE_ALT = ord(' ')
KEY_UNDO = ord('u')

# Priority setting (FR-009)
KEY_PRIORITY_1 = ord('1')  # When in priority mode
KEY_PRIORITY_2 = ord('2')
KEY_PRIORITY_3 = ord('3')
KEY_PRIORITY_4 = ord('4')
KEY_PRIORITY_5 = ord('5')

# Project operations (FR-015)
KEY_MOVE_PROJECT = ord('p')

# Tag operations (FR-025)
KEY_TAG = ord('t')

# Filter operations (FR-028 to FR-031)
KEY_FILTER = ord('f')

# Search (FR-033)
KEY_SEARCH = ord('/')
KEY_SEARCH_ALT = 6  # Ctrl+F

# Calendar operations (FR-022, FR-023, FR-024)
KEY_RESCHEDULE = ord('r')
KEY_DATE_FORWARD = ord('+')
KEY_DATE_BACK = ord('-')
KEY_TODAY = ord('t')
KEY_WEEK_VIEW = ord('w')
KEY_MONTH_VIEW = ord('m')

# Statistics operations (FR-043, FR-044)
KEY_PERIOD = ord('p')
KEY_REFRESH = ord('r')

# Settings operations (FR-045)
KEY_SAVE = ord('s')

# General operations (FR-067, FR-070)
KEY_HELP = ord('?')
KEY_QUIT = ord('q')
KEY_ESCAPE = 27
KEY_ENTER = ord('\n')
KEY_ENTER_ALT = curses.KEY_ENTER

# Archive operations (FR-017)
KEY_ARCHIVE = ord('a')

# Complete keyboard bindings reference
KEY_BINDINGS = {
    # Global navigation
    "j": "Move down",
    "k": "Move up",
    "J": "Page down",
    "K": "Page up",
    "g": "Go to top",
    "G": "Go to bottom",
    "Tab": "Next screen",
    "Shift+Tab": "Previous screen",
    "1-6": "Jump to screen 1-6",
    "?": "Show help",
    "q": "Quit application",
    "Esc": "Cancel/Close",

    # Task List screen
    "n": "New task",
    "e": "Edit selected task",
    "d / Space": "Toggle task done",
    "x": "Delete task",
    "u": "Undo delete (5 sec window)",
    "p": "Move to project",
    "t": "Edit tags",
    "f": "Apply filter",
    "/": "Search tasks",
    "1-5": "Set priority (when task selected)",

    # Projects screen
    "n": "New project",
    "e": "Edit project",
    "a": "Archive project",
    "Enter": "Expand/collapse project",

    # Calendar screen
    "r": "Reschedule task",
    "+": "Due date +1 day",
    "-": "Due date -1 day",
    "t": "Jump to today",
    "w": "Week view",
    "m": "Month view",

    # Tags & Filters screen
    "n": "New tag/filter (context)",
    "e": "Edit tag/filter",

    # Statistics screen
    "p": "Change time period",
    "r": "Refresh statistics",

    # Settings screen
    "s": "Save settings",
    "e": "Edit setting",
}

# Context-specific bindings for help modals
TASK_LIST_KEYS = {
    "j/k": "Navigate up/down",
    "g/G": "Top/Bottom",
    "n": "New task",
    "e": "Edit task",
    "d/Space": "Toggle done",
    "x": "Delete task",
    "u": "Undo delete",
    "p": "Move to project",
    "t": "Edit tags",
    "f": "Filter",
    "/": "Search",
    "1-5": "Set priority",
    "Tab/1-6": "Switch screen",
    "?": "Help",
    "q": "Quit",
}

PROJECTS_KEYS = {
    "j/k": "Navigate",
    "n": "New project",
    "e": "Edit project",
    "a": "Archive project",
    "Enter": "Expand/collapse",
    "Tab/1-6": "Switch screen",
    "?": "Help",
    "q": "Quit",
}

CALENDAR_KEYS = {
    "j/k": "Navigate",
    "r": "Reschedule",
    "+/-": "Adjust date ±1 day",
    "t": "Today",
    "w": "Week view",
    "m": "Month view",
    "Tab/1-6": "Switch screen",
    "?": "Help",
    "q": "Quit",
}

TAGS_KEYS = {
    "j/k": "Navigate",
    "n": "New tag/filter",
    "e": "Edit",
    "Tab/1-6": "Switch screen",
    "?": "Help",
    "q": "Quit",
}

STATS_KEYS = {
    "p": "Change period",
    "r": "Refresh",
    "Tab/1-6": "Switch screen",
    "?": "Help",
    "q": "Quit",
}

SETTINGS_KEYS = {
    "j/k": "Navigate",
    "e": "Edit setting",
    "s": "Save",
    "Tab/1-6": "Switch screen",
    "?": "Help",
    "q": "Quit",
}


def get_key_description(key_code: int) -> Optional[str]:
    """
    Get a human-readable description for a key code.

    Args:
        key_code: The curses key code

    Returns:
        Description string or None if not a recognized key
    """
    key_map = {
        ord('j'): "Down",
        ord('k'): "Up",
        ord('g'): "Top",
        ord('G'): "Bottom",
        ord('n'): "New",
        ord('e'): "Edit",
        ord('d'): "Done",
        ord('x'): "Delete",
        ord('u'): "Undo",
        ord('p'): "Project",
        ord('t'): "Tag/Today",
        ord('f'): "Filter",
        ord('/'): "Search",
        ord('?'): "Help",
        ord('q'): "Quit",
        ord('r'): "Reschedule/Refresh",
        ord('w'): "Week",
        ord('m'): "Month",
        ord('a'): "Archive",
        ord('s'): "Save",
        ord(' '): "Done",
        ord('\t'): "Next",
        ord('\n'): "Select",
        27: "Escape",
    }

    # Handle number keys
    if ord('1') <= key_code <= ord('6'):
        return f"Screen {chr(key_code)}"

    return key_map.get(key_code)


def get_screen_keys(screen_id: int) -> Dict[str, str]:
    """
    Get context-specific key bindings for a screen.

    Args:
        screen_id: The screen identifier (0-5)

    Returns:
        Dictionary of key bindings for that screen
    """
    from todo_master.utils.constants import (
        SCREEN_TASK_LIST, SCREEN_PROJECTS, SCREEN_CALENDAR,
        SCREEN_TAGS, SCREEN_STATS, SCREEN_SETTINGS
    )

    screen_keys = {
        SCREEN_TASK_LIST: TASK_LIST_KEYS,
        SCREEN_PROJECTS: PROJECTS_KEYS,
        SCREEN_CALENDAR: CALENDAR_KEYS,
        SCREEN_TAGS: TAGS_KEYS,
        SCREEN_STATS: STATS_KEYS,
        SCREEN_SETTINGS: SETTINGS_KEYS,
    }

    return screen_keys.get(screen_id, TASK_LIST_KEYS)


__all__ = [
    "KEY_UP",
    "KEY_DOWN",
    "KEY_PAGE_UP",
    "KEY_PAGE_DOWN",
    "KEY_TOP",
    "KEY_BOTTOM",
    "KEY_TAB",
    "KEY_SHIFT_TAB",
    "KEY_SCREEN_1",
    "KEY_SCREEN_2",
    "KEY_SCREEN_3",
    "KEY_SCREEN_4",
    "KEY_SCREEN_5",
    "KEY_SCREEN_6",
    "KEY_NEW_TASK",
    "KEY_EDIT",
    "KEY_DELETE",
    "KEY_TOGGLE_DONE",
    "KEY_TOGGLE_DONE_ALT",
    "KEY_UNDO",
    "KEY_MOVE_PROJECT",
    "KEY_TAG",
    "KEY_FILTER",
    "KEY_SEARCH",
    "KEY_SEARCH_ALT",
    "KEY_RESCHEDULE",
    "KEY_DATE_FORWARD",
    "KEY_DATE_BACK",
    "KEY_TODAY",
    "KEY_WEEK_VIEW",
    "KEY_MONTH_VIEW",
    "KEY_PERIOD",
    "KEY_REFRESH",
    "KEY_SAVE",
    "KEY_HELP",
    "KEY_QUIT",
    "KEY_ESCAPE",
    "KEY_ENTER",
    "KEY_ENTER_ALT",
    "KEY_ARCHIVE",
    "KEY_BINDINGS",
    "TASK_LIST_KEYS",
    "PROJECTS_KEYS",
    "CALENDAR_KEYS",
    "TAGS_KEYS",
    "STATS_KEYS",
    "SETTINGS_KEYS",
    "get_key_description",
    "get_screen_keys",
]
