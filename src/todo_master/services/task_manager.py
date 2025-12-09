"""
Task management service

Handles CRUD operations and business logic for tasks.
"""

from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime, timedelta

from todo_master.models.task import Task
from todo_master.models import TaskStatus, Priority
from todo_master.storage.json_store import JSONStorage
from todo_master.storage.base import NotFoundError, ValidationError
from todo_master.utils.constants import TASKS_FILE, UNDO_TIMEOUT_SECONDS


class TaskManager:
    """
    Manages task operations (FR-001 to FR-010)

    Provides CRUD operations, validation, and undo functionality.
    """

    def __init__(self, storage: JSONStorage):
        """
        Initialize task manager

        Args:
            storage: Storage instance for tasks
        """
        self.storage = storage
        self.undo_buffer: List[tuple] = []  # (timestamp, task)

    def create_task(self, title: str, **kwargs) -> Task:
        """
        Create a new task (FR-001, FR-010)

        Args:
            title: Task title (required)
            **kwargs: Additional task attributes

        Returns:
            Created task

        Raises:
            ValidationError: If task data is invalid
        """
        task = Task(title=title, **kwargs)
        task.validate()
        return self.storage.create(task)

    def get_task(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID"""
        return self.storage.read(task_id)

    def update_task(self, task_id: UUID, **changes) -> Task:
        """
        Update task with changes

        Args:
            task_id: Task UUID
            **changes: Fields to update

        Returns:
            Updated task

        Raises:
            NotFoundError: If task doesn't exist
            ValidationError: If changes are invalid
        """
        changes["updated_at"] = datetime.now()
        return self.storage.update(task_id, changes)

    def delete_task(self, task_id: UUID) -> bool:
        """
        Delete task with undo buffer (FR-006, FR-007)

        Args:
            task_id: Task UUID

        Returns:
            True if deleted

        Raises:
            NotFoundError: If task doesn't exist
        """
        task = self.get_task(task_id)
        if task:
            # Add to undo buffer
            self.undo_buffer.append((datetime.now(), task))
            # Clean old undo entries
            self._clean_undo_buffer()

        return self.storage.delete(task_id)

    def undo_delete(self) -> Optional[Task]:
        """
        Undo last delete within timeout window (FR-007)

        Returns:
            Restored task or None if no undo available
        """
        self._clean_undo_buffer()

        if not self.undo_buffer:
            return None

        timestamp, task = self.undo_buffer.pop()
        return self.storage.create(task)

    def mark_done(self, task_id: UUID) -> Task:
        """
        Mark task as done (FR-004, FR-005)

        Args:
            task_id: Task UUID

        Returns:
            Updated task
        """
        task = self.get_task(task_id)
        if task:
            task.mark_done()
            self.storage.update(task_id, {
                "status": task.status,
                "completed_at": task.completed_at,
                "updated_at": task.updated_at,
            })
        return task

    def toggle_done(self, task_id: UUID) -> Task:
        """Toggle task completion status"""
        task = self.get_task(task_id)
        if task:
            task.toggle_done()
            self.storage.update(task_id, {
                "status": task.status,
                "completed_at": task.completed_at,
                "updated_at": task.updated_at,
            })
        return task

    def list_tasks(self, filter: Optional[Dict] = None, sort: str = "-priority") -> List[Task]:
        """
        List tasks with optional filtering and sorting

        Args:
            filter: Filter criteria
            sort: Sort field (prefix with - for descending)

        Returns:
            List of tasks
        """
        return self.storage.list(filter=filter, sort=sort)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.storage.list()

    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by title and description

        Args:
            query: Search query

        Returns:
            List of matching tasks
        """
        return self.storage.search(query, fields=["title", "description"])

    def _clean_undo_buffer(self):
        """Remove undo entries older than timeout"""
        cutoff = datetime.now() - timedelta(seconds=UNDO_TIMEOUT_SECONDS)
        self.undo_buffer = [
            (ts, task) for ts, task in self.undo_buffer
            if ts > cutoff
        ]


__all__ = ["TaskManager"]
