"""Simple working hot reload system for plugins."""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

    # Import for type checking only
    from watchdog.events import (
        FileSystemEvent,
        FileSystemEventHandler,
    )
    from watchdog.observers import (
        Observer as ObserverType,
    )
else:
    # Runtime imports with error handling for missing stubs
    try:
        from watchdog.events import FileSystemEvent, FileSystemEventHandler
        from watchdog.observers import Observer as ObserverType
    except ImportError as e:
        msg = "watchdog library is required but not properly installed"
        raise RuntimeError(
            msg,
        ) from e

# ZERO TOLERANCE: Use ORIGINAL libraries ONLY - NO FALLBACKS ALLOWED
from flext_core.domain.pydantic_base import DomainBaseModel, Field
from pydantic import ConfigDict


class SimplePluginHandler(FileSystemEventHandler):
    """Simple file system event handler for plugin files."""

    def __init__(self, reload_callback: Callable[[Path], None]) -> None:
        """Initialize handler with reload callback function."""
        super().__init__()
        self.reload_callback = reload_callback

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events for Python plugin files."""
        if event.is_directory:
            return

        path = Path(str(event.src_path))
        if path.suffix == ".py" and not path.name.startswith("__"):
            self.reload_callback(path)


class SimpleHotReloadManager(DomainBaseModel):
    """Simple working hot reload manager for plugins."""

    plugin_directory: str
    observer: Any | None = Field(default=None)
    loaded_plugins: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def model_post_init(self, __context: dict[str, Any] | None, /) -> None:
        """Initialize observer and loaded plugins after model creation."""
        if ObserverType is not None:
            self.observer = ObserverType()
        if not hasattr(self, "loaded_plugins"):
            self.loaded_plugins = {}

    async def start_watching(self) -> None:
        """Start watching plugin directory for file changes."""
        if self.observer is None or ObserverType is None:
            msg = "Observer not available"
            raise RuntimeError(msg)

        handler = SimplePluginHandler(self._on_plugin_file_changed)
        self.observer.schedule(handler, self.plugin_directory, recursive=True)
        self.observer.start()

        # Initial plugin scan and load
        await self._initial_plugin_load()

    async def stop_watching(self) -> None:
        """Stop watching plugin directory and cleanup observer."""
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()

    async def _initial_plugin_load(self) -> None:
        """Load all existing plugins in the directory."""
        try:
            plugin_dir = Path(self.plugin_directory)
            for plugin_file in plugin_dir.glob("*.py"):
                if not plugin_file.name.startswith("__"):
                    await self._load_plugin(plugin_file)
        except (OSError, ImportError, RuntimeError, ValueError, AttributeError):
            pass

    def _on_plugin_file_changed(self, file_path: Path) -> None:
        task = asyncio.create_task(self._reload_plugin(file_path))
        task.add_done_callback(lambda _: None)  # Prevent dangling task warning

    async def _reload_plugin(self, file_path: Path) -> None:
        """Reload a plugin when its file changes."""
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

        except (OSError, ImportError, RuntimeError, ValueError, AttributeError):
            pass

    async def _load_plugin(self, file_path: Path) -> None:
        """Load a plugin from file."""
        try:
            plugin_name = file_path.stem

            # Use importlib for secure module loading instead of exec()
            spec = importlib.util.spec_from_file_location(plugin_name, file_path)
            if spec is None or spec.loader is None:
                return

            # Create and execute module
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_name] = module
            spec.loader.exec_module(module)

            # Look for plugin_instance or first class
            plugin_instance = None
            if hasattr(module, "plugin_instance"):
                plugin_instance = module.plugin_instance
            else:
                # Find first class in the module
                for attr_name in dir(module):
                    attr_value = getattr(module, attr_name)
                    if isinstance(attr_value, type) and not attr_name.startswith("_"):
                        plugin_instance = attr_value()
                        break

            if plugin_instance:
                self.loaded_plugins[plugin_name] = plugin_instance

        except (OSError, ImportError, RuntimeError, ValueError, AttributeError):
            pass

    async def _unload_plugin(self, plugin_name: str) -> None:
        """Unload a plugin from memory."""
        try:
            if plugin_name in self.loaded_plugins:
                plugin = self.loaded_plugins[plugin_name]
                # Call plugin cleanup if available:
                if hasattr(plugin, "cleanup"):
                    if asyncio.iscoroutinefunction(plugin.cleanup):
                        await plugin.cleanup()
                    else:
                        plugin.cleanup()
                del self.loaded_plugins[plugin_name]
        except (OSError, ImportError, RuntimeError, ValueError, AttributeError):
            pass

    def get_loaded_plugins(self) -> dict[str, Any]:
        """Get dictionary of currently loaded plugins."""
        return self.loaded_plugins.copy()

    async def reload_all_plugins(self) -> None:
        """Reload all loaded plugins from scratch."""
        # Unload all
        for plugin_name in list(self.loaded_plugins.keys()):
            await self._unload_plugin(plugin_name)

        # Reload all
        await self._initial_plugin_load()


# Convenience function for quick setup
async def create_simple_hot_reload_manager(
    plugin_directory: str,
) -> SimpleHotReloadManager:
    """Create and start a simple hot reload manager."""
    manager = SimpleHotReloadManager(plugin_directory=plugin_directory)
    await manager.start_watching()
    return manager
