"""FLEXT Plugin Core Types - Core plugin type definitions.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Core type definitions for the plugin system.
"""

from __future__ import annotations

from enum import Enum
from typing import cast

from flext_core import FlextProcessingError, FlextResult


class PluginStatus(Enum):
    """Plugin status enumeration."""

    # Lifecycle states
    UNKNOWN = "unknown"
    DISCOVERED = "discovered"
    LOADED = "loaded"
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOADING = "loading"
    ERROR = "error"
    DISABLED = "disabled"

    # Health states
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class PluginType(Enum):
    """Plugin type enumeration."""

    # Singer ETL types (for Meltano integration)
    TAP = "tap"
    TARGET = "target"
    TRANSFORM = "transform"

    # Plugin architecture types
    EXTENSION = "extension"
    SERVICE = "service"
    MIDDLEWARE = "middleware"
    TRANSFORMER = "transformer"

    # Plugin integration types
    API = "api"
    DATABASE = "database"
    NOTIFICATION = "notification"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"

    # Plugin utility types
    UTILITY = "utility"
    TOOL = "tool"
    HANDLER = "handler"
    PROCESSOR = "processor"

    # Plugin system types
    CORE = "core"
    ADDON = "addon"
    THEME = "theme"
    LANGUAGE = "language"


class PluginError(FlextProcessingError):
    """Base exception for plugin-related errors."""

    def __init__(
        self, message: str, plugin_name: str = "", plugin_id: str = "", **kwargs: object,
    ) -> None:
        """Initialize plugin error.

        Args:
            message: Error message
            plugin_name: Name of the plugin that caused the error
            plugin_id: ID of the plugin (alias for plugin_name if provided)
            **kwargs: Additional error context

        """
        super().__init__(message, **kwargs)
        # Use plugin_id if provided, otherwise use plugin_name
        self.plugin_name = plugin_id or plugin_name
        self.plugin_id = plugin_id or plugin_name


class PluginExecutionResult:
    """Result of plugin execution with status and data."""

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
        """Initialize plugin execution result.

        Args:
            success: Whether the execution was successful
            data: Execution result data
            error: Error message if execution failed
            plugin_name: Name of the executed plugin
            execution_time: Time taken for execution in seconds
            **kwargs: Additional arguments for backward compatibility

        """
        self.success = success
        self.data = kwargs.get("output_data", data)
        self.error = kwargs.get("error_message", error)
        self.plugin_name = plugin_name
        self.execution_time = execution_time

        # Additional properties for test compatibility
        self.execution_id = kwargs.get("execution_id", plugin_name)
        self.duration_ms = kwargs.get("duration_ms", execution_time * 1000)
        self.output_data = self.data
        self.error_message = self.error

    def is_success(self) -> bool:
        """Check if execution was successful."""
        return self.success

    def is_failure(self) -> bool:
        """Check if execution failed."""
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
