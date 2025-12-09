# Console Todo App Constitution

<!--
Sync Impact Report - Version 1.0.0 (Initial Constitution)
=========================================================
Version change: [none] → 1.0.0 (initial ratification)
Modified principles: N/A (initial version)
Added sections:
  - Core Principles (8 principles defined)
  - Architecture Requirements
  - Quality Standards
  - Governance

Templates requiring updates:
  ✅ .specify/templates/plan-template.md (reviewed - compatible)
  ✅ .specify/templates/spec-template.md (reviewed - compatible)
  ✅ .specify/templates/tasks-template.md (reviewed - compatible)
  ✅ .claude/commands/*.md (reviewed - no conflicts)

Follow-up TODOs: None
-->

## Core Principles

### I. Keyboard-First Interaction
Every action in the application MUST be accessible via keyboard shortcuts. Mouse interaction is optional but never required. Hot keys MUST be discoverable, memorable, and conflict-free.

**Rationale**: Power users operate primarily via keyboard. Requiring mouse interaction breaks flow and reduces productivity. This principle ensures the application serves its target audience effectively.

### II. Multi-View Organization
The application MUST provide multiple perspectives on the same task data (by project, by priority, by tag, by date). Views MUST share a common data model and stay synchronized. Users MUST be able to switch views with single-key commands.

**Rationale**: Different workflows require different mental models. A single view forces users into one way of thinking. Multiple views enable users to organize tasks according to their current context.

### III. Performance Budget (NON-NEGOTIABLE)
All user interactions MUST complete in under 50 milliseconds. The application MUST handle 1000+ tasks without observable lag. Startup time MUST be under 500ms.

**Rationale**: Console applications compete with native shell commands. Any perceived lag destroys the user experience. Performance is not a feature—it's a requirement.

### IV. Data Persistence Reliability
Task data MUST be persisted immediately on every change. The application MUST never lose data, even on abnormal termination. Storage MUST use JSON format for human readability and version control compatibility.

**Rationale**: Task data is mission-critical. Users must trust that their work is safe. Human-readable storage enables debugging, version control, and manual recovery if needed.

### V. Zero Configuration
The application MUST work immediately after installation with sensible defaults. Configuration files are optional. First-run experience MUST create initial structure automatically.

**Rationale**: Complex setup creates adoption friction. Power users appreciate customization but require a working baseline instantly.

### VI. Progressive Disclosure
Core functionality MUST be simple and immediately accessible. Advanced features MUST be discoverable but not intrusive. Help MUST be context-sensitive and available via hotkey.

**Rationale**: New users need quick wins. Expert users need power. Progressive disclosure serves both without compromising either.

### VII. Extensible Architecture
The application MUST support a plugin system for custom views and commands. Plugins MUST be isolated, safe, and documented. Core functionality MUST remain stable as plugins evolve.

**Rationale**: No single application serves all workflows. Extensibility enables community innovation while maintaining reliability for non-technical users.

### VIII. Fail Gracefully
Errors MUST provide actionable messages. Corrupted data MUST be recoverable through backups or manual intervention. The application MUST never crash without preserving state.

**Rationale**: Software fails. Users judge applications by how they handle failure. Graceful degradation and recovery build trust and reduce support burden.

## Architecture Requirements

### Data Model
- Single source of truth: JSON file at `~/.todoconsole/tasks.json` (or user-configured path)
- Automatic backups before destructive operations
- Schema versioning for safe migrations
- Immutable task IDs for cross-reference stability

### User Interface
- Built with a terminal UI framework (e.g., `blessed`, `ncurses`, `tui-rs`)
- Clear visual hierarchy using colors, borders, and spacing
- Status bar showing context (view, filters, counts)
- Single-key command mode for power operations

### Modules
- `src/models/`: Task data structures and validation
- `src/views/`: Different perspectives (list, kanban, calendar, etc.)
- `src/persistence/`: JSON storage and backup management
- `src/input/`: Keyboard handling and command parsing
- `src/plugins/`: Plugin loader and API
- `src/cli/`: Entry point and initialization

### Testing
- Unit tests for data model and persistence logic
- Integration tests for view switching and state management
- Performance benchmarks for 1000+ task scenarios
- Manual testing checklist for keyboard navigation

## Quality Standards

### Performance
- Task list rendering: < 50ms for 1000 tasks
- View switching: < 20ms
- Save operations: < 10ms
- Startup: < 500ms

### Usability
- All core actions reachable within 3 keystrokes
- Help accessible from any screen via `?`
- Undo/redo support for destructive operations
- Visual feedback for all state changes

### Reliability
- 100% data persistence: No lost tasks under normal or abnormal termination
- Automatic backup rotation (keep last 10 versions)
- Atomic file writes to prevent partial corruption
- Schema validation on load with fallback to backup

### Security
- No network access by default
- Plugin sandboxing where technically feasible
- No execution of untrusted code
- Clear security warnings for extensibility features

## Governance

This constitution establishes the non-negotiable principles for the Console Todo App. All design decisions, features, and code changes MUST align with these principles.

### Amendment Process
1. Proposed changes MUST be documented in an issue or ADR
2. Team approval required (or user for solo projects)
3. Version bump following semantic versioning
4. Migration plan for affected components
5. Update dependent templates and documentation

### Compliance Review
- All pull requests MUST verify alignment with principles
- Performance budgets MUST be enforced in CI/CD
- Architecture decisions violating principles MUST provide explicit justification in ADRs
- Complexity beyond stated requirements MUST be challenged

### Versioning Rules
- **MAJOR**: Principle removal, redefinition, or incompatible governance changes
- **MINOR**: New principle added or material guidance expansion
- **PATCH**: Clarifications, wording improvements, non-semantic fixes

**Version**: 1.0.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09
