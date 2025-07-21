"""Plugin Manager - Core plugin lifecycle management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Implements the main PluginManager class for plugin lifecycle operations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core.domain.types import ServiceResult
from flext_observability.logging import get_logger

logger = get_logger(__name__)


class PluginManager:
    """Main plugin manager for lifecycle operations."""

    def __init__(self) -> None:
        """Initialize plugin manager."""
        self._initialized = False
        self._plugins: dict[str, dict[str, Any]] = {}
        self._loaded_plugins: dict[str, dict[str, Any]] = {}

    async def initialize(self) -> None:
        """Initialize the plugin manager."""
        self._initialized = True
        logger.info("Plugin manager initialized")

    async def discover_plugins(
        self,
        search_paths: list[str] | None = None,
    ) -> dict[str, dict[str, Any]]:
        """Discover available plugins.

        Args:
            search_paths: Optional paths to search for plugins

        Returns:
            Dictionary of discovered plugins

        """
        if not self._initialized:
            await self.initialize()

        # Simple discovery implementation for testing
        discovered = {}

        if search_paths:
            for path in search_paths:
                path_obj = Path(path)
                if path_obj.exists() and path_obj.is_dir():
                    # Scan for plugin files
                    for plugin_file in path_obj.glob("*.py"):
                        if plugin_file.name.startswith("plugin_"):
                            plugin_name = plugin_file.stem
                            discovered[plugin_name] = {
                                "name": plugin_name,
                                "path": str(plugin_file),
                                "type": "python",
                            }

        self._plugins.update(discovered)
        logger.info("Discovered %d plugins", len(discovered))
        return discovered

    async def load_plugin(self, plugin_name: str) -> ServiceResult[dict[str, Any]]:
        """Load a plugin by name.

        Args:
            plugin_name: Name of the plugin to load

        Returns:
            ServiceResult with plugin data or error

        """
        if not self._initialized:
            await self.initialize()

        if plugin_name not in self._plugins:
            return ServiceResult.fail(f"Plugin '{plugin_name}' not found")

        try:
            plugin_data = self._plugins[plugin_name]
            self._loaded_plugins[plugin_name] = plugin_data
            logger.info("Loaded plugin: %s", plugin_name)
            return ServiceResult.ok(plugin_data)
        except Exception as e:
            logger.exception("Failed to load plugin: %s", plugin_name)
            return ServiceResult.fail(f"Failed to load plugin: {e}")

    async def unload_plugin(self, plugin_name: str) -> ServiceResult[bool]:
        """Unload a plugin by name.

        Args:
            plugin_name: Name of the plugin to unload

        Returns:
            ServiceResult with success status

        """
        if plugin_name not in self._loaded_plugins:
            return ServiceResult.fail(f"Plugin '{plugin_name}' not loaded")

        try:
            del self._loaded_plugins[plugin_name]
            logger.info("Unloaded plugin: %s", plugin_name)
            return ServiceResult.ok(True)
        except Exception as e:
            logger.exception("Failed to unload plugin: %s", plugin_name)
            return ServiceResult.fail(f"Failed to unload plugin: {e}")

    async def reload_plugin(self, plugin_name: str) -> ServiceResult[dict[str, Any]]:
        """Reload a plugin by name.

        Args:
            plugin_name: Name of the plugin to reload

        Returns:
            ServiceResult with plugin data or error

        """
        # Unload first
        await self.unload_plugin(plugin_name)

        # Then load again
        return await self.load_plugin(plugin_name)

    def get_loaded_plugins(self) -> dict[str, dict[str, Any]]:
        """Get all currently loaded plugins.

        Returns:
            Dictionary of loaded plugins

        """
        return self._loaded_plugins.copy()

    def is_plugin_loaded(self, plugin_name: str) -> bool:
        """Check if a plugin is currently loaded.

        Args:
            plugin_name: Name of the plugin to check

        Returns:
            True if plugin is loaded, False otherwise

        """
        return plugin_name in self._loaded_plugins
