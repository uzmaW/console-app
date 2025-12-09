"""
Backup management for data files

Handles automatic backup creation, rotation, and recovery (FR-057).
"""

import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional


class BackupManager:
    """
    Manages automatic backups of data files (FR-057)

    Features:
    - Automatic backup before destructive operations
    - Backup rotation (keep N most recent)
    - Timestamped backup names
    - Easy restoration
    """

    def __init__(self, data_dir: Path, backup_count: int = 5):
        """
        Initialize backup manager

        Args:
            data_dir: Directory containing data files
            backup_count: Number of backups to maintain (FR-057: default 5)
        """
        self.data_dir = data_dir
        self.backup_dir = data_dir / "backups"
        self.backup_count = backup_count

        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, file_path: Path) -> Optional[str]:
        """
        Create backup of a file

        Args:
            file_path: Path to file to backup

        Returns:
            Path to created backup file, or None if file doesn't exist

        Note:
            Backups are numbered .1 (most recent) to .N (oldest)
        """
        if not file_path.exists():
            return None

        # Rotate existing backups
        self._rotate_backups(file_path.name)

        # Create new backup at position 1
        backup_path = self.backup_dir / f"{file_path.name}.1"
        shutil.copy2(file_path, backup_path)

        return str(backup_path)

    def create_timestamped_backup(self, file_path: Path) -> Optional[str]:
        """
        Create timestamped backup (for manual backups)

        Args:
            file_path: Path to file to backup

        Returns:
            Path to created backup file
        """
        if not file_path.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = self.backup_dir / backup_name

        shutil.copy2(file_path, backup_path)
        return str(backup_path)

    def restore_backup(self, backup_path: Path, target_path: Path) -> bool:
        """
        Restore file from backup

        Args:
            backup_path: Path to backup file
            target_path: Path where file should be restored

        Returns:
            True if successful

        Raises:
            FileNotFoundError: If backup doesn't exist
            IOError: If restoration fails
        """
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")

        # Create backup of current file before restoring
        if target_path.exists():
            self.create_backup(target_path)

        # Restore from backup
        shutil.copy2(backup_path, target_path)
        return True

    def list_backups(self, filename: str) -> List[Path]:
        """
        List all backups for a file

        Args:
            filename: Name of the data file

        Returns:
            List of backup paths, sorted by recency (newest first)
        """
        backups = []

        # Numbered backups (.1, .2, .3, etc.)
        for i in range(1, self.backup_count + 1):
            backup_path = self.backup_dir / f"{filename}.{i}"
            if backup_path.exists():
                backups.append(backup_path)

        # Timestamped backups
        stem = Path(filename).stem
        suffix = Path(filename).suffix
        pattern = f"{stem}_*{suffix}"
        timestamped = sorted(
            self.backup_dir.glob(pattern),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        backups.extend(timestamped)

        return backups

    def get_latest_backup(self, filename: str) -> Optional[Path]:
        """
        Get most recent backup for a file

        Args:
            filename: Name of the data file

        Returns:
            Path to most recent backup, or None if no backups exist
        """
        backup_path = self.backup_dir / f"{filename}.1"
        if backup_path.exists():
            return backup_path

        # Try timestamped backups
        backups = self.list_backups(filename)
        return backups[0] if backups else None

    def clean_old_backups(self, filename: str):
        """
        Remove backups beyond the retention limit

        Args:
            filename: Name of the data file
        """
        # Remove numbered backups beyond limit
        for i in range(self.backup_count + 1, self.backup_count + 20):
            backup_path = self.backup_dir / f"{filename}.{i}"
            if backup_path.exists():
                backup_path.unlink()

    def _rotate_backups(self, filename: str):
        """
        Rotate numbered backups (shift .1 -> .2, .2 -> .3, etc.)

        Args:
            filename: Name of the data file
        """
        # Shift existing backups
        for i in range(self.backup_count - 1, 0, -1):
            old_backup = self.backup_dir / f"{filename}.{i}"
            new_backup = self.backup_dir / f"{filename}.{i + 1}"

            if old_backup.exists():
                if new_backup.exists():
                    new_backup.unlink()
                old_backup.rename(new_backup)

    def get_backup_info(self, backup_path: Path) -> dict:
        """
        Get information about a backup file

        Args:
            backup_path: Path to backup file

        Returns:
            Dictionary with backup metadata
        """
        if not backup_path.exists():
            return {}

        stat = backup_path.stat()
        return {
            "path": str(backup_path),
            "name": backup_path.name,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_mtime),
            "created_iso": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }


__all__ = ["BackupManager"]
