"""
Calendar screen - today/upcoming tasks view

Displays tasks grouped by date buckets (Today, Tomorrow, This Week, etc.).
"""

import curses
from typing import Optional, List
from datetime import date

from todo_master.ui.screens.base import BaseScreen
from todo_master.services.task_manager import TaskManager
from todo_master.utils.date_utils import group_by_date_bucket, format_relative_date


class CalendarScreen(BaseScreen):
    """
    Calendar/Today view screen

    Groups tasks by time buckets for easy scheduling.
    """

    def __init__(self, stdscr, task_manager: TaskManager):
        """
        Initialize calendar screen

        Args:
            stdscr: Main curses window
            task_manager: Task manager service
        """
        super().__init__(stdscr, "Today's Tasks")
        self.task_manager = task_manager
        self.selected_index = 0
        self.scroll_offset = 0
        self.message = ""

    def draw(self) -> None:
        """Draw the calendar view"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # Draw title
        self.draw_title()

        # Get tasks with due dates
        all_tasks = self.task_manager.list_tasks(sort="-priority")

        # Group by date bucket
        buckets = {
            "Overdue": [],
            "Today": [],
            "Tomorrow": [],
            "Next 7 days": [],
            "Later": [],
            "No due date": []
        }

        for task in all_tasks:
            if task.status.value == "done":
                continue  # Skip completed tasks
            bucket = group_by_date_bucket(task.due_date)
            buckets[bucket].append(task)

        # Calculate visible area
        list_start_y = 4
        list_height = height - 6

        # Flatten tasks for display
        display_items = []
        for bucket_name in ["Overdue", "Today", "Tomorrow", "Next 7 days", "Later", "No due date"]:
            tasks = buckets[bucket_name]
            if tasks:
                display_items.append(("header", bucket_name, len(tasks)))
                for task in tasks:
                    display_items.append(("task", task, None))

        # Draw task count
        total_tasks = sum(len(tasks) for tasks in buckets.values())
        try:
            count_text = f"Active tasks: {total_tasks}"
            self.stdscr.addstr(2, 2, count_text)
        except curses.error:
            pass

        # Adjust scroll
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + list_height:
            self.scroll_offset = self.selected_index - list_height + 1

        # Draw visible items
        for i in range(list_height):
            display_index = self.scroll_offset + i
            if display_index >= len(display_items):
                break

            item_type, item_data, extra = display_items[display_index]
            y = list_start_y + i

            if item_type == "header":
                # Draw bucket header
                header_text = f"▼ {item_data} ({extra})"
                try:
                    self.stdscr.addstr(y, 0, header_text, curses.A_BOLD)
                except curses.error:
                    pass

            elif item_type == "task":
                task = item_data
                attr = curses.A_REVERSE if display_index == self.selected_index else curses.A_NORMAL

                # Format: [status] title (due date)
                status_symbol = task.status.symbol
                due_text = format_relative_date(task.due_date) if task.due_date else ""

                max_title_len = width - 20
                title = task.title[:max_title_len] if len(task.title) > max_title_len else task.title

                task_line = f"  {status_symbol} {title}"
                if due_text:
                    task_line += f"  ({due_text})"

                try:
                    self.stdscr.addstr(y, 0, task_line[:width - 1].ljust(width - 1), attr)
                except curses.error:
                    pass

        # Draw status bar
        status_text = "d:Done  x:Delete  Tab:Tasks  1-6:Screens  q:Quit"
        if self.message:
            status_text = self.message
        self.draw_status_bar(status_text)

        self.stdscr.refresh()

    def handle_key(self, key: int) -> Optional[str]:
        """
        Handle keyboard input

        Args:
            key: Key code

        Returns:
            Action string or None
        """
        # Build display items (same as in draw)
        all_tasks = self.task_manager.list_tasks(sort="-priority")
        buckets = {
            "Overdue": [],
            "Today": [],
            "Tomorrow": [],
            "Next 7 days": [],
            "Later": [],
            "No due date": []
        }

        for task in all_tasks:
            if task.status.value == "done":
                continue
            bucket = group_by_date_bucket(task.due_date)
            buckets[bucket].append(task)

        display_items = []
        for bucket_name in ["Overdue", "Today", "Tomorrow", "Next 7 days", "Later", "No due date"]:
            tasks = buckets[bucket_name]
            if tasks:
                display_items.append(("header", bucket_name, len(tasks)))
                for task in tasks:
                    display_items.append(("task", task, None))

        # Navigation
        if key == curses.KEY_UP or key == ord('k'):
            if self.selected_index > 0:
                self.selected_index -= 1
                # Skip headers
                while self.selected_index > 0 and display_items[self.selected_index][0] == "header":
                    self.selected_index -= 1
                self.message = ""
            return None

        elif key == curses.KEY_DOWN or key == ord('j'):
            if self.selected_index < len(display_items) - 1:
                self.selected_index += 1
                # Skip headers
                while self.selected_index < len(display_items) - 1 and display_items[self.selected_index][0] == "header":
                    self.selected_index += 1
                self.message = ""
            return None

        # Toggle done
        elif key == ord('d') or key == ord('D'):
            if display_items and self.selected_index < len(display_items):
                item_type, item_data, _ = display_items[self.selected_index]
                if item_type == "task":
                    task = item_data
                    self.task_manager.toggle_done(task.id)
                    self.message = "Task marked done"
            return None

        # Delete task
        elif key == ord('x') or key == ord('X'):
            if display_items and self.selected_index < len(display_items):
                item_type, item_data, _ = display_items[self.selected_index]
                if item_type == "task":
                    task = item_data
                    self.task_manager.delete_task(task.id)
                    self.message = "Task deleted (undo with 'u')"
            return None

        # Screen navigation
        elif key == ord('1'):
            return "screen:tasks"
        elif key == ord('2'):
            return "screen:projects"
        elif key == ord('3'):
            return "screen:calendar"
        elif key == ord('4'):
            return "screen:tags"
        elif key == ord('5'):
            return "screen:stats"
        elif key == ord('6'):
            return "screen:settings"

        # Tab to tasks
        elif key == ord('\t') or key == 9:
            return "screen:tasks"

        # Quit
        elif key == ord('q') or key == ord('Q'):
            return "quit"

        return None


__all__ = ["CalendarScreen"]
