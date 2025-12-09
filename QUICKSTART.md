# Todo Master - Quick Start Guide

## Installation

```bash
# Install the application
pip install -e .
```

## First Launch

```bash
# Run Todo Master
todo-master
```

On first launch, the application will:
1. Create config directory: `~/.config/todo-master/`
2. Initialize empty task database: `tasks.json`
3. Display the main task list screen (empty)

## Basic Usage

### Creating Your First Task

1. Press `n` to open the new task dialog
2. Type your task title (e.g., "Buy groceries")
3. Press `Enter` to create the task
4. Press `Esc` to cancel

### Navigating Tasks

- `j` or `↓` - Move down to next task
- `k` or `↑` - Move up to previous task

The selected task will be highlighted.

### Marking Tasks Complete

1. Navigate to a task using `j`/`k`
2. Press `d` to toggle done/todo status
3. Done tasks show a filled circle (●)
4. Todo tasks show an empty circle (○)

### Deleting Tasks

1. Navigate to the task you want to delete
2. Press `x` to delete
3. The task is removed and added to undo buffer

### Undoing Deletion

If you accidentally delete a task:
1. Press `u` within 5 seconds
2. The task will be restored

After 5 seconds, the undo buffer is cleared.

### Quitting

Press `q` to quit the application. All changes are automatically saved.

## Example Workflow

```
1. Launch: todo-master
2. Press 'n' → Type "Buy milk" → Enter
3. Press 'n' → Type "Finish report" → Enter
4. Press 'n' → Type "Call dentist" → Enter
5. Press 'k' twice to select "Buy milk"
6. Press 'd' to mark as done
7. Press 'q' to quit
```

When you restart `todo-master`, all tasks will be loaded from disk.

## Data Storage

All data is stored in JSON format:
- **Location**: `~/.config/todo-master/tasks.json`
- **Backups**: `tasks.json.1` through `tasks.json.5` (automatic rotation)
- **Format**: Human-readable JSON (can be edited manually if needed)

## Auto-Save

The application automatically saves your tasks:
- **Frequency**: Every 5 seconds
- **Trigger**: Any modification (create, update, delete, toggle status)
- **Backup**: Automatic backup before each save

You don't need to manually save - just quit when done!

## Keyboard Reference

| Key | Action |
|-----|--------|
| `n` | Create new task |
| `d` | Toggle task done/todo |
| `x` | Delete task |
| `u` | Undo last delete (5 sec window) |
| `j` or `↓` | Move down |
| `k` or `↑` | Move up |
| `q` | Quit application |

## Tips

### Organizing Tasks
- Use clear, descriptive titles (1-200 characters)
- Tasks are sorted by priority (high priority first)
- Create tasks quickly with `n` shortcut

### Workflow Efficiency
- Use `j`/`k` vim-style navigation for speed
- Mark tasks done with `d` as you complete them
- Create new tasks throughout the day
- Review and delete old tasks with `x`

### Recovery
- If you accidentally delete: press `u` immediately
- If something goes wrong: backups are in `~/.config/todo-master/tasks.json.1`
- Manual recovery: copy a backup file over `tasks.json`

## Troubleshooting

### Application won't start
```bash
# Check if installed correctly
pip show todo-master

# Reinstall if needed
pip install -e . --force-reinstall
```

### Terminal display issues
- Ensure your terminal supports curses (most Unix terminals do)
- Try resizing your terminal window
- Minimum recommended size: 80x24 characters

### Lost data
1. Check backup files: `~/.config/todo-master/tasks.json.1` through `.5`
2. Copy a backup: `cp tasks.json.2 tasks.json`
3. Restart the application

### Tasks not saving
- Check disk space: `df -h`
- Check permissions: `ls -la ~/.config/todo-master/`
- Look for errors in terminal after quitting

## What's Next?

This is a minimal working version. Future features planned:
- Edit existing tasks
- Project organization
- Tag management
- Calendar views
- Search and filters
- Statistics dashboard
- Custom themes
- Keyboard customization

See `IMPLEMENTATION_SUMMARY.md` for full roadmap.

## Getting Help

If you encounter issues:
1. Check this guide first
2. Review `IMPLEMENTATION_SUMMARY.md` for technical details
3. Check backup files in `~/.config/todo-master/`
4. Examine `tasks.json` (it's human-readable JSON)

## Example Tasks to Try

Create these tasks to test the application:

```
n → "Learn Todo Master shortcuts" → Enter
n → "Review completed tasks" → Enter
n → "Delete unnecessary tasks" → Enter
n → "Practice undo feature" → Enter
```

Then practice:
- Marking some done with `d`
- Deleting one with `x`
- Undoing with `u`
- Navigating with `j`/`k`

Happy task managing! 🎯
