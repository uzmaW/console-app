"""
Storage layer for Todo Master application

Provides abstract storage interface and JSON-based implementation with
automatic backups and auto-save functionality.
"""

from todo_master.storage.base import (
    StorageInterface,
    StorageError,
    NotFoundError,
    ValidationError,
)
from todo_master.storage.json_store import JSONStorage
from todo_master.storage.backup import BackupManager
from todo_master.storage.auto_save import AutoSaveManager

__all__ = [
    "StorageInterface",
    "StorageError",
    "NotFoundError",
    "ValidationError",
    "JSONStorage",
    "BackupManager",
    "AutoSaveManager",
]
