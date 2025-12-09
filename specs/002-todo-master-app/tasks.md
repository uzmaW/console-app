# Tasks: Todo Master Console Application

**Feature Branch**: `002-todo-master-app`
**Input**: Design documents from `/specs/002-todo-master-app/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/storage-api.md ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted. Focus is on implementation only.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Single console application structure:
- Source code: `src/todo_master/`
- Tests: `tests/`
- Configuration: `pyproject.toml`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize Python project structure and dependencies

- [X] T001 Create project directory structure per plan.md (src/todo_master/, tests/, docs/)
- [X] T002 Initialize pyproject.toml with Python 3.11+ requirements and dependencies (python-dateutil, rapidfuzz, windows-curses)
- [X] T003 [P] Create src/todo_master/__init__.py package initializer
- [X] T004 [P] Create src/todo_master/utils/__init__.py and utils/constants.py with application constants
- [X] T005 [P] Create src/todo_master/utils/keybindings.py with keyboard shortcut definitions
- [X] T006 [P] Create tests/fixtures/ directory with sample_tasks.json and sample_settings.json
- [X] T007 [P] Configure development tools: create .gitignore, README.md with quickstart instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 Implement TaskStatus enum (todo/in_progress/done/archived) in src/todo_master/models/__init__.py
- [X] T009 [P] Implement Priority enum (low/medium/high/urgent) in src/todo_master/models/__init__.py
- [X] T010 [P] Implement ProjectColor enum in src/todo_master/models/__init__.py
- [X] T011 [P] Create abstract StorageInterface base class in src/todo_master/storage/base.py (FR-053 to FR-060)
- [X] T012 Implement JSONStorage class with CRUD operations in src/todo_master/storage/json_store.py
- [X] T013 [P] Implement BackupManager for automatic backups in src/todo_master/storage/backup.py (FR-057)
- [X] T014 [P] Implement AutoSaveManager with 5-second interval in src/todo_master/storage/auto_save.py (FR-056)
- [X] T015 [P] Create StorageError, NotFoundError, ValidationError exceptions in src/todo_master/storage/base.py
- [X] T016 [P] Implement date parsing utilities in src/todo_master/utils/date_utils.py (parse_due_date, format_relative_date)
- [ ] T017 Initialize curses application structure in src/todo_master/ui/app.py (screen initialization, color pairs)
- [ ] T018 [P] Implement ThemeManager for color schemes in src/todo_master/ui/theme.py (FR-046, FR-074)
- [ ] T019 [P] Create BaseWidget abstract class in src/todo_master/ui/widgets/base.py (position, draw, focus management)
- [ ] T020 [P] Create BaseScreen abstract class in src/todo_master/ui/screens/base.py (navigation, help modal, status bar)
- [ ] T021 Implement NavigationManager for screen switching in src/todo_master/ui/navigation.py (FR-061 to FR-063)
- [ ] T022 Create main entry point in src/todo_master/main.py (curses wrapper, app controller, error handling)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Task Management (Priority: P1) 🎯 MVP

**Goal**: Users can create, view, edit, and complete tasks in a main task list

**Independent Test**: Create a task, view it in the list, mark it complete, edit its details, and delete it. Should persist across app restarts.

### Implementation for User Story 1

- [ ] T023 [P] [US1] Create Task dataclass in src/todo_master/models/task.py (FR-001 to FR-010, all fields, validation)
- [ ] T024 [P] [US1] Implement Task.to_dict() and Task.from_dict() serialization methods
- [ ] T025 [P] [US1] Implement Task.mark_done() method that sets status and timestamps (FR-004, FR-005)
- [ ] T026 [P] [US1] Implement Task.validate() method for title length and required fields (FR-002)
- [ ] T027 [US1] Create TaskManager service in src/todo_master/services/task_manager.py (create, read, update, delete operations)
- [ ] T028 [US1] Implement TaskManager.create_task() with validation and ID generation (FR-001, FR-010)
- [ ] T029 [US1] Implement TaskManager.mark_done() method with timestamp tracking (FR-004, FR-005)
- [ ] T030 [US1] Implement TaskManager.delete_task() with 5-second undo buffer (FR-006, FR-007)
- [ ] T031 [US1] Implement TaskManager undo functionality for deletions (FR-007)
- [ ] T032 [P] [US1] Create TableWidget for task list display in src/todo_master/ui/widgets/table.py (virtual scrolling for 1000+ tasks per FR-075)
- [ ] T033 [P] [US1] Implement TableWidget.render_row() with priority indicators and due date formatting
- [ ] T034 [P] [US1] Implement TableWidget navigation (j/k keys, g/G for top/bottom per FR-065)
- [ ] T035 [P] [US1] Create FormWidget for task input in src/todo_master/ui/widgets/form.py (multi-field input)
- [ ] T036 [P] [US1] Create ModalWidget for task create/edit dialogs in src/todo_master/ui/widgets/modal.py (FR-070 Esc handling)
- [ ] T037 [US1] Implement TaskListScreen in src/todo_master/ui/screens/task_list.py with TableWidget integration
- [ ] T038 [US1] Implement TaskListScreen keyboard handlers: 'n' for new task, 'e' for edit, 'd'/Space for mark done
- [ ] T039 [US1] Implement TaskListScreen.handle_delete() with confirmation modal (FR-006) and undo notification
- [ ] T040 [US1] Implement TaskListScreen priority quick-set with '1-5' keys (FR-009)
- [ ] T041 [US1] Add task list sorting and filtering to TaskListScreen (sort by priority/due date)
- [ ] T042 [US1] Integrate JSONStorage with TaskManager for persistence (FR-053, auto-save on changes)
- [ ] T043 [US1] Implement help modal ('?' key) in TaskListScreen showing all hotkeys (FR-067)
- [ ] T044 [US1] Add status bar footer to TaskListScreen showing current view and hotkey hints (FR-066)

**Checkpoint**: At this point, User Story 1 should be fully functional - can create, view, edit, complete, and delete tasks with persistence

---

## Phase 4: User Story 2 - Project Organization (Priority: P2)

**Goal**: Users can organize tasks into projects (Inbox, Work, Personal, etc.)

**Independent Test**: Create projects, assign tasks to projects, view project-specific task lists, and see project statistics. Should work alongside existing task functionality.

### Implementation for User Story 2

- [ ] T045 [P] [US2] Create Project dataclass in src/todo_master/models/project.py (FR-011 to FR-018, all fields)
- [ ] T046 [P] [US2] Implement Project.to_dict() and Project.from_dict() serialization methods
- [ ] T047 [P] [US2] Implement Project.validate() method for unique name and length validation (FR-013)
- [ ] T048 [P] [US2] Create default projects (Inbox cyan, Personal green, Work blue) initialization in src/todo_master/models/project.py (FR-011)
- [ ] T049 [US2] Add project_id field to Task model and update Task.to_dict()/from_dict()
- [ ] T050 [US2] Implement ProjectManager service in src/todo_master/services/project_manager.py (CRUD operations)
- [ ] T051 [US2] Implement ProjectManager.create_project() with name uniqueness validation (FR-012, FR-013)
- [ ] T052 [US2] Implement ProjectManager.archive_project() method (FR-017)
- [ ] T053 [US2] Implement ProjectManager.delete_project() with active task check and move to Inbox (FR-018)
- [ ] T054 [US2] Implement ProjectManager.get_statistics() for task counts per project (FR-016)
- [ ] T055 [P] [US2] Create ProjectCard widget in src/todo_master/ui/widgets/project_card.py (show name, color, icon, stats)
- [ ] T056 [US2] Implement ProjectsScreen in src/todo_master/ui/screens/projects.py with project list display
- [ ] T057 [US2] Implement ProjectsScreen keyboard handlers: 'n' for new project, 'e' for edit, 'a' for archive
- [ ] T058 [US2] Implement ProjectsScreen project expansion/collapse on Enter to show top tasks (FR-012)
- [ ] T059 [US2] Add project color picker to project create/edit modal (7 colors per FR-014)
- [ ] T060 [US2] Add icon/emoji picker to project create/edit modal
- [ ] T061 [US2] Add project filter bar to TaskListScreen for filtering tasks by project
- [ ] T062 [US2] Implement 'p' key handler in TaskListScreen to move selected task to different project (FR-015)
- [ ] T063 [US2] Integrate projects.json storage with ProjectManager (FR-054)
- [ ] T064 [US2] Update NavigationManager to include ProjectsScreen as screen 2

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - tasks can be organized into projects

---

## Phase 5: User Story 3 - Due Date Management with Calendar View (Priority: P3)

**Goal**: Users can see tasks organized by due dates in a calendar view

**Independent Test**: Assign due dates to tasks, view calendar screen, see tasks grouped by date buckets (Overdue, Today, Tomorrow), reschedule tasks.

### Implementation for User Story 3

- [ ] T065 [P] [US3] Create DateGroup enum in src/todo_master/models/__init__.py (Overdue, Today, Tomorrow, Next7Days, Later)
- [ ] T066 [P] [US3] Implement date grouping utility in src/todo_master/utils/date_utils.py (group_tasks_by_date)
- [ ] T067 [P] [US3] Implement calculate_days_overdue() utility in src/todo_master/utils/date_utils.py (FR-021)
- [ ] T068 [P] [US3] Create DateGroupWidget in src/todo_master/ui/widgets/date_group.py (display date bucket header and tasks)
- [ ] T069 [P] [US3] Create DatePicker widget in src/todo_master/ui/widgets/date_picker.py (calendar selection interface)
- [ ] T070 [US3] Implement CalendarScreen in src/todo_master/ui/screens/calendar.py with date grouping display (FR-019 to FR-024)
- [ ] T071 [US3] Implement CalendarScreen day view showing tasks grouped by Overdue/Today/Tomorrow/Next7Days/Later (FR-020)
- [ ] T072 [US3] Implement CalendarScreen 'r' key handler to reschedule task with DatePicker (FR-022)
- [ ] T073 [US3] Implement CalendarScreen '+'/'-' key handlers for ±1 day adjustment (FR-023)
- [ ] T074 [US3] Implement CalendarScreen 't' key handler to jump to today (FR-024)
- [ ] T075 [US3] Implement CalendarScreen week view showing next 7 days (FR-024)
- [ ] T076 [US3] Implement CalendarScreen month view with calendar grid (FR-024)
- [ ] T077 [US3] Add overdue indicator rendering with days overdue count (FR-021)
- [ ] T078 [US3] Update NavigationManager to include CalendarScreen as screen 3

**Checkpoint**: All three user stories should now be independently functional - calendar provides timeline view of tasks

---

## Phase 6: User Story 4 - Tag Management and Smart Filtering (Priority: P4)

**Goal**: Users can tag tasks and create custom filters for advanced organization

**Independent Test**: Create tags, apply them to tasks, use smart filters (Today, Urgent), create custom filters with query syntax, apply filters to see filtered task lists.

### Implementation for User Story 4

- [ ] T079 [P] [US4] Create Tag dataclass in src/todo_master/models/tag.py (FR-025, FR-026)
- [ ] T080 [P] [US4] Implement Tag.count property with task query (FR-026)
- [ ] T081 [P] [US4] Create Filter dataclass in src/todo_master/models/filter.py (FR-028 to FR-031)
- [ ] T082 [P] [US4] Implement Filter.to_dict() and Filter.from_dict() serialization methods
- [ ] T083 [P] [US4] Add tags: List[str] field to Task model (already present, verify)
- [ ] T084 [US4] Create FilterEngine service in src/todo_master/services/filter_engine.py (query parsing and execution)
- [ ] T085 [US4] Implement FilterEngine.parse_query() for query DSL (FR-029: operators =, !=, <, <=, >, >=, contains, in)
- [ ] T086 [US4] Implement FilterEngine.apply_filter() with combinator logic (FR-030: AND, OR, NOT)
- [ ] T087 [US4] Implement FilterEngine.evaluate_condition() for single condition evaluation
- [ ] T088 [US4] Create predefined smart filters in FilterEngine: Today, Urgent, Overdue, This Week, Completed, Inbox (FR-027)
- [ ] T089 [P] [US4] Create TagCloud widget in src/todo_master/ui/widgets/tag_cloud.py (tag display with counts)
- [ ] T090 [P] [US4] Create FilterBuilder widget in src/todo_master/ui/widgets/filter_builder.py (query syntax input)
- [ ] T091 [US4] Implement TagsScreen in src/todo_master/ui/screens/tags.py with TagCloud and filter list sections
- [ ] T092 [US4] Implement TagsScreen 'n' key handler in tags section to create new tag
- [ ] T093 [US4] Implement TagsScreen 'n' key handler in filters section to create custom filter (FR-028, FR-031)
- [ ] T094 [US4] Add 't' key handler to TaskListScreen for adding/editing tags on selected task (FR-025)
- [ ] T095 [US4] Add 'f' key handler to TaskListScreen to open filter selection dialog
- [ ] T096 [US4] Implement active filter indicator in TaskListScreen status bar (FR-032)
- [ ] T097 [US4] Persist active filter state across screen navigation (FR-032)
- [ ] T098 [US4] Update NavigationManager to include TagsScreen as screen 4

**Checkpoint**: All four user stories should now be independently functional - advanced filtering and tagging available

---

## Phase 7: User Story 5 - Productivity Statistics and Analytics (Priority: P5)

**Goal**: Users can view statistics about task completion patterns and productivity metrics

**Independent Test**: Complete tasks over time, view Statistics screen, see completion rates, task distribution charts, and productivity metrics.

### Implementation for User Story 5

- [ ] T099 [P] [US5] Create Statistics entity in src/todo_master/models/statistics.py (computed entity, not persisted per data-model.md)
- [ ] T100 [US5] Create StatisticsService in src/todo_master/services/statistics.py (FR-038 to FR-044)
- [ ] T101 [US5] Implement StatisticsService.calculate_totals() for task counts (total, completed, active, overdue per FR-038)
- [ ] T102 [US5] Implement StatisticsService.calculate_completion_rate() for daily percentages over N days (FR-039)
- [ ] T103 [US5] Implement StatisticsService.get_distribution_by_project() for project breakdown (FR-040)
- [ ] T104 [US5] Implement StatisticsService.get_distribution_by_priority() for priority breakdown (FR-040)
- [ ] T105 [US5] Implement StatisticsService.get_top_tags() with usage counts (FR-041)
- [ ] T106 [US5] Implement StatisticsService.calculate_productivity_metrics() (avg completion time, most productive day, streak per FR-042)
- [ ] T107 [P] [US5] Create SummaryCard widget in src/todo_master/ui/widgets/summary_card.py (bordered card with title/value)
- [ ] T108 [P] [US5] Create ChartWidget in src/todo_master/ui/widgets/chart.py (horizontal/vertical bar charts using Unicode)
- [ ] T109 [US5] Implement ChartWidget.render_horizontal_bar() for project/priority distribution
- [ ] T110 [US5] Implement ChartWidget.render_vertical_bar() for completion rate over time
- [ ] T111 [US5] Implement StatsScreen in src/todo_master/ui/screens/stats.py with summary cards and charts
- [ ] T112 [US5] Add overview section to StatsScreen with 4 summary cards (total, completed, active, overdue per FR-038)
- [ ] T113 [US5] Add completion rate chart to StatsScreen (7-day bar chart per FR-039)
- [ ] T114 [US5] Add project distribution chart to StatsScreen (horizontal bar chart per FR-040)
- [ ] T115 [US5] Add priority distribution chart to StatsScreen (horizontal bar chart per FR-040)
- [ ] T116 [US5] Add tag cloud section to StatsScreen showing top tags (FR-041)
- [ ] T117 [US5] Implement 'p' key handler in StatsScreen for period selection (7/30/90 days, all time per FR-043)
- [ ] T118 [US5] Implement 'r' key handler in StatsScreen to refresh statistics (FR-044)
- [ ] T119 [US5] Update NavigationManager to include StatsScreen as screen 5

**Checkpoint**: All five user stories should now be independently functional - analytics provide insights into productivity

---

## Phase 8: User Story 6 - Application Settings and Preferences (Priority: P6)

**Goal**: Users can customize application appearance and behavior

**Independent Test**: Navigate to Settings, change preferences (theme, default project, date format), save them, restart app, verify settings persist.

### Implementation for User Story 6

- [ ] T120 [P] [US6] Create Settings dataclass in src/todo_master/models/settings.py (FR-045 to FR-052, all configuration fields)
- [ ] T121 [P] [US6] Implement Settings.to_dict() and Settings.from_dict() serialization methods
- [ ] T122 [P] [US6] Implement Settings.get_default() factory method with sensible defaults
- [ ] T123 [US6] Create SettingsManager service in src/todo_master/services/settings_manager.py (load, save, apply)
- [ ] T124 [US6] Implement SettingsManager.load_settings() from settings.json (FR-045, FR-055)
- [ ] T125 [US6] Implement SettingsManager.save_settings() with validation (FR-045)
- [ ] T126 [US6] Implement SettingsManager.apply_theme() to update ThemeManager (FR-046)
- [ ] T127 [US6] Implement auto-archive logic in TaskManager based on settings (FR-048)
- [ ] T128 [P] [US6] Create SettingsForm widget in src/todo_master/ui/widgets/settings_form.py (multi-section form)
- [ ] T129 [US6] Implement SettingsScreen in src/todo_master/ui/screens/settings.py with SettingsForm
- [ ] T130 [US6] Add Appearance section to SettingsScreen: theme, color scheme, font size (FR-046)
- [ ] T131 [US6] Add Behavior section to SettingsScreen: default project/priority, auto-archive, confirm deletes, sort (FR-047 to FR-049)
- [ ] T132 [US6] Add Date & Time section to SettingsScreen: date format, time format, week start day (FR-050 to FR-052)
- [ ] T133 [US6] Add Data section to SettingsScreen: storage location, auto-save interval, backup count
- [ ] T134 [US6] Implement 's' key handler in SettingsScreen to save settings (FR-045)
- [ ] T135 [US6] Implement data export functionality in SettingsScreen (FR-058)
- [ ] T136 [US6] Implement data import functionality in SettingsScreen (FR-059)
- [ ] T137 [US6] Update NavigationManager to include SettingsScreen as screen 6
- [ ] T138 [US6] Apply settings to all screens on startup (theme, date format, sort order, etc.)

**Checkpoint**: All six user stories should now be fully functional - application is customizable

---

## Phase 9: Search Functionality (Cross-Cutting Feature)

**Goal**: Users can search tasks globally using fuzzy matching and search syntax

**Implementation**:

- [ ] T139 [P] Create SearchService in src/todo_master/services/search.py (FR-033 to FR-037)
- [ ] T140 [P] Implement SearchService.search() with RapidFuzz fuzzy matching (FR-035)
- [ ] T141 [P] Implement SearchService.parse_search_syntax() for p:, t:, @, is: shortcuts (FR-037)
- [ ] T142 [P] Implement SearchService.highlight_matches() for result highlighting (FR-036)
- [ ] T143 Add Ctrl+F and '/' key handlers to all screens for global search (FR-033)
- [ ] T144 Create SearchModal widget in src/todo_master/ui/widgets/search_modal.py
- [ ] T145 Display search results in SearchModal with match highlighting
- [ ] T146 Add search syntax help to SearchModal footer

---

## Phase 10: Performance Optimization and Polish

**Purpose**: Performance tuning, error handling, and final polish

- [ ] T147 [P] Implement virtual scrolling optimization in TableWidget for 1000+ tasks (FR-075, SC-003)
- [ ] T148 [P] Add performance benchmarking to ensure <50ms render time (Constitution III, SC-026)
- [ ] T149 [P] Optimize search performance to meet <1 second target for 500+ tasks (SC-026)
- [ ] T150 [P] Implement terminal size validation and minimum size warning (FR-071, FR-072)
- [ ] T151 [P] Add UTF-8 encoding support verification on startup (FR-073)
- [ ] T152 [P] Implement 256-color fallback to 8-color for basic terminals (FR-074)
- [ ] T153 [P] Add comprehensive error handling for file I/O operations
- [ ] T154 [P] Implement backup recovery on corrupted file detection (SC-019)
- [ ] T155 [P] Add logging infrastructure for debugging
- [ ] T156 [P] Validate all keyboard shortcuts are conflict-free
- [ ] T157 [P] Ensure all screens show contextual help in footer (FR-066)
- [ ] T158 [P] Test application startup time meets <2 second target (SC-024)
- [ ] T159 [P] Test screen transitions meet <0.5 second target (SC-025)
- [ ] T160 [P] Verify auto-save operates within 5 seconds (FR-056, SC-004)
- [ ] T161 [P] Verify backup rotation maintains exactly 5 backups (FR-057, SC-016)
- [ ] T162 [P] Test cross-platform compatibility (Linux, macOS, Windows with windows-curses)
- [ ] T163 Create user documentation in docs/user-guide.md
- [ ] T164 [P] Create keyboard shortcuts reference in docs/keyboard-shortcuts.md
- [ ] T165 [P] Update README.md with installation and usage instructions
- [ ] T166 Run full manual test suite covering all 6 user stories independently

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - Requires US1 Task model but independently testable
  - User Story 3 (P3): Can start after Foundational - Requires US1 Task model but independently testable
  - User Story 4 (P4): Can start after Foundational - Requires US1 Task model but independently testable
  - User Story 5 (P5): Can start after Foundational - Can run independently but more meaningful with completed tasks
  - User Story 6 (P6): Can start after Foundational - Independently testable
- **Search (Phase 9)**: Can start after Foundational, enhances all user stories
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Completion Order (Recommended)

**Sequential (MVP-first)**:
1. Phase 1: Setup → Phase 2: Foundational (MUST complete)
2. Phase 3: User Story 1 (Basic Task Management) → **STOP and VALIDATE MVP**
3. Phase 4: User Story 2 (Project Organization)
4. Phase 5: User Story 3 (Calendar View)
5. Phase 6: User Story 4 (Tags and Filters)
6. Phase 7: User Story 5 (Statistics)
7. Phase 8: User Story 6 (Settings)
8. Phase 9: Search
9. Phase 10: Polish

**Parallel (if team capacity allows)**:
1. Phase 1 + Phase 2 together (team effort)
2. Once Foundational completes:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 6 (Settings - least dependencies)
3. After US1 completes:
   - US3 (Calendar), US4 (Tags), US5 (Stats) can proceed in parallel

### Within Each User Story

- Models before services (dependencies)
- Services before UI components (dependencies)
- Widgets before screens (dependencies)
- Core implementation before integration
- Story complete and validated before moving to next priority

### Parallel Opportunities Per Phase

**Phase 2 (Foundational)**:
- T008, T009, T010 (enums) - parallel
- T013, T014 (backup/autosave) - parallel after T012
- T016 (date utils) - parallel
- T018, T019, T020 (theme, widgets, screens) - parallel

**Phase 3 (US1)**:
- T023, T024, T025, T026 (Task model) - parallel
- T032, T033, T034 (TableWidget) - parallel
- T035, T036 (FormWidget, ModalWidget) - parallel

**Phase 4 (US2)**:
- T045, T046, T047, T048 (Project model) - parallel
- T055 (ProjectCard widget) - parallel with project storage tasks

---

## Parallel Example: Foundational Phase

```bash
# Launch all enums together:
Task T008: "Implement TaskStatus enum in src/todo_master/models/__init__.py"
Task T009: "Implement Priority enum in src/todo_master/models/__init__.py"
Task T010: "Implement ProjectColor enum in src/todo_master/models/__init__.py"

