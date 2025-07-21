"""Domain entities for FLEXT-PLUGIN.

REFACTORED:
    Uses flext-core mixins, types, StrEnum, and constants - NO duplication.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from flext_core.domain.constants import ConfigDefaults, FlextFramework
from flext_core.domain.pydantic_base import DomainEntity, DomainValueObject, Field
from pydantic import computed_field

from flext_plugin.core.types import (
    PluginCapability,
    PluginLifecycle,
    PluginStatus,
    PluginType,
)

__all__ = [
    "PluginConfiguration",
    "PluginExecution",
    "PluginInstance",
    "PluginLifecycle",
    "PluginMetadata",
    "PluginRegistry",
    "PluginSecurityLevel",
    "PluginStatus",
]


class PluginSecurityLevel(StrEnum):
    """Plugin security level enumeration using StrEnum for type safety."""

    LOW = "low"
    STANDARD = "standard"
    HIGH = "high"
    CRITICAL = "critical"


class PluginConfiguration(DomainValueObject):
    """Plugin configuration value object."""

    enabled: bool = Field(default=True, description="Whether plugin is enabled")
    priority: int = Field(
        default=100,
        description="Plugin execution priority",
        ge=0,
        le=1000,
    )
    settings: dict[str, Any] = Field(
        default_factory=dict,
        description="Plugin-specific settings",
    )
    dependencies: list[str] = Field(
        default_factory=list,
        description="Required dependencies",
    )
    security_level: PluginSecurityLevel = Field(default=PluginSecurityLevel.STANDARD)

    # Resource limits
    max_memory_mb: int = Field(
        default=512,
        description="Maximum memory usage in MB",
        ge=1,
        le=ConfigDefaults.MAX_PAGE_SIZE * 10,
    )
    max_cpu_percent: int = Field(
        default=50,
        description="Maximum CPU usage percentage",
        ge=1,
        le=100,
    )
    timeout_seconds: int = Field(
        default=ConfigDefaults.DEFAULT_TIMEOUT,
        description="Plugin execution timeout",
        ge=1,
        le=3600,
    )


class PluginMetadata(DomainValueObject):
    """Plugin metadata value object."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
        description="Human-readable plugin name",
    )
    version: str = Field(
        default=FlextFramework.VERSION,
        description="Semantic version string",
    )
    description: str = Field(
        default="",
        max_length=ConfigDefaults.MAX_ERROR_MESSAGE_LENGTH,
        description="Plugin description",
    )
    author: str = Field(
        default=FlextFramework.AUTHOR,
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
        description="Plugin author",
    )
    license: str = Field(
        default=FlextFramework.LICENSE,
        max_length=100,
        description="Plugin license",
    )

    # Technical specifications
    entry_point: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Python entry point",
    )
    python_version: str = Field(
        default=f">={FlextFramework.PYTHON_VERSION}",
        description="Required Python version",
    )
    dependencies: list[str] = Field(
        default_factory=list,
        description="Required Python packages",
    )

    # Plugin classification
    plugin_type: PluginType = Field(description="Plugin type")
    capabilities: list[PluginCapability] = Field(
        default_factory=list,
        description="Plugin capabilities",
    )

    # Configuration schema (renamed to avoid Pydantic.schema conflict)
    config_schema: dict[str, Any] = Field(
        default_factory=dict,
        description="JSON schema for configuration",
    )
    default_configuration: dict[str, Any] = Field(
        default_factory=dict,
        description="Default configuration values",
    )

    # Security and permissions
    required_permissions: list[str] = Field(
        default_factory=list,
        description="Required system permissions",
    )
    trusted: bool = Field(
        default=False,
        description="Whether plugin is trusted",
    )

    # URLs
    homepage: str | None = Field(None, description="Plugin homepage URL")
    repository: str | None = Field(None, description="Source repository URL")


