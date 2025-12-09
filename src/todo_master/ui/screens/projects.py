"""
Projects screen - view and manage task projects

Displays projects with task counts and allows filtering by project.
"""

import curses
from typing import Optional, Dict, List
from collections import Counter

from todo_master.ui.screens.base import BaseScreen
from todo_master.services.task_manager import TaskManager
from todo_master.services.project_manager import ProjectManager
from todo_master.ui.dialogs.input_dialog import InputDialog


class ProjectsScreen(BaseScreen):
    """
    Projects view screen (FR-012, T056-T058)

    Lists all projects with task counts and completion statistics.
    Supports creating, editing, and archiving projects.
    """

    def __init__(self, stdscr, task_manager: TaskManager, project_manager: ProjectManager):
        """
        Initialize projects screen

        Args:
            stdscr: Main curses window
            task_manager: Task manager service
            project_manager: Project manager service
        """
        super().__init__(stdscr, "Projects")
        self.task_manager = task_manager
        self.project_manager = project_manager
        self.selected_index = 0
        self.message = ""
        self.expanded_projects = set()  # Track which projects are expanded

    def draw(self) -> None:
        """Draw the projects list"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # Draw title
        self.draw_title()

        # Get projects from ProjectManager
        projects = self.project_manager.list_projects()

        # Draw project count
        try:
            count_text = f"Projects: {len(projects)}"
            self.stdscr.addstr(2, 2, count_text)
        except curses.error:
            pass

        # Calculate visible area
        list_start_y = 4
        list_height = height - 6

        # Draw projects
        for i in range(min(list_height, len(projects))):
            if i >= len(projects):
                break

            project = projects[i]
            y = list_start_y + i

            # Get statistics
            stats = self.project_manager.get_statistics(project.id, self.task_manager)

            # Highlight selected
            attr = curses.A_REVERSE if i == self.selected_index else curses.A_NORMAL

            # Format: icon name (5/10 - 50%)
            total = stats["total_tasks"]
            completed = stats["completed"]
            percentage = f"{int(stats['completion_rate'])}%"

            project_line = f" {project.icon} {project.name}  ({completed}/{total} - {percentage})"

            try:
                self.stdscr.addstr(y, 0, project_line[:width - 1].ljust(width - 1), attr)
            except curses.error:
                pass

        # Draw status bar
        status_text = "n:New  Enter:View  a:Archive  Tab:Tasks  q:Quit"
        if self.message:
            status_text = self.message
        self.draw_status_bar(status_text)

        self.stdscr.refresh()

    def handle_key(self, key: int) -> Optional[str]:
        """
        Handle keyboard input (T057)

        Args:
            key: Key code

        Returns:
            Action string or None
        """
        projects = self.project_manager.list_projects()

        # Navigation
        if key == curses.KEY_UP or key == ord('k'):
            if self.selected_index > 0:
                self.selected_index -= 1
                self.message = ""
            return None

        elif key == curses.KEY_DOWN or key == ord('j'):
            if self.selected_index < len(projects) - 1:
                self.selected_index += 1
                self.message = ""
            return None

        # New project (T057: 'n' key)
        elif key == ord('n') or key == ord('N'):
            dialog = InputDialog(self.stdscr, "New Project", "Project name:")
            name = dialog.show()
            if name:
                try:
                    project = self.project_manager.create_project(name=name)
                    self.message = f"Project created: {project.name}"
                except Exception as e:
                    self.message = f"Error: {str(e)}"
            return None

        # Archive project (T057: 'a' key)
        elif key == ord('a') or key == ord('A'):
            if projects and self.selected_index < len(projects):
                project = projects[self.selected_index]
                try:
                    self.project_manager.archive_project(project.id)
                    self.message = f"Project archived: {project.name}"
                except Exception as e:
                    self.message = f"Error: {str(e)}"
            return None

        # View project tasks (T058: Enter to expand/view)
        elif key == ord('\n') or key == curses.KEY_ENTER or key == 10:
            if projects and self.selected_index < len(projects):
                project = projects[self.selected_index]
                # Return action to switch to tasks filtered by project
                return f"view_project:{project.name}"
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


__all__ = ["ProjectsScreen"]
