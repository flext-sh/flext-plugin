"""Plugin hot reload system with watchdog integration."""

import asyncio
import importlib
import sys
from pathlib import Path
from typing import Any, Callable

from flext_core.domain.pydantic_base import DomainBaseModel
from pydantic import Field
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from flext_plugin.discovery import PluginDiscovery
from flext_plugin.loader import PluginLoader


class PluginFileHandler(FileSystemEventHandler):
    """File system event handler for plugin files."""

    def __init__(self, reload_callback: Callable[[Path], None]) -> None:
        super().__init__()
        self.reload_callback = reload_callback

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        if event.is_directory:
            return

        path = Path(event.src_path)
        if path.suffix == '.py' and not path.name.startswith('__'):
            self.reload_callback(path)


class HotReloadManager(DomainBaseModel):
    """Plugin hot reload manager with file watching capabilities."""

    plugin_directory: str
    discovery: PluginDiscovery | None = Field(default=None)
    loader: PluginLoader | None = Field(default=None)
    observer: Observer | None = Field(default=None)
    loaded_plugins: dict[str, Any] = Field(default_factory=dict)

    model_config = {"arbitrary_types_allowed": True}

    def model_post_init(self, __context: Any) -> None:
        """Initialize components after creation."""
        self.discovery = PluginDiscovery(plugin_directory=self.plugin_directory)
        self.loader = PluginLoader()
        self.observer = Observer()
        self.loaded_plugins = {}

    async def start_watching(self) -> None:
        """Start watching plugin directory for changes."""
        if self.observer is None:
            raise RuntimeError("Observer not initialized")

        handler = PluginFileHandler(self._on_plugin_file_changed)
        self.observer.schedule(handler, self.plugin_directory, recursive=True)
        self.observer.start()

        # Initial plugin scan and load
        await self._initial_plugin_load()

    async def stop_watching(self) -> None:
        """Stop watching plugin directory."""
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()

    async def _initial_plugin_load(self) -> None:
        """Load all plugins initially."""
        try:
            plugins = await self.discovery.scan()
            for plugin_info in plugins:
                await self._load_plugin(plugin_info['path'])
        except Exception:
            pass

    def _on_plugin_file_changed(self, file_path: Path) -> None:
        """Handle plugin file changes."""
        asyncio.create_task(self._reload_plugin(file_path))

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

        except Exception:
            pass

    async def _load_plugin(self, file_path: Path) -> None:
        """Load a single plugin."""
        try:
            plugin_name = file_path.stem
            plugin_instance = await self.loader.load_plugin_from_file(str(file_path))
            self.loaded_plugins[plugin_name] = plugin_instance
        except Exception:
            pass

    async def _unload_plugin(self, plugin_name: str) -> None:
        """Unload a plugin."""
        try:
            if plugin_name in self.loaded_plugins:
                plugin = self.loaded_plugins[plugin_name]
                # Call plugin cleanup if available
                if hasattr(plugin, 'cleanup'):
                    await plugin.cleanup()
                del self.loaded_plugins[plugin_name]
        except Exception:
            pass

    def get_loaded_plugins(self) -> dict[str, Any]:
        """Get currently loaded plugins."""
        return self.loaded_plugins.copy()

    async def reload_all_plugins(self) -> None:
        """Manually reload all plugins."""
        # Unload all
        for plugin_name in list(self.loaded_plugins.keys()):
            await self._unload_plugin(plugin_name)

        # Reload all
        await self._initial_plugin_load()


# Convenience function for quick setup
async def create_hot_reload_manager(plugin_directory: str) -> HotReloadManager:
    """Create and start a hot reload manager."""
    manager = HotReloadManager(plugin_directory=plugin_directory)
    await manager.start_watching()
    return manager
