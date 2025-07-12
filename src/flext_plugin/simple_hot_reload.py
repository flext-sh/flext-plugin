"""Simple working hot reload system for plugins."""

from __future__ import annotations

import asyncio
import importlib
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from watchdog.events import FileSystemEvent, FileSystemEventHandler

if TYPE_CHECKING:
    from collections.abc import Callable

    import aiofiles  # type: ignore
    from watchdog.observers import Observer
else:
    try:
        import aiofiles
        from watchdog.observers import Observer
    except ImportError:
        aiofiles = None  # type: ignore
        Observer = None  # type: ignore

from flext_core.domain.pydantic_base import DomainBaseModel, Field


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
    observer = Field(default=None)
    loaded_plugins: dict[str, Any] = Field(default_factory=dict)

    model_config: ClassVar = {"arbitrary_types_allowed": True}

    def model_post_init(self, __context: dict[str, Any] | None, /) -> None:
        """Initialize observer and loaded plugins after model creation."""
        if Observer is not None:
            self.observer = Observer()
        if not hasattr(self, "loaded_plugins"):
            self.loaded_plugins = {}

    async def start_watching(self) -> None:
        """Start watching plugin directory for file changes."""
        if self.observer is None or Observer is None:
            msg = "Observer not initialized or watchdog not available"
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
        try:
            plugin_name = file_path.stem

            # Read and execute plugin file
            async with aiofiles.open(file_path, encoding="utf-8") as f:
                plugin_code = await f.read()

            # Create module namespace
            plugin_globals: dict[str, Any] = {}
            exec(plugin_code, plugin_globals)

            # Look for plugin_instance or first class
            plugin_instance = None
            if "plugin_instance" in plugin_globals:
                plugin_instance = plugin_globals["plugin_instance"]
            else:
                # Find first class in the module
                for value in plugin_globals.values():
                    if isinstance(value, type) and value.__name__ != "type":
                        plugin_instance = value()
                        break

            if plugin_instance:
                self.loaded_plugins[plugin_name] = plugin_instance

        except (OSError, ImportError, RuntimeError, ValueError, AttributeError):
            pass

    async def _unload_plugin(self, plugin_name: str) -> None:
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
