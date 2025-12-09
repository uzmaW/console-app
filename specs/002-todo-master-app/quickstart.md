# Quick Start Guide: Todo Master Development

**Feature**: 002-todo-master-app
**Date**: 2025-12-09
**Phase**: Phase 1 - Developer Onboarding

## Prerequisites

- **Python**: 3.11 or higher
- **Terminal**: UTF-8 support, 80x24 minimum size
- **uv**: Fast Python package manager (recommended)

## Installation

### 1. Install uv (Package Manager)

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### 2. Clone and Setup Project

```bash
# Clone repository
git clone <repository-url>
cd todo-console-app

# Checkout feature branch
git checkout 002-todo-master-app

# Initialize Python environment with uv
uv venv

# Activate virtual environment
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"
```

### 3. Install Platform-Specific Dependencies

**Windows Only**:
```bash
uv pip install windows-curses
```

**All Platforms**:
```bash
# Core dependencies (from pyproject.toml)
uv pip install python-dateutil rapidfuzz

# Development dependencies
uv pip install pytest pytest-cov pytest-mock ruff
```

## Project Structure

```
todo-console-app/
├── src/
│   └── todo_master/          # Main application package
│       ├── models/           # Data models (Task, Project, etc.)
│       ├── storage/          # JSON storage layer
│       ├── ui/               # Curses UI components
│       ├── services/         # Business logic
│       └── utils/            # Helper functions
│
├── tests/
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── fixtures/             # Test data
│
├── specs/
│   └── 002-todo-master-app/  # Feature specifications
│       ├── spec.md           # Requirements
│       ├── plan.md           # Architecture plan
│       ├── data-model.md     # Data models
│       ├── research.md       # Technology decisions
│       └── contracts/        # API contracts
│
└── pyproject.toml            # Project configuration
```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/todo_master --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py

# Run tests matching pattern
pytest tests/ -k "test_task"

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Development Workflow

### 1. Create a New Feature Module

```python
# src/todo_master/models/task.py
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass
class Task:
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    # ... other fields
```

### 2. Write Tests First (TDD)

```python
# tests/unit/test_task.py
from todo_master.models import Task

def test_create_task():
    task = Task(title="Test Task")
    assert task.title == "Test Task"
    assert task.id is not None
```

### 3. Run Tests

```bash
pytest tests/unit/test_task.py -v
```

### 4. Implement Feature

```python
# Implement the Task class to pass tests
```

### 5. Verify Coverage

```bash
pytest --cov=src/todo_master/models --cov-report=term-missing
```

## Running the Application

```bash
# Run from source (development)
python -m todo_master.main

# Or with uv
uv run python -m todo_master.main
```

## Code Quality

### Linting with Ruff

```bash
# Check code quality
ruff check src/

# Auto-fix issues
ruff check src/ --fix

# Format code
ruff format src/
```

### Type Checking (Optional)

```bash
# Install mypy
uv pip install mypy

# Run type checker
mypy src/todo_master/
```

## Debugging

### Debug Mode

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# In your code
logger = logging.getLogger(__name__)
logger.debug("Task created: %s", task.id)
```

### Testing Curses UI

```bash
# Test in specific terminal size
python -m todo_master.main

# Check terminal capabilities
python -c "import curses; curses.wrapper(lambda s: print(curses.COLORS))"
```

## Common Tasks

### Add New Dependency

```bash
# Add runtime dependency
uv pip install package-name

# Add to pyproject.toml
# Edit pyproject.toml manually or use:
uv add package-name
```

### Create New Test Fixture

```python
# tests/fixtures/sample_data.py
from todo_master.models import Task, Priority

SAMPLE_TASKS = [
    Task(title="Sample Task 1", priority=Priority.HIGH),
    Task(title="Sample Task 2", priority=Priority.MEDIUM),
]
```

### Run Performance Benchmarks

```python
# tests/performance/bench_render.py
import time

def benchmark_render(task_count=1000):
    start = time.perf_counter()
    # ... rendering code
    elapsed = (time.perf_counter() - start) * 1000
    assert elapsed < 50, f"Rendering took {elapsed}ms (>50ms limit)"
```

## Documentation

### Generate API Docs

```bash
# Install pdoc
uv pip install pdoc

# Generate HTML docs
pdoc src/todo_master/ -o docs/api/

# View docs
open docs/api/index.html
```

### View Specifications

All project specifications are in `specs/002-todo-master-app/`:

- **spec.md**: Complete feature requirements
- **plan.md**: Architecture and implementation plan
- **data-model.md**: Data entity definitions
- **research.md**: Technology research and decisions
- **contracts/**: API interface contracts

## Troubleshooting

### Issue: Curses not working on Windows

**Solution**: Install windows-curses
```bash
uv pip install windows-curses
```

### Issue: Terminal too small error

**Solution**: Resize terminal to at least 80x24
```bash
# Check current size
python -c "import os; print(os.get_terminal_size())"
```

### Issue: Import errors

**Solution**: Ensure package is installed in editable mode
```bash
uv pip install -e .
```

### Issue: Tests failing with file not found

**Solution**: Run tests from project root
```bash
cd /path/to/todo-console-app
pytest tests/
```

## Next Steps

1. **Read the specification**: Start with `specs/002-todo-master-app/spec.md`
2. **Understand the architecture**: Review `specs/002-todo-master-app/plan.md`
3. **Study the data model**: Read `specs/002-todo-master-app/data-model.md`
4. **Check API contracts**: Review `specs/002-todo-master-app/contracts/`
5. **Run `/sp.tasks`**: Generate detailed implementation tasks

## Resources

- **Python Curses Programming**: https://docs.python.org/3/howto/curses.html
- **uv Documentation**: https://github.com/astral-sh/uv
- **pytest Documentation**: https://docs.pytest.org/
- **Project Constitution**: `.specify/memory/constitution.md`

## Getting Help

- Review existing tests for examples
- Check inline code documentation
- Consult specification documents in `specs/`
- Review Architecture Decision Records (ADRs) when available

---

**Ready to start coding?** Run `/sp.tasks` to generate the implementation task list!
