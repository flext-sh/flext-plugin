"""Hot reload orchestration for enterprise plugin system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import importlib
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from flext_core.domain.pydantic_base import DomainBaseModel, Field

# Use centralized logger from flext-observability - ELIMINATE DUPLICATION
from flext_observability.logging import get_logger
from flext_plugin.hot_reload.rollback import RollbackManager
from flext_plugin.hot_reload.state_manager import StateManager
from flext_plugin.hot_reload.watcher import PluginWatcher, WatchEventType

if TYPE_CHECKING:
    from flext_plugin.core.manager import PluginManager
    from flext_plugin.hot_reload.watcher import WatchEvent

logger = get_logger(__name__)


class ReloadEvent(DomainBaseModel):
    """Plugin reload event information."""

    event_type: str = Field(description="Type of reload event")
    plugin_id: str = Field(description="Plugin identifier")
    plugin_path: Path = Field(description="Plugin file path")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    success: bool = Field(default=False, description="Whether reload succeeded")
    error: str | None = Field(default=None, description="Error message if failed")
    duration_ms: int = Field(default=0, description="Reload duration in milliseconds")


class HotReloadManager:
    """Enterprise hot reload orchestration manager."""

    def __init__(
        self,
        plugin_manager: PluginManager,
        watch_directories: list[Path] | None = None,
        state_backup_dir: Path | None = None,
    ) -> None:
        """Initialize hot reload manager."""
        self.plugin_manager = plugin_manager
        self.watch_directories = watch_directories or []
        self.state_manager = StateManager(state_backup_dir)
        self.rollback_manager = RollbackManager()
        self.watcher = PluginWatcher(self.watch_directories)
        self._reload_events: list[ReloadEvent] = []
        self._is_running = False

    async def start_watching(self) -> None:
        """Start watching for plugin changes."""
        if self._is_running:
            return

        logger.info("Starting hot reload manager")
        self._is_running = True

        # Start file watcher
        await self.watcher.start()

        # Process watch events
        async for event in self.watcher.get_events():
            if event.event_type in {WatchEventType.MODIFIED, WatchEventType.CREATED}:
                await self._handle_plugin_change(event)

    async def stop_watching(self) -> None:
        """Stop watching for plugin changes."""
        if not self._is_running:
            return

        logger.info("Stopping hot reload manager")
        self._is_running = False
        await self.watcher.stop()

    async def reload_plugin(self, plugin_id: str) -> ReloadEvent:
        """Reload specific plugin with state preservation."""
        start_time = datetime.now(UTC)

        try:
            # Create reload event
            event = ReloadEvent(
                event_type="manual_reload",
                plugin_id=plugin_id,
                plugin_path=Path(f"plugin_{plugin_id}"),
                timestamp=start_time,
            )

            # Get current plugin
            plugin = await self.plugin_manager.get_plugin(plugin_id)
            if not plugin:
                event.error = f"Plugin {plugin_id} not found"
                return event

            # Backup current state
            await self.state_manager.backup_plugin_state(plugin)

            # Create rollback point
            rollback_id = await self.rollback_manager.create_rollback_point(plugin)

            try:
                # Unload current plugin
                await self.plugin_manager.unload_plugin(plugin_id)

                # Reload module
                if plugin.module_name in sys.modules:
                    importlib.reload(sys.modules[plugin.module_name])

                # Load new version
                new_plugin = await self.plugin_manager.load_plugin(plugin.path)

                # Restore state
                await self.state_manager.restore_plugin_state(new_plugin)

                # Mark success
                event.success = True
                logger.info(f"Successfully reloaded plugin {plugin_id}")

            except Exception as reload_error:
                # Rollback on failure
                logger.exception(f"Plugin reload failed, rolling back: {reload_error}")
                await self.rollback_manager.rollback(rollback_id)
                event.error = str(reload_error)

        except Exception as e:
            event.error = f"Reload orchestration failed: {e}"
            logger.exception(f"Hot reload failed for {plugin_id}: {e}")

        # Calculate duration
        end_time = datetime.now(UTC)
        event.duration_ms = int((end_time - start_time).total_seconds() * 1000)

        # Store event
        self._reload_events.append(event)

        return event

    async def _handle_plugin_change(self, event: WatchEvent) -> None:
        """Handle file system change event."""
        try:
            # Determine affected plugin
            plugin_id = self._get_plugin_id_from_path(event.path)
            if not plugin_id:
                return

            logger.info(f"Plugin change detected: {plugin_id} at {event.path}")

            # Trigger reload
            await self.reload_plugin(plugin_id)

        except Exception as e:
            logger.exception(f"Failed to handle plugin change: {e}")

    def _get_plugin_id_from_path(self, file_path: Path) -> str | None:
        """Extract plugin ID from file path."""
        # Simple implementation - plugin ID from parent directory
        if file_path.suffix == ".py":
            return file_path.parent.name
        return None

    async def get_reload_history(self, limit: int = 100) -> list[ReloadEvent]:
        """Get recent reload events."""
        return self._reload_events[-limit:]

    async def clear_reload_history(self) -> None:
        """Clear reload event history."""
        self._reload_events.clear()
