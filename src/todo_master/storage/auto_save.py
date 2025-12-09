"""
Automatic save management

Monitors data changes and automatically persists after configured interval (FR-056).
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Optional

from todo_master.storage.base import StorageInterface


class AutoSaveManager:
    """
    Manages automatic data persistence (FR-056)

    Monitors data changes and automatically saves after interval (default 5 seconds).
    Runs in background thread to avoid blocking main application.
    """

    def __init__(self, storage: StorageInterface, interval_seconds: int = 5):
        """
        Initialize auto-save manager

        Args:
            storage: Storage instance to save
            interval_seconds: Save interval in seconds (FR-056: default 5)
        """
        self.storage = storage
        self.interval = timedelta(seconds=interval_seconds)
        self.last_change = datetime.now()
        self.dirty = False
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    def mark_dirty(self):
        """
        Mark data as changed and needing save

        Call this method after any data modification to trigger auto-save.
        """
        with self._lock:
            self.dirty = True
            self.last_change = datetime.now()

    def is_dirty(self) -> bool:
        """Check if there are unsaved changes"""
        with self._lock:
            return self.dirty

    def start(self):
        """
        Start auto-save background thread

        The thread will check for changes every second and save if:
        1. Data is marked as dirty
        2. Sufficient time has passed since last change
        """
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._auto_save_loop, daemon=True)
        self.thread.start()

    def stop(self, force_save: bool = True):
        """
        Stop auto-save thread

        Args:
            force_save: If True, save any pending changes before stopping
        """
        self.running = False

        if force_save and self.dirty:
            self.force_save()

        if self.thread:
            self.thread.join(timeout=2.0)

    def force_save(self):
        """
        Force immediate save regardless of interval

        Useful for explicit save operations (e.g., on quit, settings change)
        """
        with self._lock:
            if self.dirty:
                try:
                    self.storage.save()
                    self.dirty = False
                except Exception as e:
                    print(f"Force save failed: {e}")

    def _auto_save_loop(self):
        """
        Background thread that saves at intervals

        Checks every second if:
        1. Data is dirty (has changes)
        2. Enough time has passed since last change
        """
        while self.running:
            time.sleep(1.0)  # Check every second

            with self._lock:
                if not self.dirty:
                    continue

                time_since_change = datetime.now() - self.last_change
                if time_since_change >= self.interval:
                    try:
                        self.storage.save()
                        self.dirty = False
                    except Exception as e:
                        # Don't crash on save error, just log and continue
                        print(f"Auto-save failed: {e}")

    def reset_timer(self):
        """Reset the auto-save timer (useful after manual save)"""
        with self._lock:
            self.last_change = datetime.now()

    def get_time_until_save(self) -> float:
        """
        Get time remaining until next auto-save

        Returns:
            Seconds until next save, or -1 if no pending changes
        """
        with self._lock:
            if not self.dirty:
                return -1.0

            elapsed = datetime.now() - self.last_change
            remaining = self.interval - elapsed

            return max(0.0, remaining.total_seconds())


__all__ = ["AutoSaveManager"]
