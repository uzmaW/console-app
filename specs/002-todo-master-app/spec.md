# Feature Specification: Todo Master Console Application

**Feature Branch**: `002-todo-master-app`
**Created**: 2025-12-09
**Status**: Draft
**Input**: User description: "Multi-screen console todo application with curses UI for task management, project organization, calendar view, tags/filters, statistics, and settings"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Task Management (Priority: P1)

As a user, I need to create, view, edit, and complete tasks in a main task list so I can track my daily work and responsibilities.

**Why this priority**: Core functionality that delivers immediate value. Without this, the application has no purpose. This is the minimum viable product.

**Independent Test**: Can be fully tested by creating a task, viewing it in the list, marking it complete, editing its details, and deleting it. Delivers immediate task tracking value.

**Acceptance Scenarios**:

1. **Given** I launch the application, **When** I press 'n' to create a new task, **Then** I see a form to enter task title, description, priority, and due date
2. **Given** I have created a task, **When** I view the main task list, **Then** I see the task displayed with its title, priority indicator, and due date
3. **Given** I have selected a task, **When** I press 'd' or Space, **Then** the task is marked as done with a checkbox and completion timestamp
4. **Given** I have selected a task, **When** I press 'e', **Then** I can edit the task's title, description, priority, due date, and tags
5. **Given** I have selected a task, **When** I press 'x' and confirm, **Then** the task is deleted and I see an undo notification for 5 seconds
6. **Given** I am viewing the task list, **When** I use j/k keys, **Then** I can navigate up and down through tasks
7. **Given** I have multiple tasks, **When** I press '1-5' on a selected task, **Then** the task priority is updated accordingly

---

### User Story 2 - Project Organization (Priority: P2)

As a user, I need to organize tasks into projects (Inbox, Work, Personal, etc.) so I can separate different areas of my life and focus on specific contexts.

**Why this priority**: Adds organizational structure that significantly improves usability for users with multiple responsibilities. Common use case for productivity apps.

**Independent Test**: Can be fully tested by creating projects, assigning tasks to projects, viewing project-specific task lists, and filtering tasks by project. Delivers organizational value independent of other features.

**Acceptance Scenarios**:

1. **Given** I launch the application, **When** I navigate to the Projects screen (Tab key), **Then** I see default projects: Inbox, Personal, and Work
2. **Given** I am on the Projects screen, **When** I press 'n', **Then** I can create a new project with a name, description, color, and icon
3. **Given** I have created a project, **When** I view the Projects screen, **Then** I see a project card showing task count, completed count, and overdue count
4. **Given** I am on the main task list, **When** I press 'p' on a selected task, **Then** I can move the task to a different project
5. **Given** I am on the Projects screen, **When** I press Enter on a project, **Then** the project expands/collapses to show its top tasks
6. **Given** I have selected a project, **When** I press 'e', **Then** I can edit the project's name, description, color, and icon
7. **Given** I have selected a project with no active tasks, **When** I press 'a' and confirm, **Then** the project is archived

---

### User Story 3 - Due Date Management with Calendar View (Priority: P3)

As a user, I need to see tasks organized by their due dates in a calendar view so I can understand my upcoming deadlines and plan my time effectively.

**Why this priority**: Enhances time management capabilities. Useful but not essential for basic task tracking. Users can still manage due dates from the main task list.

**Independent Test**: Can be fully tested by assigning due dates to tasks, viewing the calendar screen, and seeing tasks grouped by date buckets (Overdue, Today, Tomorrow, etc.). Delivers timeline visibility independent of other features.

**Acceptance Scenarios**:

1. **Given** I have tasks with due dates, **When** I navigate to the Calendar screen, **Then** I see tasks grouped into: Overdue, Today, Tomorrow, Next 7 days, and Later
2. **Given** I am on the Calendar screen, **When** I view overdue tasks, **Then** I see how many days ago each task was due
3. **Given** I have selected a task in the Calendar, **When** I press 'r', **Then** I can reschedule the task to a new date
4. **Given** I am on the Calendar screen, **When** I press '+' or '-' on a selected task, **Then** the due date adjusts by ±1 day
5. **Given** I am viewing the Calendar, **When** I press 't', **Then** the view jumps to today's date
6. **Given** I am on the Calendar screen, **When** I press 'w', **Then** I see a week view showing the next 7 days with tasks
7. **Given** I am on the Calendar screen, **When** I press 'm', **Then** I see a month calendar grid view

