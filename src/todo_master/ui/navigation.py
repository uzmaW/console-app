"""
Navigation manager for screen switching

Manages screen lifecycle and transitions between different views.
"""

from typing import Dict, Optional
from todo_master.ui.screens.base import BaseScreen


class NavigationManager:
    """
    Manages screen navigation and lifecycle

    Handles screen registration, activation, and transitions.
    """

    def __init__(self):
        """Initialize navigation manager"""
        self.screens: Dict[str, BaseScreen] = {}
        self.current_screen: Optional[str] = None
        self.history: list[str] = []

    def register_screen(self, name: str, screen: BaseScreen):
        """
        Register a screen

        Args:
            name: Screen identifier
            screen: Screen instance
        """
        self.screens[name] = screen

    def navigate_to(self, screen_name: str):
        """
        Navigate to a screen

        Args:
            screen_name: Name of screen to navigate to

        Raises:
            KeyError: If screen name not registered
        """
        if screen_name not in self.screens:
            raise KeyError(f"Screen '{screen_name}' not registered")

        # Deactivate current screen
        if self.current_screen:
            self.screens[self.current_screen].deactivate()
            self.history.append(self.current_screen)

        # Activate new screen
        self.current_screen = screen_name
        self.screens[screen_name].activate()

    def go_back(self) -> bool:
        """
        Navigate to previous screen

        Returns:
            True if navigation successful, False if no history
        """
        if not self.history:
            return False

        previous = self.history.pop()
        self.navigate_to(previous)
        # Remove the duplicate entry that navigate_to added
        if self.history:
            self.history.pop()
        return True

    def get_current_screen(self) -> Optional[BaseScreen]:
        """
        Get current active screen

        Returns:
            Current screen instance or None
        """
        if self.current_screen:
            return self.screens[self.current_screen]
        return None


__all__ = ["NavigationManager"]
