"""FLEXT Plugin Domain Ports - Interfaces for external dependencies.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain ports defining interfaces for plugin management operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_core import FlextResult

    from flext_plugin.domain.entities import FlextPlugin, FlextPluginConfig


class FlextPluginDiscoveryPort(ABC):
    """Port for plugin discovery operations."""

    @abstractmethod
    def discover_plugins(self, path: str) -> FlextResult[list[FlextPlugin]]:
        """Discover plugins in the given path.

        Args:
            path: Path to search for plugins

        Returns:
            FlextResult containing list of discovered plugins

        """

    @abstractmethod
    def validate_plugin(self, plugin: FlextPlugin) -> FlextResult[bool]:
        """Validate a plugin.

        Args:
            plugin: Plugin to validate

        Returns:
            FlextResult indicating if plugin is valid

        """


class FlextPluginLoaderPort(ABC):
    """Port for plugin loading operations."""

    @abstractmethod
    def load_plugin(self, plugin: FlextPlugin) -> FlextResult[bool]:
        """Load a plugin.

        Args:
            plugin: Plugin to load

        Returns:
            FlextResult indicating if loading was successful

        """

    @abstractmethod
    def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unload a plugin.

        Args:
            plugin_name: Name of plugin to unload

        Returns:
            FlextResult indicating if unloading was successful

        """

    @abstractmethod
    def is_plugin_loaded(self, plugin_name: str) -> FlextResult[bool]:
        """Check if a plugin is loaded.

        Args:
            plugin_name: Name of plugin to check

        Returns:
            FlextResult indicating if plugin is loaded

        """


class FlextPluginManagerPort(ABC):
    """Port for plugin management operations."""

    @abstractmethod
    def install_plugin(self, plugin_path: str) -> FlextResult[FlextPlugin]:
        """Install a plugin from the given path.

        Args:
            plugin_path: Path to plugin to install

        Returns:
            FlextResult containing installed plugin

        """

    @abstractmethod
    def uninstall_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Uninstall a plugin.

        Args:
            plugin_name: Name of plugin to uninstall

        Returns:
            FlextResult indicating if uninstallation was successful

        """

    @abstractmethod
    def enable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Enable a plugin.

        Args:
            plugin_name: Name of plugin to enable

        Returns:
            FlextResult indicating if enabling was successful

        """

    @abstractmethod
    def disable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Disable a plugin.

        Args:
            plugin_name: Name of plugin to disable

        Returns:
            FlextResult indicating if disabling was successful

        """

    @abstractmethod
    def get_plugin_config(self, plugin_name: str) -> FlextResult[FlextPluginConfig]:
        """Get configuration for a plugin.

        Args:
            plugin_name: Name of plugin to get config for

        Returns:
            FlextResult containing plugin configuration

        """

    @abstractmethod
    def update_plugin_config(
        self,
        plugin_name: str,
        config: FlextPluginConfig,
    ) -> FlextResult[bool]:
        """Update configuration for a plugin.

        Args:
            plugin_name: Name of plugin to update config for
            config: New plugin configuration

        Returns:
            FlextResult indicating if update was successful

        """


# Backwards compatibility aliases
PluginDiscoveryPort = FlextPluginDiscoveryPort
PluginLoaderPort = FlextPluginLoaderPort
PluginManagerPort = FlextPluginManagerPort

# Service aliases for tests (mapped to appropriate ports)
PluginDiscoveryService = FlextPluginDiscoveryPort
PluginExecutionService = FlextPluginLoaderPort  # Execution is handled by loader
PluginHotReloadService = FlextPluginLoaderPort  # Hot reload is a loader concern
PluginLifecycleService = FlextPluginManagerPort  # Lifecycle is managed by manager
PluginRegistryService = FlextPluginManagerPort  # Registry is managed by manager
PluginSecurityService = FlextPluginManagerPort  # Security is a manager concern
PluginValidationService = FlextPluginDiscoveryPort  # Validation is part of discovery
