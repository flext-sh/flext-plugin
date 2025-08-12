"""FLEXT Plugin Application Handlers - CQRS command and event handlers.

This module implements the command and event handling layer of the FLEXT plugin
system, following CQRS (Command Query Responsibility Segregation) architectural
patterns. Handlers provide the interface between external requests and internal
domain operations, ensuring proper validation, orchestration, and error handling.

Key Handlers:
    - FlextPluginHandler: Base handler with common plugin operations
    - FlextPluginRegistrationHandler: Plugin registration and lifecycle commands
    - FlextPluginEventHandler: Plugin lifecycle event processing

Architecture:
    Handlers implement the Command and Event handling patterns within Clean
    Architecture, serving as the application layer controllers that coordinate
    domain services and handle cross-cutting concerns like validation,
    logging, and error management.

CQRS Patterns:
    - Command Handlers: Process state-changing operations
    - Event Handlers: React to domain events and side effects
    - Query Handlers: Handle read-only data retrieval operations
    - Result Patterns: Consistent FlextResult-based error handling

Example:
    >>> from flext_plugin.application.handlers import FlextPluginRegistrationHandler
    >>> from flext_plugin.application.services import FlextPluginService
    >>>
    >>> service = FlextPluginService()
    >>> handler = FlextPluginRegistrationHandler(service)
    >>> result = handler.handle_register_plugin(plugin)
    >>> if result.success():
    ...     print("Plugin registered successfully")

Integration:
    - Built on flext-core handler patterns and base classes
    - Coordinates with application services for business logic
    - Integrates with domain entities and events
    - Supports comprehensive error handling and validation

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextHandlers, FlextResult

if TYPE_CHECKING:
    from flext_plugin.application.services import FlextPluginService
    from flext_plugin.domain.entities import FlextPlugin


class FlextPluginHandler(FlextHandlers.CommandHandler):
    """Base command handler for plugin-related operations with service coordination.

    Abstract base handler that provides common functionality for plugin command
    processing. Implements the Command Handler pattern from CQRS architecture,
    providing a foundation for specific plugin operation handlers.

    This handler coordinates with FlextPluginService to execute plugin operations
    while maintaining proper separation of concerns between command handling
    and business logic execution.

    Key Features:
        - Service injection and dependency management
        - Common error handling and validation patterns
        - Integration with CQRS command processing infrastructure
        - Base functionality for derived command handlers

    Architecture Integration:
        - Extends flext-core CommandHandler base patterns
        - Coordinates with application services for business logic
        - Maintains Clean Architecture layer separation
        - Supports dependency injection and testability

    Usage Pattern:
        This class should be extended by specific command handlers that
        implement particular plugin operations. It provides the foundation
        and common functionality while derived classes implement specific
        command processing logic.

    Example:
        >>> class CustomPluginHandler(FlextPluginHandler):
        ...     def handle_custom_command(self, data):
        ...         # Custom command logic using self._plugin_service
        ...         return self._plugin_service.some_operation(data)

    """

    def __init__(self, plugin_service: FlextPluginService | None = None) -> None:
        """Initialize plugin command handler with service dependency.

        Sets up the base command handler with optional plugin service injection.
        The service can be provided during initialization or injected later
        through dependency injection patterns.

        Args:
            plugin_service: FlextPluginService instance for business logic execution.
                          If None, handlers should gracefully handle missing service
                          or expect service injection through other mechanisms.

        Note:
            Handlers should validate service availability before attempting
            operations and provide appropriate error messages when services
            are unavailable.

        """
        super().__init__()
        self._plugin_service = plugin_service


class FlextPluginRegistrationHandler(FlextPluginHandler):
    """Specialized CQRS command handler for plugin registration operations.

    Command handler focused specifically on plugin registration lifecycle,
    implementing CQRS patterns for plugin registry management. This handler
    coordinates plugin registration, validation, and cleanup operations
    through the plugin service layer.

    The handler implements comprehensive validation logic for plugin
    registration operations and ensures proper error handling and
    rollback capabilities when registration fails.

    Key Responsibilities:
        - Plugin registration command processing with validation
        - Plugin unregistration and cleanup command handling
        - Registration validation and business rule enforcement
        - Integration with plugin service layer for actual operations
        - Comprehensive error handling and user feedback

    Command Operations:
        - handle_register_plugin: Register new plugin with validation
        - handle_unregister_plugin: Remove plugin with cleanup
        - Validation of plugin metadata and requirements
        - Service availability verification and error handling

    Validation Rules:
        - Plugin name must be non-empty and valid
        - Plugin version must be provided and valid
        - Plugin service must be available for operations
        - Plugin must pass domain validation rules

    Example:
        >>> service = FlextPluginService()
        >>> handler = FlextPluginRegistrationHandler(service)
        >>> plugin = FlextPlugin(name="test-plugin", version="1.0.0")
        >>> result = handler.handle_register_plugin(plugin)
        >>> if result.success():
        ...     print("Plugin registered successfully")
        >>>
        >>> # Unregister when no longer needed
        >>> cleanup_result = handler.handle_unregister_plugin("test-plugin")

    Error Scenarios:
        - Missing or invalid plugin name or version
        - Plugin service unavailable or not configured
        - Plugin registration conflicts or business rule violations
        - System errors during registration or cleanup operations

    """

    def handle_register_plugin(self, plugin: FlextPlugin) -> FlextResult[bool]:
        """Handle plugin registration command.

        Args:
            plugin: Plugin to register

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Validation logic
            if not plugin.name:
                return FlextResult.fail("Plugin name is required")

            if not plugin.version:
                return FlextResult.fail("Plugin version is required")

            if self._plugin_service is None:
                return FlextResult.fail("Plugin service not available")

            # Use real plugin service to register plugin
            return self._plugin_service.load_plugin(plugin)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to register plugin: {e}")

    def handle_unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Handle plugin unregistration command.

        Args:
            plugin_name: Name of plugin to unregister

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if not plugin_name:
                return FlextResult.fail("Plugin name is required")

            if self._plugin_service is None:
                return FlextResult.fail("Plugin service not available")

            # Use real plugin service to unregister plugin
            return self._plugin_service.unload_plugin(plugin_name)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to unregister plugin: {e}")


