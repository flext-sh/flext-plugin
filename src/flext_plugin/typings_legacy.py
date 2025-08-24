"""Legacy compatibility classes for FLEXT Plugin system.

This module maintains backwards compatibility with existing code
while the system transitions to the new centralized typing structure.
These classes will eventually be deprecated.
"""

from __future__ import annotations

from typing import cast

from flext_core import FlextProcessingError, FlextResult

from flext_plugin.domain.entities import FlextPluginEntity


class PluginError(FlextProcessingError):
    """Legacy plugin error class for backwards compatibility."""

    def __init__(
        self,
        message: str,
        plugin_name: str = "",
        plugin_id: str = "",
        **kwargs: object,
    ) -> None:
        """Initialize plugin error with message and identifiers."""
        super().__init__(message)
        self.plugin_name = plugin_id or plugin_name
        self.plugin_id = plugin_id or plugin_name
        # Store additional context if provided (except read-only properties)
        for key, value in kwargs.items():
            if key != "error_code":  # Skip read-only properties
                setattr(self, key, value)


class PluginExecutionResult:
    """Legacy execution result class for backwards compatibility."""

    def __init__(
        self,
        *,
        success: bool = False,
        data: object = None,
        error: str = "",
        plugin_name: str = "",
        execution_time: float = 0.0,
        **kwargs: object,
    ) -> None:
        """Initialize result with success flag, data, and metadata."""
        self._success = success
        self.data = kwargs.get("output_data", data)
        self.error = kwargs.get("error_message", error)
        self.plugin_name = plugin_name
        self.execution_time = execution_time
        self.execution_id = kwargs.get("execution_id", plugin_name)
        self.duration_ms = kwargs.get("duration_ms", execution_time * 1000)
        self.output_data = self.data
        self.error_message = self.error

    @property
    def success(self) -> bool:
        """Return True when execution succeeded."""
        return self._success

    def is_failure(self) -> bool:
        """Return True when execution failed."""
        return not self._success


class PluginExecutionContext:
    """Legacy execution context class for backwards compatibility."""

    def __init__(
        self,
        plugin_id: str,
        execution_id: str,
        *,
        input_data: dict[str, object] | None = None,
        context: dict[str, object] | None = None,
        timeout_seconds: int | None = None,
    ) -> None:
        """Initialize context with identifiers and optional data."""
        self.plugin_id = plugin_id
        self.execution_id = execution_id
        self.input_data = input_data or {}
        self.context = context or {}
        self.timeout_seconds = timeout_seconds


class PluginManagerResult:
    """Legacy manager result class for backwards compatibility."""

    def __init__(self, operation: str, *, success: bool = False) -> None:
        """Initialize manager result for a specific operation."""
        self.operation = operation
        self._success = success
        self.plugins_affected: list[str] = []
        self.execution_time_ms: float = 0.0
        self.details: dict[str, object] = {}
        self.errors: list[str] = []

    @property
    def success(self) -> bool:
        """Return True if operation succeeded."""
        return self._success

    @classmethod
    def create_detailed(
        cls,
        operation: str,
        config: dict[str, object],
    ) -> PluginManagerResult:
        """Create detailed manager result from a configuration mapping."""
        result = cls(operation, success=bool(config.get("success")))
        result.plugins_affected = cast("list[str]", config.get("plugins_affected", []))
        execution_time = cast("float", config.get("execution_time_ms", 0.0))
        result.execution_time_ms = float(execution_time)
        result.details = cast("dict[str, object]", config.get("details", {}))
        result.errors = cast("list[str]", config.get("errors", []))
        return result


class SimplePluginRegistry:
    """Legacy plugin registry class for backwards compatibility."""

    def __init__(self) -> None:
        """Initialize empty simple plugin registry."""
        self._plugins: dict[str, FlextPluginEntity] = {}

    async def register_plugin(
        self, plugin: FlextPluginEntity
    ) -> FlextResult[FlextPluginEntity]:
        """Register plugin instance ensuring required fields."""
        try:
            if not hasattr(plugin, "name"):
                return FlextResult[FlextPluginEntity].fail(
                    "Plugin registration failed: missing name"
                )
            if not hasattr(plugin, "metadata"):
                return FlextResult[FlextPluginEntity].fail(
                    "Plugin registration failed: missing metadata"
                )
            plugin_name: str = plugin.name
            self._plugins[plugin_name] = plugin
            return FlextResult[FlextPluginEntity].ok(plugin)
        except Exception as e:
            return FlextResult[FlextPluginEntity].fail(
                f"Plugin registration failed: {e}"
            )

    async def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unregister plugin by name."""
        if plugin_name in self._plugins:
            del self._plugins[plugin_name]
        return FlextResult[bool].ok(data=True)

    def get_plugin(self, plugin_name: str) -> FlextPluginEntity | None:
        """Get plugin instance by name."""
        return self._plugins.get(plugin_name)

    def get_plugin_count(self) -> int:
        """Return number of registered plugins."""
        return len(self._plugins)

    def list_plugins(self, plugin_type: object | None = None) -> list[object]:
        """List plugin metadata optionally filtered by type."""
        if plugin_type is None:
            return list(self._plugins.values())
        # Handle both direct comparison and string comparison for FlextPluginEntity
        return [
            p
            for p in self._plugins.values()
            if (
                hasattr(p, "plugin_type")
                and (
                    p.plugin_type == plugin_type
                    or (
                        hasattr(p.plugin_type, "value")
                        and p.plugin_type.value == plugin_type
                    )
                    or (
                        hasattr(plugin_type, "value")
                        and p.plugin_type == plugin_type.value
                    )
                )
            )
        ]

    async def cleanup_all(self) -> None:
        """Clear all registered plugins."""
        self._plugins.clear()


def create_plugin_manager(
    _container: object | None = None,
    *,
    _auto_discover: bool = True,
    _security_enabled: bool = True,
) -> SimplePluginRegistry:
    """Legacy factory function for backwards compatibility."""
    return SimplePluginRegistry()


__all__ = [
    "PluginError",
    "PluginExecutionContext",
    "PluginExecutionResult",
    "PluginManagerResult",
    "SimplePluginRegistry",
    "create_plugin_manager",
]
