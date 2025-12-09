# Storage API Contract

**Feature**: 002-todo-master-app
**Date**: 2025-12-09
**Phase**: Phase 1 - API Contracts

## Overview

This document defines the storage layer API contract for the Todo Master application. The storage layer provides a clean abstraction over data persistence, enabling future backend swaps without impacting business logic.

**Satisfies**: FR-053 to FR-060 (Data Persistence requirements)

---

## Storage Interface

### Base Storage Interface

All storage implementations must implement this abstract interface:

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Callable
from uuid import UUID

T = TypeVar('T')  # Generic entity type

class StorageInterface(Generic[T], ABC):
    """
    Abstract storage interface for CRUD operations

    Type parameter T represents the entity type (Task, Project, etc.)
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
```

---

## JSON File Storage Implementation

### JSONStorage Class

**File Structure** (FR-053, FR-054, FR-055):
```
~/.config/todo-master/
├── tasks.json          # Task storage
├── projects.json       # Project storage
├── settings.json       # Settings storage
├── backups/            # Automatic backups
│   ├── tasks.json.1    # Most recent backup
│   ├── tasks.json.2
│   ├── tasks.json.3
│   ├── tasks.json.4
│   └── tasks.json.5    # Oldest backup (FR-057: keep 5)
└── .lock               # File lock for concurrent access
```

### Implementation Contract

```python
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import json
import shutil
from filelock import FileLock

class JSONStorage(StorageInterface[T]):
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
        auto_save_interval: int = 5,  # FR-056: seconds
        backup_count: int = 5          # FR-057: number of backups
    ):
        """
        Initialize JSON storage

        Args:
            file_path: Path to JSON file
            entity_class: Entity class for serialization
            auto_save_interval: Auto-save interval in seconds
            backup_count: Number of backups to maintain
        """
        self.file_path = file_path
        self.entity_class = entity_class
        self.auto_save_interval = auto_save_interval
        self.backup_count = backup_count

        self.data: List[T] = []
        self.lock_file = file_path.parent / ".lock"
        self.last_save = datetime.now()

        # FR-060: Create directory if doesn't exist
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.backup_dir = self.file_path.parent / "backups"
        self.backup_dir.mkdir(exist_ok=True)

    def save(self) -> bool:
        """
        Save data to JSON file with atomic write

        Process:
        1. Create backup of existing file (FR-057)
        2. Serialize entities to JSON
        3. Write to temporary file
        4. Atomic rename temp -> target
        5. Rotate backups

        Returns:
            True if save successful
        """
        try:
            # 1. Create backup before save (FR-057)
            if self.file_path.exists():
                self.backup()

            # 2. Serialize data
            data_dict = {
                "version": "1.0",
                f"{self.entity_class.__name__.lower()}s": [
                    entity.to_dict() for entity in self.data
                ],
                "saved_at": datetime.now().isoformat()
            }

            # 3. Write to temp file
            temp_path = self.file_path.with_suffix('.tmp')
            with FileLock(self.lock_file):
                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(data_dict, f, indent=2, ensure_ascii=False)

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

        Returns:
            True if load successful
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
        self.data = []
        return False

    def _load_file(self, path: Path) -> bool:
        """Load and validate data from specific file"""
        with FileLock(self.lock_file):
            with open(path, 'r', encoding='utf-8') as f:
                data_dict = json.load(f)

        # Validate schema version
        version = data_dict.get("version", "1.0")
        if version != "1.0":
            data_dict = self._migrate(data_dict, version)

        # Deserialize entities
        entity_key = f"{self.entity_class.__name__.lower()}s"
        entity_dicts = data_dict.get(entity_key, [])

        self.data = []
        for entity_dict in entity_dicts:
            try:
                entity = self.entity_class.from_dict(entity_dict)
                self.data.append(entity)
            except Exception as e:
                print(f"Warning: Skipping invalid entity: {e}")

        return True

    def backup(self) -> str:
        """
        Create backup of current file (FR-057)

        Backups are named: <filename>.1, <filename>.2, etc.
        Most recent backup is .1, oldest is .<backup_count>

        Returns:
            Path to created backup file
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

    # CRUD operations implemented using self.data list
    # (create, read, update, delete, list, bulk_update, search, count)
    # Implementation details omitted for brevity
```

---

## Auto-Save Manager

### Auto-Save Contract

```python
import threading
from datetime import datetime, timedelta

