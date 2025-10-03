"""FLEXT Plugin Platform - Unified facade providing comprehensive plugin management.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import (
    FlextBus,
    FlextContainer,
    FlextContext,
    FlextDispatcher,
    FlextLogger,
    FlextProcessors,
    FlextRegistry,
    FlextResult,
    FlextService,
)

from flext_plugin.entities import FlextPluginConfig, FlextPluginEntity
from flext_plugin.flext_plugin_services import (
    FlextPluginDiscoveryService,
    FlextPluginService,
)


class FlextPluginPlatform(FlextService[None]):
    """Unified plugin management platform with complete FLEXT ecosystem integration.

    The main platform class that serves as the primary entry point for plugin
    management operations within the FLEXT ecosystem. Implements the Facade pattern
    to provide a simplified, unified interface to the complex plugin management
    subsystem while maintaining Clean Architecture principles.

    Extends FlextService and integrates the complete FLEXT ecosystem:
    - FlextBus: Event emission for plugin lifecycle events
    - FlextContainer: Dependency injection and service management
    - FlextContext: Operation context tracking and correlation
    - FlextCqrs: CQRS pattern for plugin operations and queries
    - FlextDispatcher: Message routing and command coordination
    - FlextProcessors: Processing utilities for plugin workflows
    - FlextRegistry: Component registration and discovery
    - FlextLogger: Structured logging for plugin operations
    - FlextResult: Railway-oriented programming for all operations

    Key Features:
      - Unified API facade for all plugin operations
      - Complete FLEXT ecosystem component integration
      - Dependency injection container management
      - Service lifecycle coordination and management
      - Comprehensive error handling and result coordination
      - Integration support for external systems and frameworks
    Architecture Integration:
      - Implements Clean Architecture platform layer patterns
      - Extends FlextService for consistent service behavior
      - Coordinates application services without containing business logic
      - Manages cross-cutting concerns like dependency injection
      - Provides external integration points and API boundaries
      - Maintains separation of concerns across architectural layers
    Service Coordination:
      - FlextPluginService: Core plugin management operations
      - FlextPluginDiscoveryService: Plugin discovery and validation
      - Container-based dependency injection and service resolution
      - Automatic service registration and lifecycle management
    Usage Patterns:
      - Primary entry point for external plugin management
      - Facade for complex plugin operations and workflows
      - Integration point for web APIs, CLI commands, and external systems
      - Testing boundary for comprehensive system testing
    Example:
      >>> # Initialize platform with default container
      >>> platform = FlextPluginPlatform()
      >>>
      >>> # Full plugin management workflow
      >>> discovery_result: FlextResult[object] = platform.discover_plugins("./plugins")
      >>> if discovery_result.success:
      ...     for plugin in discovery_result.value:
      ...         # Validate plugin before loading
      ...         validation = platform.validate_plugin(plugin)
      ...         if validation.success and validation.value:
      ...             # Load validated plugin
      ...             load_result: FlextResult[object] = platform.load_plugin(plugin)
      ...             if load_result.success:
      ...                 print(f"Successfully loaded plugin: {plugin.name}")
      >>>
      >>> # Configuration management
      >>> config_result: FlextResult[object] = platform.get_plugin_config("my-plugin")
      >>> if config_result.success:
      ...     config: dict[str, object] = config_result.value
      ...     # Modify configuration and update
      ...     update_result: FlextResult[object] = platform.update_plugin_config(
      ...         "my-plugin", config
      ...     )
    Error Handling:
      All platform methods return FlextResult objects for consistent error
      handling and railway-oriented programming patterns. The platform
      coordinates error handling across all service layers while providing
      meaningful error messages and recovery suggestions.
    """

    @override
    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize plugin management platform with complete FLEXT ecosystem integration.

        Sets up the platform with proper dependency injection container and
        initializes all required application services for plugin management
        operations. The platform uses the container to manage service lifecycles
        and coordinate dependencies across the plugin management system.

        Integrates complete FLEXT ecosystem components:
        - FlextBus: Event emission for plugin lifecycle events
        - FlextContainer: Dependency injection and service management
        - FlextContext: Operation context tracking and correlation
        - FlextCqrs: CQRS pattern for plugin operations and queries
        - FlextDispatcher: Message routing and command coordination
        - FlextProcessors: Processing utilities for plugin workflows
        - FlextRegistry: Component registration and discovery
        - FlextLogger: Structured logging for plugin operations

        Args:
            container: Optional FlextContainer instance for dependency injection.
                      If None, a new default container will be created and configured
                      with all required services for plugin management operations.
        Initialization Process:
            1. Container setup and configuration
            2. Service registration and dependency injection
            3. FLEXT ecosystem component integration
            4. Platform service coordination and integration
            5. Error handling and recovery mechanism setup
        Note:
            The platform automatically registers all required services in the
            container during initialization. External services can be registered
            in the provided container before platform initialization for
            customization and testing scenarios.

        Returns:
            object: Description of return value.

        """
        super().__init__()
        self.container = container or FlextContainer()
        self._logger = FlextLogger(__name__)

        # Complete FLEXT ecosystem integration
        self._bus = FlextBus()
        self._context = FlextContext()
        self._cqrs = FlextCqrs()
        self._dispatcher = FlextDispatcher()
        self._processors = FlextProcessors()
        self._registry = FlextRegistry(dispatcher=self._dispatcher)

        self._setup_services()

    @override
    def execute(self) -> FlextResult[None]:
        """Execute platform initialization (required by FlextService)."""
        return FlextResult[None].ok(None)

    def _setup_services(self) -> None:
        """Set up platform services in the container."""
        # Register services in container
        # DRY SOLID pattern: Use container kwarg for service initialization
        self.container.register(
            "plugin_service",
            FlextPluginService(container=self.container),
        )
        self.container.register(
            "plugin_discovery_service",
            FlextPluginDiscoveryService(container=self.container),
        )

    @property
    def plugin_service(self) -> FlextPluginService:
        """Get plugin management service."""
        result: FlextResult[object] = self.container.get("plugin_service")
        if result.success and isinstance(result.data, FlextPluginService):
            return result.data
        msg: str = f"Failed to get plugin service: {result.error}"
        raise RuntimeError(msg)

    @property
    def discovery_service(self) -> FlextPluginDiscoveryService:
        """Get plugin discovery service."""
        result: FlextResult[object] = self.container.get("plugin_discovery_service")
        if result.success and isinstance(result.data, FlextPluginDiscoveryService):
            return result.data
        msg: str = f"Failed to get discovery service: {result.error}"
        raise RuntimeError(msg)

    def discover_plugins(self, path: str) -> FlextResult[list[FlextPluginEntity]]:
        """Discover plugins in the given path.

        Args:
            path: Path to search for plugins
        Returns:
            FlextResult containing list of discovered plugins

        """
        return self.plugin_service.discover_plugins(path)

    def load_plugin(self, plugin: FlextPluginEntity) -> FlextResult[bool]:
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

    def install_plugin(self, plugin_path: str) -> FlextResult[FlextPluginEntity]:
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

    def scan_directory(
        self,
        directory_path: str,
    ) -> FlextResult[list[FlextPluginEntity]]:
        """Scan directory for plugins.

        Args:
            directory_path: Directory to scan
        Returns:
            FlextResult containing discovered plugins

        """
        return self.discovery_service.scan_directory(directory_path)

    def validate_plugin(self, plugin: FlextPluginEntity) -> FlextResult[bool]:
        """Validate plugin integrity.

        Args:
            plugin: Plugin to validate
        Returns:
            FlextResult indicating if plugin is valid

        """
        return self.discovery_service.validate_plugin_integrity(plugin)


__all__ = [
    "FlextPluginPlatform",
]