class PluginInstance(DomainEntity):
    """Plugin instance domain entity using enhanced mixins for code reduction."""

    plugin_id: str = Field(..., description="Plugin identifier")
    metadata: PluginMetadata = Field(..., description="Plugin metadata")
    configuration: PluginConfiguration = Field(
        default_factory=PluginConfiguration,
        description="Plugin configuration",
    )

    # Plugin state - renamed to avoid conflict with StatusMixin
    lifecycle_state: PluginLifecycle = Field(
        default=PluginLifecycle.UNREGISTERED,
        description="Current lifecycle state",
    )
    plugin_status: PluginStatus = Field(
        default=PluginStatus.UNKNOWN,
        description="Current operational status",
    )

    # Runtime information
    is_initialized: bool = Field(
        default=False,
        description="Whether plugin is initialized",
    )
    last_health_check: datetime | None = Field(
        None,
        description="Last health check time",
    )
    health_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Latest health check data",
    )

    # Execution statistics
    execution_count: int = Field(default=0, description="Number of executions", ge=0)
    last_execution: datetime | None = Field(None, description="Last execution time")
    average_execution_time_ms: float = Field(
        default=0.0,
        description="Average execution time in milliseconds",
        ge=0.0,
    )

    # Resource usage
    current_memory_mb: float = Field(
        default=0.0,
        description="Current memory usage in MB",
        ge=0.0,
    )
    peak_memory_mb: float = Field(
        default=0.0,
        description="Peak memory usage in MB",
        ge=0.0,
    )

    # Error tracking
    error_count: int = Field(default=0, description="Number of errors", ge=0)
    last_error: str | None = Field(None, description="Last error message")
    last_error_time: datetime | None = Field(None, description="Last error time")

    @property
    def is_healthy(self) -> bool:
        """Check if the plugin is in a healthy status.

        Returns:
            True if plugin status is HEALTHY, False otherwise.

        """
        return self.plugin_status == PluginStatus.HEALTHY

    @computed_field
    def is_active(self) -> bool:
        """Check if the plugin is in an active lifecycle state.

        Returns:
            True if plugin lifecycle state is ACTIVE, False otherwise.

        """
        return self.lifecycle_state == PluginLifecycle.ACTIVE

    @property
    def can_execute(self) -> bool:
        """Check if the plugin can currently execute.

        Returns:
            True if plugin is active, initialized, enabled, and healthy/degraded.

        """
        return (
            self.is_active()
            and self.is_initialized
            and self.configuration.enabled
            and self.plugin_status in {PluginStatus.HEALTHY, PluginStatus.DEGRADED}
        )

    def record_execution(self, execution_time_ms: float, success: bool = True) -> None:
        """Record a plugin execution and update performance metrics.

        Args:
            execution_time_ms: Execution time in milliseconds.
            success: Whether the execution was successful.

        """
        self.execution_count += 1
        self.last_execution = datetime.now(UTC)

        if success:
            # Update average execution time
            if self.execution_count == 1:
                self.average_execution_time_ms = execution_time_ms
            else:
                # Running average
                self.average_execution_time_ms = (
                    self.average_execution_time_ms * (self.execution_count - 1)
                    + execution_time_ms
                ) / self.execution_count

    def record_error(self, error_message: str) -> None:
        """Record a plugin error and update error tracking.

        Args:
            error_message: Description of the error that occurred.

        """
        self.error_count += 1
        self.last_error = error_message
        self.last_error_time = datetime.now(UTC)
        self.plugin_status = PluginStatus.UNHEALTHY

    def update_health(self, health_data: dict[str, Any]) -> None:
        """Update plugin health status based on health check data.

        Args:
            health_data: Dictionary containing health check results and status.

        """
        self.health_data = health_data
        self.last_health_check = datetime.now(UTC)

        # Update status based on health data
        if health_data.get("status") == "healthy":
            self.plugin_status = PluginStatus.HEALTHY
        elif health_data.get("status") == "degraded":
            self.plugin_status = PluginStatus.DEGRADED
        elif health_data.get("status") == "unhealthy":
            self.plugin_status = PluginStatus.UNHEALTHY
        else:
            self.plugin_status = PluginStatus.UNKNOWN

    def update_resource_usage(self, memory_mb: float) -> None:
        """Update plugin resource usage metrics.

        Args:
            memory_mb: Current memory usage in megabytes.

        """
        self.current_memory_mb = memory_mb
        self.peak_memory_mb = max(self.peak_memory_mb, memory_mb)

    def transition_to(self, new_state: PluginLifecycle) -> None:
        """Transition the plugin to a new lifecycle state.

        Args:
            new_state: The new lifecycle state to transition to.

        """
        self.lifecycle_state = new_state

        # Update status based on lifecycle state
        if new_state == PluginLifecycle.ACTIVE:
            if self.plugin_status == PluginStatus.UNKNOWN:
                self.plugin_status = PluginStatus.HEALTHY
        elif new_state == PluginLifecycle.ERROR:
            self.plugin_status = PluginStatus.UNHEALTHY
        elif new_state in {PluginLifecycle.STOPPED, PluginLifecycle.UNREGISTERED}:
            self.plugin_status = PluginStatus.UNKNOWN


