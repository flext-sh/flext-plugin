"""Plugin hot reload system with watchdog integration."""

from __future__ import annotations

import asyncio
import importlib
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from flext_core.domain.pydantic_base import DomainBaseModel, Field
from flext_plugin.discovery import PluginDiscovery
from flext_plugin.loader import PluginLoader


class PluginFileHandler(FileSystemEventHandler):
    """File system event handler for plugin files."""

    def __init__(self, reload_callback: Callable[[Path], None]) -> None:
        super().__init__()
        self.reload_callback = reload_callback

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events.
        
        Args:
            event: The file system event that occurred.

        """
        if event.is_directory:
            return

        path = Path(event.src_path)
        if path.suffix == ".py" and not path.name.startswith("__"):
            self.reload_callback(path)


class HotReloadManager(DomainBaseModel):
    """Plugin hot reload manager with file watching capabilities."""

    plugin_directory: str
    discovery = Field(default=None)
    loader: PluginLoader | None = Field(default=None)
    observer: Observer | None = Field(default=None)
    loaded_plugins: dict[str, Any] = Field(default_factory=dict)

    model_config: ClassVar = {"arbitrary_types_allowed": True}

    def model_post_init(self, __context: Any, /) -> None:
        """Initialize model after creation.
        
        Args:
            __context: Pydantic context.

        """
        self.discovery = PluginDiscovery(plugin_directory=self.plugin_directory)
        self.loader = PluginLoader()
        self.observer = Observer()
        self.loaded_plugins = {}

    async def start_watching(self) -> None:
        """Start watching for plugin file changes.
        
        Raises:
            RuntimeError: If observer is not initialized.

        """
        if self.observer is None:
            msg = "Observer not initialized"
            raise RuntimeError(msg)

        handler = PluginFileHandler(self._on_plugin_file_changed)
        self.observer.schedule(handler, self.plugin_directory, recursive=True)
        self.observer.start()

        # Initial plugin scan and load
        await self._initial_plugin_load()

    async def stop_watching(self) -> None:
        """Stop watching for plugin file changes."""
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()

    async def _initial_plugin_load(self) -> None:
        try:
            plugins = await self.discovery.scan()
            for plugin_info in plugins:
                await self._load_plugin(plugin_info["path"])
        except Exception:
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

        except Exception:
            pass

    async def _load_plugin(self, file_path: Path) -> None:
        try:
            plugin_name = file_path.stem
            plugin_instance = await self.loader.load_plugin_from_file(str(file_path))
            self.loaded_plugins[plugin_name] = plugin_instance
        except Exception:
            pass

    async def _unload_plugin(self, plugin_name: str) -> None:
        try:
            if plugin_name in self.loaded_plugins:
                plugin = self.loaded_plugins[plugin_name]
                # Call plugin cleanup if available:
                if hasattr(plugin, "cleanup"):
                    await plugin.cleanup()
                del self.loaded_plugins[plugin_name]
        except Exception:
            pass

    def get_loaded_plugins(self) -> dict[str, Any]:
        """Get a copy of currently loaded plugins.
        
        Returns:
            Dictionary of loaded plugins keyed by plugin name.

        """
        return self.loaded_plugins.copy()

    async def reload_all_plugins(self) -> None:
        """Reload all currently loaded plugins."""
        # Unload all
        for plugin_name in list(self.loaded_plugins.keys()):
            await self._unload_plugin(plugin_name)

        # Reload all
        await self._initial_plugin_load()


# Convenience function for quick setup
async def create_hot_reload_manager(plugin_directory: str) -> HotReloadManager:
    manager = HotReloadManager(plugin_directory=plugin_directory)
    await manager.start_watching()
    return manager
