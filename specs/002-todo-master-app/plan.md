# Implementation Plan: Todo Master Console Application

**Branch**: `002-todo-master-app` | **Date**: 2025-12-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-todo-master-app/spec.md`

## Summary

Todo Master is a multi-screen terminal-based task management application providing comprehensive productivity features through an intuitive keyboard-driven interface. The application offers six distinct views (Task List, Projects, Calendar, Tags & Filters, Statistics, Settings) for organizing and visualizing tasks, with real-time data persistence and robust backup mechanisms.

**Technical Approach**: Python-based curses application with JSON file storage, modular architecture separating UI rendering from business logic, and widget-based UI components for reusable interface elements.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**:
- `windows-curses` (Windows compatibility)
- `python-dateutil` (date parsing and manipulation)
- Standard library: `curses`, `json`, `uuid`, `datetime`, `pathlib`

**Storage**: JSON files at `~/.config/todo-master/` (tasks.json, projects.json, settings.json)
**Testing**: pytest with pytest-cov for coverage tracking
**Target Platform**: Cross-platform terminal (Linux, macOS, Windows with windows-curses)
**Project Type**: Single console application (CLI-based TUI)
**Performance Goals**:
- 50ms max for user interactions (Constitution III)
- Handle 1000+ tasks without lag
- <500ms startup time
- <50ms task list rendering for 1000 tasks

**Constraints**:
- Minimum terminal size: 80x24
- UTF-8 encoding support required
- 256-color terminal recommended (fallback to 8 colors)
- No network dependencies
- Immediate data persistence on every change

**Scale/Scope**:
- 6 main screens/views
- 75 functional requirements
- 26 success criteria
- Support for 1000+ tasks
- Plugin architecture for future extensibility

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Principle I: Keyboard-First Interaction
**Compliant**: All 6 screens designed with comprehensive keyboard shortcuts (n/e/d/x/p/t/f keys, j/k navigation, Tab/Shift+Tab screen switching, 1-6 direct screen jumps). Mouse support is optional enhancement only (FR-069).

### ✅ Principle II: Multi-View Organization
**Compliant**: Six synchronized views share common data model (Task, Project, Tag entities). Single-key screen switching via number keys 1-6 (FR-063) and Tab navigation (FR-062). All views operate on same JSON storage.

### ✅ Principle III: Performance Budget (NON-NEGOTIABLE)
**Compliant**:
- FR-075: Virtual scrolling for large task lists ensures <50ms rendering
- SC-003: 50+ tasks navigation must be smooth
- SC-024: Application launches in <2 seconds
- SC-025: Screen transitions <0.5 seconds
- SC-026: Search results in <1 second for 500+ tasks

### ✅ Principle IV: Data Persistence Reliability
**Compliant**:
- FR-056: Auto-save every 5 seconds
- FR-057: Automatic backups (maintain 5 most recent)
- FR-053-055: JSON format for human readability
- SC-004: Data persisted within 5 seconds
- SC-016: 5 automatic backups maintained
- SC-019: Recovery from corrupted files via backup

### ✅ Principle V: Zero Configuration
**Compliant**:
- FR-060: Auto-create `~/.config/todo-master/` on first run
- FR-011: Three default projects provided (Inbox, Personal, Work)
- FR-027: Predefined smart filters available immediately
- No configuration required to start using application

### ✅ Principle VI: Progressive Disclosure
**Compliant**:
- P1 user story (Basic Task Management) provides immediate core value
- FR-067: Help modal accessible via '?' key from any screen
- FR-066: Contextual hotkey help footer on each screen
- Advanced features (tags, filters, statistics) accessible but not required

### ⚠️  Principle VII: Extensible Architecture
**Deferred to Phase 5**: Plugin system marked as optional enhancement. Core architecture will be modular to support future plugin development without requiring it for v1.0.

**Justification**: Spec focuses on core feature delivery. Modular design (separate view/model/storage layers) creates foundation for plugins without upfront complexity.

### ✅ Principle VIII: Fail Gracefully
**Compliant**:
- Edge case handling defined for 10 scenarios (empty title, corrupted files, terminal resize, etc.)
- FR-057: Automatic backups before destructive operations
- SC-019: Recovery from corrupted data via backup loading
- Validation errors provide actionable messages (FR-002 title validation)

**Gate Status**: ✅ PASSED - All non-negotiable principles satisfied. Plugin architecture deferred appropriately.

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-master-app/
├── spec.md              # Feature specification (COMPLETED)
├── plan.md              # This file (IN PROGRESS)
├── research.md          # Phase 0 output (TO BE CREATED)
├── data-model.md        # Phase 1 output (TO BE CREATED)
├── quickstart.md        # Phase 1 output (TO BE CREATED)
├── contracts/           # Phase 1 output (TO BE CREATED)
│   └── storage-api.md   # JSON storage interface contract
├── checklists/          # Validation checklists
│   └── requirements.md  # Spec quality checklist (COMPLETED)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── todo_master/
│   ├── __init__.py
│   ├── main.py              # Entry point and application controller
│   │
│   ├── models/              # Data models and business logic
│   │   ├── __init__.py
│   │   ├── task.py          # Task model with validation (FR-001 to FR-010)
│   │   ├── project.py       # Project model (FR-011 to FR-018)
│   │   ├── tag.py           # Tag model (FR-025 to FR-026)
│   │   ├── filter.py        # Filter/query model (FR-028 to FR-031)
│   │   └── settings.py      # Settings model (FR-045 to FR-052)
│   │
│   ├── storage/             # Data persistence layer
│   │   ├── __init__.py
│   │   ├── base.py          # Abstract storage interface
│   │   ├── json_store.py    # JSON file storage (FR-053 to FR-060)
│   │   └── backup.py        # Backup management (FR-057)
│   │
│   ├── ui/                  # User interface layer
│   │   ├── __init__.py
│   │   ├── app.py           # Main UI application controller
│   │   ├── theme.py         # Color schemes and themes (FR-046)
│   │   │
│   │   ├── widgets/         # Reusable UI components
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # Base widget class
│   │   │   ├── table.py     # Task table widget
│   │   │   ├── form.py      # Input form widgets
│   │   │   ├── modal.py     # Modal dialog widget
│   │   │   ├── menu.py      # Dropdown menu widget
│   │   │   └── chart.py     # Chart rendering for statistics
│   │   │
│   │   ├── screens/         # Full-screen views
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # Base screen class with navigation
│   │   │   ├── task_list.py # Main task list screen (User Story 1)
│   │   │   ├── projects.py  # Project management screen (User Story 2)
│   │   │   ├── calendar.py  # Calendar/timeline view (User Story 3)
│   │   │   ├── tags.py      # Tags and filters screen (User Story 4)
│   │   │   ├── stats.py     # Statistics screen (User Story 5)
│   │   │   └── settings.py  # Settings screen (User Story 6)
│   │   │
│   │   └── navigation.py    # Screen navigation manager (FR-061 to FR-063)
│   │
│   ├── services/            # Business logic services
│   │   ├── __init__.py
│   │   ├── task_manager.py  # Task CRUD operations
│   │   ├── search.py        # Search and fuzzy matching (FR-033 to FR-037)
│   │   ├── filter_engine.py # Query parser and execution (FR-028 to FR-032)
│   │   ├── statistics.py    # Analytics computation (FR-038 to FR-044)
│   │   └── validator.py     # Data validation utilities
│   │
│   └── utils/               # Shared utilities
│       ├── __init__.py
│       ├── date_utils.py    # Date parsing and formatting
│       ├── keybindings.py   # Keyboard shortcut definitions
│       └── constants.py     # Application constants

tests/
├── unit/                    # Unit tests for models and services
│   ├── test_models.py
│   ├── test_storage.py
│   ├── test_services.py
│   └── test_validators.py
│
├── integration/             # Integration tests for workflows
│   ├── test_task_workflows.py
│   ├── test_data_persistence.py
│   └── test_screen_navigation.py
│
└── fixtures/                # Test data and fixtures
    ├── sample_tasks.json
    └── sample_settings.json

docs/
├── user-guide.md            # End-user documentation
├── keyboard-shortcuts.md    # Complete hotkey reference
└── developer.md             # Development guide
```

