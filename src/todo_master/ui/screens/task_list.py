"""
Task list screen - main view for todo items

Displays tasks and handles keyboard navigation for basic CRUD operations.
"""

import curses
from typing import List, Optional
from uuid import UUID

from todo_master.ui.screens.base import BaseScreen
from todo_master.ui.dialogs.input_dialog import InputDialog
from todo_master.models.task import Task
from todo_master.models import TaskStatus, Priority
from todo_master.services.task_manager import TaskManager


class TaskListScreen(BaseScreen):
    """
    Main task list view with keyboard navigation

    Handles basic operations: create, toggle done, delete, quit
    """

    def __init__(self, stdscr, task_manager: TaskManager, project_manager=None):
        """
        Initialize task list screen

        Args:
            stdscr: Main curses window
            task_manager: Task manager service
            project_manager: Optional project manager for filtering (T061)
        """
        super().__init__(stdscr, "Todo Master")
        self.task_manager = task_manager
        self.project_manager = project_manager
        self.selected_index = 0
        self.scroll_offset = 0
        self.message = ""
        self.project_filter = None  # Current project filter (T061)

    def draw(self) -> None:
        """Draw the task list"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # Draw title
        title = self.title
        if self.project_filter:
            title = f"{self.title} - {self.project_filter}"
        self.stdscr.addstr(0, (width - len(title)) // 2, f" {title} ", curses.A_BOLD)

        # Get tasks (apply project filter if set - T061)
        filter_dict = {"project": self.project_filter} if self.project_filter else None
        tasks = self.task_manager.list_tasks(filter=filter_dict, sort="-priority")

        # Draw task count
        try:
            count_text = f"Tasks: {len(tasks)}"
            self.stdscr.addstr(2, 2, count_text)
        except curses.error:
            pass

        # Calculate visible area
        list_start_y = 4
        list_height = height - 6  # Leave room for title, count, status bar

        # Adjust scroll if needed
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + list_height:
            self.scroll_offset = self.selected_index - list_height + 1

        # Draw visible tasks
        for i in range(list_height):
            task_index = self.scroll_offset + i
            if task_index >= len(tasks):
                break

            task = tasks[task_index]
            y = list_start_y + i

            # Highlight selected task
            attr = curses.A_REVERSE if task_index == self.selected_index else curses.A_NORMAL

            # Format task line: [status] priority title
            status_symbol = task.status.symbol
            priority_text = task.priority.value[0].upper()  # First letter

            # Truncate title to fit
            max_title_len = width - 15
            title = task.title[:max_title_len] if len(task.title) > max_title_len else task.title

            task_line = f" {status_symbol} [{priority_text}] {title}"

            try:
                self.stdscr.addstr(y, 0, task_line[:width - 1].ljust(width - 1), attr)
            except curses.error:
                pass

        # Draw status bar with keybindings
        status_text = "n:New  d:Done  x:Delete  p:Move  2:Projects  q:Quit"
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
        tasks = self.task_manager.list_tasks(sort="-priority")

        # Navigation
        if key == curses.KEY_UP or key == ord('k'):
            if self.selected_index > 0:
                self.selected_index -= 1
                self.message = ""
            return None

        elif key == curses.KEY_DOWN or key == ord('j'):
            if self.selected_index < len(tasks) - 1:
                self.selected_index += 1
                self.message = ""
            return None

        # New task
        elif key == ord('n') or key == ord('N'):
            dialog = InputDialog(self.stdscr, "New Task", "Task title:")
            title = dialog.show()
            if title:
                try:
                    # Create task with current project filter if set
                    project = self.project_filter if self.project_filter else "Inbox"
                    task = self.task_manager.create_task(title=title, project=project)
                    self.message = f"Task created in {project}: {task.title}"
                    self.selected_index = 0  # Jump to top
                except Exception as e:
                    self.message = f"Error: {str(e)}"
            return None

        # Toggle done
        elif key == ord('d') or key == ord('D'):
            if tasks and self.selected_index < len(tasks):
                task = tasks[self.selected_index]
                self.task_manager.toggle_done(task.id)
                self.message = f"Task marked {'done' if task.status == TaskStatus.TODO else 'not done'}"
            return None

        # Delete task
        elif key == ord('x') or key == ord('X'):
            if tasks and self.selected_index < len(tasks):
                task = tasks[self.selected_index]
                self.task_manager.delete_task(task.id)
                self.message = f"Task deleted (undo with 'u' within 5 seconds)"
                # Adjust selection if needed
                if self.selected_index >= len(self.task_manager.list_tasks()):
                    self.selected_index = max(0, self.selected_index - 1)
            return None

        # Undo delete
        elif key == ord('u') or key == ord('U'):
            restored = self.task_manager.undo_delete()
            if restored:
                self.message = f"Task restored: {restored.title}"
            else:
                self.message = "No task to undo"
            return None

        # Move to project (T062: 'p' key)
        elif key == ord('p') or key == ord('P'):
            if tasks and self.selected_index < len(tasks) and self.project_manager:
                task = tasks[self.selected_index]
                # Show project selection dialog
                dialog = InputDialog(self.stdscr, "Move to Project", "Project name:")
                project_name = dialog.show()
                if project_name:
                    try:
                        # Verify project exists
                        project = self.project_manager.get_by_name(project_name)
                        if project:
                            self.task_manager.update_task(task.id, project=project_name)
                            self.message = f"Task moved to {project_name}"
                        else:
                            self.message = f"Project '{project_name}' not found"
                    except Exception as e:
                        self.message = f"Error: {str(e)}"
            return None

        # Screen navigation
        elif key == ord('1'):
            return "screen:tasks"
        elif key == ord('2'):
            return "screen:projects"

        # Quit
        elif key == ord('q') or key == ord('Q'):
            return "quit"

        return None

    def set_project_filter(self, project_name: Optional[str]):
        """
        Set project filter (T061)

        Args:
            project_name: Project name to filter by, or None for all tasks
        """
        self.project_filter = project_name
        self.selected_index = 0
        self.scroll_offset = 0


__all__ = ["TaskListScreen"]
