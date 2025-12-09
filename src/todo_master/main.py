"""
Todo Master - Main entry point

Console-based todo application with keyboard-driven interface.
"""

import curses
import sys
from pathlib import Path

from todo_master.models.task import Task
from todo_master.models.project import Project
from todo_master.storage.json_store import JSONStorage
from todo_master.storage.auto_save import AutoSaveManager
from todo_master.services.task_manager import TaskManager
from todo_master.services.project_manager import ProjectManager
from todo_master.ui.screens.task_list import TaskListScreen
from todo_master.ui.screens.projects import ProjectsScreen
from todo_master.ui.navigation import NavigationManager
from todo_master.ui.theme import ThemeManager
from todo_master.utils.constants import CONFIG_DIR, TASKS_FILE

# Projects file path
PROJECTS_FILE = CONFIG_DIR / "projects.json"


class TodoMasterApp:
    """
    Main application controller

    Manages lifecycle, storage, and screen navigation.
    """

    def __init__(self, stdscr):
        """
        Initialize application

        Args:
            stdscr: Main curses window
        """
        self.stdscr = stdscr
        self.running = True

        # Setup curses
        curses.curs_set(0)  # Hide cursor by default
        self.stdscr.keypad(True)  # Enable special keys

        # Initialize theme
        self.theme = ThemeManager()
        self.theme.initialize()

        # Initialize storage (T063, T064)
        self._init_storage()

        # Initialize services
        self.task_manager = TaskManager(self.task_storage)
        self.project_manager = ProjectManager(self.project_storage)

        # Initialize auto-save for both storages
        self.task_auto_save = AutoSaveManager(self.task_storage, interval_seconds=5)
        self.task_auto_save.start()
        self.project_auto_save = AutoSaveManager(self.project_storage, interval_seconds=5)
        self.project_auto_save.start()

        # Initialize screens
        self.task_list_screen = TaskListScreen(
            self.stdscr,
            self.task_manager,
            self.project_manager
        )
        self.projects_screen = ProjectsScreen(
            self.stdscr,
            self.task_manager,
            self.project_manager
        )

        # Initialize navigation (T064)
        self.navigation = NavigationManager()
        self.navigation.register_screen("tasks", self.task_list_screen)
        self.navigation.register_screen("projects", self.projects_screen)
        self.navigation.navigate_to("tasks")  # Start on tasks screen

    def _init_storage(self):
        """Initialize storage for tasks and projects (T063)"""
        # Ensure config directory exists
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        # Create task storage
        self.task_storage = JSONStorage(TASKS_FILE, Task)
        try:
            self.task_storage.load()
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading tasks: {e}", file=sys.stderr)
            print("Starting with empty task list...", file=sys.stderr)

        # Create project storage (T063)
        self.project_storage = JSONStorage(PROJECTS_FILE, Project)
        try:
            self.project_storage.load()
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading projects: {e}", file=sys.stderr)
            print("Starting with default projects...", file=sys.stderr)

    def run(self):
        """
        Main event loop (T064)

        Handles screen drawing, keyboard input, and navigation.
        """
        try:
            while self.running:
                # Get current screen
                current_screen = self.navigation.get_current_screen()
                if not current_screen:
                    break

                # Draw screen
                current_screen.draw()

                # Get input
                key = self.stdscr.getch()

                # Handle input
                action = current_screen.handle_key(key)

                # Process actions (T064: screen navigation)
                if action == "quit":
                    self.running = False
                elif action and action.startswith("screen:"):
                    # Navigate to different screen
                    screen_name = action.split(":", 1)[1]
                    try:
                        self.navigation.navigate_to(screen_name)
                    except KeyError:
                        current_screen.message = f"Screen '{screen_name}' not available"
                elif action and action.startswith("view_project:"):
                    # Filter tasks by project
                    project_name = action.split(":", 1)[1]
                    self.task_list_screen.set_project_filter(project_name)
                    self.navigation.navigate_to("tasks")

                # Mark storages as dirty after any key (auto-save will handle it)
                self.task_auto_save.mark_dirty()
                self.project_auto_save.mark_dirty()

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            pass

        finally:
            # Cleanup
            self._cleanup()

    def _cleanup(self):
        """Cleanup resources before exit"""
        # Stop auto-save for both storages
        self.task_auto_save.stop()
        self.project_auto_save.stop()

        # Save any pending changes
        try:
            self.task_storage.save()
        except Exception as e:
            print(f"Error saving tasks: {e}", file=sys.stderr)

        try:
            self.project_storage.save()
        except Exception as e:
            print(f"Error saving projects: {e}", file=sys.stderr)


def main():
    """
    Application entry point

    Initializes curses and runs the application.
    """
    try:
        curses.wrapper(lambda stdscr: TodoMasterApp(stdscr).run())
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


__all__ = ["TodoMasterApp", "main"]
