"""FLEXT Plugin Loader - Dynamic Plugin Loading with Hot Reload Support.

REFACTORED:
    Uses flext-core patterns with proper error handling and security.
    Zero tolerance for duplication.
"""

from __future__ import annotations

import importlib.util
from typing import TYPE_CHECKING, Any, ClassVar

from flext_core.domain.pydantic_base import DomainBaseModel

if TYPE_CHECKING:
    from pathlib import Path


class PluginLoader(DomainBaseModel):
    """Simple plugin loader for development and hot reload."""

    security_enabled: bool = True
    loaded_plugins: ClassVar[dict[str, Any]] = {}
    plugin_modules: ClassVar[dict[str, Any]] = {}

    model_config: ClassVar = {"arbitrary_types_allowed": True}

    def load_plugin(self, file_path: Path) -> Any:
        """Load a plugin from a Python file.

        Args:
            file_path: Path to the plugin file

        Returns:
            Loaded plugin instance

        Raises:
            ImportError: If plugin cannot be loaded
            ValueError: If plugin is invalid

        """
        def _handle_import_error(error: str) -> None:
            """Handle import error by raising appropriate exception."""
            raise ImportError(error)

        def _handle_value_error(error: str) -> None:
            """Handle value error by raising appropriate exception."""
            raise ValueError(error)

        try:
            # Create module spec
            spec = importlib.util.spec_from_file_location(
                file_path.stem, file_path,
            )
            if spec is None or spec.loader is None:
                msg = f"Failed to create spec for {file_path}"
                _handle_import_error(msg)

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Store module for hot reload
            self.plugin_modules[file_path.stem] = module

            # Look for get_plugin function first
            if hasattr(module, "get_plugin"):
                plugin = module.get_plugin()
                self.loaded_plugins[file_path.stem] = plugin
                return plugin

            # Fallback to any class that has execute method
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    hasattr(attr, "execute")
                    and callable(attr)
                    and attr_name != "execute"
                ):
                    plugin = attr()
                    self.loaded_plugins[file_path.stem] = plugin
                    return plugin

            msg = f"No plugin found in {file_path}"
            _handle_value_error(msg)
        except Exception as e:
            msg = f"Failed to load plugin from {file_path}: {e}"
            _handle_import_error(msg)

    async def unload_plugin(self, plugin_name: str) -> None:
        """Unload plugin by name."""
        if plugin_name in self.loaded_plugins:
            plugin = self.loaded_plugins[plugin_name]
            if hasattr(plugin, "cleanup"):
                await plugin.cleanup()
            del self.loaded_plugins[plugin_name]

        if plugin_name in self.plugin_modules:
            del self.plugin_modules[plugin_name]

    async def reload_plugin(self, plugin_name: str, file_path: str) -> Any:
        """Reload plugin from file."""
        await self.unload_plugin(plugin_name)
        return await self.load_plugin_from_file(file_path)

    def get_loaded_plugins(self) -> dict[str, Any]:
        """Get copy of loaded plugins."""
        return self.loaded_plugins.copy()

    async def cleanup_all(self) -> None:
        """Cleanup all loaded plugins."""
        for plugin_name in list(self.loaded_plugins.keys()):
            await self.unload_plugin(plugin_name)

        self.loaded_plugins.clear()
        self.plugin_modules.clear()
