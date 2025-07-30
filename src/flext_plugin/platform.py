"""FLEXT Plugin Platform - Unified plugin management platform.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Platform class providing unified access to plugin management services.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextContainer, FlextResult

from flext_plugin.application.services import (
    FlextPluginDiscoveryService,
    FlextPluginService,
)

if TYPE_CHECKING:
    from flext_plugin.domain.entities import FlextPlugin, FlextPluginConfig


class FlextPluginPlatform:
    """FLEXT Plugin Platform."""

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize plugin platform.

        Args:
            container: Optional FLEXT container instance.

        """
        self.container = container or FlextContainer()
        self._setup_services()

    def _setup_services(self) -> None:
        """Setup platform services."""
        # Register services in container
        # DRY SOLID pattern: Use container kwarg for service initialization
        self.container.register(
            "plugin_service", FlextPluginService(container=self.container),
        )
        self.container.register(
            "plugin_discovery_service",
            FlextPluginDiscoveryService(container=self.container),
        )

    @property
    def plugin_service(self) -> FlextPluginService:
        """Get plugin management service."""
        result = self.container.get("plugin_service")
        if result.is_success and isinstance(result.data, FlextPluginService):
            return result.data
        msg = f"Failed to get plugin service: {result.error}"
        raise RuntimeError(msg)

    @property
    def discovery_service(self) -> FlextPluginDiscoveryService:
        """Get plugin discovery service."""
        result = self.container.get("plugin_discovery_service")
        if result.is_success and isinstance(result.data, FlextPluginDiscoveryService):
            return result.data
        msg = f"Failed to get discovery service: {result.error}"
        raise RuntimeError(msg)

    def discover_plugins(self, path: str) -> FlextResult[list[FlextPlugin]]:
        """Discover plugins in the given path.

        Args:
            path: Path to search for plugins

        Returns:
            FlextResult containing list of discovered plugins

        """
        return self.plugin_service.discover_plugins(path)

    def load_plugin(self, plugin: FlextPlugin) -> FlextResult[bool]:
        """Load a plugin.

        Args:
            plugin: Plugin to load

        Returns:
            FlextResult indicating if loading was successful

        """
        return self.plugin_service.load_plugin(plugin)

    def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unload a plugin.

        Args:
            plugin_name: Name of plugin to unload

        Returns:
            FlextResult indicating if unloading was successful

        """
        return self.plugin_service.unload_plugin(plugin_name)

    def install_plugin(self, plugin_path: str) -> FlextResult[FlextPlugin]:
        """Install a plugin from the given path.

        Args:
            plugin_path: Path to plugin to install

        Returns:
            FlextResult containing installed plugin

        """
        return self.plugin_service.install_plugin(plugin_path)

    def uninstall_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Uninstall a plugin.

        Args:
            plugin_name: Name of plugin to uninstall

        Returns:
            FlextResult indicating if uninstallation was successful

        """
        return self.plugin_service.uninstall_plugin(plugin_name)

    def enable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Enable a plugin.

        Args:
            plugin_name: Name of plugin to enable

        Returns:
            FlextResult indicating if enabling was successful

        """
        return self.plugin_service.enable_plugin(plugin_name)

    def disable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Disable a plugin.

        Args:
            plugin_name: Name of plugin to disable

        Returns:
            FlextResult indicating if disabling was successful

        """
        return self.plugin_service.disable_plugin(plugin_name)

    def get_plugin_config(self, plugin_name: str) -> FlextResult[FlextPluginConfig]:
        """Get configuration for a plugin.

        Args:
            plugin_name: Name of plugin to get config for

        Returns:
            FlextResult containing plugin configuration

        """
        return self.plugin_service.get_plugin_config(plugin_name)

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
        return self.plugin_service.update_plugin_config(plugin_name, config)

    def is_plugin_loaded(self, plugin_name: str) -> FlextResult[bool]:
        """Check if a plugin is loaded.

        Args:
            plugin_name: Name of plugin to check

        Returns:
            FlextResult indicating if plugin is loaded

        """
        return self.plugin_service.is_plugin_loaded(plugin_name)

    def scan_directory(self, directory_path: str) -> FlextResult[list[FlextPlugin]]:
        """Scan directory for plugins.

        Args:
            directory_path: Directory to scan

        Returns:
            FlextResult containing discovered plugins

        """
        return self.discovery_service.scan_directory(directory_path)

    def validate_plugin(self, plugin: FlextPlugin) -> FlextResult[bool]:
        """Validate plugin integrity.

        Args:
            plugin: Plugin to validate

        Returns:
            FlextResult indicating if plugin is valid

        """
        return self.discovery_service.validate_plugin_integrity(plugin)


# Backwards compatibility alias
PluginPlatform = FlextPluginPlatform
