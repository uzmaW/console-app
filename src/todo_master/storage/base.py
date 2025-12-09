"""
Abstract storage interface and exceptions

Defines the contract for all storage implementations (FR-053 to FR-060).
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict
from uuid import UUID


# Generic entity type
T = TypeVar('T')


# Storage exceptions (T015)
class StorageError(Exception):
    """Base exception for storage operations"""
    pass


class NotFoundError(StorageError):
    """Entity not found in storage"""
    pass


class ValidationError(StorageError):
    """Entity data failed validation"""
    pass


class CorruptedDataError(StorageError):
    """Stored data is corrupted"""
    pass


# Abstract storage interface (T011)
class StorageInterface(Generic[T], ABC):
    """
    Abstract storage interface for CRUD operations

    Type parameter T represents the entity type (Task, Project, etc.)
    All storage implementations must implement this interface.
    """

    @abstractmethod
    def create(self, entity: T) -> T:
        """
        Create a new entity

        Args:
            entity: Entity to create (ID will be generated if not set)

        Returns:
            Created entity with generated ID

        Raises:
            ValidationError: If entity data is invalid
            StorageError: If persistence fails
        """
        pass

    @abstractmethod
    def read(self, id: UUID) -> Optional[T]:
        """
        Read entity by ID

        Args:
            id: UUID of entity to retrieve

        Returns:
            Entity if found, None otherwise

        Raises:
            StorageError: If read operation fails
        """
        pass

    @abstractmethod
    def update(self, id: UUID, changes: Dict) -> T:
        """
        Update entity with partial changes

        Args:
            id: UUID of entity to update
            changes: Dictionary of fields to update

        Returns:
            Updated entity

        Raises:
            NotFoundError: If entity with ID doesn't exist
            ValidationError: If changes are invalid
            StorageError: If update fails
        """
        pass

    @abstractmethod
    def delete(self, id: UUID) -> bool:
        """
        Delete entity by ID

        Args:
            id: UUID of entity to delete

        Returns:
            True if deleted, False if not found

        Raises:
            StorageError: If deletion fails
        """
        pass

    @abstractmethod
    def list(
        self,
        filter: Optional[Dict] = None,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[T]:
        """
        List entities with optional filtering and pagination

        Args:
            filter: Dictionary filter criteria (None = all entities)
            sort: Sort field name (prefix with '-' for descending)
            limit: Maximum number of results (None = unlimited)
            offset: Number of results to skip

        Returns:
            List of matching entities

        Raises:
            StorageError: If query fails

        Examples:
            # Get all tasks
            storage.list()

            # Get active tasks sorted by priority
            storage.list(filter={"status": "todo"}, sort="-priority")

            # Paginate results
            storage.list(limit=20, offset=40)
        """
        pass

    @abstractmethod
    def bulk_update(self, ids: List[UUID], changes: Dict) -> int:
        """
        Update multiple entities at once

        Args:
            ids: List of entity UUIDs to update
            changes: Dictionary of fields to update

        Returns:
            Number of entities updated

        Raises:
            ValidationError: If changes are invalid
            StorageError: If update fails
        """
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        fields: List[str],
        limit: Optional[int] = None
    ) -> List[T]:
        """
        Full-text search across specified fields

        Args:
            query: Search query string
            fields: List of field names to search
            limit: Maximum results (None = unlimited)

        Returns:
            List of matching entities, sorted by relevance

        Raises:
            StorageError: If search fails

        Examples:
            # Search tasks by title and description
            storage.search("authentication", fields=["title", "description"])
        """
        pass

    @abstractmethod
    def count(self, filter: Optional[Dict] = None) -> int:
        """
        Count entities matching filter

        Args:
            filter: Dictionary filter criteria (None = count all)

        Returns:
            Number of matching entities

        Raises:
            StorageError: If count fails
        """
        pass

    @abstractmethod
    def save(self) -> bool:
        """
        Persist all pending changes to storage

        Returns:
            True if save successful, False otherwise

        Raises:
            StorageError: If persistence fails

        Note:
            Implementation should be atomic (all or nothing)
        """
        pass

    @abstractmethod
    def load(self) -> bool:
        """
        Load data from storage into memory

        Returns:
            True if load successful, False otherwise

        Raises:
            StorageError: If load fails
            ValidationError: If stored data is invalid

        Note:
            Should attempt backup recovery if primary data is corrupted
        """
        pass

    @abstractmethod
    def backup(self) -> str:
        """
        Create backup of current data

        Returns:
            Path to created backup file

        Raises:
            StorageError: If backup creation fails
        """
        pass

    @abstractmethod
    def restore(self, backup_path: str) -> bool:
        """
        Restore data from backup file

        Args:
            backup_path: Path to backup file

        Returns:
            True if restore successful

        Raises:
            StorageError: If restore fails
            ValidationError: If backup data is invalid
        """
        pass


__all__ = [
    "StorageInterface",
    "StorageError",
    "NotFoundError",
    "ValidationError",
    "CorruptedDataError",
]
