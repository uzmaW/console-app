"""
JSON file-based storage implementation

Provides persistent storage using JSON files with atomic writes,
automatic backups, and corruption recovery (FR-053 to FR-060).
"""

import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional, TypeVar, Generic, Callable, Any
from uuid import UUID
from datetime import datetime
from filelock import FileLock

from todo_master.storage.base import (
    StorageInterface,
    StorageError,
    NotFoundError,
    ValidationError,
    CorruptedDataError,
)

T = TypeVar('T')


class JSONStorage(StorageInterface[T], Generic[T]):
    """
    JSON file-based storage implementation

    Features:
    - Atomic writes via temp file + rename (FR-056)
    - Automatic backups before writes (FR-057)
    - Backup rotation (keep 5 most recent)
    - Schema validation on load
    - Corruption recovery from backups
    """

    def __init__(
        self,
        file_path: Path,
        entity_class: type,
        backup_count: int = 5
    ):
        """
        Initialize JSON storage

        Args:
            file_path: Path to JSON file
            entity_class: Entity class for serialization
            backup_count: Number of backups to maintain (FR-057)
        """
        self.file_path = file_path
        self.entity_class = entity_class
        self.backup_count = backup_count

        self.data: Dict[UUID, T] = {}  # In-memory storage indexed by ID
        self.lock_file = file_path.parent / ".lock"
        self.last_save = datetime.now()

        # FR-060: Create directory if doesn't exist
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.backup_dir = self.file_path.parent / "backups"
        self.backup_dir.mkdir(exist_ok=True)

    def create(self, entity: T) -> T:
        """Create new entity with auto-generated ID if needed"""
        # Generate UUID if not set
        if not hasattr(entity, 'id') or entity.id is None:
            from uuid import uuid4
            entity.id = uuid4()

        # Validate entity
        if hasattr(entity, 'validate'):
            entity.validate()

        # Store in memory
        self.data[entity.id] = entity
        return entity

    def read(self, id: UUID) -> Optional[T]:
        """Read entity by ID (O(1) lookup)"""
        return self.data.get(id)

    def update(self, id: UUID, changes: Dict) -> T:
        """Update entity with partial changes"""
        entity = self.data.get(id)
        if entity is None:
            raise NotFoundError(f"Entity with ID {id} not found")

        # Apply changes
        for key, value in changes.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        # Update timestamp if available
        if hasattr(entity, 'updated_at'):
            entity.updated_at = datetime.now()

        # Validate after changes
        if hasattr(entity, 'validate'):
            entity.validate()

        return entity

    def delete(self, id: UUID) -> bool:
        """Delete entity by ID"""
        if id in self.data:
            del self.data[id]
            return True
        return False

    def list(
        self,
        filter: Optional[Dict] = None,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[T]:
        """List entities with filtering, sorting, and pagination"""
        entities = list(self.data.values())

        # Apply filter
        if filter:
            entities = [e for e in entities if self._matches_filter(e, filter)]

        # Apply sort
        if sort:
            reverse = sort.startswith('-')
            sort_field = sort.lstrip('-')
            entities.sort(
                key=lambda e: getattr(e, sort_field, None) or "",
                reverse=reverse
            )

        # Apply pagination
        if offset:
            entities = entities[offset:]
        if limit:
            entities = entities[:limit]

        return entities

    def bulk_update(self, ids: List[UUID], changes: Dict) -> int:
        """Update multiple entities at once"""
        count = 0
        for id in ids:
            try:
                self.update(id, changes)
                count += 1
            except NotFoundError:
                continue
        return count

    def search(
        self,
        query: str,
        fields: List[str],
        limit: Optional[int] = None
    ) -> List[T]:
        """Full-text search across specified fields"""
        query_lower = query.lower()
        results = []

        for entity in self.data.values():
            # Check if query matches any field
            for field in fields:
                value = getattr(entity, field, None)
                if value and query_lower in str(value).lower():
                    results.append(entity)
                    break

        if limit:
            results = results[:limit]

        return results

    def count(self, filter: Optional[Dict] = None) -> int:
        """Count entities matching filter"""
        if not filter:
            return len(self.data)

        return len([e for e in self.data.values() if self._matches_filter(e, filter)])

    def save(self) -> bool:
        """
        Save data to JSON file with atomic write (FR-056)

        Process:
        1. Create backup of existing file (FR-057)
        2. Serialize entities to JSON
        3. Write to temporary file
        4. Atomic rename temp -> target
        5. Rotate backups
        """
        try:
            # 1. Create backup before save (FR-057)
            if self.file_path.exists():
                self.backup()

            # 2. Serialize data
            data_dict = {
                "version": "1.0",
                f"{self.entity_class.__name__.lower()}s": [
                    entity.to_dict() if hasattr(entity, 'to_dict') else vars(entity)
                    for entity in self.data.values()
                ],
                "saved_at": datetime.now().isoformat()
            }

            # 3. Write to temp file
            temp_path = self.file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=2, ensure_ascii=False, default=str)

            # 4. Atomic rename (POSIX guarantees atomicity)
            temp_path.replace(self.file_path)

            # 5. Rotate backups
            self._rotate_backups()

            self.last_save = datetime.now()
            return True

        except Exception as e:
            raise StorageError(f"Failed to save {self.file_path}: {e}")

    def load(self) -> bool:
        """
        Load data from JSON file with backup recovery

        Process:
        1. Attempt to load primary file
        2. If corrupted, try backups in order
        3. Validate schema version
        4. Deserialize entities
        """
        # Try primary file first
        if self.file_path.exists():
            try:
                return self._load_file(self.file_path)
            except (json.JSONDecodeError, ValidationError) as e:
                print(f"Warning: Primary file corrupted: {e}")

        # Try backups in order (most recent first)
        for i in range(1, self.backup_count + 1):
            backup_path = self.backup_dir / f"{self.file_path.name}.{i}"
            if backup_path.exists():
                try:
                    print(f"Attempting recovery from backup {i}...")
                    if self._load_file(backup_path):
                        # Restore successful, save as primary
                        self.save()
                        return True
                except Exception:
                    continue

        # No valid data found, start fresh
        self.data = {}
        return False

    def backup(self) -> str:
        """
        Create backup of current file (FR-057)

        Backups are named: <filename>.1, <filename>.2, etc.
        Most recent backup is .1, oldest is .<backup_count>
        """
        if not self.file_path.exists():
            return ""

        # Shift existing backups
        for i in range(self.backup_count - 1, 0, -1):
            old_backup = self.backup_dir / f"{self.file_path.name}.{i}"
            new_backup = self.backup_dir / f"{self.file_path.name}.{i + 1}"
            if old_backup.exists():
                shutil.move(str(old_backup), str(new_backup))

        # Create new backup at position 1
        backup_path = self.backup_dir / f"{self.file_path.name}.1"
        shutil.copy2(self.file_path, backup_path)

        return str(backup_path)

    def restore(self, backup_path: str) -> bool:
        """Restore data from backup file"""
        backup_path_obj = Path(backup_path)
        if not backup_path_obj.exists():
            raise StorageError(f"Backup file not found: {backup_path}")

        try:
            # Load from backup
            if self._load_file(backup_path_obj):
                # Save as primary
                self.save()
                return True
        except Exception as e:
            raise StorageError(f"Failed to restore from backup: {e}")

        return False

    def _load_file(self, path: Path) -> bool:
        """Load and validate data from specific file"""
        with open(path, 'r', encoding='utf-8') as f:
            data_dict = json.load(f)

        # Validate schema version
        version = data_dict.get("version", "1.0")
        if version != "1.0":
            data_dict = self._migrate(data_dict, version)

        # Deserialize entities
        entity_key = f"{self.entity_class.__name__.lower()}s"
        entity_dicts = data_dict.get(entity_key, [])

        self.data = {}
        for entity_dict in entity_dicts:
            try:
                # Use from_dict if available, otherwise create directly
                if hasattr(self.entity_class, 'from_dict'):
                    entity = self.entity_class.from_dict(entity_dict)
                else:
                    entity = self.entity_class(**entity_dict)

                self.data[entity.id] = entity
            except Exception as e:
                print(f"Warning: Skipping invalid entity: {e}")

        return True

    def _rotate_backups(self):
        """Remove backups beyond backup_count limit"""
        for i in range(self.backup_count + 1, self.backup_count + 10):
            old_backup = self.backup_dir / f"{self.file_path.name}.{i}"
            if old_backup.exists():
                old_backup.unlink()

    def _migrate(self, data: dict, from_version: str) -> dict:
        """Migrate data from older schema version"""
        # Future migrations would go here
        return data

    def _matches_filter(self, entity: T, filter: Dict) -> bool:
        """Check if entity matches filter criteria"""
        for key, value in filter.items():
            entity_value = getattr(entity, key, None)

            # Handle special cases
            if isinstance(value, list):
                if entity_value not in value:
                    return False
            elif entity_value != value:
                return False

        return True


__all__ = ["JSONStorage"]