# After storage interface (T011, T012):
Task T013: "Implement BackupManager in src/todo_master/storage/backup.py"
Task T014: "Implement AutoSaveManager in src/todo_master/storage/auto_save.py"
Task T016: "Implement date utilities in src/todo_master/utils/date_utils.py"
```

---

## Parallel Example: User Story 1

```bash
# Launch all Task model tasks together:
Task T023: "Create Task dataclass in src/todo_master/models/task.py"
Task T024: "Implement Task.to_dict() and Task.from_dict()"
Task T025: "Implement Task.mark_done() method"
Task T026: "Implement Task.validate() method"

# Launch all widget tasks together:
Task T032: "Create TableWidget in src/todo_master/ui/widgets/table.py"
Task T035: "Create FormWidget in src/todo_master/ui/widgets/form.py"
Task T036: "Create ModalWidget in src/todo_master/ui/widgets/modal.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

This is the **RECOMMENDED** approach for initial development:

1. ✅ Complete Phase 1: Setup (~7 tasks)
2. ✅ Complete Phase 2: Foundational (~15 tasks) - CRITICAL blocker
3. ✅ Complete Phase 3: User Story 1 (~22 tasks)
4. **STOP and VALIDATE**:
   - Can create tasks with all fields
   - Can view task list with proper rendering
   - Can mark tasks complete
   - Can edit task details
   - Can delete tasks with undo
   - Data persists across restarts
   - Virtual scrolling works smoothly
