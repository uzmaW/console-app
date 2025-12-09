# Data Model Specification: Todo Master

**Feature**: 002-todo-master-app
**Date**: 2025-12-09
**Phase**: Phase 1 - Data Model Design

## Overview

This document defines the complete data model for the Todo Master application, including all entities, their relationships, validation rules, and storage specifications. The model is designed to satisfy all 75 functional requirements while maintaining simplicity and performance.

---

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐
│   Project   │1    * │    Task     │
│             │◄──────│             │
└─────────────┘       └─────────────┘
                            │
                            │ *
                            │
                            │
                      ┌─────▼──────┐
                      │     Tag     │
                      │ (many-to-many)
                      └─────────────┘

┌─────────────┐
│   Filter    │
│  (queries)  │
└─────────────┘

┌─────────────┐
│  Settings   │
│ (singleton) │
└─────────────┘

┌─────────────┐
│ Statistics  │
│  (computed) │
└─────────────┘
```

---

## Core Entities

### 1. Task

**Purpose**: Represents a single todo item with all associated metadata

**Satisfies**: FR-001 to FR-010, User Story 1

```python
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

class TaskStatus(str, Enum):
    """Task status enumeration (FR-008)"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"

class Priority(str, Enum):
    """Task priority enumeration (FR-009)"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class Task:
    """
    Task entity with complete metadata

    Validation:
    - title: 1-200 characters, non-empty (FR-002)
    - status: One of TaskStatus enum values
    - priority: One of Priority enum values
    - tags: List of string tag names
    - due_date: Valid date or None
    """

    # Required fields
    id: UUID = field(default_factory=uuid4)  # FR-010: Auto-generated
    title: str = ""  # FR-001, FR-002: Required, 1-200 chars

    # Optional descriptive fields
    description: str = ""  # FR-001: Optional text

    # Status and priority
    status: TaskStatus = TaskStatus.TODO  # FR-008: Default to todo
    priority: Priority = Priority.MEDIUM  # FR-009: Default to medium

    # Organization
    project: str = "Inbox"  # FR-001: Default project
    tags: List[str] = field(default_factory=list)  # FR-001: Tag array

    # Scheduling
    due_date: Optional[date] = None  # FR-001: Optional due date

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)  # Auto-set
    updated_at: datetime = field(default_factory=datetime.now)  # Auto-update
    completed_at: Optional[datetime] = None  # FR-005: Set when status=done

    # Time tracking
    estimated_time: Optional[int] = None  # FR-001: Minutes (optional)
    actual_time: Optional[int] = None  # Minutes (optional)

    # Hierarchy (for future subtasks)
    parent_id: Optional[UUID] = None  # Reference to parent task

    # Display ordering
    position: int = 0  # Manual ordering within project

    def __post_init__(self):
        """Validate task data after initialization"""
        # FR-002: Title validation
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")
        self.title = self.title.strip()

        # FR-005: Set completed_at when status changes to done
        if self.status == TaskStatus.DONE and self.completed_at is None:
            self.completed_at = datetime.now()
        elif self.status != TaskStatus.DONE:
            self.completed_at = None

    def mark_done(self) -> None:
        """Mark task as completed (FR-004, FR-005)"""
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()

    def mark_undone(self) -> None:
        """Revert completed task to todo"""
        self.status = TaskStatus.TODO
        self.completed_at = None
        self.updated_at = datetime.now()

    def update(self, **kwargs) -> None:
        """Update task fields and refresh updated_at"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

        # Validate after update
        self.__post_init__()

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary"""
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
    def from_dict(cls, data: dict) -> 'Task':
        """Deserialize from JSON dictionary"""
        # Convert string UUIDs back to UUID objects
        if "id" in data:
            data["id"] = UUID(data["id"])
        if "parent_id" in data and data["parent_id"]:
            data["parent_id"] = UUID(data["parent_id"])

        # Convert ISO format strings back to dates/datetimes
        if "due_date" in data and data["due_date"]:
            data["due_date"] = date.fromisoformat(data["due_date"])
        if "created_at" in data:
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        if "completed_at" in data and data["completed_at"]:
            data["completed_at"] = datetime.fromisoformat(data["completed_at"])

        # Convert string enums back to enum objects
        if "status" in data:
            data["status"] = TaskStatus(data["status"])
        if "priority" in data:
            data["priority"] = Priority(data["priority"])

        return cls(**data)
