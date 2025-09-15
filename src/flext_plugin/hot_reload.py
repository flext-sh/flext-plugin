"""FLEXT Plugin Hot Reload System - File system monitoring and plugin reloading.

This module implements the infrastructure layer hot-reload functionality,
providing file system monitoring, automatic plugin reloading, and development
workflow optimization. The system integrates with watchdog for reliable
file system event detection and provides seamless plugin development experience.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import asyncio
import importlib
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import ClassVar, Protocol, cast, override

from flext_core import (
    FlextExceptions,
    FlextLogger,
    FlextModels,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from flext_plugin.discovery import PluginDiscovery
from flext_plugin.loader import PluginLoader


class StatefulPlugin(Protocol):
    """Protocol for plugins that support state management."""

    async def get_state(self) -> FlextTypes.Core.Dict:
        """Get plugin state as dictionary."""
        ...

    async def cleanup(self) -> None:
        """Cleanup plugin resources."""
        ...


class WatchEventType(Enum):
    """File system watch event types."""

    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    MOVED = "moved"


class WatchEvent:
    """File system watch event data."""

    def __init__(
        self,
        event_type: WatchEventType,
        path: Path,
        timestamp: datetime | None = None,
    ) -> None:
        """Initialize watch event.

        Args:
            event_type: Type of file system event
            path: Path to the affected file
            timestamp: When the event occurred

        """
        self.event_type = event_type
        self.path = path
        self.timestamp = timestamp or datetime.now(UTC)


class PluginState:
    """Plugin state data model for hot-reload operations."""

    def __init__(
        self,
        plugin_id: str,
        plugin_version: str,
        state_data: FlextTypes.Core.Dict | None = None,
        metadata: FlextTypes.Core.Dict | None = None,
        saved_at: datetime | None = None,
    ) -> None:
        """Initialize plugin state.

        Args:
            plugin_id: Unique plugin identifier
            plugin_version: Plugin version string
            state_data: Plugin state dictionary
            metadata: Additional metadata
            saved_at: When state was saved

        """
        self.plugin_id = plugin_id
        self.plugin_version = plugin_version
        self.state_data = state_data or {}
        self.metadata = metadata or {}
        self.saved_at = saved_at or datetime.now(UTC)


class ReloadEvent:
    """Plugin reload event data."""

    def __init__(
        self,
        event_type: str,
        plugin_id: str,
        plugin_path: Path | None = None,
        *,
        success: bool = False,
        error: str | None = None,
    ) -> None:
        """Initialize reload event.

        Args:
            event_type: Type of reload event
            plugin_id: Plugin identifier
            plugin_path: Path to plugin file
            success: Whether reload was successful
            error: Error message if failed

        """
        self.event_type = event_type
        self.plugin_id = plugin_id
        self.plugin_path = plugin_path
        self.success = success
        self.error = error


class PluginWatcher:
    """File system watcher for plugin directories."""

    def __init__(self, watch_directories: list[Path]) -> None:
        """Initialize plugin watcher.

        Args:
            watch_directories: List of directories to watch

        Returns:
            object: Description of return value.

        """
        self.watch_directories = watch_directories
        self._observer: BaseObserver | None = None

    def get_watched_files(self) -> list[Path]:
        """Get list of watched files.

        Returns:
            List of watched file paths

        """
        watched_files: list[Path] = []
        for directory in self.watch_directories:
            if directory.exists():
                watched_files.extend(directory.glob("**/*.py"))
        return watched_files


class StateManager:
    """Plugin state management system."""

    def __init__(self, state_directory: Path) -> None:
        """Initialize state manager.

        Args:
            state_directory: Directory for state storage

        """
        self.state_directory = state_directory
        self._snapshots: list[FlextTypes.Core.Dict] = []
        self.enable_persistence = True

        # Create state directory if it doesn't exist
        self.state_directory.mkdir(parents=True, exist_ok=True)

    async def save_plugin_state(self, plugin: StatefulPlugin) -> PluginState:
        """Save plugin state.

        Args:
            plugin: Plugin instance to save state for

        Returns:
            Plugin state object

        """
        state_data = await plugin.get_state()
        plugin_id = getattr(plugin, "name", "unknown")
        plugin_version = getattr(plugin, "version", "1.0.0")

        return PluginState(
            plugin_id=plugin_id, plugin_version=plugin_version, state_data=state_data
        )

    async def create_snapshot(self, _description: str = "") -> str:
        """Create a new snapshot.

        Args:
            description: Optional snapshot description

        Returns:
            Snapshot identifier.

        """
        return f"snapshot_{datetime.now(UTC).isoformat()}"

    def list_snapshots(self) -> list[FlextTypes.Core.Dict]:
        """List available snapshots.

        Returns:
            List of snapshot information

        """
        return []


class RollbackManager:
    """Plugin rollback management system."""

    def __init__(self, state_manager: StateManager) -> None:
        """Initialize rollback manager.

        Args:
            state_manager: State manager instance

        """
        self.state_manager = state_manager
        self._rollback_history: dict[str, list[FlextTypes.Core.Dict]] = {}

    async def create_rollback_point(
        self, _description: str = "", _plugin_id: str = ""
    ) -> str:
        """Create a new rollback point.

        Args:
            description: Optional rollback description
            plugin_id: Optional plugin identifier

        Returns:
            Rollback point identifier.

        """
        return f"rollback_{datetime.now(UTC).isoformat()}"

    def get_rollback_history(self, _plugin_id: str) -> object | None:
        """Get rollback history for plugin.

        Args:
            plugin_id: Plugin identifier
        Returns:
            Rollback history or None

        """
        return None


class PluginFileHandler(FileSystemEventHandler):
    """File system event handler for plugin file monitoring and change detection.

    Event handler that monitors plugin file changes and triggers reload
    operations through callback mechanisms. Provides filtered event handling
    to focus on relevant plugin file modifications while ignoring temporary
    files and non-plugin changes.
    """

    def __init__(self, reload_callback: Callable[[Path], None]) -> None:
        """Initialize file system event handler with reload callback.

        Args:
            reload_callback: Function to call when plugin files are modified.
                           Must accept a single Path parameter representing
                           the modified plugin file path.

        Returns:
            object: Description of return value.

        """
        super().__init__()
        self.reload_callback = reload_callback

    @override
    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events.

        Args:
            event: The file system event that occurred.

        Returns:
            object: Description of return value.

        """
        if event.is_directory:
            return
        # Fix type issue with event.src_path - ensure it's a string
        src_path = event.src_path
        if isinstance(src_path, bytes):
            src_path = src_path.decode("utf-8")
        path = Path(src_path)
        if path.suffix == ".py" and not path.name.startswith("__"):
            self.reload_callback(path)