5. **DEPLOY/DEMO MVP**: Working task management application

**Why this works**: User Story 1 provides complete basic task management value. Users can start tracking tasks immediately. Each subsequent story adds orthogonal value without breaking existing functionality.

### Incremental Delivery (Recommended for Production)

After MVP validation:

1. **Foundation** (Phases 1-2): ~22 tasks → **Checkpoint: Foundation ready**
2. **MVP** (+ Phase 3): +22 tasks → **Checkpoint: Basic task management working** → Deploy/Demo
3. **+Projects** (+ Phase 4): +20 tasks → **Checkpoint: Task organization working** → Deploy/Demo
4. **+Calendar** (+ Phase 5): +14 tasks → **Checkpoint: Timeline view working** → Deploy/Demo
5. **+Tags/Filters** (+ Phase 6): +20 tasks → **Checkpoint: Advanced organization working** → Deploy/Demo
6. **+Statistics** (+ Phase 7): +21 tasks → **Checkpoint: Analytics working** → Deploy/Demo
7. **+Settings** (+ Phase 8): +19 tasks → **Checkpoint: Customization working** → Deploy/Demo
8. **+Search** (+ Phase 9): +8 tasks → **Checkpoint: Global search working** → Deploy/Demo
9. **Polish** (Phase 10): +20 tasks → **Checkpoint: Production-ready** → Final release