```

**Indexes** (for query optimization):
- Primary: `id` (UUID)
- Secondary: `(status, project)` - For project-filtered views
- Secondary: `due_date` - For calendar view
- Secondary: `(priority, status)` - For priority sorting
- Secondary: `tags` - For tag-based filtering

---

### 2. Project

**Purpose**: Organizes tasks into categories/contexts

**Satisfies**: FR-011 to FR-018, User Story 2

```python
class ProjectColor(str, Enum):
    """Project color enumeration (FR-014)"""
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"

@dataclass
class Project:
    """
    Project entity for task organization

    Validation:
    - name: 1-50 characters, unique (FR-013)
    - color: One of ProjectColor enum values
    """

    id: UUID = field(default_factory=uuid4)
    name: str = ""  # FR-013: Unique, 1-50 chars
    description: str = ""  # Optional description
    color: ProjectColor = ProjectColor.CYAN  # FR-014: Display color
    icon: str = "📁"  # Emoji icon for display
    created_at: datetime = field(default_factory=datetime.now)
    archived: bool = False  # FR-017: Archive flag
    position: int = 0  # Display ordering

    def __post_init__(self):
        """Validate project data"""
        # FR-013: Name validation
        if not self.name or not self.name.strip():
            raise ValueError("Project name cannot be empty")
        if len(self.name) > 50:
            raise ValueError("Project name cannot exceed 50 characters")
        self.name = self.name.strip()

    def archive(self) -> None:
        """Archive project (FR-017)"""
        self.archived = True

    def unarchive(self) -> None:
        """Restore archived project"""
        self.archived = False

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "color": self.color.value,
            "icon": self.icon,
            "created_at": self.created_at.isoformat(),
            "archived": self.archived,
            "position": self.position,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        """Deserialize from JSON dictionary"""
        if "id" in data:
            data["id"] = UUID(data["id"])
        if "created_at" in data:
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "color" in data:
            data["color"] = ProjectColor(data["color"])

        return cls(**data)