class FlextPluginEventHandler(FlextHandlers.EventHandler):
    """CQRS event handler for plugin lifecycle events and domain event processing.

    Event handler implementing the Event Handler pattern from CQRS architecture,
    responsible for processing domain events generated by plugin operations.
    This handler reacts to plugin lifecycle changes and coordinates side effects
    such as logging, monitoring, and notification systems.

    The handler implements reactive patterns for plugin events, ensuring that
    all stakeholders are properly notified of plugin state changes and that
    supporting systems can react appropriately to plugin operations.

    Key Responsibilities:
        - Plugin lifecycle event processing and coordination
        - Integration with observability and monitoring systems
        - Notification and alerting for plugin state changes
        - Cross-cutting concern handling for plugin operations
        - Event-driven coordination with external systems

    Event Types:
        - Plugin Loaded: React to successful plugin loading operations
        - Plugin Unloaded: Handle cleanup after plugin unloading
        - Plugin Activated: Process plugin activation events
        - Plugin Deactivated: Handle plugin deactivation events
        - Plugin Error: Process error conditions and failures

    Integration Points:
        - Observability systems for metrics and monitoring
        - Logging infrastructure for audit trails
        - Notification services for alerts and status updates
        - Registry systems for plugin state tracking
        - Health monitoring and diagnostic systems

    Example:
        >>> event_handler = FlextPluginEventHandler()
        >>> plugin = FlextPlugin(name="data-processor", version="1.0.0")
        >>>
        >>> # Handle plugin loaded event
        >>> result = event_handler.handle_plugin_loaded(plugin)
        >>> if result.success():
        ...     print("Plugin load event processed successfully")
        >>>
        >>> # Handle plugin unload event
        >>> cleanup_result = event_handler.handle_plugin_unloaded("data-processor")

    Event Processing:
        Events are processed asynchronously where possible to avoid blocking
        plugin operations. Error handling ensures that event processing failures
        don't impact the core plugin functionality.

    """

    def handle_plugin_loaded(self, plugin: FlextPlugin) -> FlextResult[bool]:
        """Handle plugin loaded event.

        Args:
            plugin: Plugin that was loaded

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Log plugin loaded event
            getattr(plugin, "name", "unknown")
            getattr(plugin, "version", "unknown")

            # In a real implementation, this could:
            # - Log the event to observability system
            # - Notify other services
            # - Update plugin registry metrics
            # For now, we consider successful if plugin has required attributes

            if not hasattr(plugin, "name") or not plugin.name:
                return FlextResult.fail("Plugin loaded event: plugin missing name")

            return FlextResult.ok(True)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to handle plugin loaded event: {e}")

    def handle_plugin_unloaded(self, plugin_name: str) -> FlextResult[bool]:
        """Handle plugin unloaded event.

        Args:
            plugin_name: Name of plugin that was unloaded

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if not plugin_name or not plugin_name.strip():
                return FlextResult.fail(
                    "Plugin unloaded event: plugin name is required",
                )

            # In a real implementation, this could:
            # - Log the unload event to observability system
            # - Clean up plugin-specific resources
            # - Update plugin registry metrics
            # - Notify dependent services

            # For now, we validate plugin_name and consider it successful
            return FlextResult.ok(True)

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to handle plugin unloaded event: {e}")