Each checkpoint delivers independently valuable functionality.

### Parallel Team Strategy

With 3 developers available after Foundation completes:

**Week 1**: Foundation (all together)
- Complete Phases 1-2 as team effort
- Critical: Ensure storage, models, base UI working

**Week 2**: Parallel user stories
- Developer A: Phase 3 (User Story 1 - Task Management)
- Developer B: Phase 4 (User Story 2 - Projects)
- Developer C: Phase 8 (User Story 6 - Settings - least dependencies)

**Week 3**: Parallel user stories
- Developer A: Phase 5 (User Story 3 - Calendar)
- Developer B: Phase 6 (User Story 4 - Tags/Filters)
- Developer C: Phase 7 (User Story 5 - Statistics)

**Week 4**: Integration & Polish
- All developers: Phase 9 (Search) + Phase 10 (Polish)
- Integration testing across all stories
- Performance optimization

---

## Task Statistics

- **Total Tasks**: 166
- **Setup Tasks**: 7 (Phase 1)
- **Foundational Tasks**: 15 (Phase 2) - BLOCKING
- **User Story 1 Tasks**: 22 (Phase 3) - MVP
- **User Story 2 Tasks**: 20 (Phase 4)
- **User Story 3 Tasks**: 14 (Phase 5)
- **User Story 4 Tasks**: 20 (Phase 6)
- **User Story 5 Tasks**: 21 (Phase 7)
- **User Story 6 Tasks**: 19 (Phase 8)
- **Search Tasks**: 8 (Phase 9)
- **Polish Tasks**: 20 (Phase 10)

