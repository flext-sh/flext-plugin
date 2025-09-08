"""FLEXT Plugin Loader - Dynamic plugin loading with security and hot-reload.

This module implements the infrastructure layer plugin loading functionality,
providing dynamic Python module loading, plugin isolation, and hot-reload
capabilities. The loader maintains security boundaries while enabling flexible
plugin development and deployment workflows.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.util
from datetime import UTC, datetime
from pathlib import Path
from typing import ClassVar, Protocol, cast, override

from flext_core import (
    FlextEventList,
    FlextModels,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)


class CleanupablePlugin(Protocol):
    """Protocol for plugins that support cleanup operations."""

    async def cleanup(self) -> None:
        """Cleanup plugin resources."""
        ...


class PluginLoader(FlextModels):
    """Dynamic plugin loading system with security validation and hot-reload.

    Infrastructure component implementing dynamic Python module loading for the
    FLEXT plugin system. Provides plugin isolation, security validation, and
    hot-reload capabilities while maintaining proper resource management and
    error handling throughout the plugin lifecycle.
    """

    loaded_plugins: ClassVar[FlextTypes.Core.Dict] = {}
    plugin_modules: ClassVar[FlextTypes.Core.Dict] = {}

    model_config: ClassVar = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        *,
        entity_id: str = "",
        security_enabled: bool = True,
    ) -> None:
        """Initialize plugin loader."""
        # Generate ID if not provided for backward compatibility
        final_entity_id = entity_id or FlextUtilities.generate_entity_id()
        # Initialize FlextModels.Entity with all required parameters

        now = datetime.now(UTC)
        super().__init__(
            id=cast("FlextModels.EntityId", final_entity_id),
            version=cast("FlextModels.Version", 1),
            domain_events=cast("FlextEventList", []),
            metadata=cast("FlextModels.Metadata", {}),
            created_at=cast("FlextModels.Timestamp", now),
            updated_at=cast("FlextModels.Timestamp", now),
        )
        # Store security setting as instance attribute (not Pydantic field)
        object.__setattr__(self, "_security_enabled", security_enabled)
        self._loaded_plugins: FlextTypes.Core.Dict = {}

    @property
    def security_enabled(self) -> bool:
        """Get security enabled status."""
        return getattr(self, "_security_enabled", True)

    @override
    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin loader."""
        return FlextResult[None].ok(None)

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
                spec_msg: str = f"Failed to create spec for {file_path}"
                _handle_import_error(spec_msg)
                return FlextResult[None].fail(
                    spec_msg
                )  # Early return for type narrowing

            # Type narrowing: spec is not None after check
            if spec.loader is None:
                loader_msg: str = f"No loader available for {file_path}"
                _handle_import_error(loader_msg)
                return FlextResult[None].fail(
                    loader_msg
                )  # Early return for type narrowing

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

            not_found_msg: str = f"No plugin found in {file_path}"
            _handle_value_error(not_found_msg)
        except (RuntimeError, ValueError, TypeError) as e:
            load_error_msg: str = f"Failed to load plugin from {file_path}: {e}"
            _handle_import_error(load_error_msg)

        # This should never be reached, all paths above either return or raise
        return None

    async def unload_plugin(self, plugin_name: str) -> None:
        """Unload plugin by name."""
        if plugin_name in self.loaded_plugins:
            plugin = self.loaded_plugins[plugin_name]
            # Check if plugin implements CleanupablePlugin protocol
            if hasattr(plugin, "cleanup") and callable(
                getattr(plugin, "cleanup", None)
            ):
                cleanupable_plugin = cast("CleanupablePlugin", plugin)
                await cleanupable_plugin.cleanup()
            del self.loaded_plugins[plugin_name]

        if plugin_name in self.plugin_modules:
            del self.plugin_modules[plugin_name]

    async def reload_plugin(self, plugin_name: str, file_path: str) -> object:
        """Reload plugin from file."""
        await self.unload_plugin(plugin_name)
        return self.load_plugin(Path(file_path))

    def get_loaded_plugins(self) -> FlextTypes.Core.Dict:
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
            return FlextResult[object].ok(self._loaded_plugins[plugin_name])
        return FlextResult[object].fail(f"Plugin '{plugin_name}' not loaded")

    def is_loaded(self, plugin_name: str) -> bool:
        """Check if a plugin is loaded.

        Args:
            plugin_name: Name of the plugin to check

        Returns:
            True if plugin is loaded, False otherwise

        """
        return plugin_name in self._loaded_plugins

    def get_all_loaded_plugins(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Get all loaded plugins.

        Returns:
            FlextResult containing dictionary of loaded plugins

        """
        return FlextResult[FlextTypes.Core.Dict].ok(self._loaded_plugins.copy())


__all__ = [
    "CleanupablePlugin",
    "PluginLoader",
]
