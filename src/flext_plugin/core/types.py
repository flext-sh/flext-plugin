"""FLEXT Plugin Core Types - Foundational type system for plugin management.

This module provides the core type definitions, enumerations, and result objects
that form the foundation of the FLEXT plugin system. It defines plugin lifecycle
states, categorization types, error handling classes, and execution contexts
following enterprise software patterns.

The type system is designed to support:
- Plugin lifecycle management with clear state transitions
- Singer/Meltano ecosystem integration for data pipeline plugins
- Microservice and API integration patterns
- Comprehensive error handling with detailed context
- Type-safe plugin execution and result management

Architecture Integration:
    Built on flext-core foundation patterns, this module integrates with:
    - FlextResult for railway-oriented programming
    - FlextProcessingError for consistent error handling
    - Clean Architecture layer separation
    - Domain-Driven Design type modeling

Example:
    >>> from flext_plugin.core.types import PluginStatus, PluginType
    >>> status = PluginStatus.ACTIVE
    >>> plugin_type = PluginType.TAP  # Singer data extraction
    >>> print(f"Plugin type: {plugin_type.value}, Status: {status.value}")

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import Enum
from typing import cast

from flext_core import FlextProcessingError, FlextResult


class PluginStatus(Enum):
    """Plugin lifecycle and health status enumeration.

    Defines the complete set of plugin states throughout the plugin lifecycle,
    from initial discovery through active execution and potential error states.
    The status system supports both operational states and health monitoring.

    Lifecycle Flow:
        UNKNOWN → DISCOVERED → LOADED → ACTIVE ↔ INACTIVE
                                    ↓
                             ERROR → DISABLED

    Health States:
        HEALTHY/UNHEALTHY can be combined with operational states
        to provide comprehensive plugin monitoring.

    Usage:
        >>> plugin.status = PluginStatus.ACTIVE
        >>> if plugin.status in [PluginStatus.ACTIVE, PluginStatus.INACTIVE]:
        ...     print("Plugin is operational")
    """

    # Lifecycle states - Primary operational states
    UNKNOWN = "unknown"          # Initial state, plugin not yet analyzed
    DISCOVERED = "discovered"    # Plugin found but not yet loaded
    LOADED = "loaded"           # Plugin loaded into memory, ready for activation
    ACTIVE = "active"           # Plugin is running and available for execution
    INACTIVE = "inactive"       # Plugin loaded but not currently active
    LOADING = "loading"         # Transitional state during plugin loading
    ERROR = "error"             # Plugin encountered error and cannot operate
    DISABLED = "disabled"       # Plugin intentionally disabled by system/user

    # Health states - Can be combined with lifecycle states
    HEALTHY = "healthy"         # Plugin is functioning normally
    UNHEALTHY = "unhealthy"     # Plugin showing signs of degraded performance


class PluginType(Enum):
    """Plugin categorization system for FLEXT ecosystem integration.

    Comprehensive plugin type classification supporting multiple integration
    patterns across the FLEXT platform. Types are organized by functional
    category to enable discovery, validation, and orchestration.

    Categories:
        - Singer ETL: Data pipeline integration with Meltano
        - Architecture: Microservice and system integration patterns
        - Integration: External system connectivity
        - Utility: General-purpose tools and processors
        - System: Core platform extensions and themes

    Singer Integration:
        TAP, TARGET, and TRANSFORM types automatically integrate with
        Meltano projects and follow Singer specification patterns.

    Usage:
        >>> plugin_type = PluginType.TAP
        >>> if plugin_type in [PluginType.TAP, PluginType.TARGET]:
        ...     print("Singer ecosystem plugin")
    """

    # Singer ETL types - Data pipeline integration with Meltano ecosystem
    TAP = "tap"                     # Data extraction from sources (Singer spec)
    TARGET = "target"               # Data loading to destinations (Singer spec)
    TRANSFORM = "transform"         # Data transformation with DBT integration

    # Architecture types - Microservice and system integration patterns
    EXTENSION = "extension"         # Platform extensions and add-ons
    SERVICE = "service"             # Microservice components
    MIDDLEWARE = "middleware"       # Request/response processing
    TRANSFORMER = "transformer"    # Data transformation utilities

    # Integration types - External system connectivity
    API = "api"                     # REST/GraphQL API endpoints
    DATABASE = "database"           # Database connectivity (Oracle, PostgreSQL)
    NOTIFICATION = "notification"   # Notification and messaging services
    AUTHENTICATION = "authentication"  # Authentication providers
    AUTHORIZATION = "authorization"     # Authorization and access control

    # Utility types - General-purpose tools and processors
    UTILITY = "utility"             # General-purpose utilities
    TOOL = "tool"                   # Development and REDACTED_LDAP_BIND_PASSWORDistrative tools
    HANDLER = "handler"             # Event and message handlers
    PROCESSOR = "processor"         # Data and content processors

    # System types - Core platform components
    CORE = "core"                   # Core system plugins
    ADDON = "addon"                 # System add-ons and enhancements
    THEME = "theme"                 # UI themes and customizations
    LANGUAGE = "language"           # Language and localization plugins


class PluginError(FlextProcessingError):
    """Base exception for plugin-related errors in the FLEXT ecosystem.

    Extends FlextProcessingError to provide plugin-specific error context
    and metadata. This exception class serves as the base for all plugin
    system errors, enabling consistent error handling and debugging.

    The error includes plugin identification information to help with
    troubleshooting and error tracking across the plugin lifecycle.

    Attributes:
        plugin_name: Name of the plugin that caused the error
        plugin_id: Unique identifier for the plugin (alias for plugin_name)
        message: Human-readable error message

    Usage:
        >>> try:
        ...     plugin.execute(data)
        ... except PluginError as e:
        ...     logger.error(f"Plugin {e.plugin_name} failed: {e}")

    """

    def __init__(
        self,
        message: str,
        plugin_name: str = "",
        plugin_id: str = "",
        **kwargs: object,
    ) -> None:
        """Initialize plugin error with context information.

        Args:
            message: Human-readable error description explaining what went wrong
            plugin_name: Name of the plugin that caused the error, used for
                        identification and logging purposes
            plugin_id: Unique identifier for the plugin, takes precedence over
                      plugin_name if both are provided
            **kwargs: Additional error context passed to the base exception,
                     may include stack traces, error codes, or other metadata

        Note:
            If both plugin_name and plugin_id are provided, plugin_id takes
            precedence and is used for both attributes to maintain consistency.

        """
        super().__init__(message, **kwargs)
        # Use plugin_id if provided, otherwise use plugin_name
        self.plugin_name = plugin_id or plugin_name
        self.plugin_id = plugin_id or plugin_name


class PluginExecutionResult:
    """Comprehensive result container for plugin execution operations.

    Encapsulates the outcome of plugin execution with detailed metadata,
    performance metrics, and error information. Provides a standardized
    interface for handling plugin execution results across the FLEXT ecosystem.

    This class supports both success and failure scenarios, including
    partial failures where some data is available despite errors.

    Attributes:
        success: Boolean indicating execution success
        data: Primary execution result data
        error: Error message for failures
        plugin_name: Name of the executed plugin
        execution_time: Execution duration in seconds
        duration_ms: Execution duration in milliseconds (derived)
        execution_id: Unique execution identifier

    Usage:
        >>> result = PluginExecutionResult(
        ...     success=True,
        ...     data={"processed": 100},
        ...     plugin_name="data-processor",
        ...     execution_time=0.5
        ... )
        >>> if result.is_success():
        ...     print(f"Processed {result.data['processed']} items")

    """

    def __init__(
        self,
        *,
        success: bool = False,
        data: object = None,
        error: str = "",
        plugin_name: str = "",
        execution_time: float = 0.0,
        **kwargs: object,  # Accept additional arguments for backward compatibility
    ) -> None:
        """Initialize plugin execution result with comprehensive metadata.

        Args:
            success: True if plugin execution completed successfully,
                    False if any errors occurred during execution
            data: Primary result data from plugin execution, can be any
                 serializable object (dict, list, string, etc.)
            error: Human-readable error message describing any failures
                  that occurred during execution
            plugin_name: Name of the plugin that was executed, used for
                        logging and debugging purposes
            execution_time: Total execution time in seconds (float precision),
                          used for performance monitoring and optimization
            **kwargs: Additional execution metadata for backward compatibility,
                     supports legacy field names and custom execution context

        Note:
            The kwargs parameter provides backward compatibility with older
            versions and supports additional metadata like execution_id,
            output_data, error_message, and duration_ms.

        """
        self.success = success
        self.data = kwargs.get("output_data", data)
        self.error = kwargs.get("error_message", error)
        self.plugin_name = plugin_name
        self.execution_time = execution_time

        # Additional properties for comprehensive result tracking
        self.execution_id = kwargs.get("execution_id", plugin_name)
        self.duration_ms = kwargs.get("duration_ms", execution_time * 1000)

        # Backward compatibility aliases
        self.output_data = self.data
        self.error_message = self.error

    def is_success(self) -> bool:
        """Check if plugin execution was successful.

        Returns:
            True if the plugin executed without errors, False otherwise.

        Note:
            Success is determined by the success flag set during initialization,
            not by the presence or absence of data or error messages.

        """
        return self.success

    def is_failure(self) -> bool:
        """Check if plugin execution failed.

        Returns:
            True if the plugin execution encountered errors, False otherwise.

        Note:
            This is the logical inverse of is_success() for convenience
            in error handling and control flow.

        """
        return not self.success


class PluginExecutionContext:
    """Context for plugin execution."""

    def __init__(
        self,
        plugin_id: str,
        execution_id: str,
        *,
        input_data: dict[str, object] | None = None,
        context: dict[str, object] | None = None,
        timeout_seconds: int | None = None,
    ) -> None:
        """Initialize plugin execution context."""
        self.plugin_id = plugin_id
        self.execution_id = execution_id
        self.input_data = input_data or {}
        self.context = context or {}
        self.timeout_seconds = timeout_seconds


class PluginManagerResult:
    """Result of plugin manager operations."""

    def __init__(self, operation: str, *, success: bool = False) -> None:
        """Initialize plugin manager result with minimal parameters."""
        self.operation = operation
        self.success = success
        self.plugins_affected: list[str] = []
        self.execution_time_ms: float = 0.0
        self.details: dict[str, object] = {}
        self.errors: list[str] = []

    @classmethod
    def create_detailed(
        cls,
        operation: str,
        config: dict[str, object],
    ) -> PluginManagerResult:
        """Create detailed plugin manager result from config dict."""
        result = cls(operation, success=bool(config.get("success")))
        result.plugins_affected = cast("list[str]", config.get("plugins_affected", []))
        execution_time = cast("float", config.get("execution_time_ms", 0.0))
        result.execution_time_ms = (
            float(execution_time) if execution_time is not None else 0.0
        )
        result.details = cast("dict[str, object]", config.get("details", {}))
        result.errors = cast("list[str]", config.get("errors", []))
        return result


class SimplePluginRegistry:
    """Simple plugin registry for testing."""

    def __init__(self) -> None:
        """Initialize simple registry."""
        self._plugins: dict[str, object] = {}

    async def register_plugin(self, plugin: object) -> FlextResult[object]:
        """Register a plugin."""
        try:
            # Mock validation - check if plugin has metadata and name
            if not hasattr(plugin, "metadata") or plugin.metadata is None:
                return FlextResult.fail("Plugin registration failed: missing metadata")

            if not hasattr(plugin.metadata, "name"):
                return FlextResult.fail("Plugin registration failed: missing name")

            self._plugins[plugin.metadata.name] = plugin
            return FlextResult.ok(plugin)
        except Exception as e:
            return FlextResult.fail(f"Plugin registration failed: {e}")

    async def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unregister a plugin."""
        if plugin_name in self._plugins:
            del self._plugins[plugin_name]
        plugin_unregistered = True
        return FlextResult.ok(plugin_unregistered)

    def get_plugin(self, plugin_name: str) -> object | None:
        """Get a plugin by name."""
        return self._plugins.get(plugin_name)

    def get_plugin_count(self) -> int:
        """Get plugin count."""
        return len(self._plugins)

    def list_plugins(self, plugin_type: PluginType | None = None) -> list[object]:
        """List plugins with optional type filter."""
        if plugin_type is None:
            return [
                p.metadata for p in self._plugins.values() if hasattr(p, "metadata")
            ]

        return [
            p.metadata
            for p in self._plugins.values()
            if hasattr(p, "metadata")
            and hasattr(p.metadata, "plugin_type")
            and p.metadata.plugin_type == plugin_type
        ]

    async def cleanup_all(self) -> None:
        """Cleanup all plugins."""
        self._plugins.clear()


def create_plugin_manager(
    _container: object | None = None,
    *,
    _auto_discover: bool = True,
    _security_enabled: bool = True,
) -> object:
    """Create plugin manager - factory function.

    Note: This is a lightweight factory that delays import to avoid circular
    dependencies. The actual PluginManager implementation should be imported
    when needed.
    """
    # Return a simple registry as default implementation
    # This avoids circular imports while providing functionality
    return SimplePluginRegistry()


__all__ = [
    "PluginError",
    "PluginExecutionContext",
    "PluginExecutionResult",
    "PluginManagerResult",
    "PluginStatus",
    "PluginType",
    "SimplePluginRegistry",
    "create_plugin_manager",
]