**Parallel Opportunities**: 67 tasks marked [P] can run in parallel with other tasks in same phase

**MVP Scope**: Phases 1-3 = 44 tasks = minimum viable product

---

## Notes

- **[P] marker**: Tasks that can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story] label**: Maps each task to its user story for traceability (US1-US6)
- **Independent stories**: Each user story can be tested independently after its phase completes
- **Constitution compliance**: Virtual scrolling (T147), performance benchmarks (T148-T149), backup management (T154)
- **No tests**: Tests not requested in specification, so focus is on implementation only
- **Cross-platform**: Windows compatibility via windows-curses (T002, T162)
- **Commit strategy**: Commit after each logical group of tasks or at end of each user story phase

---

## Validation Checklist

Before considering implementation complete:

- [ ] All 6 user stories independently functional
- [ ] All 75 functional requirements (FR-001 to FR-075) implemented
- [ ] All 26 success criteria (SC-001 to SC-026) validated
- [ ] Performance targets met (<50ms render, <1s search, <2s startup)
- [ ] Data persistence reliable (auto-save, backups, corruption recovery)
- [ ] Cross-platform compatibility verified (Linux, macOS, Windows)
- [ ] All 6 screens accessible via keyboard shortcuts
- [ ] Help system comprehensive and accurate
- [ ] Documentation complete (user guide, keyboard shortcuts, developer guide)
