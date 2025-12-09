"""
Simple input dialog for text entry

Provides a basic curses-based text input dialog.
"""

import curses


class InputDialog:
    """
    Simple text input dialog

    Shows a prompt and collects user input.
    """

    def __init__(self, stdscr, title: str, prompt: str, default: str = ""):
        """
        Initialize input dialog

        Args:
            stdscr: Main curses window
            title: Dialog title
            prompt: Input prompt text
            default: Default input value
        """
        self.stdscr = stdscr
        self.title = title
        self.prompt = prompt
        self.input_text = default
        self.cursor_pos = len(default)

    def show(self) -> str:
        """
        Show dialog and get input

        Returns:
            User input string (empty if cancelled)
        """
        curses.curs_set(1)  # Show cursor

        while True:
            self._draw()

            key = self.stdscr.getch()

            # Enter key - submit
            if key == ord('\n') or key == curses.KEY_ENTER or key == 10:
                curses.curs_set(0)
                return self.input_text

            # Escape or Ctrl+C - cancel
            elif key == 27 or key == 3:
                curses.curs_set(0)
                return ""

            # Backspace
            elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                if self.cursor_pos > 0:
                    self.input_text = (
                        self.input_text[:self.cursor_pos - 1] +
                        self.input_text[self.cursor_pos:]
                    )
                    self.cursor_pos -= 1

            # Delete
            elif key == curses.KEY_DC:
                if self.cursor_pos < len(self.input_text):
                    self.input_text = (
                        self.input_text[:self.cursor_pos] +
                        self.input_text[self.cursor_pos + 1:]
                    )

            # Arrow keys
            elif key == curses.KEY_LEFT:
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
            elif key == curses.KEY_RIGHT:
                if self.cursor_pos < len(self.input_text):
                    self.cursor_pos += 1
            elif key == curses.KEY_HOME:
                self.cursor_pos = 0
            elif key == curses.KEY_END:
                self.cursor_pos = len(self.input_text)

            # Regular character
            elif 32 <= key <= 126:
                char = chr(key)
                self.input_text = (
                    self.input_text[:self.cursor_pos] +
                    char +
                    self.input_text[self.cursor_pos:]
                )
                self.cursor_pos += 1

    def _draw(self):
        """Draw the dialog"""
        height, width = self.stdscr.getmaxyx()

        # Calculate dialog position and size
        dialog_width = min(60, width - 4)
        dialog_height = 7
        dialog_y = (height - dialog_height) // 2
        dialog_x = (width - dialog_width) // 2

        # Draw box
        try:
            for y in range(dialog_height):
                self.stdscr.addstr(
                    dialog_y + y,
                    dialog_x,
                    " " * dialog_width,
                    curses.A_REVERSE
                )

            # Draw title
            title_text = f" {self.title} "
            self.stdscr.addstr(
                dialog_y,
                dialog_x + (dialog_width - len(title_text)) // 2,
                title_text,
                curses.A_REVERSE | curses.A_BOLD
            )

            # Draw prompt
            self.stdscr.addstr(
                dialog_y + 2,
                dialog_x + 2,
                self.prompt,
                curses.A_REVERSE
            )

            # Draw input box
            input_y = dialog_y + 4
            input_x = dialog_x + 2
            input_width = dialog_width - 4

            # Draw input background
            self.stdscr.addstr(
                input_y,
                input_x,
                " " * input_width,
                curses.A_NORMAL
            )

            # Draw input text
            visible_text = self.input_text[:input_width - 1]
            self.stdscr.addstr(input_y, input_x, visible_text, curses.A_NORMAL)

            # Position cursor
            cursor_x = input_x + min(self.cursor_pos, input_width - 1)
            self.stdscr.move(input_y, cursor_x)

            # Draw help text
            help_text = "Enter:OK  Esc:Cancel"
            self.stdscr.addstr(
                dialog_y + dialog_height - 1,
                dialog_x + (dialog_width - len(help_text)) // 2,
                help_text,
                curses.A_REVERSE | curses.A_DIM
            )

        except curses.error:
            pass

        self.stdscr.refresh()


__all__ = ["InputDialog"]
