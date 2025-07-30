"""FLEXT Plugin Application Services - Plugin management services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Application services for plugin management operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from flext_core import FlextContainer, FlextDomainService, FlextResult

from flext_plugin.core.types import SimplePluginRegistry
from flext_plugin.domain.ports import (
    FlextPluginDiscoveryPort,
    FlextPluginLoaderPort,
    FlextPluginManagerPort,
)

if TYPE_CHECKING:
    from flext_plugin.domain.entities import FlextPlugin, FlextPluginConfig


class FlextPluginService(FlextDomainService):
    """Main plugin management service."""

    container: FlextContainer
    model_config: ClassVar = {"arbitrary_types_allowed": True, "frozen": False}

    def __init__(self, **kwargs: object) -> None:
        """Initialize plugin service."""
        # Extract container from kwargs or create default
        container_arg = kwargs.pop("container", None)
        if container_arg is not None:
            kwargs["container"] = container_arg
        else:
            kwargs["container"] = FlextContainer()

        super().__init__(**kwargs)

        # Store private attributes
        object.__setattr__(self, "_discovery_port", None)
        object.__setattr__(self, "_loader_port", None)
        object.__setattr__(self, "_manager_port", None)

    def execute(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        _ = args, kwargs  # Mark as intentionally unused
        return FlextResult.fail("Use specific service methods instead of execute")

    @property
    def discovery_port(self) -> FlextPluginDiscoveryPort:
        """Get plugin discovery port."""
        discovery_port = getattr(self, "_discovery_port", None)
        if discovery_port is None:
            result = self.container.get("plugin_discovery_port")
            if result.is_success and isinstance(result.data, FlextPluginDiscoveryPort):
                object.__setattr__(self, "_discovery_port", result.data)
                return result.data
        if isinstance(discovery_port, FlextPluginDiscoveryPort):
            return discovery_port
        # Return a mock implementation if none available
        return SimplePluginRegistry()

    @property
    def loader_port(self) -> FlextPluginLoaderPort:
        """Get plugin loader port."""
        loader_port = getattr(self, "_loader_port", None)
        if loader_port is None:
            result = self.container.get("plugin_loader_port")
            if result.is_success and isinstance(result.data, FlextPluginLoaderPort):
                object.__setattr__(self, "_loader_port", result.data)
                return result.data
        if isinstance(loader_port, FlextPluginLoaderPort):
            return loader_port
        # Return a mock implementation if none available
        return SimplePluginRegistry()

    @property
    def manager_port(self) -> FlextPluginManagerPort:
        """Get plugin manager port."""
        manager_port = getattr(self, "_manager_port", None)
        if manager_port is None:
            result = self.container.get("plugin_manager_port")
            if result.is_success and isinstance(result.data, FlextPluginManagerPort):
                object.__setattr__(self, "_manager_port", result.data)
                return result.data
        if isinstance(manager_port, FlextPluginManagerPort):
            return manager_port
        # Return a mock implementation if none available
        return SimplePluginRegistry()

    def discover_plugins(self, path: str) -> FlextResult[list[FlextPlugin]]:
        """Discover plugins in the given path.

        Args:
            path: Path to search for plugins

        Returns:
            FlextResult containing list of discovered plugins

        """
        try:
            if not path:
                return FlextResult.fail("Path is required for plugin discovery")

            return self.discovery_port.discover_plugins(path)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to discover plugins: {e}")

    def load_plugin(self, plugin: FlextPlugin) -> FlextResult[bool]:
        """Load a plugin.

        Args:
            plugin: Plugin to load

        Returns:
            FlextResult indicating if loading was successful

        """
        try:
            if not plugin.is_valid():
                return FlextResult.fail("Invalid plugin")

            # Validate plugin first
            validation_result = self.discovery_port.validate_plugin(plugin)
            if not validation_result.is_success or not validation_result.data:
                return FlextResult.fail("Plugin validation failed")

            return self.loader_port.load_plugin(plugin)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to load plugin: {e}")

    def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unload a plugin.

        Args:
            plugin_name: Name of plugin to unload

        Returns:
            FlextResult indicating if unloading was successful

        """
        try:
            if not plugin_name:
                return FlextResult.fail("Plugin name is required")

            return self.loader_port.unload_plugin(plugin_name)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to unload plugin: {e}")

    def install_plugin(self, plugin_path: str) -> FlextResult[FlextPlugin]:
        """Install a plugin from the given path.

        Args:
            plugin_path: Path to plugin to install

        Returns:
            FlextResult containing installed plugin

        """
        try:
            if not plugin_path:
                return FlextResult.fail("Plugin path is required")

            return self.manager_port.install_plugin(plugin_path)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to install plugin: {e}")

    def uninstall_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Uninstall a plugin.

        Args:
            plugin_name: Name of plugin to uninstall

        Returns:
            FlextResult indicating if uninstallation was successful

        """
        try:
            if not plugin_name:
                return FlextResult.fail("Plugin name is required")

            return self.manager_port.uninstall_plugin(plugin_name)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to uninstall plugin: {e}")

    def enable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Enable a plugin.

        Args:
            plugin_name: Name of plugin to enable

        Returns:
            FlextResult indicating if enabling was successful

        """
        try:
            if not plugin_name:
                return FlextResult.fail("Plugin name is required")

            return self.manager_port.enable_plugin(plugin_name)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to enable plugin: {e}")

    def disable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Disable a plugin.

        Args:
            plugin_name: Name of plugin to disable

        Returns:
            FlextResult indicating if disabling was successful

        """
        try:
            if not plugin_name:
                return FlextResult.fail("Plugin name is required")

            return self.manager_port.disable_plugin(plugin_name)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to disable plugin: {e}")

    def get_plugin_config(self, plugin_name: str) -> FlextResult[FlextPluginConfig]:
        """Get configuration for a plugin.

        Args:
            plugin_name: Name of plugin to get config for

        Returns:
            FlextResult containing plugin configuration

        """
        try:
            if not plugin_name:
                return FlextResult.fail("Plugin name is required")

            return self.manager_port.get_plugin_config(plugin_name)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to get plugin config: {e}")

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
        try:
            if not plugin_name:
                return FlextResult.fail("Plugin name is required")

            if not config.is_valid():
                return FlextResult.fail("Invalid plugin configuration")

            return self.manager_port.update_plugin_config(plugin_name, config)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to update plugin config: {e}")

    def is_plugin_loaded(self, plugin_name: str) -> FlextResult[bool]:
        """Check if a plugin is loaded.

        Args:
            plugin_name: Name of plugin to check

        Returns:
            FlextResult indicating if plugin is loaded

        """
        try:
            if not plugin_name:
                return FlextResult.fail("Plugin name is required")

            return self.loader_port.is_plugin_loaded(plugin_name)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to check plugin status: {e}")


class FlextPluginDiscoveryService(FlextDomainService):
    """Service for plugin discovery operations."""

    container: FlextContainer
    model_config: ClassVar = {"arbitrary_types_allowed": True, "frozen": False}

    def __init__(self, **kwargs: object) -> None:
        """Initialize plugin discovery service."""
        # Extract container from kwargs or create default
        container_arg = kwargs.pop("container", None)
        if container_arg is not None:
            kwargs["container"] = container_arg
        else:
            kwargs["container"] = FlextContainer()

        super().__init__(**kwargs)

        # Store private attributes
        object.__setattr__(self, "_discovery_port", None)

    def execute(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        _ = args, kwargs  # Mark as intentionally unused
        return FlextResult.fail("Use specific service methods instead of execute")

    @property
    def discovery_port(self) -> FlextPluginDiscoveryPort:
        """Get plugin discovery port."""
        discovery_port = getattr(self, "_discovery_port", None)
        if discovery_port is None:
            result = self.container.get("plugin_discovery_port")
            if result.is_success and isinstance(result.data, FlextPluginDiscoveryPort):
                object.__setattr__(self, "_discovery_port", result.data)
                return result.data
        if isinstance(discovery_port, FlextPluginDiscoveryPort):
            return discovery_port
        # Return a mock implementation if none available
        return SimplePluginRegistry()

    def scan_directory(self, directory_path: str) -> FlextResult[list[FlextPlugin]]:
        """Scan directory for plugins.

        Args:
            directory_path: Directory to scan

        Returns:
            FlextResult containing discovered plugins

        """
        try:
            if not directory_path:
                return FlextResult.fail("Directory path is required")

            return self.discovery_port.discover_plugins(directory_path)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to scan directory: {e}")

    def validate_plugin_integrity(self, plugin: FlextPlugin) -> FlextResult[bool]:
        """Validate plugin integrity.

        Args:
            plugin: Plugin to validate

        Returns:
            FlextResult indicating if plugin is valid

        """
        try:
            if not plugin:
                return FlextResult.fail("Plugin is required")

            return self.discovery_port.validate_plugin(plugin)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to validate plugin: {e}")


# Backwards compatibility aliases
PluginService = FlextPluginService
PluginDiscoveryService = FlextPluginDiscoveryService