class AutoSaveManager:
    """
    Manages automatic data persistence (FR-056)

    Monitors data changes and automatically saves after interval
    """

    def __init__(self, storage: StorageInterface, interval_seconds: int = 5):
        """
        Initialize auto-save manager

        Args:
            storage: Storage instance to save
            interval_seconds: Save interval (FR-056: default 5 seconds)
        """
        self.storage = storage
        self.interval = timedelta(seconds=interval_seconds)
        self.last_change = datetime.now()
        self.dirty = False
        self.running = False
        self.thread: Optional[threading.Thread] = None

    def mark_dirty(self):
        """Mark data as changed and needing save"""
        self.dirty = True
        self.last_change = datetime.now()

    def start(self):
        """Start auto-save background thread"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._auto_save_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop auto-save thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def force_save(self):
        """Force immediate save"""
        if self.dirty:
            self.storage.save()
            self.dirty = False

    def _auto_save_loop(self):
        """Background thread that saves at intervals"""
        import time

        while self.running:
            time.sleep(1.0)  # Check every second

            if not self.dirty:
                continue

            time_since_change = datetime.now() - self.last_change
            if time_since_change >= self.interval:
                try:
                    self.storage.save()
                    self.dirty = False
                except Exception as e:
                    print(f"Auto-save failed: {e}")
```

---

## Error Handling

### Storage Exceptions

```python
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
```

---

## Usage Examples

### Initializing Storage

```python
from pathlib import Path
from todo_master.models import Task
from todo_master.storage import JSONStorage, AutoSaveManager

# Initialize storage
storage_path = Path.home() / ".config" / "todo-master" / "tasks.json"
task_storage = JSONStorage(
    file_path=storage_path,
    entity_class=Task,
    auto_save_interval=5,  # FR-056
    backup_count=5         # FR-057
)

# Load existing data
task_storage.load()

# Setup auto-save
auto_save = AutoSaveManager(task_storage, interval_seconds=5)
auto_save.start()
```

### CRUD Operations

```python
# Create
new_task = Task(title="Fix authentication bug", priority=Priority.URGENT)
task_storage.create(new_task)
auto_save.mark_dirty()

# Read
task = task_storage.read(new_task.id)

# Update
task_storage.update(new_task.id, {"status": TaskStatus.DONE})
auto_save.mark_dirty()

# Delete
task_storage.delete(new_task.id)
auto_save.mark_dirty()

# List with filtering
active_tasks = task_storage.list(filter={"status": "todo"}, sort="-priority")

# Search
results = task_storage.search("authentication", fields=["title", "description"])

# Bulk update
task_storage.bulk_update(
    ids=[task1.id, task2.id, task3.id],
    changes={"project": "Work"}
)
auto_save.mark_dirty()
```

### Backup and Recovery

```python
# Manual backup
backup_path = task_storage.backup()
print(f"Backup created: {backup_path}")

# Force save
auto_save.force_save()

# Restore from backup
task_storage.restore(backup_path)
```

---

## Performance Requirements

### Performance Targets

| Operation | Target | Requirement |
|-----------|--------|-------------|
| Load (1000 tasks) | <1 second | SC-024 (startup time) |
| Save (1000 tasks) | <10ms | Constitution III |
| Create task | <5ms | Constitution III |
| Read task by ID | <1ms | O(1) lookup |
| List tasks (filtered) | <20ms | Constitution III |
| Search (500 tasks) | <1 second | SC-026 |
| Backup operation | <50ms | Non-blocking |

### Optimization Strategies

1. **In-memory operations**: All CRUD on in-memory data structure
2. **Lazy persistence**: Write to disk only when dirty
3. **Atomic writes**: Temp file + rename prevents corruption
4. **Indexed lookups**: UUID-based dictionary for O(1) reads
5. **Background auto-save**: Non-blocking persistence

---

## Testing Contract

### Required Test Coverage

```python
# Unit tests
def test_create_entity():
    """Test entity creation and ID generation"""

def test_read_existing_entity():
    """Test reading entity by ID"""

def test_read_nonexistent_entity():
    """Test reading non-existent entity returns None"""

def test_update_entity():
    """Test updating entity fields"""

def test_delete_entity():
    """Test deleting entity"""

def test_list_all_entities():
    """Test listing all entities"""

def test_list_with_filter():
    """Test filtering entities"""

def test_list_with_sort():
    """Test sorting entities"""

def test_search_entities():
    """Test full-text search"""

def test_bulk_update():
    """Test updating multiple entities"""

def test_atomic_save():
    """Test atomic write operation"""

def test_backup_creation():
    """Test backup file creation (FR-057)"""

def test_backup_rotation():
    """Test backup rotation (keep 5)"""

def test_corruption_recovery():
    """Test recovery from corrupted primary file"""

def test_auto_save_trigger():
    """Test auto-save after interval (FR-056)"""

# Integration tests
def test_save_and_load_cycle():
    """Test data persists across save/load cycle"""

def test_concurrent_access():
    """Test file locking prevents corruption"""

def test_backup_restore_cycle():
    """Test full backup and restore workflow"""
```

---

## Summary

This storage API contract provides:

- ✅ **Abstract interface** for future storage backends
- ✅ **JSON file implementation** satisfying FR-053 to FR-060
- ✅ **Atomic writes** preventing data corruption
- ✅ **Automatic backups** with rotation (FR-057)
- ✅ **Auto-save** every 5 seconds (FR-056)
- ✅ **Corruption recovery** from backups
- ✅ **Performance optimization** meeting Constitution III
- ✅ **Clear error handling** with typed exceptions
- ✅ **Comprehensive testing** requirements

**Next Steps**: Create `quickstart.md` with developer setup instructions