**Structure Decision**: Single console application structure selected. The application is a standalone Python CLI tool with no web/mobile components. Modular architecture separates concerns:
- **models/**: Pure business logic, no UI dependencies
- **storage/**: Abstract storage interface allows future backends
- **ui/**: Curses-specific rendering isolated for potential rewrite
- **services/**: Reusable business logic accessible from any UI layer
- **screens/**: One module per view, independently testable

This structure supports the deferred plugin system (Principle VII) by maintaining clear boundaries between layers.

## Complexity Tracking

**No violations requiring justification.** All constitution principles are satisfied or appropriately deferred (plugin system to Phase 5).

## Phase 0: Research & Technology Choices

### Research Tasks

1. **Python Curses Best Practices**
   - Research: Modern curses application patterns, window management, color handling
   - Decision needed: Direct curses vs higher-level wrapper (e.g., `urwid`, `blessed`)
   - Output: Technology choice with rationale in research.md

2. **Virtual Scrolling Implementation**
   - Research: Efficient rendering for 1000+ item lists in terminal
   - Decision needed: Pagination strategy, viewport management, performance optimization
   - Output: Scrolling architecture in research.md

3. **Fuzzy Search Algorithms**
   - Research: Fuzzy matching algorithms suitable for task search (Levenshtein, trigram, etc.)
   - Decision needed: Algorithm choice balancing accuracy and performance
   - Output: Search implementation approach in research.md

4. **Terminal Compatibility Testing**
   - Research: Cross-platform curses differences (Linux/macOS/Windows)
   - Decision needed: Windows compatibility approach (`windows-curses` vs alternative)
   - Output: Platform support strategy in research.md

5. **Date Parsing Libraries**
   - Research: `python-dateutil` vs alternatives for natural language dates
   - Decision needed: Library selection for due date handling
   - Output: Date handling approach in research.md

6. **Chart Rendering in Terminal**
   - Research: ASCII/Unicode chart rendering techniques for statistics screen
   - Decision needed: Custom rendering vs library (e.g., `plotext`, `asciichartpy`)
   - Output: Visualization strategy in research.md

### Technology Stack Summary

**Core Framework**: Python 3.11+ with standard library `curses`

**Dependencies** (to be validated in Phase 0):
- `windows-curses` - Windows compatibility layer
- `python-dateutil` - Date parsing and manipulation
- `pytest` + `pytest-cov` - Testing framework
- TBD: Fuzzy search library (e.g., `fuzzywuzzy`, `thefuzz`)
- TBD: Chart rendering library or custom implementation

**Storage**: JSON files (no database)
**Package Manager**: `uv` for fast dependency management
**Build Tool**: Standard Python packaging (`pyproject.toml`)

## Phase 1: Core Architecture & Data Model

### Data Model Design

#### Task Entity
**Satisfies**: FR-001 to FR-010, User Story 1

```python
@dataclass
class Task:
    id: UUID                    # FR-010: Auto-generated unique ID
    title: str                  # FR-001, FR-002: 1-200 chars, required
    description: str = ""       # FR-001: Optional text
    status: TaskStatus          # FR-008: todo/in_progress/done/archived
    priority: Priority          # FR-009: low/medium/high/urgent
    project: str = "Inbox"      # FR-001: Project assignment
    tags: List[str]             # FR-001: Tag array
    due_date: Optional[date]    # FR-001: Optional due date
    created_at: datetime        # Auto-timestamp
    updated_at: datetime        # Auto-timestamp on modification
    completed_at: Optional[datetime]  # FR-005: Set when marked done
    estimated_time: Optional[int]     # FR-001: Minutes (optional)
    actual_time: Optional[int]        # Minutes (optional)
    parent_id: Optional[UUID]         # For future subtask support
    position: int = 0                 # Display ordering
```

#### Project Entity
**Satisfies**: FR-011 to FR-018, User Story 2

```python
@dataclass
class Project:
    id: UUID                    # Unique identifier
    name: str                   # FR-013: Unique, 1-50 chars
    description: str = ""       # Optional description
    color: ProjectColor         # FR-014: Enum of 7 colors
    icon: str = "📁"           # Emoji icon
    created_at: datetime
    archived: bool = False      # FR-017: Archive flag
    position: int = 0           # Display ordering
```

#### Tag Entity
**Satisfies**: FR-025 to FR-026, User Story 4

```python
@dataclass
class Tag:
    name: str                   # Primary key
    color: str = "yellow"       # Display color

    @property
    def count(self) -> int:     # FR-026: Computed usage count
        # Calculated from task query
```

#### Filter Entity
**Satisfies**: FR-028 to FR-031, User Story 4

```python
@dataclass
class Filter:
    id: UUID
    name: str                   # Filter display name
    query: Dict[str, Any]       # JSON query specification
    icon: str = "🔍"
    hotkey: Optional[str]       # FR-031: Single char hotkey
```

#### Settings Entity
**Satisfies**: FR-045 to FR-052, User Story 6

```python
@dataclass
class Settings:
    theme: str = "dark"                    # FR-046: dark/light/auto
    color_scheme: str = "solarized"
    show_completed: bool = False
    default_priority: str = "medium"       # FR-047
    auto_archive_completed: int = 7        # FR-048: Days
    sort_by: str = "priority"
    confirm_delete: bool = True            # FR-049
    date_format: str = "%Y-%m-%d"          # FR-050
    time_format: str = "24h"               # FR-051: 24h/12h
    week_starts_on: str = "Monday"         # FR-052
```

### Storage Layer Architecture

**Satisfies**: FR-053 to FR-060

#### Interface Contract

```python
class StorageInterface(ABC):
    """Abstract storage interface for future extensibility"""

    @abstractmethod
    def create(self, model: T) -> T:
        """Create new entity"""

    @abstractmethod
    def read(self, id: UUID) -> Optional[T]:
        """Read entity by ID"""

    @abstractmethod
    def update(self, id: UUID, changes: Dict) -> T:
        """Update entity with changes"""

    @abstractmethod
    def delete(self, id: UUID) -> bool:
        """Delete entity"""

    @abstractmethod
    def list(self, filter: Optional[Dict] = None) -> List[T]:
        """List entities with optional filter"""

    @abstractmethod
    def save(self) -> bool:
        """Persist to storage"""
```

#### JSON Storage Implementation

**File Locations** (FR-053 to FR-055):
- `~/.config/todo-master/tasks.json`
- `~/.config/todo-master/projects.json`
- `~/.config/todo-master/settings.json`

**Features**:
- Auto-save every 5 seconds (FR-056)
- Atomic writes via temp file + rename
- Automatic backups before writes (FR-057)
- Backup rotation (keep 5 most recent)
- Schema validation on load
- Fallback to backup on corruption

### UI Architecture

#### Component Hierarchy

```
App (Main Controller)
├── NavigationManager (Screen switching)
├── ThemeManager (Colors and styles)
└── ScreenManager
    ├── TaskListScreen (P1 - Main View)
    │   ├── TableWidget (Task display)
    │   ├── FilterBar (Project/quick filters)
    │   ├── SearchInput (FR-033)
    │   └── TaskModal (Create/edit form)
    │
    ├── ProjectsScreen (P2 - Organization)
    │   ├── ProjectCard (Per-project widget)
    │   └── ProjectModal (CRUD operations)
    │
    ├── CalendarScreen (P3 - Timeline)
    │   ├── DateGroupWidget (Overdue/Today/Tomorrow)
    │   └── DatePicker (Reschedule interface)
    │
    ├── TagsScreen (P4 - Advanced filtering)
    │   ├── TagCloud (Tag display)
    │   ├── FilterBuilder (Custom queries)
    │   └── FilterList (Smart + custom filters)
    │
    ├── StatsScreen (P5 - Analytics)
    │   ├── SummaryCards (Overview metrics)
    │   ├── ChartWidget (Bar charts)
    │   └── PeriodSelector (Time range)
    │
    └── SettingsScreen (P6 - Configuration)
        └── SettingsForm (Multi-section form)
```

#### Base Classes

**BaseScreen**: Abstract class for all screens
- Common navigation (Tab, number keys, j/k)
- Help modal ('?' key)
- Status bar rendering
- Input handling delegation

**BaseWidget**: Reusable UI component
- Position and dimension management
- Draw/refresh lifecycle
- Event handling
- Focus management

### Service Layer

#### TaskManager Service
**Responsibilities**:
- Task CRUD operations (FR-001 to FR-010)
- Business logic validation
- Timestamp management
- Undo buffer for deletions (FR-007)

#### SearchService
**Satisfies**: FR-033 to FR-037
- Full-text search across title/description/tags
- Fuzzy matching implementation
- Query syntax parsing (p:, t:, @, is:)
- Result ranking

#### FilterEngine
**Satisfies**: FR-028 to FR-032
- Query DSL parsing
- Operator evaluation (=, !=, <, >, <=, >=, contains, in)
- Combinator logic (AND, OR, NOT)
- Query execution against task list

#### StatisticsService
**Satisfies**: FR-038 to FR-044
- Metrics computation (totals, completion rate)
- Time-series aggregation (7/30/90 days)
- Productivity analysis (streaks, peak times)
- Distribution calculations (by project/priority)

## Phase 2: Implementation Roadmap

### Milestone 1: Foundation (P1 Requirements)
**Target**: Basic task management fully functional

**Components**:
1. Data models with validation
2. JSON storage with auto-save
3. Curses UI initialization
4. TaskListScreen with table widget
5. Task CRUD operations
6. Basic navigation (j/k, Enter, Esc)

**Exit Criteria**:
- Can create, view, edit, delete tasks
- Data persists across sessions
- UI renders correctly in 80x24 terminal
- All P1 acceptance scenarios pass

### Milestone 2: Organization (P2 Requirements)
**Target**: Project-based task organization

**Components**:
1. Project model and storage
2. ProjectsScreen with cards
3. Project CRUD operations
4. Task-project assignment
5. Project filtering in TaskListScreen

**Exit Criteria**:
- Can create and manage projects
- Tasks organized by projects
- Project statistics display correctly
- All P2 acceptance scenarios pass

### Milestone 3: Timeline & Search (P3-P4 Requirements)
**Target**: Calendar view and advanced filtering

**Components**:
1. CalendarScreen with date grouping
2. Date utilities and formatting
3. Tag management
4. TagsScreen with filter builder
5. SearchService with fuzzy matching
6. Filter query engine

**Exit Criteria**:
- Calendar view groups tasks by date
- Tag system operational
- Search works with syntax
- Custom filters can be created
- All P3-P4 acceptance scenarios pass

### Milestone 4: Analytics & Polish (P5-P6 Requirements)
**Target**: Complete feature set with optimization

**Components**:
1. StatisticsService
2. StatsScreen with charts
3. SettingsScreen
4. Theme system
5. Performance optimization (virtual scrolling)
6. Comprehensive testing

**Exit Criteria**:
- All 6 screens functional
- Statistics display correctly
- Settings persist
- Handles 1000+ tasks smoothly
- All P5-P6 acceptance scenarios pass
- >80% test coverage

## Architecture Decision Records

### ADR-001: Use Standard Library Curses
**Decision**: Use Python's built-in `curses` module with `windows-curses` for Windows compatibility

**Rationale**:
- Zero additional dependencies on Unix systems
- Direct control over performance (Constitution III)
- Mature, well-documented API
- Predictable behavior across platforms

**Alternatives Considered**:
- `urwid`: Higher-level but heavier, potential performance overhead
- `blessed`: Simpler API but less control for complex layouts
- `textual`: Modern but new, unknown performance characteristics

**Implications**:
- More boilerplate for UI components
- Need custom widget library
- Direct responsibility for performance optimization

### ADR-002: JSON File Storage
**Decision**: Store all data in JSON files at `~/.config/todo-master/`

**Rationale**:
- Human-readable for debugging and version control (Constitution IV)
- No database setup required (Constitution V)
- Simple backup/restore mechanism
- Cross-platform compatibility
- Direct file system atomic writes

**Alternatives Considered**:
- SQLite: Overkill for simple CRUD, adds query complexity
- YAML: Slower parsing, more complex schema
- Binary format: Not human-readable, violates Constitution IV

**Implications**:
- Manual indexing for search performance
- In-memory loading required for queries
- File locking needed for concurrent access (future)

### ADR-003: Modular Screen Architecture
**Decision**: Each view is an independent Screen class inheriting from BaseScreen

**Rationale**:
- Easy to add new views (Constitution VII extensibility)
- Clear separation of concerns
- Independent testing per screen
- Simple navigation implementation

**Alternatives Considered**:
- Single-screen with mode switching: Hard to maintain, poor testability
- Tab-based interface: Less flexible for six distinct views

**Implications**:
- Consistent interface contract across screens
- Navigation manager coordinates screen lifecycle
- Shared widgets reduce code duplication

## Testing Strategy

### Unit Tests
**Coverage Target**: >80% (Constitution compliance)

**Focus Areas**:
- Data model validation (FR-002, FR-013 title/name validation)
- Storage operations (create, read, update, delete)
- Query parser and filter engine
- Search algorithm accuracy
- Statistics calculations
- Date utilities

### Integration Tests

**Workflows**:
1. Task lifecycle: create → edit → mark done → delete
2. Project assignment and filtering
3. Data persistence across app restarts
4. Backup creation and restoration
5. Screen navigation flows
6. Filter application and result updates

### Performance Tests

**Benchmarks** (Constitution III):
- Task list rendering with 1000 tasks: <50ms
- Search across 500 tasks: <1 second (SC-026)
- Screen switching: <500ms (SC-025)
- Application startup: <2 seconds (SC-024)
- Auto-save operation: <10ms

### Manual Testing Checklist

**Platform Compatibility**:
- [ ] Linux (various terminals: gnome-terminal, alacritty, kitty)
- [ ] macOS (Terminal.app, iTerm2)
- [ ] Windows (cmd.exe, PowerShell, Windows Terminal)

**Terminal Sizes**:
- [ ] Minimum 80x24
- [ ] Recommended 120x40
- [ ] Behavior on resize below minimum

**Keyboard Navigation**:
- [ ] All actions accessible via keyboard
- [ ] Hotkey conflicts identified and resolved
- [ ] Help modal shows accurate shortcuts

## Risk Management

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Curses complexity delays development | Medium | High | Build widget library early in Phase 1; reuse patterns |
| Performance issues with 1000+ tasks | Medium | Critical | Implement virtual scrolling from start; benchmark continuously |
| Windows compatibility problems | Low | Medium | Test on Windows early; use windows-curses proven solution |
| Terminal rendering inconsistencies | Medium | Medium | Test across multiple terminal emulators; document requirements |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Feature scope creep | High | High | Strict adherence to prioritized user stories; defer to Phase 5 |
| Underestimated UI complexity | Medium | Medium | Allocate 40% of timeline to UI development |
| Testing bottleneck at end | Medium | High | Test-driven development; automate from start |

### Quality Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data loss bugs | Low | Critical | Automated backup testing; recovery scenarios in test suite |
| Poor keyboard UX | Medium | High | Early user testing; iterate on key bindings |
| Performance regression | Medium | Medium | Continuous benchmarking in CI/CD |

## Next Steps

**Immediate Actions**:
1. ✅ Complete Phase 0 research (research.md)
2. ✅ Define detailed data models (data-model.md)
3. ✅ Document storage API contracts (contracts/storage-api.md)
4. ✅ Create quickstart guide (quickstart.md)
5. Update agent context with new technologies

**Phase 2 Trigger**: Run `/sp.tasks` to generate detailed implementation tasks from this plan

**Success Metrics**:
- All Constitution checks remain green
- Research answers all NEEDS CLARIFICATION items
- Data model maps to all 75 functional requirements
- Architecture supports all 6 user stories independently
