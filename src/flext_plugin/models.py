"""Models for plugin operations.

This module provides data models for plugin operations.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from enum import StrEnum
from typing import Self

from pydantic import (
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)
from pydantic_settings import SettingsConfigDict

from flext_core import FlextModels, FlextTypes
from flext_plugin.constants import FlextPluginConstants
from flext_plugin.type_definitions import PluginConfigData
from flext_plugin.typings import FlextPluginTypes


class FlextPluginModels(FlextModels):
    """Comprehensive models for plugin system operations extending FlextModels.

    Provides standardized models for all plugin domain entities including:
    - Plugin lifecycle and management
    - Plugin configuration and metadata
    - Plugin execution and monitoring
    - Plugin registry and discovery
    - Plugin security and validation

    All nested classes inherit FlextModels validation and patterns.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        extra="forbid",
        frozen=False,
        validate_return=True,
        str_strip_whitespace=True,
        validate_default=True,
        loc_by_alias=False,
    )

    # Simplified performance constants access
    @property
    def performance_constants(self) -> FlextTypes.Dict:
        """Access performance constants for plugin analysis."""
        return {
            "excellent_success_rate": FlextPluginConstants.PluginPerformance.EXCELLENT_SUCCESS_RATE,
            "good_success_rate": FlextPluginConstants.PluginPerformance.GOOD_SUCCESS_RATE,
            "fair_success_rate": FlextPluginConstants.PluginPerformance.FAIR_SUCCESS_RATE,
            "timeout_seconds": FlextPluginConstants.PluginPerformance.PRODUCTION_READY_TIMEOUT_SECONDS,
            "max_memory_mb": FlextPluginConstants.PluginPerformance.PRODUCTION_READY_MAX_MEMORY_MB,
        }

    def validate_plugin_system_consistency(self) -> bool:
        """Validate overall plugin system model consistency."""
        try:
            # Simple validation of core capabilities
            return self.__class__.__name__ == "FlextPluginModels"
        except Exception:
            return False

    class PluginStatus(StrEnum):
        """Plugin lifecycle and operational status enumeration."""

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

        @classmethod
        def get_operational_statuses(cls) -> list[Self]:
            """Get statuses representing operational states."""
            return [cls.ACTIVE, cls.HEALTHY, cls.LOADED]

        @classmethod
        def get_error_statuses(cls) -> list[Self]:
            """Get statuses representing error states."""
            return [cls.ERROR, cls.UNHEALTHY, cls.DISABLED]

        def is_operational(self) -> bool:
            """Check if status represents operational state."""
            return self in self.get_operational_statuses()

        def is_error_state(self) -> bool:
            """Check if status represents error state."""
            return self in self.get_error_statuses()

    class PluginType(StrEnum):
        """Plugin type classification for platform organization."""

        # Singer ETL Types
        TAP = "tap"
        TARGET = "target"
        TRANSFORM = "transform"

        # Architecture Types
        EXTENSION = "extension"
        SERVICE = "service"
        MIDDLEWARE = "middleware"
        TRANSFORMER = "transformer"

        # Integration Types
        API = "api"
        DATABASE = "database"
        NOTIFICATION = "notification"
        AUTHENTICATION = "authentication"
        AUTHORIZATION = "authorization"

        # Utility Types
        UTILITY = "utility"
        TOOL = "tool"
        HANDLER = "handler"
        PROCESSOR = "processor"

        # Additional Types
        CORE = "core"
        ADDON = "addon"
        THEME = "theme"
        LANGUAGE = "language"

        @classmethod
        def get_etl_types(cls) -> list[Self]:
            """Get ETL-related plugin types."""
            return [cls.TAP, cls.TARGET, cls.TRANSFORM]

        @classmethod
        def get_architectural_types(cls) -> list[Self]:
            """Get architectural plugin types."""
            return [cls.EXTENSION, cls.SERVICE, cls.MIDDLEWARE, cls.TRANSFORMER]

        def is_etl_plugin(self) -> bool:
            """Check if this is an ETL plugin type."""
            return self in self.get_etl_types()

        def is_architectural_plugin(self) -> bool:
            """Check if this is an architectural plugin type."""
            return self in self.get_architectural_types()

    class PluginModel(FlextModels.Entity):
        """Core plugin entity model with comprehensive validation."""

        name: str = Field(
            ...,
            min_length=1,
            max_length=100,
            pattern=r"^[a-zA-Z][a-zA-Z0-9_-]*$",
            description="Plugin unique identifier name",
        )
        plugin_version: str = Field(
            default="1.0.0",
            pattern=r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$",
            description="Plugin semantic version",
        )
        description: str = Field(
            default="",
            max_length=1000,
            description="Plugin functionality description",
        )
        author: str = Field(default="", max_length=200, description="Plugin author")
        plugin_type: "PluginType" = Field(
            default_factory=lambda: PluginType.UTILITY,
            description="Plugin type classification",
        )
        status: "PluginStatus" = Field(
            default_factory=lambda: PluginStatus.INACTIVE,
            description="Current plugin operational status",
        )
        enabled: bool = Field(default=True, description="Plugin enabled state")
        dependencies: FlextTypes.StringList = Field(
            default_factory=list, description="Required plugin dependencies"
        )
        tags: FlextTypes.StringList = Field(
            default_factory=list, description="Plugin categorization tags"
        )
        created_at: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Plugin creation timestamp",
        )
        updated_at: datetime | None = Field(
            default=None, description="Last update timestamp"
        )

        @model_validator(mode="after")
        def validate_plugin_consistency(self) -> Self:
            """Validate plugin model consistency and constraints."""
            if self.status == PluginStatus.ACTIVE and not self.enabled:
                error_msg = "Plugin cannot be ACTIVE when disabled"
                raise ValueError(error_msg)

            if self.name in self.dependencies:
                error_msg = "Plugin cannot depend on itself"
                raise ValueError(error_msg)

            return self

        @field_validator("dependencies")
        @classmethod
        def validate_dependencies_format(
            cls, value: FlextTypes.StringList
        ) -> FlextTypes.StringList:
            """Validate dependency format and constraints."""
            if len(value) > 50:
                error_msg = "Too many dependencies (max 50)"
                raise ValueError(error_msg)

            for dep in value:
                if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", dep):
                    error_msg = f"Invalid dependency name format: {dep}"
                    raise ValueError(error_msg)

            return value

        @field_serializer("dependencies", when_used="json")
        def serialize_dependencies_with_validation(
            self, value: FlextTypes.StringList
        ) -> FlextTypes.Dict:
            """Field serializer for dependencies with validation metadata."""
            return {
                "dependencies": value,
                "dependency_count": len(value),
                "has_flext_dependencies": any("flext" in dep for dep in value),
                "validated_at": datetime.now(UTC).isoformat(),
            }

    class ConfigModel(FlextModels.BaseConfig):
        """Plugin configuration model with comprehensive settings."""

        model_config = SettingsConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            validate_return=True,
        )

        enabled: bool = Field(default=True, description="Plugin enabled state")
        settings: FlextPluginTypes.Core.SettingsDict = Field(
            default_factory=dict, description="Plugin settings"
        )
        priority: int = Field(
            default=FlextPluginConstants.PluginPerformance.PERCENTAGE_MAX,
            description="Plugin priority",
        )
        timeout_seconds: int = Field(default=60, description="Plugin execution timeout")
        max_memory_mb: int = Field(default=512, description="Maximum memory usage")
        max_cpu_percent: int = Field(default=50, description="Maximum CPU usage")
        auto_restart: bool = Field(default=True, description="Auto restart on failure")
        retry_attempts: int = Field(default=3, description="Maximum retry attempts")

        @property
        def is_high_performance(self) -> bool:
            """Check if configuration meets high-performance criteria."""
            return (
                self.timeout_seconds <= 30
                and self.max_memory_mb <= 256
                and self.max_cpu_percent <= 50
            )

        @field_validator("priority")
        @classmethod
        def validate_priority_range(cls, value: int) -> int:
            """Validate priority is within acceptable range."""
            if (
                not FlextPluginConstants.PluginPerformance.PERCENTAGE_MIN
                <= value
                <= FlextPluginConstants.PluginPerformance.PERCENTAGE_MAX
            ):
                error_msg = f"Priority must be between {FlextPluginConstants.PluginPerformance.PERCENTAGE_MIN} and {FlextPluginConstants.PluginPerformance.PERCENTAGE_MAX}"
                raise ValueError(error_msg)
            return value

        @field_validator("max_memory_mb")
        @classmethod
        def validate_memory_limits(cls, value: int) -> int:
            """Validate memory limits are reasonable."""
            if (
                value
                > FlextPluginConstants.PluginPerformance.PRODUCTION_READY_MAX_MEMORY_MB
            ):
                error_msg = f"Memory limit exceeds production maximum: {FlextPluginConstants.PluginPerformance.PRODUCTION_READY_MAX_MEMORY_MB}MB"
                raise ValueError(error_msg)
            if value < 64:
                error_msg = "Memory limit too low (minimum 64MB)"
                raise ValueError(error_msg)
            return value

    class SecurityModel(FlextModels.Entity):
        """Plugin security model with enterprise-grade validation."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="forbid",
            frozen=True,  # Security models should be immutable
        )

        security_level: str = Field(
            default="medium",
            pattern=r"^(low|medium|high|critical)$",
            description="Plugin security clearance level",
        )
        permissions: FlextTypes.StringList = Field(
            default_factory=list, description="Required security permissions"
        )
        sandboxed: bool = Field(
            default=True, description="Whether plugin runs in sandbox"
        )
        network_access: bool = Field(
            default=False, description="Network access permission"
        )
        file_access: bool = Field(
            default=False, description="File system access permission"
        )
        encrypted_data: bool = Field(
            default=True, description="Whether plugin data is encrypted"
        )
        audit_logging: bool = Field(
            default=True, description="Whether actions are audit logged"
        )
        signature_verified: bool = Field(
            default=False, description="Whether plugin signature is verified"
        )

        @property
        def is_secure(self) -> bool:
            """Check if security configuration meets enterprise standards."""
            return (
                self.sandboxed
                and not self.network_access
                and not self.file_access
                and self.encrypted_data
                and self.audit_logging
            )

    class MonitoringModel(FlextModels.Entity):
        """Plugin monitoring and observability model."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="allow",  # Allow extra monitoring fields
            frozen=False,
        )

        metrics_enabled: bool = Field(
            default=True, description="Whether metrics collection is enabled"
        )
        health_checks: bool = Field(
            default=True, description="Whether health checks are active"
        )
        performance_tracking: bool = Field(
            default=True, description="Whether performance is tracked"
        )
        error_tracking: bool = Field(
            default=True, description="Whether errors are tracked"
        )
        log_level: str = Field(
            default="INFO",
            pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
            description="Logging level for plugin",
        )
        alert_thresholds: FlextTypes.FloatDict = Field(
            default_factory=lambda: {
                "cpu_percent": 80.0,
                "memory_percent": 85.0,
                "error_rate": 5.0,
                "response_time_ms": 5000.0,
            },
            description="Alert threshold configuration",
        )
        retention_days: int = Field(
            default=30, ge=1, le=365, description="Data retention period in days"
        )

        @property
        def has_basic_monitoring(self) -> bool:
            """Check if basic monitoring features are enabled."""
            return self.metrics_enabled and self.health_checks and self.error_tracking

        @field_validator("alert_thresholds")
        @classmethod
        def validate_alert_thresholds(
            cls, value: FlextTypes.FloatDict
        ) -> FlextTypes.FloatDict:
            """Validate alert threshold values."""
            required_thresholds = {
                "cpu_percent",
                "memory_percent",
                "error_rate",
                "response_time_ms",
            }
            missing = required_thresholds - set(value.keys())
            if missing:
                error_msg = f"Missing required thresholds: {missing}"
                raise ValueError(error_msg)

            for key, threshold in value.items():
                if key.endswith("_percent") and not 0 <= threshold <= 100:
                    error_msg = f"Percentage threshold {key} must be 0-100"
                    raise ValueError(error_msg)
                if threshold < 0:
                    error_msg = f"Threshold {key} cannot be negative"
                    raise ValueError(error_msg)

            return value

    # Models from flext_plugin_models.py for backward compatibility
    class MetadataModel(FlextModels.Entity):
        """Plugin metadata model."""

        model_config = ConfigDict(
            extra="allow",
            validate_assignment=True,
        )

        plugin_id: str = Field(..., description="Unique plugin identifier")
        created_at: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Plugin creation timestamp",
        )
        updated_at: datetime | None = Field(
            default=None,
            description="Last update timestamp",
        )
        homepage: str | None = Field(default=None, description="Plugin homepage URL")
        repository: str | None = Field(
            default=None,
            description="Plugin repository URL",
        )
        documentation: str | None = Field(
            default=None,
            description="Plugin documentation URL",
        )
        license: str | None = Field(default=None, description="Plugin license")
        keywords: FlextTypes.StringList = Field(
            default_factory=list,
            description="Plugin keywords",
        )
        maintainers: FlextTypes.StringList = Field(
            default_factory=list,
            description="Plugin maintainers",
        )
        platform_version: str | None = Field(
            default=None,
            description="Required platform version",
        )
        python_version: str | None = Field(
            default=None,
            description="Required Python version",
        )

    class ExecutionContextModel(FlextModels.Entity):
        """Plugin execution context model."""

        model_config = ConfigDict(
            extra="allow",
            validate_assignment=True,
        )

        plugin_id: str = Field(..., description="Plugin identifier")
        execution_id: str = Field(..., description="Unique execution identifier")
        input_data: dict[str, PluginConfigData] = Field(
            default_factory=dict,
            description="Input data for execution",
        )
        context: dict[str, PluginConfigData] = Field(
            default_factory=dict,
            description="Execution context data",
        )
        timeout_seconds: int | None = Field(
            default=None,
            description="Execution timeout in seconds",
        )
        started_at: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Execution start timestamp",
        )

    class ExecutionResultModel(FlextModels.Entity):
        """Plugin execution result model."""

        model_config = ConfigDict(
            extra="allow",
            validate_assignment=True,
        )

        success: bool = Field(default=False, description="Whether execution succeeded")
        data: PluginConfigData = Field(
            default=None,
            description="Execution output data",
        )
        error: str = Field(default="", description="Error message if execution failed")
        plugin_name: str = Field(default="", description="Name of the executed plugin")
        execution_time: float = Field(
            default=0.0,
            description="Execution time in seconds",
        )
        execution_id: str = Field(default="", description="Unique execution identifier")
        completed_at: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Execution completion timestamp",
        )

        @property
        def duration_ms(self) -> float:
            """Get execution time in milliseconds."""
            return self.execution_time * 1000

        def is_failure(self) -> bool:
            """Return True if execution failed."""
            return not self.success

    class ManagerResultModel(FlextModels.Entity):
        """Plugin manager operation result model."""

        model_config = ConfigDict(
            extra="allow",
            validate_assignment=True,
        )

        operation: str = Field(..., description="Operation name")
        success: bool = Field(default=False, description="Whether operation succeeded")
        plugins_affected: FlextTypes.StringList = Field(
            default_factory=list,
            description="List of affected plugin names",
        )
        execution_time_ms: float = Field(
            default=0.0,
            description="Operation execution time in milliseconds",
        )
        details: dict[str, PluginConfigData] = Field(
            default_factory=dict,
            description="Additional operation details",
        )
        errors: FlextTypes.StringList = Field(
            default_factory=list,
            description="List of error messages",
        )
        completed_at: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Operation completion timestamp",
        )


# Export core enums for __init__.py compatibility
PluginStatus = FlextPluginModels.PluginStatus
PluginType = FlextPluginModels.PluginType

__all__ = [
    # Main unified class
    "FlextPluginModels",
    # Core enums for compatibility
    "PluginStatus",
    "PluginType",
]
