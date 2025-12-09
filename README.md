# Todo Master

A powerful multi-screen terminal-based task management application with curses UI.

## 🚧 Current Status: Minimal Working Application (MVP)

**Version**: 1.0.0-alpha
**Status**: ✅ Core functionality implemented and working

This is a **minimal working version** with essential task management features. See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for complete details on what's implemented and [QUICKSTART.md](QUICKSTART.md) for usage instructions.

## Features

### ✅ Implemented (v1.0.0-alpha)

- **Task Management**: Create, view, complete, and delete tasks
- **Keyboard-First**: Complete keyboard control with vim-style navigation (j/k, arrows)
- **Status Tracking**: Visual status indicators (○ todo, ● done) with timestamps
- **Undo Delete**: 5-second undo window for accidental deletions
- **Auto-Save**: Automatic data persistence every 5 seconds
- **Backup Management**: Maintains 5 automatic backups for data recovery
- **JSON Storage**: Human-readable storage at ~/.config/todo-master/
- **Cross-Platform**: Works on Linux, macOS, and Windows
- **Priority Support**: Task priority levels (low, medium, high, urgent)

### 🔜 Planned Features

- **Edit Tasks**: Modify existing task details
- **Multi-screen Interface**: Dedicated screens for Projects, Calendar, Tags, Statistics, Settings
- **Project Organization**: Organize tasks into projects (Inbox, Work, Personal, etc.)
- **Calendar Views**: Timeline view with date grouping (Overdue, Today, Tomorrow, etc.)
- **Tags & Filters**: Tag tasks and create smart filters with query syntax
- **Statistics**: Track productivity with completion rates and analytics
- **Search**: Fuzzy search across tasks
- **Custom Themes**: Customize colors and appearance

## Requirements

- Python 3.11 or higher
- Terminal with UTF-8 support
- Minimum terminal size: 80x24 (recommended: 120x40)
- 256-color terminal recommended (falls back to 8 colors)

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd todo-console-app

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -e .

# For development
pip install -e ".[dev]"
```

### Windows Setup

On Windows, you'll need the windows-curses package:

```bash
pip install windows-curses
```

### Usage

```bash
# Run the application
todo-master

# Or run directly from source
python -m todo_master.main
```

## Keyboard Shortcuts

### Global Navigation
- `j/k`: Move down/up
- `g/G`: Go to top/bottom
- `Tab`: Next screen
- `1-6`: Jump to screen 1-6
- `?`: Show help
- `q`: Quit
- `Esc`: Cancel/Close

### Task Management
- `n`: New task
- `e`: Edit task
- `d` or `Space`: Toggle done
- `x`: Delete task
- `u`: Undo delete (5 second window)
- `p`: Move to project
- `t`: Edit tags
- `f`: Apply filter
- `/`: Search tasks
- `1-5`: Set priority (low to urgent)

### Calendar View
- `r`: Reschedule task
- `+/-`: Adjust date ±1 day
- `t`: Jump to today
- `w`: Week view
- `m`: Month view

## Project Structure

```
todo-console-app/
├── src/todo_master/        # Main application code
│   ├── models/             # Data models (Task, Project, etc.)
│   ├── storage/            # JSON storage and backup
│   ├── ui/                 # Curses UI components
│   │   ├── widgets/        # Reusable UI widgets
│   │   └── screens/        # Screen implementations
│   ├── services/           # Business logic services
│   └── utils/              # Utility functions
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test data
├── docs/                   # Documentation
└── specs/                  # Feature specifications
```

## Data Storage

All data is stored in JSON format at:
- Linux/macOS: `~/.config/todo-master/`
- Windows: `%USERPROFILE%\.config\todo-master\`

Files:
- `tasks.json`: All tasks
- `projects.json`: Projects
- `settings.json`: User preferences
- `backups/`: Automatic backups (5 most recent)

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/todo_master --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py
```

### Code Quality

```bash
# Lint code
ruff check src/

# Format code
ruff format src/
```

### Documentation

See the `docs/` directory for detailed documentation:
- User Guide
- Keyboard Shortcuts Reference
- Developer Guide

## Performance Targets

- Task list rendering: <50ms for 1000+ tasks (virtual scrolling)
- Search results: <1 second for 500+ tasks
- Application startup: <2 seconds
- Screen transitions: <0.5 seconds
- Auto-save operation: <10ms

## Troubleshooting

### Terminal too small error
Resize your terminal to at least 80x24 characters.

### Curses not working on Windows
Install windows-curses: `pip install windows-curses`

### Colors not displaying correctly
Ensure your terminal supports 256 colors. The app will fall back to 8 colors if needed.

### Data corruption
The app maintains 5 automatic backups. If data is corrupted, it will automatically recover from the most recent valid backup.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run tests and linting
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Authors

Todo Master Team

## Acknowledgments

- Built with Python's standard library `curses`
- Uses `python-dateutil` for date parsing
- Uses `rapidfuzz` for fuzzy search
