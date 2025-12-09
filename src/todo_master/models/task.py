"""
Task model for todo items
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4

from todo_master.models import TaskStatus, Priority
from todo_master.storage.base import ValidationError


@dataclass
class Task:
    """
    Task entity representing a todo item (FR-001 to FR-010)

    Attributes:
        id: Unique identifier (auto-generated)
        title: Task title (1-200 chars, required)
        description: Optional description
        status: Task status (todo/in_progress/done/archived)
        priority: Priority level (low/medium/high/urgent)
        project: Project name (default: "Inbox")
        tags: List of tag names
        due_date: Optional due date
        created_at: Creation timestamp
        updated_at: Last update timestamp
        completed_at: Completion timestamp (set when marked done)
        estimated_time: Estimated time in minutes
        actual_time: Actual time spent in minutes
        parent_id: Parent task ID for subtasks
        position: Display order position
    """

    # Core fields
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    description: str = ""

    # Status and priority
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM

    # Organization
    project: str = "Inbox"
    tags: List[str] = field(default_factory=list)

    # Dates
    due_date: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    # Time tracking
    estimated_time: Optional[int] = None  # minutes
    actual_time: Optional[int] = None  # minutes

    # Hierarchy
    parent_id: Optional[UUID] = None
    position: int = 0

    def validate(self) -> None:
        """
        Validate task data (FR-002)

        Raises:
            ValidationError: If validation fails
        """
        # Title validation (FR-002: 1-200 chars)
        if not self.title or len(self.title) == 0:
            raise ValidationError("Task title cannot be empty")
        if len(self.title) > 200:
            raise ValidationError("Task title cannot exceed 200 characters")

        # Status validation
        if not isinstance(self.status, TaskStatus):
            raise ValidationError(f"Invalid status: {self.status}")

        # Priority validation
        if not isinstance(self.priority, Priority):
            raise ValidationError(f"Invalid priority: {self.priority}")

    def mark_done(self) -> None:
        """
        Mark task as completed (FR-004, FR-005)

        Sets status to DONE and records completion timestamp.
        """
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()

    def mark_undone(self) -> None:
        """Mark task as not completed"""
        self.status = TaskStatus.TODO
        self.completed_at = None
        self.updated_at = datetime.now()

    def toggle_done(self) -> None:
        """Toggle completion status"""
        if self.status == TaskStatus.DONE:
            self.mark_undone()
        else:
            self.mark_done()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert task to dictionary for JSON serialization

        Returns:
            Dictionary representation of task
        """
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "project": self.project,
            "tags": self.tags,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "estimated_time": self.estimated_time,
            "actual_time": self.actual_time,
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "position": self.position,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """
        Create task from dictionary

        Args:
            data: Dictionary with task data

        Returns:
            Task instance
        """
        # Parse UUID
        task_id = UUID(data["id"]) if "id" in data else uuid4()

        # Parse dates
        due_date = None
        if data.get("due_date"):
            due_date = date.fromisoformat(data["due_date"])

        created_at = datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now()
        updated_at = datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else datetime.now()

        completed_at = None
        if data.get("completed_at"):
            completed_at = datetime.fromisoformat(data["completed_at"])

        parent_id = None
        if data.get("parent_id"):
            parent_id = UUID(data["parent_id"])

        return cls(
            id=task_id,
            title=data.get("title", ""),
            description=data.get("description", ""),
            status=TaskStatus(data.get("status", "todo")),
            priority=Priority(data.get("priority", "medium")),
            project=data.get("project", "Inbox"),
            tags=data.get("tags", []),
            due_date=due_date,
            created_at=created_at,
            updated_at=updated_at,
            completed_at=completed_at,
            estimated_time=data.get("estimated_time"),
            actual_time=data.get("actual_time"),
            parent_id=parent_id,
            position=data.get("position", 0),
        )


__all__ = ["Task"]
