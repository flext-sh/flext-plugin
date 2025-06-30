"""Simple plugin loader for hot reload functionality."""

import importlib
import inspect
from pathlib import Path
from typing import Any

from flext_core.domain.pydantic_base import DomainBaseModel


class PluginLoader(DomainBaseModel):
    """Simple plugin loader for development and hot reload."""

    security_enabled: bool = True
    loaded_plugins: dict[str, Any] = {}
    plugin_modules: dict[str, Any] = {}

    model_config = {"arbitrary_types_allowed": True}

    async def load_plugin_from_file(self, file_path: str) -> Any:
        """Load plugin directly from a Python file.

        Args:
        ----
            file_path: Path to the Python plugin file

        Returns:
        -------
            Plugin instance from the file

        """
        import importlib.util

        try:
            path = Path(file_path)
            spec = importlib.util.spec_from_file_location(path.stem, file_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot load module from {file_path}")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Store module for hot reload
            self.plugin_modules[path.stem] = module

            # Look for get_plugin function first
            if hasattr(module, 'get_plugin'):
                plugin = module.get_plugin()
                self.loaded_plugins[path.stem] = plugin
                return plugin

            # Fallback to any class that has execute method
            for name in dir(module):
                obj = getattr(module, name)
                if inspect.isclass(obj) and hasattr(obj, 'execute'):
                    plugin = obj()
                    self.loaded_plugins[path.stem] = plugin
                    return plugin

            raise ValueError(f"No valid plugin class found in {file_path}")

        except Exception:
            raise

    async def unload_plugin(self, plugin_name: str) -> None:
        """Unload a plugin by name."""
        if plugin_name in self.loaded_plugins:
            plugin = self.loaded_plugins[plugin_name]
            # Call cleanup if available
            if hasattr(plugin, 'cleanup'):
                await plugin.cleanup()
            del self.loaded_plugins[plugin_name]

        if plugin_name in self.plugin_modules:
            del self.plugin_modules[plugin_name]

    async def reload_plugin(self, plugin_name: str) -> Any:
        """Hot-reload a plugin by name."""
        if plugin_name in self.plugin_modules:
            # Unload first
            await self.unload_plugin(plugin_name)

            # Reload module
            module = self.plugin_modules.get(plugin_name)
            if module:
                importlib.reload(module)

                # Reload plugin instance
                if hasattr(module, 'get_plugin'):
                    plugin = module.get_plugin()
                    self.loaded_plugins[plugin_name] = plugin
                    return plugin

        return None

    def get_loaded_plugins(self) -> dict[str, Any]:
        """Get currently loaded plugins."""
        return self.loaded_plugins.copy()

    async def cleanup_all(self) -> None:
        """Cleanup all loaded plugins."""
        for plugin_name in list(self.loaded_plugins.keys()):
            await self.unload_plugin(plugin_name)

        self.loaded_plugins.clear()
        self.plugin_modules.clear()
