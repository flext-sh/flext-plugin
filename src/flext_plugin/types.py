"""Type definitions and enums for the enterprise plugin system.

REFACTORED:
Uses flext-core StrEnum, types, and constants - NO duplication.
"""

from __future__ import annotations

import traceback
from datetime import UTC, datetime
from typing import Any, TypedDict

from flext_core.domain.constants import ConfigDefaults
from flext_core.domain.pydantic_base import DomainBaseModel, Field
from pydantic import ConfigDict

from flext_plugin.core.types import (
    PluginCapability,
    PluginLifecycle,
    PluginStatus,
    PluginType,
)

# Export types for easy access
__all__ = [
    "PluginCapability",
    "PluginContext",
    "PluginData",
    "PluginError",
    "PluginExecutionContext",
    "PluginExecutionResult",
    "PluginLifecycle",
    "PluginResult",
    "PluginStatus",
    "PluginType",
]

# Type aliases for plugin system
PluginData = dict[str, Any] | list[Any] | str | int | float | bool | None
PluginContext = dict[str, Any]
PluginResult = PluginData | dict[str, PluginData]
ConfigurationDict = dict[str, Any]
MetadataDict = dict[str, Any]


class PluginExecutionResult(DomainBaseModel):
    """Result container for plugin execution with comprehensive metadata."""

    model_config = ConfigDict(frozen=False)

    # Execution outcome
    success: bool = Field(description="Whether the plugin execution succeeded")
    result: Any = Field(default=None, description="The plugin execution result data")
    error: str | None = Field(
        default=None,
        description="Error message if execution failed",
    )

    # Execution metadata
    plugin_id: str = Field(
        description="Unique identifier of the executed plugin",
        min_length=1,
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
    )
    execution_id: str = Field(
        description="Unique identifier for this execution",
        min_length=1,
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
    )
    start_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    end_time: datetime | None = Field(
        default=None,
        description="Execution completion time",
    )
    duration_ms: int | None = Field(
        default=None,
        description="Execution duration in milliseconds",
    )

    # Context and tracing
    execution_context: dict[str, Any] = Field(
        default_factory=dict,
        description="Execution context metadata",
    )
    trace_id: str | None = Field(default=None, description="Distributed tracing ID")
    span_id: str | None = Field(default=None, description="Distributed tracing span ID")

    # Resource usage
    memory_usage_mb: float | None = Field(
        default=None,
        description="Peak memory usage in MB",
    )
    cpu_time_ms: float | None = Field(
        default=None,
        description="CPU time consumed in milliseconds",
    )

    def mark_completed(
        self,
        result: PluginResult = None,
        error: str | None = None,
    ) -> None:
        """Mark the plugin execution as completed with result or error.

        Args:
            result: The execution result data if successful.
            error: Error message if execution failed.

        """
        self.end_time = datetime.now(UTC)
        if self.start_time:
            duration = (self.end_time - self.start_time).total_seconds() * 1000
            self.duration_ms = int(duration)

        if error:
            self.success = False
            self.error = error
        else:
            self.success = True
            self.result = result


class PluginError(Exception):
    """Base exception for plugin system errors."""

    def __init__(
        self,
        message: str,
        plugin_id: str | None = None,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
        cause: Exception | None = None,
    ) -> None:
        """Initialize plugin error with message and optional context."""
        super().__init__(message)
        self.message = message
        self.plugin_id = plugin_id
        self.error_code = error_code
        self.details = details or {}
        self.cause = cause
        self.timestamp = datetime.now(UTC)
        self.traceback = traceback.format_exc() if cause else None

    def to_dict(self) -> dict[str, Any]:
        """Convert the plugin error to a dictionary representation.

        Returns:
            Dictionary containing error details including message, plugin_id,
            error_code, details, timestamp, traceback, and cause.

        """
        return {
            "message": self.message,
            "plugin_id": self.plugin_id,
            "error_code": self.error_code,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "traceback": self.traceback,
            "cause": str(self.cause) if self.cause else None,
        }


class PluginValidationError(PluginError):
    """Exception raised when plugin validation fails."""

    def __init__(
        self,
        message: str,
        plugin_id: str,
        validation_failures: list[str],
        **kwargs: dict[str, Any],
    ) -> None:
        """Initialize validation error with specific failure details."""
        super().__init__(message, plugin_id, "VALIDATION_FAILED", kwargs.get("cause"))
        self.validation_failures = validation_failures
        self.details["validation_failures"] = validation_failures


class PluginLoadError(PluginError):
    """Exception raised when plugin loading fails."""

    def __init__(self, message: str, plugin_id: str, **kwargs: dict[str, Any]) -> None:
        """Initialize load error with plugin context."""
        super().__init__(message, plugin_id, "LOAD_FAILED", kwargs.get("cause"))


class PluginExecutionError(PluginError):
    """Exception raised when plugin execution fails."""

    def __init__(
        self,
        message: str,
        plugin_id: str,
        execution_id: str | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        """Initialize execution error with execution context."""
        super().__init__(message, plugin_id, "EXECUTION_FAILED", kwargs.get("cause"))
        self.execution_id = execution_id
        if execution_id:
            self.details["execution_id"] = execution_id


class PluginDependencyError(PluginError):
    """Exception raised when plugin dependency resolution fails."""

    def __init__(
        self,
        message: str,
        plugin_id: str,
        missing_dependencies: list[str],
        **kwargs: dict[str, Any],
    ) -> None:
        """Initialize dependency error with missing dependencies list."""
        super().__init__(message, plugin_id, "DEPENDENCY_FAILED", kwargs.get("cause"))
        self.missing_dependencies = missing_dependencies
        self.details["missing_dependencies"] = missing_dependencies


class PluginSecurityError(PluginError):
    """Exception raised when plugin security validation fails."""

    def __init__(
        self,
        message: str,
        plugin_id: str,
        security_violations: list[str],
        **kwargs: dict[str, Any],
    ) -> None:
        """Initialize security error with violations list."""
        super().__init__(message, plugin_id, "SECURITY_VIOLATION", kwargs.get("cause"))
        self.security_violations = security_violations
        self.details["security_violations"] = security_violations


# Type definitions for plugin configuration
class PluginConfigDict(TypedDict):
    """Plugin configuration dictionary for runtime settings."""

    enabled: bool
    priority: int
    settings: dict[str, Any]
    dependencies: list[str]
    security_level: str
    resource_limits: dict[str, Any]


class PluginMetadataDict(TypedDict):
    """Plugin metadata dictionary for identification and discovery."""

    id: str
    name: str
    version: str
    description: str
    author: str
    license: str
    plugin_type: str
    entry_point: str
    dependencies: list[str]
    capabilities: list[str]
    configuration_schema: dict[str, Any]


class PluginExecutionContext(TypedDict):
    """Plugin execution context dictionary for runtime tracking."""

    execution_id: str
    plugin_id: str
    user_id: str
    session_id: str
    trace_id: str
    environment: str
    request_metadata: dict[str, Any]
    resource_limits: dict[str, Any]
