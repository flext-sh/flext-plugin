"""FLEXT Plugin Application Services - Orchestrating business logic with CQRS.

This module implements the application layer services following Clean Architecture
principles, providing orchestration of plugin management operations through
domain entities and infrastructure ports. The services coordinate complex
workflows while maintaining separation of concerns and testability.

Key Services:
    - FlextPluginService: Core plugin management operations and lifecycle
    - FlextPluginDiscoveryService: Plugin discovery and validation operations

Architecture:
    These services form the application layer bridge between the platform
    (presentation) layer and domain layer, orchestrating business operations
    without containing business logic. They coordinate domain entities,
    handle cross-cutting concerns, and implement transaction boundaries.

CQRS Integration:
    Services implement Command Query Responsibility Segregation patterns,
    separating read operations (queries) from write operations (commands)
    for scalable plugin management operations.

Example:
    >>> from flext_plugin.application.services import FlextPluginService
    >>> service = FlextPluginService()
    >>> result = await service.discover_plugins("./plugins")
    >>> if result.success():
    ...     plugins = result.data
    ...     print(f"Discovered {len(plugins)} plugins")

Integration:
    - Built on flext-core domain service patterns
    - Integrates with flext-observability for monitoring
    - Coordinates with domain entities and infrastructure ports
    - Supports dependency injection and testability

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar, override

from flext_core import FlextContainer, FlextResult
from flext_core.domain_services import FlextDomainService

from flext_plugin.domain.entities import FlextPluginConfig, FlextPluginEntity
from flext_plugin.domain.ports import (
    FlextPluginDiscoveryPort,
    FlextPluginLoaderPort,
    FlextPluginManagerPort,
)


class FlextPluginService(FlextDomainService[object]):
    """Core plugin management service orchestrating plugin lifecycle operations.

    Application service providing comprehensive plugin management capabilities
    through coordination of domain entities and infrastructure ports. Implements
    the application layer of Clean Architecture, handling use cases and workflows
    without containing business logic.
    This service acts as the primary orchestrator for plugin operations,
    coordinating between discovery, loading, management, and configuration
    concerns while maintaining transaction boundaries and error handling.
    Key Responsibilities:
      - Plugin discovery and validation coordination
      - Plugin loading and unloading lifecycle management
      - Plugin installation and removal operations
      - Plugin configuration management and updates
      - Plugin state validation and health monitoring
    Architecture Integration:
      - Implements Clean Architecture application service patterns
      - Coordinates domain entities through infrastructure ports
      - Provides dependency injection and container integration
      - Supports comprehensive error handling and logging
    Port Dependencies:
      - FlextPluginDiscoveryPort: Plugin discovery and validation
      - FlextPluginLoaderPort: Plugin loading and memory management
      - FlextPluginManagerPort: Plugin installation and configuration
    Example:
      >>> service = FlextPluginService()
      >>> # Discover plugins in directory
      >>> discovery_result = service.discover_plugins("./plugins")
      >>> if discovery_result.success():
      ...     plugins = discovery_result.data
      ...     for plugin in plugins:
      ...         load_result = service.load_plugin(plugin)
      ...         if load_result.success():
      ...             print(f"Loaded plugin: {plugin.name}")
    Error Handling:
      All service methods return FlextResult objects for consistent
      error handling and railway-oriented programming patterns.
      Comprehensive exception handling with detailed error messages.
    """

    container: FlextContainer
    model_config: ClassVar = {"arbitrary_types_allowed": True, "frozen": False}

    def __init__(self, **kwargs: object) -> None:
        """Initialize plugin management service with dependency injection container.

        Sets up the application service with proper dependency injection container
        and initializes infrastructure port references. The service uses lazy loading
        for ports to support various deployment and testing scenarios.

        Args:
            **kwargs: Configuration parameters including:
                - container: FlextContainer instance for dependency injection
                - Additional configuration parameters passed to base service
        Note:
            If no container is provided, a default FlextContainer instance is created.
            Port dependencies are resolved lazily through the container.

        """
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

    @override
    def execute(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        _ = args, kwargs  # Mark as intentionally unused
        return FlextResult[object].fail(
            "Use specific service methods instead of execute"
        )

    @property
    def discovery_port(self) -> FlextPluginDiscoveryPort:
        """Get plugin discovery port."""
        discovery_port = getattr(self, "_discovery_port", None)
        if discovery_port is None:
            result = self.container.get("plugin_discovery_port")
            if result.success and isinstance(result.data, FlextPluginDiscoveryPort):
                discovery_port_data: FlextPluginDiscoveryPort = result.data  # noqa: E501
                object.__setattr__(self, "_discovery_port", discovery_port_data)
                return discovery_port_data
        if isinstance(discovery_port, FlextPluginDiscoveryPort):
            return discovery_port

        # Return a mock implementation if none available
        # Create a simple adapter that implements the interface
        class MockDiscoveryPort(FlextPluginDiscoveryPort):
            @override
            def discover_plugins(
                self,
                path: str,  # noqa: ARG002
            ) -> FlextResult[list[FlextPluginEntity]]:
                return FlextResult[list[FlextPluginEntity]].ok([])

            @override
            def validate_plugin(self, plugin: FlextPluginEntity) -> FlextResult[bool]:  # noqa: ARG002
                success = True
                return FlextResult[bool].ok(success)

        return MockDiscoveryPort()

    @property
    def loader_port(self) -> FlextPluginLoaderPort:
        """Get plugin loader port."""
        loader_port = getattr(self, "_loader_port", None)
        if loader_port is None:
            result = self.container.get("plugin_loader_port")
            if result.success and isinstance(result.data, FlextPluginLoaderPort):
                loader_port_data: FlextPluginLoaderPort = result.data  # noqa: E501
                object.__setattr__(self, "_loader_port", loader_port_data)
                return loader_port_data
        if isinstance(loader_port, FlextPluginLoaderPort):
            return loader_port

        # Return a mock implementation if none available
        # Create a simple adapter that implements the interface
        class MockLoaderPort(FlextPluginLoaderPort):
            @override
            def load_plugin(self, plugin: FlextPluginEntity) -> FlextResult[bool]:  # noqa: ARG002
                success = True
                return FlextResult[bool].ok(success)

            @override
            def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:  # noqa: ARG002
                success = True
                return FlextResult[bool].ok(success)

            @override
            def is_plugin_loaded(self, plugin_name: str) -> FlextResult[bool]:  # noqa: ARG002
                loaded = False
                return FlextResult[bool].ok(loaded)

        return MockLoaderPort()

    @property
    def manager_port(self) -> FlextPluginManagerPort:
        """Get plugin manager port."""
        manager_port = getattr(self, "_manager_port", None)
        if manager_port is None:
            result = self.container.get("plugin_manager_port")
            if result.success and isinstance(result.data, FlextPluginManagerPort):
                manager_port_data: FlextPluginManagerPort = result.data  # noqa: E501
                object.__setattr__(self, "_manager_port", manager_port_data)
                return manager_port_data
        if isinstance(manager_port, FlextPluginManagerPort):
            return manager_port

        # Return a mock implementation if none available
        # Create a simple adapter that implements the interface
        class MockManagerPort(FlextPluginManagerPort):
            @override
            def install_plugin(
                self,
                plugin_path: str,  # noqa: ARG002
            ) -> FlextResult[FlextPluginEntity]:
                return FlextResult[FlextPluginEntity].fail("Mock implementation")

            @override
            def uninstall_plugin(self, plugin_name: str) -> FlextResult[bool]:  # noqa: ARG002
                success = True
                return FlextResult[bool].ok(success)

            @override
            def enable_plugin(self, plugin_name: str) -> FlextResult[bool]:  # noqa: ARG002
                success = True
                return FlextResult[bool].ok(success)

            @override
            def disable_plugin(self, plugin_name: str) -> FlextResult[bool]:  # noqa: ARG002
                success = True
                return FlextResult[bool].ok(success)

            @override
            def get_plugin_config(
                self,
                plugin_name: str,  # noqa: ARG002
            ) -> FlextResult[FlextPluginConfig]:
                return FlextResult[FlextPluginConfig].fail("Mock implementation")

            @override
            def update_plugin_config(
                self,
                plugin_name: str,  # noqa: ARG002
                config: FlextPluginConfig,  # noqa: ARG002
            ) -> FlextResult[bool]:
                success = True
                return FlextResult[bool].ok(success)

        return MockManagerPort()

    def discover_plugins(self, path: str) -> FlextResult[list[FlextPluginEntity]]:
        """Discover plugins in the given path.

        Args:
            path: Path to search for plugins
        Returns:
            FlextResult containing list of discovered plugins

        """
        try:
            if not path:
                return FlextResult[list[FlextPluginEntity]].fail(
                    "Path is required for plugin discovery"
                )
            return self.discovery_port.discover_plugins(path)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[list[FlextPluginEntity]].fail(
                f"Failed to discover plugins: {e}"
            )

    def load_plugin(self, plugin: FlextPluginEntity) -> FlextResult[bool]:
        """Load a plugin.

        Args:
            plugin: Plugin to load
        Returns:
            FlextResult indicating if loading was successful

        """
        try:
            if not plugin.is_valid():
                return FlextResult[bool].fail("Invalid plugin")
            # Validate plugin first
            validation_result = self.discovery_port.validate_plugin(plugin)
            validation_data: bool = validation_result.data  # noqa: E501
            if not validation_result.success or not validation_data:
                return FlextResult[bool].fail("Plugin validation failed")
            return self.loader_port.load_plugin(plugin)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to load plugin: {e}")

    def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unload a plugin.

        Args:
            plugin_name: Name of plugin to unload
        Returns:
            FlextResult indicating if unloading was successful

        """
        try:
            if not plugin_name:
                return FlextResult[bool].fail("Plugin name is required")
            return self.loader_port.unload_plugin(plugin_name)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to unload plugin: {e}")

    def install_plugin(self, plugin_path: str) -> FlextResult[FlextPluginEntity]:
        """Install a plugin from the given path.

        Args:
            plugin_path: Path to plugin to install
        Returns:
            FlextResult containing installed plugin

        """
        try:
            if not plugin_path:
                return FlextResult[FlextPluginEntity].fail("Plugin path is required")
            return self.manager_port.install_plugin(plugin_path)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[FlextPluginEntity].fail(f"Failed to install plugin: {e}")

    def uninstall_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Uninstall a plugin.

        Args:
            plugin_name: Name of plugin to uninstall
        Returns:
            FlextResult indicating if uninstallation was successful

        """
        try:
            if not plugin_name:
                return FlextResult[bool].fail("Plugin name is required")
            return self.manager_port.uninstall_plugin(plugin_name)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to uninstall plugin: {e}")

    def enable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Enable a plugin.

        Args:
            plugin_name: Name of plugin to enable
        Returns:
            FlextResult indicating if enabling was successful

        """
        try:
            if not plugin_name:
                return FlextResult[bool].fail("Plugin name is required")
            return self.manager_port.enable_plugin(plugin_name)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to enable plugin: {e}")

    def disable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Disable a plugin.

        Args:
            plugin_name: Name of plugin to disable
        Returns:
            FlextResult indicating if disabling was successful

        """
        try:
            if not plugin_name:
                return FlextResult[bool].fail("Plugin name is required")
            return self.manager_port.disable_plugin(plugin_name)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to disable plugin: {e}")

    def get_plugin_config(self, plugin_name: str) -> FlextResult[FlextPluginConfig]:
        """Get configuration for a plugin.

        Args:
            plugin_name: Name of plugin to get config for
        Returns:
            FlextResult containing plugin configuration

        """
        try:
            if not plugin_name:
                return FlextResult[FlextPluginConfig].fail("Plugin name is required")
            return self.manager_port.get_plugin_config(plugin_name)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[FlextPluginConfig].fail(
                f"Failed to get plugin config: {e}"
            )

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
                return FlextResult[bool].fail("Plugin name is required")
            if not config.is_valid():
                return FlextResult[bool].fail("Invalid plugin configuration")
            return self.manager_port.update_plugin_config(plugin_name, config)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to update plugin config: {e}")

    def is_plugin_loaded(self, plugin_name: str) -> FlextResult[bool]:
        """Check if a plugin is loaded.

        Args:
            plugin_name: Name of plugin to check
        Returns:
            FlextResult indicating if plugin is loaded

        """
        try:
            if not plugin_name:
                return FlextResult[bool].fail("Plugin name is required")
            return self.loader_port.is_plugin_loaded(plugin_name)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to check plugin status: {e}")


class FlextPluginDiscoveryService(FlextDomainService[object]):
    """Specialized service for plugin discovery and validation operations."""

    container: FlextContainer
    model_config: ClassVar = {"arbitrary_types_allowed": True, "frozen": False}

    def __init__(self, **kwargs: object) -> None:
        """Initialize plugin discovery service with dependency injection container."""
        # Extract container from kwargs or create default
        container_arg = kwargs.pop("container", None)
        if container_arg is not None:
            kwargs["container"] = container_arg
        else:
            kwargs["container"] = FlextContainer()
        super().__init__(**kwargs)
        # Store private attributes
        object.__setattr__(self, "_discovery_port", None)

    @override
    def execute(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        _ = args, kwargs  # Mark as intentionally unused
        return FlextResult[object].fail(
            "Use specific service methods instead of execute"
        )

    @property
    def discovery_port(self) -> FlextPluginDiscoveryPort:
        """Get plugin discovery port."""
        discovery_port = getattr(self, "_discovery_port", None)
        if discovery_port is None:
            result = self.container.get("plugin_discovery_port")
            if result.success and isinstance(result.data, FlextPluginDiscoveryPort):
                discovery_port_data: FlextPluginDiscoveryPort = result.data  # noqa: E501
                object.__setattr__(self, "_discovery_port", discovery_port_data)
                return discovery_port_data
        if isinstance(discovery_port, FlextPluginDiscoveryPort):
            return discovery_port

        # Return a mock implementation if none available
        # Create a simple adapter that implements the interface
        class MockDiscoveryPort(FlextPluginDiscoveryPort):
            @override
            def discover_plugins(
                self, path: str  # noqa: ARG002
            ) -> FlextResult[list[FlextPluginEntity]]:
                return FlextResult[list[FlextPluginEntity]].ok([])

            @override
            def validate_plugin(self, plugin: FlextPluginEntity) -> FlextResult[bool]:  # noqa: ARG002
                success = True
                return FlextResult[bool].ok(success)

        return MockDiscoveryPort()

    def scan_directory(
        self, directory_path: str
    ) -> FlextResult[list[FlextPluginEntity]]:
        """Scan directory for plugins.

        Args:
            directory_path: Directory to scan
        Returns:
            FlextResult containing discovered plugins

        """
        try:
            if not directory_path:
                return FlextResult[list[FlextPluginEntity]].fail(
                    "Directory path is required"
                )
            return self.discovery_port.discover_plugins(directory_path)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[list[FlextPluginEntity]].fail(
                f"Failed to scan directory: {e}"
            )

    def validate_plugin_integrity(self, plugin: FlextPluginEntity | None) -> FlextResult[bool]:
        """Validate plugin integrity.

        Args:
            plugin: Plugin to validate (can be None)

        Returns:
            FlextResult indicating if plugin is valid

        """
        try:
            if not plugin:
                return FlextResult[bool].fail("Plugin is required")
            return self.discovery_port.validate_plugin(plugin)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Failed to validate plugin: {e}")


# Backwards compatibility aliases
PluginService = FlextPluginService
PluginDiscoveryService = FlextPluginDiscoveryService
