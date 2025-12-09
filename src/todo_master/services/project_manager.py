"""
Project management service

Handles CRUD operations and business logic for projects.
"""

from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime

from todo_master.models.project import Project, create_default_projects
from todo_master.storage.json_store import JSONStorage
from todo_master.storage.base import NotFoundError, ValidationError


class ProjectManager:
    """
    Manages project operations (FR-011 to FR-018)

    Provides CRUD operations, validation, and statistics.
    """

    def __init__(self, storage: JSONStorage):
        """
        Initialize project manager

        Args:
            storage: Storage instance for projects
        """
        self.storage = storage
        self._ensure_defaults()

    def _ensure_defaults(self):
        """Ensure default projects exist (FR-011)"""
        existing = self.storage.list()
        if not existing:
            # Create default projects
            for project in create_default_projects():
                self.storage.create(project)

    def create_project(self, name: str, **kwargs) -> Project:
        """
        Create a new project (FR-012, FR-013)

        Args:
            name: Project name (required, must be unique)
            **kwargs: Additional project attributes

        Returns:
            Created project

        Raises:
            ValidationError: If project data is invalid or name not unique
        """
        # Check name uniqueness (FR-012)
        existing = self.get_by_name(name)
        if existing:
            raise ValidationError(f"Project '{name}' already exists")

        project = Project(name=name, **kwargs)
        project.validate()
        return self.storage.create(project)

    def get_project(self, project_id: UUID) -> Optional[Project]:
        """Get project by ID"""
        return self.storage.read(project_id)

    def get_by_name(self, name: str) -> Optional[Project]:
        """
        Get project by name

        Args:
            name: Project name

        Returns:
            Project or None if not found
        """
        projects = self.storage.list(filter={"name": name})
        return projects[0] if projects else None

    def update_project(self, project_id: UUID, **changes) -> Project:
        """
        Update project with changes

        Args:
            project_id: Project UUID
            **changes: Fields to update

        Returns:
            Updated project

        Raises:
            NotFoundError: If project doesn't exist
            ValidationError: If changes are invalid or name not unique
        """
        # Check name uniqueness if changing name
        if "name" in changes:
            existing = self.get_by_name(changes["name"])
            if existing and existing.id != project_id:
                raise ValidationError(f"Project '{changes['name']}' already exists")

        changes["updated_at"] = datetime.now()
        return self.storage.update(project_id, changes)

    def archive_project(self, project_id: UUID) -> Project:
        """
        Archive project (FR-017)

        Args:
            project_id: Project UUID

        Returns:
            Updated project

        Raises:
            NotFoundError: If project doesn't exist
        """
        return self.update_project(project_id, is_archived=True)

    def unarchive_project(self, project_id: UUID) -> Project:
        """
        Unarchive project

        Args:
            project_id: Project UUID

        Returns:
            Updated project
        """
        return self.update_project(project_id, is_archived=False)

    def delete_project(self, project_id: UUID, task_manager=None) -> bool:
        """
        Delete project (FR-018)

        Note: Caller must handle moving active tasks to Inbox before deletion.
        This is enforced at the UI level.

        Args:
            project_id: Project UUID
            task_manager: Optional TaskManager to check for active tasks

        Returns:
            True if deleted

        Raises:
            NotFoundError: If project doesn't exist
            ValidationError: If project has active tasks
        """
        project = self.get_project(project_id)
        if not project:
            raise NotFoundError(f"Project {project_id} not found")

        # Check for active tasks if task_manager provided
        if task_manager:
            tasks = task_manager.list_tasks(filter={"project": project.name})
            if tasks:
                raise ValidationError(
                    f"Cannot delete project '{project.name}' - it has {len(tasks)} active tasks. "
                    "Move tasks to another project first."
                )

        return self.storage.delete(project_id)

    def list_projects(self, include_archived: bool = False) -> List[Project]:
        """
        List projects

        Args:
            include_archived: Whether to include archived projects

        Returns:
            List of projects
        """
        projects = self.storage.list()
        if not include_archived:
            projects = [p for p in projects if not p.is_archived]
        return sorted(projects, key=lambda p: p.name.lower())

    def get_statistics(self, project_id: UUID, task_manager) -> Dict:
        """
        Get project statistics (FR-016)

        Args:
            project_id: Project UUID
            task_manager: TaskManager instance to query tasks

        Returns:
            Dictionary with statistics
        """
        project = self.get_project(project_id)
        if not project:
            raise NotFoundError(f"Project {project_id} not found")

        tasks = task_manager.list_tasks(filter={"project": project.name})

        total = len(tasks)
        completed = sum(1 for task in tasks if task.status.value == "done")
        in_progress = sum(1 for task in tasks if task.status.value == "in_progress")
        todo = sum(1 for task in tasks if task.status.value == "todo")

        return {
            "project_name": project.name,
            "total_tasks": total,
            "completed": completed,
            "in_progress": in_progress,
            "todo": todo,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
        }

    def get_all_statistics(self, task_manager) -> List[Dict]:
        """
        Get statistics for all projects

        Args:
            task_manager: TaskManager instance

        Returns:
            List of statistics dictionaries
        """
        stats = []
        for project in self.list_projects():
            stats.append(self.get_statistics(project.id, task_manager))
        return stats


__all__ = ["ProjectManager"]