---

### User Story 4 - Tag Management and Smart Filtering (Priority: P4)

As a user, I need to tag tasks with keywords and create custom filters so I can quickly find related tasks and create views for specific contexts (#urgent, #backend, etc.).

**Why this priority**: Power-user feature that adds flexibility. Nice to have but not essential for core task management. Users can still search and browse tasks without tags.

**Independent Test**: Can be fully tested by creating tags, applying them to tasks, creating smart filters, and viewing filtered task lists. Delivers advanced organization independent of other features.

**Acceptance Scenarios**:

1. **Given** I am on the main task list, **When** I press 't' on a selected task, **Then** I can add one or more tags to the task
2. **Given** I navigate to the Tags & Filters screen, **When** I view the tags section, **Then** I see all tags with their usage count
3. **Given** I am on the Tags & Filters screen, **When** I press 'n' in the tags section, **Then** I can create a new tag with a name and color
4. **Given** I have tags on tasks, **When** I view the Tags & Filters screen, **Then** I see predefined smart filters: Today, Urgent, Overdue, This Week, Completed, Inbox
5. **Given** I am on the Tags & Filters screen, **When** I press 'n' in the filters section, **Then** I can create a custom filter with a name, query syntax, and optional hotkey
6. **Given** I have created a filter, **When** I press 'f' and select the filter, **Then** I see tasks matching the filter criteria in the main task list
7. **Given** I am using a filter, **When** I view the main task list, **Then** I see an active filter indicator showing which filter is applied

---

### User Story 5 - Productivity Statistics and Analytics (Priority: P5)

As a user, I want to see statistics about my task completion patterns so I can understand my productivity trends and identify areas for improvement.

**Why this priority**: Insightful but not actionable for task management itself. Users can track and complete tasks without seeing statistics. Valuable for reflection and motivation.

**Independent Test**: Can be fully tested by completing tasks over time, viewing the Statistics screen, and seeing completion rates, task distribution by project/priority, and productivity metrics. Delivers analytical insights independent of other features.

**Acceptance Scenarios**:

1. **Given** I have completed tasks, **When** I navigate to the Statistics screen, **Then** I see overview cards showing: total tasks, completed count, active count, and overdue count
2. **Given** I am on the Statistics screen, **When** I view the completion rate chart, **Then** I see a 7-day bar chart showing daily completion percentages
3. **Given** I have tasks across multiple projects, **When** I view the Statistics screen, **Then** I see a horizontal bar chart showing task count by project
4. **Given** I have tasks with different priorities, **When** I view the Statistics screen, **Then** I see a horizontal bar chart showing task count by priority level
5. **Given** I have used tags on tasks, **When** I view the Statistics screen, **Then** I see a tag cloud showing top tags with their usage counts
6. **Given** I am on the Statistics screen, **When** I press 'p', **Then** I can change the time period to view statistics for: 7 days, 30 days, 90 days, or all time
7. **Given** I am viewing statistics, **When** I press 'r', **Then** the statistics refresh with current data

---

### User Story 6 - Application Settings and Preferences (Priority: P6)

As a user, I need to customize the application's appearance and behavior so I can tailor it to my preferences and workflow.

**Why this priority**: Customization feature that enhances user experience but is not required for core functionality. Users can use the app with default settings.

**Independent Test**: Can be fully tested by navigating to Settings, changing preferences (theme, default project, date format), saving them, and observing the changes persist across sessions. Delivers personalization independent of other features.

**Acceptance Scenarios**:

1. **Given** I navigate to the Settings screen, **When** I view the Appearance section, **Then** I can select theme (Dark/Light/Auto), color scheme, font size, and toggle icons
2. **Given** I am on the Settings screen, **When** I view the Behavior section, **Then** I can set default project, default priority, auto-archive days, confirm deletes, show completed, and sort order
3. **Given** I am on the Settings screen, **When** I view the Date & Time section, **Then** I can select date format, time format (24h/12h), and week start day
4. **Given** I am on the Settings screen, **When** I view the Data section, **Then** I see the storage location and can configure auto-save interval and backup count
5. **Given** I have changed settings, **When** I press 's', **Then** the settings are saved and applied immediately
6. **Given** I am on the Settings screen, **When** I press the Export Data button, **Then** I can export all tasks and projects to a file
7. **Given** I have exported data, **When** I press the Import Data button, **Then** I can import tasks and projects from a previously exported file

---

### Edge Cases

- What happens when the user tries to create a task with an empty title?
  - System displays validation error and requires a non-empty title before saving

- What happens when the terminal window is resized below minimum size (80x24)?
  - System displays a message indicating minimum terminal size requirement and suggests resizing

- What happens when the user has hundreds of tasks and scrolls through the list?
  - System efficiently renders only visible rows to maintain performance

- What happens when two tasks have the same title?
  - System allows duplicate titles since tasks are identified by unique UUIDs

- What happens when the user deletes a project that has active tasks?
  - System shows a confirmation dialog warning about active tasks; if confirmed, tasks are moved to Inbox before project deletion

- What happens when the JSON storage files become corrupted?
  - System attempts to load from the most recent backup file (up to 5 backups maintained)

- What happens when the user presses 'x' to delete but then wants to undo?
  - System shows an undo notification for 5 seconds; pressing 'u' within this window restores the deleted task

- What happens when a filter query has invalid syntax?
  - System displays a syntax error message and doesn't apply the filter, showing available query operators

- What happens when the user has no tasks with due dates and views the Calendar?
  - System displays an empty calendar with a message suggesting to add due dates to tasks

- What happens when the terminal doesn't support 256 colors?
  - System falls back to basic ANSI colors for priority indicators and UI elements

## Requirements *(mandatory)*

### Functional Requirements

**Task Management**
- **FR-001**: System MUST allow users to create tasks with title (required), description, priority, project, tags, and due date
- **FR-002**: System MUST validate that task titles are not empty and are between 1-200 characters
- **FR-003**: System MUST allow users to edit all task properties after creation
- **FR-004**: System MUST allow users to mark tasks as done with a checkbox toggle (Space or 'd' key)
- **FR-005**: System MUST record completion timestamp when a task is marked as done
- **FR-006**: System MUST allow users to delete tasks with confirmation dialog
- **FR-007**: System MUST provide a 5-second undo window after task deletion
- **FR-008**: System MUST support task status values: todo, in_progress, done, archived
- **FR-009**: System MUST support priority levels: low, medium, high, urgent
- **FR-010**: System MUST assign unique UUIDs to each task automatically

**Project Management**
- **FR-011**: System MUST provide three default projects: Inbox (cyan), Personal (green), Work (blue)
- **FR-012**: System MUST allow users to create custom projects with name, description, color, and icon
- **FR-013**: System MUST validate project names are unique and between 1-50 characters
- **FR-014**: System MUST support project colors: red, green, yellow, blue, magenta, cyan, white
- **FR-015**: System MUST allow users to move tasks between projects
- **FR-016**: System MUST display task statistics per project: total tasks, completed count, overdue count
- **FR-017**: System MUST allow users to archive projects
- **FR-018**: System MUST prevent deletion of projects with active tasks (require confirmation and auto-move to Inbox)

**Calendar and Due Dates**
- **FR-019**: System MUST allow users to set due dates on tasks in YYYY-MM-DD format
- **FR-020**: System MUST group tasks in calendar view by: Overdue, Today, Tomorrow, Next 7 days, Later
- **FR-021**: System MUST calculate and display days overdue for past-due tasks
- **FR-022**: System MUST allow users to reschedule tasks by selecting new dates
- **FR-023**: System MUST provide quick date adjustment with +/- keys (±1 day)
- **FR-024**: System MUST support day view, week view, and month view for calendar

**Tags and Filtering**
- **FR-025**: System MUST allow users to apply multiple tags to a single task
- **FR-026**: System MUST track tag usage count across all tasks
- **FR-027**: System MUST provide predefined smart filters: Today, Urgent, Overdue, This Week, Completed, Inbox
- **FR-028**: System MUST allow users to create custom filters with query syntax
- **FR-029**: System MUST support filter query operators: =, !=, <, <=, >, >=, contains, in
- **FR-030**: System MUST support filter query combinators: AND, OR, NOT
- **FR-031**: System MUST allow users to assign optional hotkeys (single characters) to filters
- **FR-032**: System MUST persist active filter state across screen navigation

**Search**
- **FR-033**: System MUST provide global search accessible with Ctrl+F or '/' key
- **FR-034**: System MUST search task titles, descriptions, and tags
- **FR-035**: System MUST support fuzzy matching for search queries
- **FR-036**: System MUST highlight search matches in results
- **FR-037**: System MUST support search syntax shortcuts: p:Project, t:tag, @date, is:status

**Statistics**
- **FR-038**: System MUST calculate and display total tasks, completed tasks, active tasks, and overdue tasks
- **FR-039**: System MUST generate completion rate charts for last 7 days with daily percentages
- **FR-040**: System MUST display task distribution by project and priority as bar charts
- **FR-041**: System MUST show top tags with usage counts
- **FR-042**: System MUST calculate productivity metrics: average completion time, most productive day, current streak
- **FR-043**: System MUST support time period selection: 7 days, 30 days, 90 days, all time
- **FR-044**: System MUST refresh statistics on demand when user presses 'r'

**Settings and Preferences**
- **FR-045**: System MUST persist user settings across sessions
- **FR-046**: System MUST support theme selection: Dark, Light, Auto
- **FR-047**: System MUST allow configuration of default project and default priority
- **FR-048**: System MUST support auto-archive of completed tasks after N days (configurable)
- **FR-049**: System MUST allow users to toggle delete confirmations
- **FR-050**: System MUST support date format customization (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY)
- **FR-051**: System MUST support time format selection: 24-hour or 12-hour
- **FR-052**: System MUST allow users to set week start day (Monday-Sunday)

**Data Persistence**
- **FR-053**: System MUST store tasks in JSON format at ~/.config/todo-master/tasks.json
- **FR-054**: System MUST store projects in JSON format at ~/.config/todo-master/projects.json
- **FR-055**: System MUST store settings in JSON format at ~/.config/todo-master/settings.json
- **FR-056**: System MUST auto-save changes every 5 seconds (configurable)
- **FR-057**: System MUST create automatic backups before saving (maintain 5 most recent backups)
- **FR-058**: System MUST support data export to JSON file
- **FR-059**: System MUST support data import from JSON file
- **FR-060**: System MUST create ~/.config/todo-master/ directory if it doesn't exist

**Navigation and UI**
- **FR-061**: System MUST provide 6 screens: Task List, Projects, Calendar, Tags & Filters, Statistics, Settings
- **FR-062**: System MUST support Tab/Shift+Tab for screen navigation
- **FR-063**: System MUST support number keys (1-6) to jump directly to screens
- **FR-064**: System MUST display current screen indicator in the UI
- **FR-065**: System MUST support vim-style navigation: j/k for up/down, g/G for top/bottom
- **FR-066**: System MUST display hotkey help footer on each screen
- **FR-067**: System MUST support '?' key to show comprehensive help modal
- **FR-068**: System MUST render UI using curses library for terminal graphics
- **FR-069**: System MUST support mouse interactions: click to select, double-click to edit, right-click for context menu
- **FR-070**: System MUST handle Esc key to close modals and cancel operations

**Performance and Constraints**
- **FR-071**: System MUST require minimum terminal size of 80x24 characters
- **FR-072**: System MUST recommend terminal size of 120x40 characters for optimal display
- **FR-073**: System MUST support UTF-8 character encoding for icons and international text
- **FR-074**: System MUST support 256-color terminals for priority indicators and UI elements
- **FR-075**: System MUST efficiently render large task lists (hundreds of tasks) by using virtual scrolling

### Key Entities

- **Task**: Represents a todo item with properties including unique ID (UUID), title (1-200 chars), optional description, status (todo/in_progress/done/archived), priority (low/medium/high/urgent), project assignment, tag list, optional due date, created timestamp, updated timestamp, optional completed timestamp, optional time estimates (estimated and actual in minutes), optional parent task reference for subtasks, and position for ordering

- **Project**: Represents a task collection/category with properties including unique ID (UUID), unique name (1-50 chars), optional description, color (red/green/yellow/blue/magenta/cyan/white), icon/emoji character, created timestamp, archived status flag, and position for display ordering. Has one-to-many relationship with Tasks

- **Tag**: Represents a keyword label for tasks with properties including name (primary key), display color, and computed usage count (number of tasks using this tag). Has many-to-many relationship with Tasks through task tag arrays

- **Filter**: Represents a saved query for viewing task subsets with properties including unique ID (UUID), filter name, query specification (JSON structure with operators and conditions), optional icon/emoji, and optional single-character hotkey. Queries can reference task properties using operators (=, !=, <, >, <=, >=, contains, in) and combinators (AND, OR, NOT)

- **Settings**: Represents user preferences with properties including theme choice (dark/light/auto), color scheme name, default project, default priority, auto-archive period (days), delete confirmation toggle, show completed toggle, sort preference, date format string, time format (24h/12h), week start day, storage location path, auto-save interval, and backup count

- **Statistics**: Computed entity (not persisted) that aggregates task data with properties including total task count, completed today count, overdue count, task counts grouped by priority, task counts grouped by project, overall completion rate percentage, average completion time in minutes, most productive day of week, current consecutive completion streak in days, and selected time period for calculations

## Success Criteria *(mandatory)*

### Measurable Outcomes

**Core Task Management**
- **SC-001**: Users can create a new task with title and priority in under 10 seconds using keyboard shortcuts
- **SC-002**: Users can mark a task as complete with a single keypress (Space or 'd')
- **SC-003**: Users can navigate through a list of 50+ tasks smoothly without noticeable lag
- **SC-004**: Task data is persisted to disk within 5 seconds of any change

**Organization and Discovery**
- **SC-005**: Users can organize tasks into at least 3 projects and switch between project views
- **SC-006**: Users can find a specific task using search in under 5 seconds regardless of total task count
- **SC-007**: Users can create and apply custom filters to view task subsets based on multiple criteria
- **SC-008**: Users can view all overdue tasks in a single dedicated calendar view

**Visual Clarity**
- **SC-009**: Users can distinguish between 4 priority levels using visual indicators (colors/symbols) at a glance
- **SC-010**: Users can see task due dates displayed in human-readable relative format ("Today", "Tomorrow", "3 days ago")
- **SC-011**: Application renders correctly in terminals with minimum size of 80x24 characters
- **SC-012**: All UI elements are visible and usable in both 256-color and basic color terminal modes

**Productivity Insights**
- **SC-013**: Users can view completion statistics for configurable time periods (7/30/90 days, all time)
- **SC-014**: Users can see their daily completion rate displayed as a visual chart
- **SC-015**: Users can identify their most-used tags and projects through statistics visualization

**Data Integrity and Reliability**
- **SC-016**: Application maintains up to 5 automatic backups of task data
- **SC-017**: Users can export all tasks and projects to a portable JSON file
- **SC-018**: Users can import previously exported data without losing information
- **SC-019**: Application recovers from corrupted data files by loading the most recent valid backup

**Usability and Efficiency**
- **SC-020**: Users can access any of the 6 main screens with a single keystroke (number keys 1-6)
- **SC-021**: Users can complete common actions (create, edit, delete, complete tasks) without using a mouse
- **SC-022**: Application displays contextual help showing all available keyboard shortcuts on each screen
- **SC-023**: Users can customize at least 8 appearance and behavior settings to match their preferences

**Performance**
- **SC-024**: Application launches in under 2 seconds on standard hardware
- **SC-025**: Screen transitions (Tab navigation) complete in under 0.5 seconds
- **SC-026**: Search results appear within 1 second for databases with 500+ tasks
