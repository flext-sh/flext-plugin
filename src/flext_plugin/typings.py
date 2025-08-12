"""FLEXT Plugin Types - Centralized type system for plugin management.

All plugin type definitions and simple result/context classes are centralized
here to avoid duplication. Prefer importing from this module.
"""
from __future__ import annotations

from enum import Enum
from typing import cast

from flext_core import FlextProcessingError, FlextResult


class PluginStatus(Enum):
    UNKNOWN = "unknown"
    DISCOVERED = "discovered"
    LOADED = "loaded"
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOADING = "loading"
    ERROR = "error"
    DISABLED = "disabled"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class PluginType(Enum):
    TAP = "tap"
    TARGET = "target"
    TRANSFORM = "transform"
    EXTENSION = "extension"
    SERVICE = "service"
    MIDDLEWARE = "middleware"
    TRANSFORMER = "transformer"
    API = "api"
    DATABASE = "database"
    NOTIFICATION = "notification"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    UTILITY = "utility"
    TOOL = "tool"
    HANDLER = "handler"
    PROCESSOR = "processor"
    CORE = "core"
    ADDON = "addon"
    THEME = "theme"
    LANGUAGE = "language"


class PluginError(FlextProcessingError):
    def __init__(self, message: str, plugin_name: str = "", plugin_id: str = "", **kwargs: object) -> None:
        super().__init__(message)
        self.plugin_name = plugin_id or plugin_name
        self.plugin_id = plugin_id or plugin_name


class PluginExecutionResult:
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
        return self._success

    def is_failure(self) -> bool:
        return not self._success


class PluginExecutionContext:
    def __init__(
        self,
        plugin_id: str,
        execution_id: str,
        *,
        input_data: dict[str, object] | None = None,
        context: dict[str, object] | None = None,
        timeout_seconds: int | None = None,
    ) -> None:
        self.plugin_id = plugin_id
        self.execution_id = execution_id
        self.input_data = input_data or {}
        self.context = context or {}
        self.timeout_seconds = timeout_seconds


class PluginManagerResult:
    def __init__(self, operation: str, *, success: bool = False) -> None:
        self.operation = operation
        self._success = success
        self.plugins_affected: list[str] = []
        self.execution_time_ms: float = 0.0
        self.details: dict[str, object] = {}
        self.errors: list[str] = []

    @property
    def success(self) -> bool:
        return self._success

    @classmethod
    def create_detailed(cls, operation: str, config: dict[str, object]) -> PluginManagerResult:
        result = cls(operation, success=bool(config.get("success")))
        result.plugins_affected = cast("list[str]", config.get("plugins_affected", []))
        execution_time = cast("float", config.get("execution_time_ms", 0.0))
        result.execution_time_ms = float(execution_time) if execution_time is not None else 0.0
        result.details = cast("dict[str, object]", config.get("details", {}))
        result.errors = cast("list[str]", config.get("errors", []))
        return result


class SimplePluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, object] = {}

    async def register_plugin(self, plugin: object) -> FlextResult[object]:
        try:
            if not hasattr(plugin, "metadata") or plugin.metadata is None:
                return FlextResult.fail("Plugin registration failed: missing metadata")
            if not hasattr(plugin.metadata, "name"):
                return FlextResult.fail("Plugin registration failed: missing name")
            self._plugins[plugin.metadata.name] = plugin
            return FlextResult.ok(plugin)
        except Exception as e:
            return FlextResult.fail(f"Plugin registration failed: {e}")

    async def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        if plugin_name in self._plugins:
            del self._plugins[plugin_name]
        return FlextResult.ok(True)

    def get_plugin(self, plugin_name: str) -> object | None:
        return self._plugins.get(plugin_name)

    def get_plugin_count(self) -> int:
        return len(self._plugins)

    def list_plugins(self, plugin_type: PluginType | None = None) -> list[object]:
        if plugin_type is None:
            return [p.metadata for p in self._plugins.values() if hasattr(p, "metadata")]
        return [
            p.metadata
            for p in self._plugins.values()
            if hasattr(p, "metadata") and hasattr(p.metadata, "plugin_type") and p.metadata.plugin_type == plugin_type
        ]

    async def cleanup_all(self) -> None:
        self._plugins.clear()


def create_plugin_manager(_container: object | None = None, *, _auto_discover: bool = True, _security_enabled: bool = True) -> object:
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
