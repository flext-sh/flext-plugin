"""Plugin hot reload system with watchdog integration."""

from __future__ import annotations

import asyncio
import importlib
import sys
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from flext_core import FlextEntity, FlextProcessingError, FlextResult
from flext_core.utilities import FlextGenerators
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from flext_plugin.loader import PluginLoader

if TYPE_CHECKING:
    from collections.abc import Callable

    from watchdog.observers.api import BaseObserver

    from flext_plugin.discovery import PluginDiscovery


class PluginFileHandler(FileSystemEventHandler):
    """File system event handler for plugin files."""

    def __init__(self, reload_callback: Callable[[Path], None]) -> None:
        """Initialize handler with reload callback function."""
        super().__init__()
        self.reload_callback = reload_callback

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events.

        Args:
            event: The file system event that occurred.

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


class HotReloadManager(FlextEntity):
    """Plugin hot reload manager with file watching capabilities."""

    plugin_directory: str

    model_config: ClassVar = {"arbitrary_types_allowed": True}

    def __init__(self, *, plugin_directory: str, **kwargs: object) -> None:
        """Initialize hot reload manager."""
        # Generate ID for FlextEntity
        entity_id = str(kwargs.get("id", FlextGenerators.generate_entity_id()))

        super().__init__(id=entity_id)

        # Store plugin_directory as instance attribute (not Pydantic field)
        object.__setattr__(self, "plugin_directory", plugin_directory)
        # Store non-Pydantic attributes directly
        object.__setattr__(self, "_discovery", None)
        object.__setattr__(self, "_loader", None)
        object.__setattr__(self, "_observer", None)
        object.__setattr__(self, "_loaded_plugins", {})

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
    def loaded_plugins(self) -> dict[str, object]:
        """Get loaded plugins dictionary."""
        return getattr(self, "_loaded_plugins", {})

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate domain rules for hot reload manager."""
        if not self.plugin_directory:
            return FlextResult.fail("Plugin directory cannot be empty")
        return FlextResult.ok(None)

    def model_post_init(self, __context: dict[str, object] | None, /) -> None:
        """Initialize model after creation.

        Args:
            __context: Pydantic context.

        """
        # Create simplified discovery to avoid abstract class instantiation
        object.__setattr__(self, "_discovery", None)  # We'll create this on-demand
        object.__setattr__(self, "_loader", PluginLoader())
        object.__setattr__(self, "_observer", Observer())
        object.__setattr__(self, "_loaded_plugins", {})

    async def start_watching(self) -> None:
        """Start watching for plugin file changes.

        Raises:
            RuntimeError: If observer is not initialized.

        """
        observer = self.observer
        if observer is None:
            msg = "Observer not initialized"
            raise FlextProcessingError(msg)

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
        except (OSError, RuntimeError, ValueError, KeyError):
            pass

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

        except (OSError, RuntimeError, ValueError, ImportError, AttributeError):
            pass

    async def _load_plugin(self, file_path: Path) -> None:
        """Load a plugin from file path."""
        try:
            plugin_name = file_path.stem
            loader = self.loader
            if loader:
                plugin_instance = loader.load_plugin(file_path)
                loaded_plugins = getattr(self, "_loaded_plugins", {})
                loaded_plugins[plugin_name] = plugin_instance
        except (OSError, RuntimeError, ValueError, ImportError, AttributeError):
            pass

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
        except (RuntimeError, ValueError, AttributeError, KeyError):
            pass

    def get_loaded_plugins(self) -> dict[str, object]:
        """Get a copy of currently loaded plugins.

        Returns:
            Dictionary of loaded plugins keyed by plugin name.

        """
        return self.loaded_plugins.copy()

    async def reload_all_plugins(self) -> None:
        """Reload all currently loaded plugins."""
        # Unload all
        loaded_plugins = getattr(self, "_loaded_plugins", {})
        for plugin_name in list(loaded_plugins.keys()):
            await self._unload_plugin(plugin_name)

        # Reload all
        await self._initial_plugin_load()


# Convenience function for quick setup
async def create_hot_reload_manager(plugin_directory: str) -> HotReloadManager:
    """Create and start hot reload manager for plugin directory."""
    manager = HotReloadManager(plugin_directory=plugin_directory)
    await manager.start_watching()
    return manager