class PluginRegistry(DomainEntity):
    """Plugin registry domain entity using enhanced mixins for code reduction."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
        description="Registry name",
    )
    registry_url: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Registry URL",
    )

    # Registry configuration
    is_enabled: bool = Field(default=True, description="Whether registry is enabled")
    requires_authentication: bool = Field(
        default=False,
        description="Whether registry requires authentication",
    )
    api_key: str | None = Field(None, description="API key for authentication")

    # Security settings
    verify_signatures: bool = Field(
        default=True,
        description="Whether to verify plugin signatures",
    )
    trusted_publishers: list[str] = Field(
        default_factory=list,
        description="List of trusted publishers",
    )

    # Cache settings
    cache_duration_hours: int = Field(
        default=24,
        description="Plugin metadata cache duration",
        ge=1,
        le=168,  # Max 7 days
    )

    # Statistics
    plugin_count: int = Field(default=0, description="Number of plugins", ge=0)
    last_sync: datetime | None = Field(None, description="Last synchronization time")
    sync_error_count: int = Field(default=0, description="Sync error count", ge=0)

    @property
    def is_available(self) -> bool:
        """Check if the plugin registry is available for use.

        Returns:
            True if registry is enabled and has a valid URL, False otherwise.

        """
        return self.is_enabled and self.registry_url is not None

    def record_sync(self, success: bool = True, plugin_count: int = 0) -> None:
        """Record a registry synchronization attempt.

        Args:
            success: Whether the synchronization was successful.
            plugin_count: Number of plugins found during sync.

        """
        self.last_sync = datetime.now(UTC)
        if success:
            self.plugin_count = plugin_count
            self.sync_error_count = 0
        else:
            self.sync_error_count += 1


class PluginExecution(DomainEntity):
    """Plugin execution domain entity using enhanced mixins for code reduction."""

    plugin_id: str = Field(..., description="Plugin identifier")
    execution_id: str = Field(..., description="Unique execution identifier")

    # Execution context
    user_id: str | None = Field(None, description="User who triggered execution")
    trace_id: str | None = Field(None, description="Distributed tracing ID")
    span_id: str | None = Field(None, description="Distributed tracing span ID")

    # Input and output
    input_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Execution input data",
    )
    output_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Execution output data",
    )

    # Execution state
    execution_status: str = Field(
        default="pending",
        description="Execution status",
    )
    success: bool = Field(default=False, description="Whether execution succeeded")
    error_message: str | None = Field(None, description="Error message if failed")

    # Timing information
    start_time: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Execution start time",
    )
    end_time: datetime | None = Field(None, description="Execution end time")
    duration_ms: int | None = Field(
        None,
        description="Execution duration in milliseconds",
    )

    # Resource usage
    memory_usage_mb: float | None = Field(None, description="Peak memory usage")
    cpu_time_ms: float | None = Field(None, description="CPU time consumed")

    # Context metadata
    execution_context: dict[str, Any] = Field(
        default_factory=dict,
        description="Execution context metadata",
    )

    @property
    def is_completed(self) -> bool:
        """Check if the plugin execution has completed.

        Returns:
            True if execution has an end time, False otherwise.

        """
        return self.end_time is not None

    @property
    def is_running(self) -> bool:
        """Check if the plugin execution is currently running.

        Returns:
            True if execution has no end time and status is running.

        """
        return self.end_time is None and self.execution_status == "running"

    def mark_started(self) -> None:
        """Mark the plugin execution as started.

        Sets start time to current UTC time and status to running.
        """
        self.start_time = datetime.now(UTC)
        self.execution_status = "running"

    def mark_completed(
        self,
        success: bool = True,
        error_message: str | None = None,
    ) -> None:
        """Mark the plugin execution as completed.

        Args:
            success: Whether the execution was successful.
            error_message: Error message if execution failed.

        """
        self.end_time = datetime.now(UTC)
        self.success = success
        self.error_message = error_message
        self.execution_status = "completed" if success else "failed"

        if self.start_time:
            duration = (self.end_time - self.start_time).total_seconds() * 1000
            self.duration_ms = int(duration)

    def update_resource_usage(self, memory_mb: float, cpu_time_ms: float) -> None:
        """Update resource usage metrics for the execution.

        Args:
            memory_mb: Peak memory usage in megabytes.
            cpu_time_ms: CPU time consumed in milliseconds.

        """
        self.memory_usage_mb = memory_mb
        self.cpu_time_ms = cpu_time_ms
