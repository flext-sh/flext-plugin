"""FLEXT Plugin core types - Unified typing system using flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

This module imports from the unified typing system in flext-core and defines
plugin-specific types using modern Python 3.13 patterns, StrEnum, and Pydantic v2.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

# Import from unified core typing system - eliminate duplication
from flext_core.domain.shared_types import (
    PluginType as CorePluginType,
    ServiceResult,
)

# ==============================================================================
# PLUGIN-SPECIFIC ENUMS USING STRENUM
# ==============================================================================

# Re-export core PluginType for compatibility
PluginType = CorePluginType


class PluginStatus(StrEnum):
    """Plugin status states using modern StrEnum."""

    UNKNOWN = "unknown"
    DISCOVERED = "discovered"
    LOADING = "loading"
    LOADED = "loaded"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    UNLOADING = "unloading"
    UNLOADED = "unloaded"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class PluginLifecycle(StrEnum):
    """Plugin lifecycle state enumeration using StrEnum."""

    CREATED = "created"
    VALIDATED = "validated"
    REGISTERED = "registered"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    ACTIVATED = "activated"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"
    UNLOADING = "unloading"
    UNLOADED = "unloaded"
    DESTROYED = "destroyed"
    UNREGISTERED = "unregistered"
    ACTIVE = "active"
    STOPPED = "stopped"
    ERROR = "error"
    FAILED = "failed"
    TERMINATED = "terminated"


class PluginCapability(StrEnum):
    """Plugin capability enumeration using StrEnum."""

    ASYNC_EXECUTION = "async_execution"
    SYNC_EXECUTION = "sync_execution"
    HOT_RELOAD = "hot_reload"
    CONFIG_VALIDATION = "config_validation"
    HEALTH_CHECK = "health_check"
    METRICS_COLLECTION = "metrics_collection"
    LOGGING = "logging"
    CACHING = "caching"
    SECURITY = "security"
    RATE_LIMITING = "rate_limiting"
    STREAMING = "streaming"
    BATCH_PROCESSING = "batch_processing"
    TRANSACTION_SUPPORT = "transaction_support"
    STATE_MANAGEMENT = "state_management"


# ==============================================================================
# PLUGIN EXCEPTIONS USING PROFESSIONAL ERROR HANDLING
# ==============================================================================


class PluginError(Exception):
    """Base exception for plugin-related errors with comprehensive context."""

    def __init__(
        self,
        message: str,
        plugin_name: str | None = None,
        plugin_id: str | None = None,
        error_code: str | None = None,
        cause: Exception | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize plugin error with comprehensive error context.

        Args:
            message: Error message
            plugin_name: Name of the plugin that caused the error
            plugin_id: ID of the plugin that caused the error
            error_code: Error code for categorization
            cause: Original exception that caused this error
            **kwargs: Additional error context

        """
        super().__init__(message)
        self.message = message
        self.plugin_name = plugin_name
        self.plugin_id = plugin_id
        self.error_code = error_code
        self.cause = cause
        self.context = kwargs
        self.timestamp = datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary for structured logging."""
        return {
            "message": self.message,
            "plugin_name": self.plugin_name,
            "plugin_id": self.plugin_id,
            "error_code": self.error_code,
            "timestamp": self.timestamp.isoformat(),
            "cause": str(self.cause) if self.cause else None,
            "context": self.context,
        }


class PluginLoadError(PluginError):
    """Exception raised when plugin loading fails."""


class PluginValidationError(PluginError):
    """Exception raised when plugin validation fails."""


class PluginExecutionError(PluginError):
    """Exception raised when plugin execution fails."""


class PluginConfigurationError(PluginError):
    """Exception raised when plugin configuration is invalid."""


class PluginDependencyError(PluginError):
    """Exception raised when plugin dependency resolution fails."""


class PluginSecurityError(PluginError):
    """Exception raised when plugin security validation fails."""


# ==============================================================================
# PLUGIN EXECUTION RESULT USING MODERN PATTERNS
# ==============================================================================


class PluginExecutionResult:
    """Result of plugin execution with comprehensive metrics and context."""

    def __init__(
        self,
        execution_id: str,
        success: bool,
        duration_ms: int,
        output_data: dict[str, Any] | None = None,
        error_message: str | None = None,
        plugin_name: str | None = None,
        plugin_id: str | None = None,
        memory_usage_mb: float | None = None,
        cpu_time_ms: float | None = None,
    ) -> None:
        """Initialize execution result with comprehensive metrics.

        Args:
            execution_id: Unique identifier for this execution
            success: Whether the execution was successful
            duration_ms: Execution duration in milliseconds
            output_data: Output data from the execution
            error_message: Error message if execution failed
            plugin_name: Name of the executed plugin
            plugin_id: ID of the executed plugin
            memory_usage_mb: Memory usage in megabytes
            cpu_time_ms: CPU time consumed in milliseconds

        """
        self.execution_id = execution_id
        self.success = success
        self.duration_ms = duration_ms
        self.output_data = output_data or {}
        self.error_message = error_message
        self.plugin_name = plugin_name
        self.plugin_id = plugin_id
        self.memory_usage_mb = memory_usage_mb
        self.cpu_time_ms = cpu_time_ms
        self.timestamp = datetime.now(UTC)

    def to_service_result(self) -> ServiceResult[dict[str, Any]]:
        """Convert to ServiceResult for unified error handling."""
        if self.success:
            return ServiceResult.ok(self.output_data)
        return ServiceResult.fail(self.error_message or "Plugin execution failed")

    def __repr__(self) -> str:
        """String representation of execution result."""
        status = "SUCCESS" if self.success else "FAILED"
        plugin_info = f" plugin={self.plugin_name}" if self.plugin_name else ""
        return (
            f"PluginExecutionResult(id={self.execution_id}, status={status}, "
            f"duration={self.duration_ms}ms{plugin_info})"
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for structured logging and serialization."""
        return {
            "execution_id": self.execution_id,
            "success": self.success,
            "duration_ms": self.duration_ms,
            "output_data": self.output_data,
            "error_message": self.error_message,
            "plugin_name": self.plugin_name,
            "plugin_id": self.plugin_id,
            "memory_usage_mb": self.memory_usage_mb,
            "cpu_time_ms": self.cpu_time_ms,
            "timestamp": self.timestamp.isoformat(),
        }


# ==============================================================================
# EXPORTS - ALL PLUGIN CORE TYPES
# ==============================================================================

__all__ = [
    "PluginCapability",
    "PluginConfigurationError",
    "PluginDependencyError",
    # Exception classes
    "PluginError",
    "PluginExecutionError",
    # Result classes
    "PluginExecutionResult",
    "PluginLifecycle",
    "PluginLoadError",
    "PluginSecurityError",
    # Plugin-specific enums
    "PluginStatus",
    # Core types from unified system
    "PluginType",
    "PluginValidationError",
]
