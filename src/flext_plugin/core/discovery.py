"""Plugin discovery system using entry points and file system scanning.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import importlib.metadata
import importlib.util
import inspect
import os
from typing import TYPE_CHECKING, Any

# Use centralized logger from flext-observability - ELIMINATE DUPLICATION
from flext_observability.logging import get_logger
from flext_plugin.core.base import Plugin
from flext_plugin.core.types import PluginError, PluginType
from flext_plugin.domain.value_objects import PluginMetadata

if TYPE_CHECKING:
    from pathlib import Path


logger = get_logger(__name__)


class DiscoveredPlugin:
    """Container for discovered plugin information."""

    def __init__(
        self,
        metadata: PluginMetadata,
        plugin_class: type[Plugin],
        source: str,
        entry_point_name: str | None = None,
    ) -> None:
        """Initialize discovered plugin container."""
        self.metadata = metadata
        self.plugin_class = plugin_class
        self.source = source
        self.entry_point_name = entry_point_name

    def __repr__(self) -> str:
        return f"DiscoveredPlugin({self.metadata.id}, source={self.source})"


class PluginDiscovery:
    """Plugin discovery system for finding and registering plugins.

    Discovers plugins through multiple mechanisms:
    - Python entry points (for installed packages)
    - File system scanning (for local plugins)
    - Direct registration (for programmatic use)
    """

    def __init__(
        self,
        plugin_directories: list[Path] | None = None,
        entry_point_groups: list[str] | None = None,
    ) -> None:
        """Initialize plugin discovery system."""
        self.plugin_directories = plugin_directories or []
        self.entry_point_groups = entry_point_groups or [
            "flext.plugins",
            "flext.extractors",
            "flext.loaders",
            "flext.transformers",
        ]
        self._discovered_plugins: dict[str, DiscoveredPlugin] = {}
        self._blacklisted_plugins: set[str] = set()

    def add_plugin_directory(self, directory: Path) -> None:
        """Add a directory to the plugin search path.

        Args:
            directory: The directory path to add.

        """
        if directory not in self.plugin_directories:
            self.plugin_directories.append(directory)

    def blacklist_plugin(self, plugin_id: str) -> None:
        """Blacklist a plugin to prevent it from being discovered.

        Args:
            plugin_id: The plugin ID to blacklist.

        """
        self._blacklisted_plugins.add(plugin_id)

    def is_blacklisted(self, plugin_id: str) -> bool:
        """Check if a plugin is blacklisted.

        Args:
            plugin_id: The plugin ID to check.

        Returns:
            True if the plugin is blacklisted, False otherwise.

        """
        return plugin_id in self._blacklisted_plugins

    async def discover_all(self) -> dict[str, DiscoveredPlugin]:
        """Discover all available plugins.

        Returns:
            Dictionary mapping plugin IDs to discovered plugin info.

        """
        # Clear previous discoveries
        self._discovered_plugins.clear()

        # Discover from entry points
        await self._discover_entry_points()

        # Discover from file system
        await self._discover_file_system()

        # Filter out blacklisted plugins
        filtered = {
            plugin_id: plugin
            for plugin_id, plugin in self._discovered_plugins.items()
            if not self.is_blacklisted(plugin_id)
        }

        logger.info("Discovered %d plugins", len(filtered))
        return filtered

    async def discover_by_type(
        self,
        plugin_type: PluginType,
    ) -> dict[str, DiscoveredPlugin]:
        """Discover plugins by type.

        Args:
            plugin_type: The type of plugins to discover.

        Returns:
            Dictionary mapping plugin IDs to discovered plugin info.

        """
        all_plugins = await self.discover_all()
        return {
            plugin_id: plugin
            for plugin_id, plugin in all_plugins.items()
            if plugin.metadata.plugin_type == plugin_type
        }

    async def _discover_entry_points(self) -> None:
        """Discover plugins through Python entry points.

        Scans configured entry point groups for plugin classes.
        """
        for group in self.entry_point_groups:
            try:
                entry_points = importlib.metadata.entry_points(group=group)

                for ep in entry_points:
                    try:
                        plugin_class = ep.load()

                        if self._validate_plugin_class(plugin_class):
                            metadata = plugin_class.METADATA

                            if metadata.id not in self._discovered_plugins:
                                discovered = DiscoveredPlugin(
                                    metadata=metadata,
                                    plugin_class=plugin_class,
                                    source="entry_point",
                                    entry_point_name=ep.name,
                                )
                                self._discovered_plugins[metadata.id] = discovered
                                logger.debug(
                                    "Discovered plugin via entry point: %s",
                                    metadata.id,
                                )

                    except (
                        ImportError,
                        AttributeError,
                        ModuleNotFoundError,
                        ValueError,
                    ) as e:
                        logger.warning("Failed to load entry point %s: %s", ep.name, e)

            except (ImportError, RuntimeError, ValueError) as e:
                logger.warning("Failed to scan entry point group %s: %s", group, e)

    async def _discover_file_system(self) -> None:
        """Discover plugins through file system scanning.

        Scans configured directories for plugin files.
        """
        for directory in self.plugin_directories:
            if not directory.exists():
                logger.warning("Plugin directory does not exist: %s", directory)
                continue

            await self._scan_directory(directory)

    async def _scan_directory(self, directory: Path) -> None:
        """Scan a directory for plugin files.

        Args:
            directory: The directory to scan.

        """
        for py_file in directory.rglob("*.py"):
            if py_file.name.startswith("_"):
                continue

            try:
                # Convert file path to module name
                relative_path = py_file.relative_to(directory.parent)
                module_name = str(relative_path).replace(os.sep, ".")[
                    :-3
                ]  # Remove .py extension

                # Import module
                spec = importlib.util.spec_from_file_location(module_name, py_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Find plugin classes in module
                    for _name, obj in inspect.getmembers(module):
                        if (
                            inspect.isclass(obj)
                            and issubclass(obj, Plugin)
                            and obj is not Plugin
                            and self._validate_plugin_class(obj)
                        ):
                            metadata = obj.METADATA

                            if metadata.id not in self._discovered_plugins:
                                discovered = DiscoveredPlugin(
                                    metadata=metadata,
                                    plugin_class=obj,
                                    source="file",
                                )
                                self._discovered_plugins[metadata.id] = discovered
                                logger.debug(
                                    "Discovered plugin from file: %s",
                                    metadata.id,
                                )

            except (OSError, ImportError, AttributeError, ValueError, SyntaxError) as e:
                logger.warning("Failed to scan file %s: %s", py_file, e)

    def _validate_plugin_class(self, plugin_class: type[Any]) -> bool:
        """Validate that a class is a valid plugin.

        Args:
            plugin_class: The class to validate.

        Returns:
            True if the class is a valid plugin, False otherwise.

        """
        try:
            # Check if it's a Plugin subclass:
            if not issubclass(plugin_class, Plugin):
                return False

            # Check if it has metadata:
            if not hasattr(plugin_class, "METADATA"):
                logger.warning(
                    "Plugin class %s missing METADATA",
                    plugin_class.__name__,
                )
                return False

            # Check if metadata is valid:
            metadata = plugin_class.METADATA
            if not isinstance(metadata, PluginMetadata):
                logger.warning(
                    "Plugin class %s has invalid METADATA",
                    plugin_class.__name__,
                )
                return False

            # Check required methods
            required_methods = ["initialize", "cleanup", "health_check", "execute"]
            for method in required_methods:
                if not hasattr(plugin_class, method):
                    logger.warning(
                        "Plugin class %s missing method: %s",
                        plugin_class.__name__,
                        method,
                    )
                    return False

            return True

        except (AttributeError, TypeError, ValueError) as e:
            logger.warning("Failed to validate plugin class %s: %s", plugin_class, e)
            return False

    def register_plugin(
        self,
        plugin_class: type[Plugin],
        override: bool = False,
    ) -> None:
        """Manually register a plugin class.

        Args:
            plugin_class: The plugin class to register.
            override: Whether to override existing registrations.

        Raises:
            PluginError: If the plugin class is invalid or already registered.

        """
        if not self._validate_plugin_class(plugin_class):
            msg = f"Invalid plugin class: {plugin_class.__name__}"
            raise PluginError(
                msg,
                error_code="INVALID_PLUGIN",
            )

        metadata = plugin_class.METADATA

        if metadata.id in self._discovered_plugins and not override:
            msg = f"Plugin already registered: {metadata.id}"
            raise PluginError(
                msg,
                plugin_id=metadata.id,
                error_code="DUPLICATE_PLUGIN",
            )

        discovered = DiscoveredPlugin(
            metadata=metadata,
            plugin_class=plugin_class,
            source="manual",
        )
        self._discovered_plugins[metadata.id] = discovered
        logger.info("Manually registered plugin: %s", metadata.id)

    def get_discovered_plugin(self, plugin_id: str) -> DiscoveredPlugin | None:
        """Get a discovered plugin by ID.

        Args:
            plugin_id: The plugin ID to retrieve.

        Returns:
            The discovered plugin or None if not found.

        """
        return self._discovered_plugins.get(plugin_id)
