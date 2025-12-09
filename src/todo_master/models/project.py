"""
Project model for task organization

Represents a project that can contain multiple tasks.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

from todo_master.models import ProjectColor
from todo_master.storage.base import ValidationError


# Default projects (FR-011)
DEFAULT_PROJECTS = [
    {
        "name": "Inbox",
        "color": ProjectColor.CYAN,
        "icon": "📥",
        "description": "Default project for new tasks",
    },
    {
        "name": "Personal",
        "color": ProjectColor.GREEN,
        "icon": "🏠",
        "description": "Personal tasks and goals",
    },
    {
        "name": "Work",
        "color": ProjectColor.BLUE,
        "icon": "💼",
        "description": "Work-related tasks",
    },
]


@dataclass
class Project:
    """
    Project entity for task organization (FR-011 to FR-018)

    Attributes:
        id: Unique identifier (auto-generated)
        name: Project name (3-50 chars, unique, required)
        description: Optional description
        color: Project color from predefined set
        icon: Emoji or icon character
        is_archived: Whether project is archived
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    # Core fields
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str = ""

    # Appearance
    color: ProjectColor = ProjectColor.CYAN
    icon: str = "📁"

    # Status
    is_archived: bool = False

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def validate(self) -> None:
        """
        Validate project data (FR-013)

        Raises:
            ValidationError: If validation fails
        """
        # Name validation (FR-013: 3-50 chars)
        if not self.name or len(self.name) < 3:
            raise ValidationError("Project name must be at least 3 characters")
        if len(self.name) > 50:
            raise ValidationError("Project name cannot exceed 50 characters")

        # Color validation
        if not isinstance(self.color, ProjectColor):
            raise ValidationError(f"Invalid color: {self.color}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert project to dictionary for JSON serialization

        Returns:
            Dictionary representation of project
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "color": self.color.value,
            "icon": self.icon,
            "is_archived": self.is_archived,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """
        Create project from dictionary

        Args:
            data: Dictionary with project data

        Returns:
            Project instance
        """
        project_id = UUID(data["id"]) if "id" in data else uuid4()
        created_at = datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now()
        updated_at = datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else datetime.now()

        return cls(
            id=project_id,
            name=data.get("name", ""),
            description=data.get("description", ""),
            color=ProjectColor(data.get("color", "cyan")),
            icon=data.get("icon", "📁"),
            is_archived=data.get("is_archived", False),
            created_at=created_at,
            updated_at=updated_at,
        )


def create_default_projects() -> list[Project]:
    """
    Create the default projects (FR-011)

    Returns:
        List of default Project instances
    """
    projects = []
    for default in DEFAULT_PROJECTS:
        project = Project(
            name=default["name"],
            color=default["color"],
            icon=default["icon"],
            description=default["description"],
        )
        projects.append(project)
    return projects


__all__ = ["Project", "DEFAULT_PROJECTS", "create_default_projects"]