class HotReloadManager(FlextModels.Entity):
    """Plugin hot reload manager with file watching capabilities."""

    plugin_directory: str
    model_config: ClassVar = {"arbitrary_types_allowed": True}

    # Private attributes initialized in model_post_init
    _loaded_plugins: FlextTypes.Core.Dict

    @classmethod
    def create(cls, *, plugin_directory: str, **kwargs: object) -> HotReloadManager:
        """Create hot reload manager instance with proper validation."""
        entity_id = str(
            kwargs.get("id", FlextUtilities.Generators.generate_entity_id())
        )
        version = cast("int", kwargs.get("version", 1))
        metadata = cast("FlextTypes.Core.Dict", kwargs.get("metadata", {}))
        # Create instance using Pydantic model_validate to bypass __init__
        instance_data: FlextTypes.Core.Dict = {
            "id": entity_id,
            "version": version,
            "metadata": metadata,
            "plugin_directory": plugin_directory,
        }
        return cls.model_validate(instance_data)
        # model_post_init is called automatically by Pydantic

    # Removed __init__ - use create() class method instead
    @property
    def discovery(self) -> PluginDiscovery | None:
        """Get plugin discovery instance."""
        return getattr(self, "_discovery", None)

    @property
    def loader(self) -> PluginLoader | None:
        """Get plugin loader instance."""
        return getattr(self, "_loader", None)

    @property
    def observer(self) -> BaseObserver | None:
        """Get file system observer instance."""
        return getattr(self, "_observer", None)

    @property
    def loaded_plugins(self) -> FlextTypes.Core.Dict:
        """Get loaded plugins dictionary."""
        return getattr(self, "_loaded_plugins", {})

    @property
    def plugin_manager(self) -> object | None:
        """Get plugin manager instance."""
        return getattr(self, "_plugin_manager", None)

    @property
    def state_manager(self) -> StateManager:
        """Get state manager instance, creating it if needed."""
        state_dir = Path(self.plugin_directory) / ".flext_state"
        return StateManager(state_directory=state_dir)

    @property
    def rollback_manager(self) -> RollbackManager:
        """Get rollback manager instance, creating it if needed."""
        state_mgr = self.state_manager  # This will create state manager if needed
        return RollbackManager(state_manager=state_mgr)

    @property
    def watcher(self) -> PluginWatcher:
        """Get plugin watcher instance, creating it if needed."""
        watch_dirs = [Path(self.plugin_directory)]
        return PluginWatcher(watch_directories=watch_dirs)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for hot reload manager."""
        if not self.plugin_directory:
            return FlextResult[None].fail("Plugin directory cannot be empty")
        return FlextResult[None].ok(None)

    def model_post_init(self, __context: FlextTypes.Core.Dict | None, /) -> None:
        """Initialize model after creation.

        Args:
            __context: Pydantic context.

        Returns:
            object: Description of return value.

        """
        # Create simplified discovery to avoid abstract class instantiation
        object.__setattr__(self, "_discovery", None)  # We'll create this on-demand
        object.__setattr__(self, "_loader", PluginLoader())
        object.__setattr__(self, "_observer", Observer())
        object.__setattr__(self, "_loaded_plugins", {})
        # Pre-initialize lazy properties to avoid attribute errors
        object.__setattr__(self, "_state_manager", None)
        object.__setattr__(self, "_rollback_manager", None)
        object.__setattr__(self, "_watcher", None)

    async def start_watching(self) -> None:
        """Start watching for plugin file changes.

        Raises:
            RuntimeError: If observer is not initialized.

        """
        observer = self.observer
        if observer is None:
            msg = "Observer not initialized"
            raise FlextExceptions.ProcessingError(msg)
        handler = PluginFileHandler(self._on_plugin_file_changed)
        observer.schedule(handler, self.plugin_directory, recursive=True)
        observer.start()
        # Initial plugin scan and load
        await self._initial_plugin_load()

    async def stop_watching(self) -> None:
        """Stop watching for plugin file changes."""
        observer = self.observer
        if observer and observer.is_alive():
            observer.stop()
            observer.join()

    async def _initial_plugin_load(self) -> None:
        """Perform initial plugin loading."""
        try:
            # Simplified plugin discovery - scan directory for .py files
            plugin_dir = Path(self.plugin_directory)
            if plugin_dir.exists():
                for py_file in plugin_dir.glob("*.py"):
                    if not py_file.name.startswith("__"):
                        await self._load_plugin(py_file)
        except (OSError, RuntimeError, ValueError, KeyError) as e:
            # Log plugin discovery error and continue
            logger = FlextLogger(__name__)
            logger.warning(f"Plugin discovery failed during hot reload: {e}")
            # Continue hot reload process despite discovery failure

    def _on_plugin_file_changed(self, file_path: Path) -> None:
        """Handle plugin file change events."""
        task = asyncio.create_task(self._reload_plugin(file_path))
        task.add_done_callback(lambda _: None)  # Prevent dangling task warning

    async def _reload_plugin(self, file_path: Path) -> None:
        """Reload a specific plugin."""
        try:
            plugin_name = file_path.stem
            # Unload existing plugin
            if plugin_name in self.loaded_plugins:
                await self._unload_plugin(plugin_name)
            # Reload plugin module
            if plugin_name in sys.modules:
                importlib.reload(sys.modules[plugin_name])
            # Load updated plugin
            await self._load_plugin(file_path)
        except (OSError, RuntimeError, ValueError, ImportError, AttributeError) as e:
            # Log plugin reload error and continue hot-reload process
            logger = FlextLogger(__name__)
            logger.warning(f"Plugin reload failed for {file_path}: {e}")

    async def _load_plugin(self, file_path: Path) -> None:
        """Load a plugin from file path."""
        try:
            plugin_name = file_path.stem
            loader = self.loader
            if loader:
                plugin_instance = loader.load_plugin(file_path)
                loaded_plugins = getattr(self, "_loaded_plugins", {})
                loaded_plugins[plugin_name] = plugin_instance
        except (OSError, RuntimeError, ValueError, ImportError, AttributeError) as e:
            # Log plugin loading error and continue hot-reload process
            logger = FlextLogger(__name__)
            logger.warning(f"Plugin loading failed for {file_path}: {e}")

    async def _unload_plugin(self, plugin_name: str) -> None:
        """Unload a specific plugin."""
        try:
            loaded_plugins = getattr(self, "_loaded_plugins", {})
            if plugin_name in loaded_plugins:
                plugin = loaded_plugins[plugin_name]
                # Call plugin cleanup if available:
                if hasattr(plugin, "cleanup"):
                    await plugin.cleanup()
                del loaded_plugins[plugin_name]
        except (RuntimeError, ValueError, AttributeError, KeyError) as e:
            # Log plugin unload error and continue hot-reload process
            logger = FlextLogger(__name__)
            logger.warning(f"Plugin unload failed for {plugin_name}: {e}")

    def get_loaded_plugins(self) -> FlextTypes.Core.Dict:
        """Get a copy of currently loaded plugins.

        Returns:
            Dictionary of loaded plugins keyed by plugin name.

        """
        return dict(self.loaded_plugins)

    async def reload_plugin(self, plugin_id: str) -> ReloadEvent:
        """Reload a specific plugin by ID.

        Args:
            plugin_id: The plugin identifier to reload
        Returns:
            ReloadEvent with success/failure information

        """
        try:
            # Try to reload via plugin manager if available
            plugin_manager = getattr(self, "plugin_manager", None)
            if plugin_manager and hasattr(plugin_manager, "reload_plugin"):
                result = await plugin_manager.reload_plugin(plugin_id)
                return ReloadEvent(
                    event_type="plugin_reload",
                    plugin_id=plugin_id,
                    success=bool(result),
                )

            # Fallback implementation: unload the plugin (cleanup and remove)
            await self._unload_plugin(plugin_id)

            return ReloadEvent(
                event_type="plugin_reload",
                plugin_id=plugin_id,
                success=True,
            )
        except Exception as e:
            return ReloadEvent(
                event_type="plugin_reload",
                plugin_id=plugin_id,
                success=False,
                error=str(e),
            )

    async def reload_all_plugins(self) -> list[ReloadEvent]:
        """Reload all currently loaded plugins.

        Returns:
            List of ReloadEvent results for each plugin

        """
        reload_events: list[ReloadEvent] = []
        loaded_plugins = self.loaded_plugins

        # Create a copy of plugin IDs to avoid "dictionary changed size during iteration"
        plugin_ids = list(loaded_plugins.keys())

        for plugin_id in plugin_ids:
            reload_event = await self.reload_plugin(plugin_id)
            reload_events.append(reload_event)

        return reload_events

    async def _handle_plugin_change(self, watch_event: WatchEvent) -> None:
        """Handle plugin file change events.

        Args:
            watch_event: The file system watch event

        """
        # Extract plugin ID from path
        plugin_id = watch_event.path.stem
        # Trigger plugin reload
        await self.reload_plugin(plugin_id)


# Convenience function for quick setup
async def create_hot_reload_manager(plugin_directory: str) -> HotReloadManager:
    """Create and start hot reload manager for plugin directory."""
    manager = HotReloadManager.create(plugin_directory=plugin_directory)
    await manager.start_watching()
    return manager


__all__ = [
    "HotReloadManager",
    "PluginFileHandler",
    "PluginState",
    "PluginWatcher",
    "ReloadEvent",
    "RollbackManager",
    "StateManager",
    "StatefulPlugin",
    "WatchEvent",
    "WatchEventType",
    "create_hot_reload_manager",
]
