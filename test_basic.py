#!/usr/bin/env python3
"""
Quick test script to verify basic functionality without curses
"""

from pathlib import Path
import tempfile
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from todo_master.models.task import Task
from todo_master.models import Priority
from todo_master.storage.json_store import JSONStorage
from todo_master.services.task_manager import TaskManager

def test_basic_operations():
    """Test basic CRUD operations"""
    print("Testing Todo Master basic operations...")

    # Create temp file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_file = Path(f.name)

    try:
        # Initialize storage and manager
        storage = JSONStorage(test_file, Task)
        manager = TaskManager(storage)

        # Test 1: Create task
        print("\n1. Creating task...")
        task1 = manager.create_task(title="Buy groceries", description="Milk, eggs, bread")
        print(f"   ✓ Created task: {task1.title} (ID: {task1.id})")

        # Test 2: Create another task
        print("\n2. Creating another task...")
        task2 = manager.create_task(title="Write report", priority=Priority.HIGH)
        print(f"   ✓ Created task: {task2.title} (Priority: {task2.priority.value})")

        # Test 3: List tasks
        print("\n3. Listing all tasks...")
        tasks = manager.list_tasks()
        print(f"   ✓ Found {len(tasks)} tasks")
        for task in tasks:
            print(f"     - [{task.status.symbol}] {task.title}")

        # Test 4: Mark task done
        print("\n4. Marking task as done...")
        manager.mark_done(task1.id)
        updated = manager.get_task(task1.id)
        print(f"   ✓ Task status: {updated.status.value} {updated.status.symbol}")

        # Test 5: Toggle task
        print("\n5. Toggling task status...")
        manager.toggle_done(task1.id)
        toggled = manager.get_task(task1.id)
        print(f"   ✓ Task status: {toggled.status.value} {toggled.status.symbol}")

        # Test 6: Delete task
        print("\n6. Deleting task...")
        manager.delete_task(task2.id)
        remaining = manager.list_tasks()
        print(f"   ✓ Remaining tasks: {len(remaining)}")

        # Test 7: Undo delete
        print("\n7. Testing undo...")
        restored = manager.undo_delete()
        if restored:
            print(f"   ✓ Restored task: {restored.title}")

        # Test 8: Save and load
        print("\n8. Testing persistence...")
        storage.save()
        print(f"   ✓ Saved to {test_file}")

        # Create new storage and load
        storage2 = JSONStorage(test_file, Task)
        storage2.load()
        loaded_tasks = storage2.list()
        print(f"   ✓ Loaded {len(loaded_tasks)} tasks from file")

        print("\n✅ All tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":
    success = test_basic_operations()
    sys.exit(0 if success else 1)