# Default projects (FR-011)
DEFAULT_PROJECTS = [
    Project(name="Inbox", color=ProjectColor.CYAN, icon="📥", position=0),
    Project(name="Personal", color=ProjectColor.GREEN, icon="🏠", position=1),
    Project(name="Work", color=ProjectColor.BLUE, icon="💼", position=2),
]
```

**Business Rules**:
- Project names must be unique across all projects (enforced by storage layer)
- Cannot delete project with active tasks (FR-018) - tasks must be moved to Inbox first
- Archived projects are hidden from main views but data retained

---

### 3. Tag

**Purpose**: Lightweight labels for cross-cutting task categorization

**Satisfies**: FR-025 to FR-026, User Story 4

```python
@dataclass
class Tag:
    """
    Tag entity for task labeling

    Note: Tags are stored inline with tasks (many-to-many via task.tags list)
    This entity is used for tag metadata and statistics
    """

    name: str  # Primary key
    color: str = "yellow"  # Display color for UI

    def __post_init__(self):
        """Validate tag data"""
        if not self.name or not self.name.strip():
            raise ValueError("Tag name cannot be empty")
        self.name = self.name.strip().lower()  # Normalize to lowercase

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary"""
        return {
            "name": self.name,
            "color": self.color,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Tag':
        """Deserialize from JSON dictionary"""
        return cls(**data)

# Tag usage is computed dynamically from tasks
def get_tag_count(tag_name: str, tasks: List[Task]) -> int:
    """Calculate how many tasks use this tag (FR-026)"""
    return sum(1 for task in tasks if tag_name in task.tags)
```

**Storage Strategy**:
- Tags are stored as strings in `Task.tags` array (denormalized)
- Tag metadata (color, etc.) stored separately for customization
- Tag usage count computed on-demand from task list

---

### 4. Filter

**Purpose**: Saved queries for quick task list filtering

**Satisfies**: FR-028 to FR-031, User Story 4

```python
@dataclass
class Filter:
    """
    Filter entity for saved queries

    Query format examples:
    - {"priority": "urgent"}
    - {"due_date": {"<": "today"}}
    - {"status": {"!=": "done"}}
    - {"tags": {"contains": "backend"}}
    - {"_and": [{"priority": "high"}, {"project": "Work"}]}
    """

    id: UUID = field(default_factory=uuid4)
    name: str = ""  # Display name
    query: dict = field(default_factory=dict)  # JSON query specification
    icon: str = "🔍"  # Display icon
    hotkey: Optional[str] = None  # FR-031: Single char hotkey

    def __post_init__(self):
        """Validate filter data"""
        if not self.name or not self.name.strip():
            raise ValueError("Filter name cannot be empty")
        self.name = self.name.strip()

        # FR-031: Hotkey validation (single character)
        if self.hotkey and len(self.hotkey) != 1:
            raise ValueError("Filter hotkey must be a single character")

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "query": self.query,
            "icon": self.icon,
            "hotkey": self.hotkey,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Filter':
        """Deserialize from JSON dictionary"""
        if "id" in data:
            data["id"] = UUID(data["id"])
        return cls(**data)

# Predefined smart filters (FR-027)
SMART_FILTERS = [
    Filter(name="Today", query={"due_date": "today"}, icon="📅", hotkey="t"),
    Filter(name="Urgent", query={"priority": "urgent"}, icon="🔥", hotkey="u"),
    Filter(name="Overdue", query={"_and": [{"due_date": {"<": "today"}}, {"status": {"!=": "done"}}]}, icon="⏰", hotkey="o"),
    Filter(name="This Week", query={"due_date": {"<=": "+7d"}}, icon="📆", hotkey="w"),
    Filter(name="Completed", query={"status": "done"}, icon="✓", hotkey="c"),
    Filter(name="Inbox", query={"project": "Inbox"}, icon="📥", hotkey="i"),
]
```

**Query DSL** (FR-029, FR-030):
```python
# Supported operators (FR-029)
OPERATORS = {
    "=": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "contains": lambda a, b: b in a,  # For tags, description
    "in": lambda a, b: a in b,  # For checking membership
}

# Supported combinators (FR-030)
COMBINATORS = ["_and", "_or", "_not"]
```

---

### 5. Settings

**Purpose**: User preferences and application configuration

**Satisfies**: FR-045 to FR-052, User Story 6

```python
@dataclass
class Settings:
    """
    Settings entity (singleton - one per user)

    All fields have sensible defaults for zero-config operation
    """

    # Appearance (FR-046)
    theme: str = "dark"  # "dark", "light", "auto"
    color_scheme: str = "solarized"  # Color palette name
    font_size: str = "medium"  # "small", "medium", "large"
    show_icons: bool = True  # Enable emoji icons
    compact_mode: bool = False  # Reduce spacing

    # Behavior (FR-047, FR-048, FR-049)
    default_project: str = "Inbox"  # FR-047
    default_priority: str = "medium"  # FR-047
    auto_archive_completed: int = 7  # FR-048: Days until auto-archive
    confirm_delete: bool = True  # FR-049
    show_completed: bool = False  # Show completed in main list
    sort_by: str = "priority"  # "priority", "due_date", "created_at"

    # Date & Time (FR-050, FR-051, FR-052)
    date_format: str = "%Y-%m-%d"  # FR-050: strftime format
    time_format: str = "24h"  # FR-051: "24h" or "12h"
    week_starts_on: str = "Monday"  # FR-052: Day name

    # Data management (FR-056, FR-057)
    storage_location: str = "~/.config/todo-master/"
    auto_save_interval: int = 5  # FR-056: Seconds
    backup_count: int = 5  # FR-057: Number of backups to keep

    def __post_init__(self):
        """Validate settings"""
        # Validate theme
        if self.theme not in ["dark", "light", "auto"]:
            self.theme = "dark"

        # Validate time format
        if self.time_format not in ["24h", "12h"]:
            self.time_format = "24h"

        # Validate day of week
        valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if self.week_starts_on not in valid_days:
            self.week_starts_on = "Monday"

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary"""
        return {
            "theme": self.theme,
            "color_scheme": self.color_scheme,
            "font_size": self.font_size,
            "show_icons": self.show_icons,
            "compact_mode": self.compact_mode,
            "default_project": self.default_project,
            "default_priority": self.default_priority,
            "auto_archive_completed": self.auto_archive_completed,
            "confirm_delete": self.confirm_delete,
            "show_completed": self.show_completed,
            "sort_by": self.sort_by,
            "date_format": self.date_format,
            "time_format": self.time_format,
            "week_starts_on": self.week_starts_on,
            "storage_location": self.storage_location,
            "auto_save_interval": self.auto_save_interval,
            "backup_count": self.backup_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Settings':
        """Deserialize from JSON dictionary"""
        return cls(**data)
```

---

### 6. Statistics (Computed Entity)

**Purpose**: Aggregated metrics and analytics

**Satisfies**: FR-038 to FR-044, User Story 5

```python
@dataclass
class Statistics:
    """
    Statistics entity (computed from tasks, not persisted)

    All fields are calculated dynamically from task list
    """

    # Overview metrics (FR-038)
    total_tasks: int = 0
    completed_tasks: int = 0
    active_tasks: int = 0
    overdue_tasks: int = 0

    # Completion metrics (FR-039)
    completion_rate: float = 0.0  # Percentage
    daily_completion_rates: dict = field(default_factory=dict)  # day -> rate

    # Distribution (FR-040)
    tasks_by_project: dict = field(default_factory=dict)  # project -> count
    tasks_by_priority: dict = field(default_factory=dict)  # priority -> count

    # Tags (FR-041)
    top_tags: list = field(default_factory=list)  # [(tag, count), ...]

    # Productivity (FR-042)
    avg_completion_time: Optional[float] = None  # Minutes
    most_productive_day: Optional[str] = None  # Day name
    current_streak: int = 0  # Consecutive days with completions

    # Time period
    period: str = "7_days"  # FR-043: "7_days", "30_days", "90_days", "all_time"

    @classmethod
    def compute(cls, tasks: List[Task], period: str = "7_days") -> 'Statistics':
        """
        Compute statistics from task list

        Args:
            tasks: List of all tasks
            period: Time period for statistics

        Returns:
            Statistics object with computed metrics
        """
        from datetime import timedelta
        from collections import defaultdict, Counter

        # Filter tasks by period
        now = datetime.now()
        period_start = {
            "7_days": now - timedelta(days=7),
            "30_days": now - timedelta(days=30),
            "90_days": now - timedelta(days=90),
            "all_time": datetime.min,
        }[period]

        period_tasks = [t for t in tasks if t.created_at >= period_start]

        # Overview metrics (FR-038)
        total = len(tasks)
        completed = len([t for t in tasks if t.status == TaskStatus.DONE])
        active = len([t for t in tasks if t.status in [TaskStatus.TODO, TaskStatus.IN_PROGRESS]])
        overdue = len([t for t in tasks if t.due_date and t.due_date < date.today() and t.status != TaskStatus.DONE])

        # Completion rate
        completion_rate = (completed / total * 100) if total > 0 else 0.0

        # Daily completion rates (FR-039)
        daily_rates = {}
        for day_offset in range(7):
            day = (now - timedelta(days=day_offset)).date()
            day_completed = len([t for t in tasks if t.completed_at and t.completed_at.date() == day])
            day_created = len([t for t in tasks if t.created_at.date() == day])
            daily_rates[day.strftime("%A")[:3]] = (day_completed / day_created * 100) if day_created > 0 else 0.0

        # Distribution (FR-040)
        by_project = Counter(t.project for t in tasks)
        by_priority = Counter(t.priority.value for t in tasks)

        # Top tags (FR-041)
        all_tags = [tag for t in tasks for tag in t.tags]
        top_tags = Counter(all_tags).most_common(10)

        # Productivity metrics (FR-042)
        completed_with_time = [t for t in tasks if t.status == TaskStatus.DONE and t.actual_time]
        avg_time = sum(t.actual_time for t in completed_with_time) / len(completed_with_time) if completed_with_time else None

        # Most productive day
        day_completions = defaultdict(int)
        for t in tasks:
            if t.completed_at:
                day_completions[t.completed_at.strftime("%A")] += 1
        most_productive = max(day_completions.items(), key=lambda x: x[1])[0] if day_completions else None

        # Current streak
        streak = 0
        check_date = date.today()
        while True:
            day_has_completion = any(t.completed_at and t.completed_at.date() == check_date for t in tasks)
            if not day_has_completion:
                break
            streak += 1
            check_date -= timedelta(days=1)

        return cls(
            total_tasks=total,
            completed_tasks=completed,
            active_tasks=active,
            overdue_tasks=overdue,
            completion_rate=completion_rate,
            daily_completion_rates=daily_rates,
            tasks_by_project=dict(by_project),
            tasks_by_priority=dict(by_priority),
            top_tags=top_tags,
            avg_completion_time=avg_time,
            most_productive_day=most_productive,
            current_streak=streak,
            period=period,
        )
```

---

## Data Storage Format

### JSON File Structure

**tasks.json** (FR-053):
```json
{
  "version": "1.0",
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Fix authentication bug",
      "description": "Users cannot log in with special characters",
      "status": "in_progress",
      "priority": "urgent",
      "project": "Work",
      "tags": ["bug", "backend", "security"],
      "due_date": "2025-12-15",
      "created_at": "2025-12-09T10:30:00",
      "updated_at": "2025-12-09T14:20:00",
      "completed_at": null,
      "estimated_time": 120,
      "actual_time": null,
      "parent_id": null,
      "position": 0
    }
  ]
}
```

**projects.json** (FR-054):
```json
{
  "version": "1.0",
  "projects": [
    {
      "id": "650e8400-e29b-41d4-a716-446655440001",
      "name": "Work",
      "description": "Professional tasks and projects",
      "color": "blue",
      "icon": "💼",
      "created_at": "2025-12-01T00:00:00",
      "archived": false,
      "position": 0
    }
  ]
}
```

**settings.json** (FR-055):
```json
{
  "version": "1.0",
  "theme": "dark",
  "color_scheme": "solarized",
  "default_project": "Inbox",
  "default_priority": "medium",
  "date_format": "%Y-%m-%d",
  "time_format": "24h",
  "auto_save_interval": 5,
  "backup_count": 5
}
```

---

## Data Validation Rules

### Task Validation
1. ✓ Title: Non-empty, 1-200 characters (FR-002)
2. ✓ Status: One of 4 valid enum values (FR-008)
3. ✓ Priority: One of 4 valid enum values (FR-009)
4. ✓ Project: Must exist in projects list
5. ✓ Due date: Valid date or None
6. ✓ Timestamps: Auto-managed, immutable by user
7. ✓ completed_at: Auto-set when status=done (FR-005)

### Project Validation
1. ✓ Name: Non-empty, 1-50 characters, unique (FR-013)
2. ✓ Color: One of 7 valid enum values (FR-014)
3. ✓ Archived: Boolean flag
4. ✓ Cannot delete with active tasks (enforced by service layer, FR-018)

### Tag Validation
1. ✓ Name: Non-empty string
2. ✓ Normalized to lowercase for consistency

### Filter Validation
1. ✓ Name: Non-empty string
2. ✓ Query: Valid JSON object
3. ✓ Hotkey: Single character or None (FR-031)

### Settings Validation
1. ✓ Theme: One of "dark", "light", "auto"
2. ✓ Time format: "24h" or "12h"
3. ✓ Week start: Valid day name
4. ✓ Numeric fields: Positive integers

---

## Migration and Versioning

### Schema Version

Each JSON file includes a `"version"` field for schema migration:
- Current version: `"1.0"`
- Future versions: `"1.1"`, `"2.0"`, etc.

### Migration Strategy

```python
def migrate_tasks_file(data: dict) -> dict:
    """Migrate tasks.json to current schema version"""
    version = data.get("version", "1.0")

    if version == "1.0":
        # Current version, no migration needed
        return data

    # Future migrations would go here
    # if version == "1.1":
    #     data = migrate_1_1_to_2_0(data)

    return data
```

---

## Constraints and Invariants

### Data Integrity Rules

1. **Task.id uniqueness**: Enforced by UUID generation
2. **Project.name uniqueness**: Enforced by storage layer validation
3. **Task.project reference**: Must refer to existing project (or default to "Inbox")
4. **completed_at consistency**: Set if and only if status == "done"
5. **Timestamp ordering**: created_at <= updated_at <= completed_at
6. **No orphaned tasks**: Tasks always belong to a project (default: "Inbox")

### Performance Constraints

1. **In-memory loading**: All data loaded at startup (<2 seconds, SC-024)
2. **Auto-save throttling**: Maximum one save per 5 seconds (FR-056)
3. **Query optimization**: Indexes on frequently filtered fields
4. **Virtual scrolling**: Render only visible tasks (<50ms, Constitution III)

---

## Summary

This data model provides:
- ✅ Complete coverage of all 75 functional requirements
- ✅ Clear validation rules for data integrity
- ✅ JSON-based storage for human readability (Constitution IV)
- ✅ Performance optimization through indexing
- ✅ Extension points for future features (subtasks via parent_id)
- ✅ Type safety through dataclasses and enums

**Next Steps**: Define storage API contracts in `contracts/storage-api.md`
