"""FLEXT Plugin Loader - Dynamic Plugin Loading with Hot Reload Support.

REFACTORED:
    Uses flext-core patterns with proper error handling and security.
    Zero tolerance for duplication.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import ClassVar

from flext_core import FlextEntity, FlextResult
from flext_core.utilities import FlextGenerators


class PluginLoader(FlextEntity):
    """Simple plugin loader for development and hot reload."""

    loaded_plugins: ClassVar[dict[str, object]] = {}
    plugin_modules: ClassVar[dict[str, object]] = {}

    model_config: ClassVar = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        *,
        entity_id: str = "",
        security_enabled: bool = True,
    ) -> None:
        """Initialize plugin loader."""
        # Generate ID if not provided for backward compatibility
        final_entity_id = (
            entity_id or FlextGenerators.generate_entity_id()
        )
        super().__init__(id=final_entity_id)
        # Store security setting as instance attribute (not Pydantic field)
        object.__setattr__(self, "_security_enabled", security_enabled)
        self._loaded_plugins: dict[str, object] = {}

    @property
    def security_enabled(self) -> bool:
        """Get security enabled status."""
        return getattr(self, "_security_enabled", True)

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin loader."""
        return FlextResult.ok(None)

    def load_plugin(self, file_path: Path) -> object:
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
                file_path.stem,
                file_path,
            )
            if spec is None:
                msg = f"Failed to create spec for {file_path}"
                _handle_import_error(msg)
                return FlextResult.fail(msg)  # Early return for type narrowing

            # Type narrowing: spec is not None after check
            if spec.loader is None:
                msg = f"No loader available for {file_path}"
                _handle_import_error(msg)
                return FlextResult.fail(msg)  # Early return for type narrowing

            module = importlib.util.module_from_spec(spec)
            # spec and spec.loader are guaranteed to be non-None here
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
        except (RuntimeError, ValueError, TypeError) as e:
            msg = f"Failed to load plugin from {file_path}: {e}"
            _handle_import_error(msg)

        # This should never be reached, all paths above either return or raise
        return None

    async def unload_plugin(self, plugin_name: str) -> None:
        """Unload plugin by name."""
        if plugin_name in self.loaded_plugins:
            plugin = self.loaded_plugins[plugin_name]
            if hasattr(plugin, "cleanup"):
                await plugin.cleanup()
            del self.loaded_plugins[plugin_name]

        if plugin_name in self.plugin_modules:
            del self.plugin_modules[plugin_name]

    async def reload_plugin(self, plugin_name: str, file_path: str) -> object:
        """Reload plugin from file."""
        await self.unload_plugin(plugin_name)
        return self.load_plugin(Path(file_path))

    def get_loaded_plugins(self) -> dict[str, object]:
        """Get copy of loaded plugins."""
        return self.loaded_plugins.copy()

    async def cleanup_all(self) -> None:
        """Cleanup all loaded plugins."""
        for plugin_name in list(self.loaded_plugins.keys()):
            await self.unload_plugin(plugin_name)

        self.loaded_plugins.clear()
        self.plugin_modules.clear()

    def get_loaded_plugin(self, plugin_name: str) -> FlextResult[object]:
        """Get a loaded plugin by name.

        Args:
            plugin_name: Name of the plugin to retrieve

        Returns:
            FlextResult containing the loaded plugin or error

        """
        if plugin_name in self._loaded_plugins:
            return FlextResult.ok(self._loaded_plugins[plugin_name])
        return FlextResult.fail(f"Plugin '{plugin_name}' not loaded")

    def is_loaded(self, plugin_name: str) -> bool:
        """Check if a plugin is loaded.

        Args:
            plugin_name: Name of the plugin to check

        Returns:
            True if plugin is loaded, False otherwise

        """
        return plugin_name in self._loaded_plugins

    def get_all_loaded_plugins(self) -> FlextResult[dict[str, object]]:
        """Get all loaded plugins.

        Returns:
            FlextResult containing dictionary of loaded plugins

        """
        return FlextResult.ok(self._loaded_plugins.copy())
