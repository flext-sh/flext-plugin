"""Rollback management for plugin hot reload functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import inspect
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from flext_core.domain.pydantic_base import DomainBaseModel, Field

# Use centralized logger from flext-observability - ELIMINATE DUPLICATION
from flext_observability.logging import get_logger

if TYPE_CHECKING:
    from flext_plugin.core.base import Plugin
    from flext_plugin.hot_reload.state_manager import StateManager

logger = get_logger(__name__)


class RollbackPoint(DomainBaseModel):
    """Represents a rollback point in plugin history."""

    rollback_id: str = Field(description="Unique rollback point identifier")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When rollback point was created",
    )
    description: str = Field(description="Rollback point description")
    plugin_id: str = Field(description="Plugin identifier")
    plugin_version: str = Field(description="Plugin version at rollback point")
    state_snapshot_id: str = Field(description="Associated state snapshot ID")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )


class RollbackHistory(DomainBaseModel):
    """Rollback history for a plugin."""

    plugin_id: str = Field(description="Plugin identifier")
    rollback_points: list[RollbackPoint] = Field(
        default_factory=list,
        description="List of rollback points",
    )
    max_history_size: int = Field(
        default=10,
        description="Maximum number of rollback points to keep",
    )

    def add_rollback_point(self, point: RollbackPoint) -> None:
        """Add a rollback point to the history.

        Args:
            point: The rollback point to add.

        """
        self.rollback_points.append(point)

        # Trim history if needed:
        if len(self.rollback_points) > self.max_history_size:
            # Remove oldest points
            self.rollback_points = self.rollback_points[-self.max_history_size :]

    def get_latest_point(self) -> RollbackPoint | None:
        """Get the latest rollback point.

        Returns:
            The latest rollback point or None if no points exist.

        """
        if not self.rollback_points:
            return None
        return self.rollback_points[-1]

    def get_point_by_id(self, rollback_id: str) -> RollbackPoint | None:
        """Get a rollback point by its ID.

        Args:
            rollback_id: The rollback point ID to search for.

        Returns:
            The rollback point or None if not found.

        """
        for point in self.rollback_points:
            if point.rollback_id == rollback_id:
                return point
        return None


class RollbackManager:
    """Manages rollback operations for plugin hot reload.

    Provides rollback capabilities to recover from failed reload operations or unwanted plugin updates.
    """

    def __init__(
        self, state_manager: StateManager, backup_directory: Path | None = None,
    ) -> None:
        """Initialize rollback manager with state manager and backup directory."""
        self.state_manager = state_manager
        self.backup_directory = backup_directory or Path.cwd() / ".plugin_backups"

        if not self.backup_directory.exists():
            self.backup_directory.mkdir(parents=True, exist_ok=True)

        self._histories: dict[str, RollbackHistory] = {}
        self._plugin_backups: dict[str, dict[str, Path]] = {}

    async def create_rollback_point(
        self, plugin: Plugin, description: str, backup_code: bool = True,
    ) -> str:
        """Create a new rollback point for a plugin.

        Args:
            plugin: The plugin to create a rollback point for.
            description: Description of the rollback point.
            backup_code: Whether to backup the plugin code.

        Returns:
            The ID of the created rollback point.

        """
        plugin_id = plugin.metadata.id
        rollback_id = str(uuid4())

        # Create state snapshot
        snapshot_id = await self.state_manager.create_snapshot(
            description=f"Rollback point: {description}",
            plugin_ids=[plugin_id],
        )

        # Backup plugin code if requested:
        if backup_code:
            backup_path = await self._backup_plugin_code(plugin, rollback_id)
            if plugin_id not in self._plugin_backups:
                self._plugin_backups[plugin_id] = {}
            self._plugin_backups[plugin_id][rollback_id] = backup_path

        # Create rollback point
        point = RollbackPoint(
            rollback_id=rollback_id,
            description=description,
            plugin_id=plugin_id,
            plugin_version=plugin.metadata.version,
            state_snapshot_id=snapshot_id,
            metadata={"code_backed_up": backup_code},
        )

        # Add to history
        if plugin_id not in self._histories:
            self._histories[plugin_id] = RollbackHistory(plugin_id=plugin_id)

        self._histories[plugin_id].add_rollback_point(point)

        logger.info(
            "Created rollback point for plugin %s",
            plugin_id,
            rollback_id=rollback_id,
            description=description,
        )

        return rollback_id

    async def rollback_plugin(
        self, plugin_id: str, rollback_id: str | None = None, restore_code: bool = True,
    ) -> dict[str, Any]:
        """Rollback a plugin to a previous state.

        Args:
            plugin_id: The ID of the plugin to rollback.
            rollback_id: The specific rollback point ID, or None for latest.
            restore_code: Whether to restore the plugin code.

        Returns:
            Dictionary with rollback operation results.

        Raises:
            ValueError: If rollback point is not found.

        """
        # Get rollback history
        history = self._histories.get(plugin_id)
        if not history:
            msg = f"No rollback history for plugin {plugin_id}"
            raise ValueError(msg)

        # Get rollback point
        if rollback_id:
            point = history.get_point_by_id(rollback_id)
        else:
            point = history.get_latest_point()

        if not point:
            msg = f"Rollback point not found: {rollback_id}"
            raise ValueError(msg)

        result = {
            "rollback_id": point.rollback_id,
            "plugin_id": plugin_id,
            "from_version": "unknown",
            "to_version": point.plugin_version,
            "state_restored": False,
            "code_restored": False,
            "errors": [],
        }

        # Restore state
        try:
            restore_results = await self.state_manager.restore_snapshot(
                point.state_snapshot_id,
            )
            result["state_restored"] = restore_results.get(plugin_id, False)
        except Exception as e:
            logger.error(
                "Error restoring state for plugin %s: %s",
                plugin_id,
                e,
                exc_info=True,
            )
            result["errors"].append(f"State restoration failed: {e!s}")

        # Restore code if requested:
        if restore_code and point.metadata.get("code_backed_up"):
            try:
                await self._restore_plugin_code(plugin_id, point.rollback_id)
                result["code_restored"] = True
            except Exception as e:
                logger.error(
                    "Error restoring code for plugin %s: %s",
                    plugin_id,
                    e,
                    exc_info=True,
                )
                result["errors"].append(f"Code restoration failed: {e!s}")

        logger.info(
            "Rolled back plugin %s",
            plugin_id,
            rollback_id=point.rollback_id,
            state_restored=result["state_restored"],
            code_restored=result["code_restored"],
        )

        return result

    async def _backup_plugin_code(self, plugin: Plugin, rollback_id: str) -> Path:
        """Backup plugin code to a file.

        Args:
            plugin: The plugin to backup.
            rollback_id: The rollback point ID.

        Returns:
            Path to the backup file.

        Raises:
            ValueError: If plugin source file cannot be determined.

        """
        plugin_module = inspect.getmodule(plugin.__class__)
        if not plugin_module or not hasattr(plugin_module, "__file__"):
            msg = "Cannot determine plugin module file"
            raise ValueError(msg)

        source_file = Path(plugin_module.__file__)
        if not source_file.exists():
            msg = f"Plugin source file not found: {source_file}"
            raise ValueError(msg)

        # Create backup directory
        plugin_backup_dir = self.backup_directory / plugin.metadata.id
        plugin_backup_dir.mkdir(exist_ok=True)

        # Backup file
        backup_file = plugin_backup_dir / f"{rollback_id}_{source_file.name}"
        shutil.copy2(source_file, backup_file)

        logger.debug(
            "Backed up plugin code",
            plugin_id=plugin.metadata.id,
            source=str(source_file),
            backup=str(backup_file),
        )

        return backup_file

    async def _restore_plugin_code(self, plugin_id: str, rollback_id: str) -> None:
        """Restore plugin code from a backup.

        Args:
            plugin_id: The plugin ID to restore.
            rollback_id: The rollback point ID.

        Raises:
            ValueError: If backup file is not found.

        """
        # Get backup path
        if (
            plugin_id not in self._plugin_backups
            or rollback_id not in self._plugin_backups[plugin_id]
        ):
            msg = f"No code backup found for rollback {rollback_id}"
            raise ValueError(msg)

        backup_file = self._plugin_backups[plugin_id][rollback_id]
        if not backup_file.exists():
            msg = f"Backup file not found: {backup_file}"
            raise ValueError(msg)

        # Determine target path
        # This is simplified - in reality would need to track original location
        target_file = backup_file.parent.parent / backup_file.name.split("_", 1)[1]

        # Restore file
        shutil.copy2(backup_file, target_file)

        logger.debug(
            "Restored plugin code",
            plugin_id=plugin_id,
            backup=str(backup_file),
            target=str(target_file),
        )

    def get_rollback_history(self, plugin_id: str) -> RollbackHistory | None:
        """Get the rollback history for a plugin.

        Args:
            plugin_id: The plugin ID to get history for.

        Returns:
            The rollback history or None if not found.

        """
        return self._histories.get(plugin_id)

    def list_rollback_points(
        self, plugin_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """List all rollback points.

        Args:
            plugin_id: Optional plugin ID to filter by.

        Returns:
            List of rollback point information dictionaries.

        """
        points = []

        for pid, history in self._histories.items():
            if plugin_id and pid != plugin_id:
                continue

            points.extend(
                [
                    {
                        "rollback_id": point.rollback_id,
                        "plugin_id": point.plugin_id,
                        "created_at": point.created_at,
                        "description": point.description,
                        "version": point.plugin_version,
                        "has_code_backup": point.metadata.get("code_backed_up", False),
                    }
                    for point in history.rollback_points
                ],
            )

        return points

    def cleanup_old_backups(self, days_to_keep: int = 30) -> int:
        """Clean up old backup files.

        Args:
            days_to_keep: Number of days to keep backup files.

        Returns:
            Number of files deleted.

        """
        import time

        deleted_count = 0
        cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)

        for backup_file in self.backup_directory.rglob("*"):
            if backup_file.is_file():
                if backup_file.stat().st_mtime < cutoff_time:
                    backup_file.unlink()
                    deleted_count += 1

        logger.info(
            "Cleaned up %d old backup files",
            deleted_count,
            days_to_keep=days_to_keep,
        )

        return deleted_count
