"""FLEXT Plugin API - Thin facade for comprehensive plugin management.

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

from flext_plugin.flext_plugin_platform import FlextPluginPlatform


class FlextPlugin(FlextService[None]):
    """Thin facade for comprehensive plugin management with complete FLEXT ecosystem integration.

    The main entry point for all plugin operations within the FLEXT ecosystem.
    Implements the Facade pattern to provide a simplified, unified interface to the
    complex plugin management subsystem while maintaining Clean Architecture principles.

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
      - FlextPluginPlatform: Core plugin platform with lifecycle management
      - Container-based dependency injection and service resolution
      - Automatic service registration and lifecycle management
      - Event-driven architecture for plugin state changes
      - Comprehensive monitoring and observability integration

    Usage Patterns:
      - Primary entry point for external plugin management
      - Facade for complex plugin operations and workflows
      - Integration point for web APIs, CLI commands, and external systems
      - Testing boundary for comprehensive system testing

    Example:
      >>> # Initialize plugin system with default configuration
      >>> plugin_system = FlextPlugin()
      >>>
      >>> # Full plugin management workflow
      >>> discovery_result: FlextResult[list] = plugin_system.discover_plugins("./plugins")
      >>> if discovery_result.success:
      ...     for plugin in discovery_result.value:
      ...         # Validate plugin before loading
      ...         validation = plugin_system.validate_plugin(plugin)
      ...         if validation.success and validation.value:
      ...             # Load validated plugin
      ...             load_result: FlextResult[bool] = plugin_system.load_plugin(plugin)
      ...             if load_result.success:
      ...                 print(f"Successfully loaded plugin: {plugin.name}")
      >>>
      >>> # Configuration management
      >>> config_result: FlextResult[dict] = plugin_system.get_plugin_config("my-plugin")
      >>> if config_result.success:
      ...     config: dict[str, object] = config_result.value
      ...     # Modify configuration and update
      ...     update_result: FlextResult[bool] = plugin_system.update_plugin_config(
      ...         "my-plugin", config
      ...     )

    Error Handling:
      All facade methods return FlextResult objects for consistent error
      handling and railway-oriented programming patterns. The facade
      coordinates error handling across all service layers while providing
      meaningful error messages and recovery suggestions.

    Args:
        container: Optional FlextContainer instance for dependency injection.
                  If None, uses the global container with all required services
                  for plugin management operations.
    """

    @override
    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize plugin management facade with complete FLEXT ecosystem integration.

        Sets up the plugin system facade with proper dependency injection container and
        initializes all required application services for plugin management operations.
        The facade uses the container to manage service lifecycles and coordinate
        dependencies across the plugin management system.

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
        """
        super().__init__()
        self._container = container or FlextContainer()

        # Complete FLEXT ecosystem integration
        self._bus = FlextBus()
        self._context = FlextContext()
        self._dispatcher = FlextDispatcher()
        self._processors = FlextProcessors()
        self._registry = FlextRegistry(dispatcher=self._dispatcher)
        self._logger = FlextLogger(__name__)

        # Core platform service
        self._platform = FlextPluginPlatform(self._container)

    @override
    def execute(self) -> FlextResult[None]:
        """Execute facade initialization (required by FlextService)."""
        return FlextResult[None].ok(None)

    # Delegate all operations to the platform with FLEXT ecosystem integration
    def discover_plugins(self, path: str) -> FlextResult[list]:
        """Discover plugins in the given path."""
        return self._platform.discover_plugins(path)

    def load_plugin(self, plugin) -> FlextResult[bool]:
        """Load a plugin."""
        return self._platform.load_plugin(plugin)

    def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unload a plugin."""
        return self._platform.unload_plugin(plugin_name)

    def install_plugin(self, plugin_path: str) -> FlextResult:
        """Install a plugin from the given path."""
        return self._platform.install_plugin(plugin_path)

    def uninstall_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Uninstall a plugin."""
        return self._platform.uninstall_plugin(plugin_name)

    def enable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Enable a plugin."""
        return self._platform.enable_plugin(plugin_name)

    def disable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Disable a plugin."""
        return self._platform.disable_plugin(plugin_name)

    def get_plugin_config(self, plugin_name: str) -> FlextResult:
        """Get configuration for a plugin."""
        return self._platform.get_plugin_config(plugin_name)

    def update_plugin_config(self, plugin_name: str, config) -> FlextResult[bool]:
        """Update configuration for a plugin."""
        return self._platform.update_plugin_config(plugin_name, config)

    def is_plugin_loaded(self, plugin_name: str) -> FlextResult[bool]:
        """Check if a plugin is loaded."""
        return self._platform.is_plugin_loaded(plugin_name)

    def scan_directory(self, directory_path: str) -> FlextResult[list]:
        """Scan directory for plugins."""
        return self._platform.scan_directory(directory_path)

    def validate_plugin(self, plugin) -> FlextResult[bool]:
        """Validate plugin integrity."""
        return self._platform.validate_plugin(plugin)


__all__ = [
    "FlextPlugin",
]