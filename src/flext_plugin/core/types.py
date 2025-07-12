"""Type definitions and enums for the enterprise plugin system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import traceback
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from flext_core.domain.pydantic_base import DomainBaseModel, Field


class PluginType(str, Enum):
    """Plugin type enumeration."""

    EXTRACTOR = "extractor"
    TRANSFORMER = "transformer"
    LOADER = "loader"
    UTILITY = "utility"
    ORCHESTRATOR = "orchestrator"


class PluginStatus(str, Enum):
    """Plugin lifecycle status enumeration."""

    INACTIVE = "inactive"
    LOADING = "loading"
    ACTIVE = "active"
    FAILED = "failed"
    RELOADING = "reloading"
    STOPPING = "stopping"


class ExecutionStatus(str, Enum):
    """Plugin execution status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PluginConfig(DomainBaseModel):
    """Plugin configuration model."""

    # Basic plugin information
    name: str = Field(description="Plugin name")
    version: str = Field(description="Plugin version")
    description: str = Field(description="Plugin description")
    plugin_type: PluginType = Field(description="Type of plugin")

    # Entry point and dependencies
    entry_point: str = Field(description="Main entry point module path")
    dependencies: list[str] = Field(
        default_factory=list,
        description="List of required dependencies",
    )
    python_requires: str = Field(
        default=">=3.11",
        description="Required Python version",
    )

    # Runtime configuration
    timeout_seconds: int = Field(
        default=300,
        description="Plugin execution timeout",
    )
    max_memory_mb: int = Field(
        default=512,
        description="Maximum memory usage in MB",
    )
    enable_hot_reload: bool = Field(
        default=True,
        description="Whether hot reload is enabled",
    )

    # Custom configuration
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Plugin-specific configuration",
    )


class PluginMetadata(DomainBaseModel):
    """Plugin metadata and runtime information."""

    # Core identification
    plugin_id: str = Field(description="Unique plugin identifier")
    config: PluginConfig = Field(description="Plugin configuration")

    # Runtime state
    status: PluginStatus = Field(
        default=PluginStatus.INACTIVE,
        description="Current plugin status",
    )

    # Lifecycle timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Plugin creation time",
    )
    last_loaded_at: datetime | None = Field(
        default=None,
        description="Last successful load time",
    )
    last_executed_at: datetime | None = Field(
        default=None,
        description="Last execution time",
    )

    # File system tracking
    plugin_path: str = Field(description="Path to plugin files")
    file_hash: str = Field(description="Hash of plugin files for change detection")

    # Error tracking
    last_error: str | None = Field(
        default=None,
        description="Last error message",
    )
    error_count: int = Field(
        default=0,
        description="Total error count",
    )


class ExecutionResult(DomainBaseModel):
    """Plugin execution result."""

    # Execution outcome
    success: bool = Field(description="Whether the plugin execution succeeded")
    result: Any = Field(default=None, description="The plugin execution result data")
    error: str | None = Field(
        default=None,
        description="Error message if execution failed",
    )

    # Execution metadata
    plugin_id: str = Field(description="Unique identifier of the executed plugin")
    execution_id: str = Field(description="Unique identifier for this execution")
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
        description="Execution context data",
    )
    traceback_info: str | None = Field(
        default=None,
        description="Traceback information for failed executions",
    )

    def set_error(self, error: Exception) -> None:
        """Set error information from an exception."""
        self.success = False
        self.error = str(error)
        self.traceback_info = traceback.format_exc()

    def set_completed(self, result: Any = None) -> None:
        """Mark execution as completed successfully."""
        self.success = True
        self.result = result
        self.end_time = datetime.now(UTC)
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            self.duration_ms = int(duration.total_seconds() * 1000)


class PluginEvent(DomainBaseModel):
    """Plugin lifecycle event."""

    event_id: str = Field(description="Unique event identifier")
    plugin_id: str = Field(description="Plugin identifier")
    event_type: str = Field(description="Type of event")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Event timestamp",
    )
    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Event-specific data",
    )
    source: str = Field(description="Event source component")


class HotReloadEvent(DomainBaseModel):
    """Hot reload event information."""

    plugin_id: str = Field(description="Plugin being reloaded")
    event_type: str = Field(description="Type of reload event")
    file_path: str = Field(description="Path of changed file")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Event timestamp",
    )
    success: bool = Field(description="Whether reload was successful")
    error_message: str | None = Field(
        default=None,
        description="Error message if reload failed",
    )


class PluginError(Exception):
    """Base exception for plugin system errors."""

    def __init__(self, message: str, plugin_id: str | None = None, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.plugin_id = plugin_id
        self.cause = cause


class PluginDiscoveryError(PluginError):
    """Error during plugin discovery."""



class PluginLoadError(PluginError):
    """Error during plugin loading."""



class PluginExecutionError(PluginError):
    """Error during plugin execution."""



class PluginValidationError(PluginError):
    """Error during plugin validation."""



class PluginDependencyError(PluginError):
    """Error during plugin dependency resolution."""



class PluginLifecycleError(PluginError):
    """Error during plugin lifecycle operations."""



class PluginSecurityError(PluginError):
    """Error related to plugin security validation."""



class PluginCapability(str, Enum):
    """Plugin capability enumeration."""

    HOT_RELOAD = "hot_reload"
    ASYNC_EXECUTION = "async_execution"
    STATE_PERSISTENCE = "state_persistence"
    HEALTH_CHECK = "health_check"
    METRICS_EXPORT = "metrics_export"


class PluginExecutionResult(DomainBaseModel):
    """Result of plugin execution with comprehensive metadata."""

    success: bool = Field(description="Whether execution succeeded")
    result: Any = Field(default=None, description="Execution result data")
    error_message: str | None = Field(default=None, description="Error message if failed")
    execution_time_ms: int = Field(description="Execution time in milliseconds")
    memory_used_mb: float = Field(description="Memory used during execution")
    plugin_id: str = Field(description="ID of executed plugin")


class PluginLifecycle(str, Enum):
    """Plugin lifecycle state enumeration."""

    DISCOVERED = "discovered"
    VALIDATED = "validated"
    LOADED = "loaded"
    ACTIVATED = "activated"
    DEACTIVATED = "deactivated"
    UNLOADED = "unloaded"
    FAILED = "failed"


# Type aliases for clean interfaces
PluginRegistry = dict[str, PluginMetadata]
ExecutionHistory = list[ExecutionResult]
EventLog = list[PluginEvent]
