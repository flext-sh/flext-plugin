"""FLEXT Plugin Models - Plugin system data models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from enum import StrEnum
from typing import Self

from flext_core import FlextConstants, FlextModels
from pydantic import (
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)
from pydantic_settings import SettingsConfigDict

from flext_plugin.constants import FlextPluginConstants
from flext_plugin.types import FlextPluginTypes


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

    class PluginStatus(StrEnum):
        """Plugin lifecycle and operational status enumeration."""

        UNKNOWN = FlextPluginConstants.Lifecycle.STATUS_UNKNOWN
        DISCOVERED = FlextPluginConstants.Lifecycle.STATUS_DISCOVERED
        LOADED = FlextPluginConstants.Lifecycle.STATUS_LOADED
        ACTIVE = FlextPluginConstants.Lifecycle.STATUS_ACTIVE
        INACTIVE = FlextPluginConstants.Lifecycle.STATUS_INACTIVE
        LOADING = FlextPluginConstants.Lifecycle.STATUS_LOADING
        ERROR = FlextPluginConstants.Lifecycle.STATUS_ERROR
        DISABLED = FlextPluginConstants.Lifecycle.STATUS_DISABLED
        HEALTHY = FlextPluginConstants.Lifecycle.STATUS_HEALTHY
        UNHEALTHY = FlextPluginConstants.Lifecycle.STATUS_UNHEALTHY

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
        TAP = FlextPluginConstants.Types.TYPE_TAP
        TARGET = FlextPluginConstants.Types.TYPE_TARGET
        TRANSFORM = FlextPluginConstants.Types.TYPE_TRANSFORM

        # Architecture Types
        EXTENSION = FlextPluginConstants.Types.TYPE_EXTENSION
        SERVICE = FlextPluginConstants.Types.TYPE_SERVICE
        MIDDLEWARE = FlextPluginConstants.Types.TYPE_MIDDLEWARE
        TRANSFORMER = FlextPluginConstants.Types.TYPE_TRANSFORMER

        # Integration Types
        API = FlextPluginConstants.Types.TYPE_API
        DATABASE = FlextPluginConstants.Types.TYPE_DATABASE
        NOTIFICATION = FlextPluginConstants.Types.TYPE_NOTIFICATION
        AUTHENTICATION = FlextPluginConstants.Types.TYPE_AUTHENTICATION
        AUTHORIZATION = FlextPluginConstants.Types.TYPE_AUTHORIZATION

        # Utility Types
        UTILITY = FlextPluginConstants.Types.TYPE_UTILITY
        TOOL = FlextPluginConstants.Types.TYPE_TOOL
        HANDLER = FlextPluginConstants.Types.TYPE_HANDLER
        PROCESSOR = FlextPluginConstants.Types.TYPE_PROCESSOR

        # Additional Types
        CORE = FlextPluginConstants.Types.TYPE_CORE
        ADDON = FlextPluginConstants.Types.TYPE_ADDON
        THEME = FlextPluginConstants.Types.TYPE_THEME
        LANGUAGE = FlextPluginConstants.Types.TYPE_LANGUAGE

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
            min_length=FlextPluginConstants.PluginValidation.MIN_PLUGIN_NAME_LENGTH,
            max_length=FlextPluginConstants.PluginValidation.MAX_PLUGIN_NAME_LENGTH,
            pattern=FlextPluginConstants.PluginValidation.PLUGIN_NAME_PATTERN,
            description="Plugin unique identifier name",
        )
        plugin_version: str = Field(
            default="1.0.0",
            pattern=FlextPluginConstants.PluginValidation.VERSION_PATTERN,
            description="Plugin semantic version",
        )
        description: str = Field(
            default="",
            max_length=FlextPluginConstants.PluginValidation.MAX_DESCRIPTION_LENGTH,
            description="Plugin functionality description",
        )
        author: str = Field(
            default="",
            max_length=FlextPluginConstants.PluginValidation.MAX_AUTHOR_LENGTH,
            description="Plugin author",
        )
        plugin_type: FlextPluginModels.PluginType = Field(
            description="Plugin type classification",
        )
        status: FlextPluginModels.PluginStatus = Field(
            description="Current plugin operational status",
        )
        enabled: bool = Field(default=True, description="Plugin enabled state")
        dependencies: FlextPluginTypes.Core.StringList = Field(
            default_factory=list, description="Required plugin dependencies"
        )
        tags: FlextPluginTypes.Core.StringList = Field(
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
            if (
                self.status == FlextPluginModels.PluginStatus.ACTIVE
                and not self.enabled
            ):
                error_msg = FlextPluginConstants.PluginMessages.PLUGIN_CANNOT_BE_ACTIVE_WHEN_DISABLED
                raise ValueError(error_msg)

            if self.name in self.dependencies:
                error_msg = (
                    FlextPluginConstants.PluginMessages.PLUGIN_CANNOT_DEPEND_ON_ITSELF
                )
                raise ValueError(error_msg)

            return self

        @field_validator("dependencies")
        @classmethod
        def validate_dependencies_format(
            cls, value: FlextPluginTypes.Core.StringList
        ) -> FlextPluginTypes.Core.StringList:
            """Validate dependency format and constraints."""
            if len(value) > FlextPluginConstants.PluginValidation.MAX_DEPENDENCIES:
                error_msg = FlextPluginConstants.PluginMessages.TOO_MANY_DEPENDENCIES
                raise ValueError(error_msg)

            for dep in value:
                if not re.match(
                    FlextPluginConstants.PluginValidation.PLUGIN_NAME_PATTERN, dep
                ):
                    error_msg = FlextPluginConstants.PluginMessages.INVALID_DEPENDENCY_FORMAT.format(
                        dep=dep
                    )
                    raise ValueError(error_msg)

            return value

        @field_serializer("dependencies", when_used="json")
        def serialize_dependencies_with_validation(
            self, value: FlextPluginTypes.Core.StringList
        ) -> FlextPluginTypes.Core.PluginDict:
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
            default=100,
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
                self.timeout_seconds <= FlextConstants.Performance.DEFAULT_TIMEOUT_LIMIT
                and self.max_memory_mb
                <= FlextConstants.Performance.MEMORY_CACHE_MAX_SIZE
                // 1048576  # Convert bytes to MB
                and self.max_cpu_percent
                <= FlextConstants.Performance.CPU_THRESHOLD_PERCENT
            )

        @field_validator("priority")
        @classmethod
        def validate_priority_range(cls, value: int) -> int:
            """Validate priority is within acceptable range."""
            if (
                not FlextPluginConstants.PluginValidation.MIN_PRIORITY
                <= value
                <= FlextPluginConstants.PluginValidation.MAX_PRIORITY
            ):
                error_msg = FlextPluginConstants.PluginMessages.PRIORITY_MUST_BE_BETWEEN_0_AND_100
                raise ValueError(error_msg)
            return value

        @field_validator("max_memory_mb")
        @classmethod
        def validate_memory_limits(cls, value: int) -> int:
            """Validate memory limits are reasonable."""
            if value > FlextPluginConstants.Performance.READY_MAX_MEMORY_MB:
                error_msg = (
                    FlextPluginConstants.PluginMessages.MEMORY_LIMIT_EXCEEDS_MAXIMUM
                )
                raise ValueError(error_msg)
            if value < FlextPluginConstants.Performance.MINIMUM_MEMORY_LIMIT_MB:
                error_msg = FlextPluginConstants.PluginMessages.MEMORY_LIMIT_TOO_LOW
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
            default=FlextPluginConstants.PluginSecurity.SECURITY_MEDIUM,
            pattern=FlextPluginConstants.PluginValidation.SECURITY_LEVEL_PATTERN,
            description="Plugin security clearance level",
        )
        permissions: FlextPluginTypes.Core.StringList = Field(
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
            default=FlextPluginConstants.Monitoring.DEFAULT_LOG_LEVEL,
            pattern=FlextPluginConstants.PluginValidation.LOG_LEVEL_PATTERN,
            description="Logging level for plugin",
        )
        alert_thresholds: FlextPluginTypes.Core.FloatDict = Field(
            default_factory=lambda: {
                "cpu_percent": FlextPluginConstants.Monitoring.DEFAULT_CPU_THRESHOLD,
                "memory_percent": FlextPluginConstants.Monitoring.DEFAULT_MEMORY_THRESHOLD,
                "error_rate": FlextPluginConstants.Monitoring.DEFAULT_ERROR_RATE_THRESHOLD,
                "response_time_ms": FlextPluginConstants.Monitoring.DEFAULT_RESPONSE_TIME_THRESHOLD,
            },
            description="Alert threshold configuration",
        )
        retention_days: int = Field(
            default=FlextPluginConstants.Monitoring.DEFAULT_RETENTION_DAYS,
            ge=FlextPluginConstants.Monitoring.MIN_RETENTION_DAYS,
            le=FlextPluginConstants.Monitoring.MAX_RETENTION_DAYS,
            description="Data retention period in days",
        )

        @property
        def has_basic_monitoring(self) -> bool:
            """Check if basic monitoring features are enabled."""
            return self.metrics_enabled and self.health_checks and self.error_tracking

        @field_validator("alert_thresholds")
        @classmethod
        def validate_alert_thresholds(
            cls, value: FlextPluginTypes.Core.FloatDict
        ) -> FlextPluginTypes.Core.FloatDict:
            """Validate alert threshold values."""
            required_thresholds = {
                "cpu_percent",
                "memory_percent",
                "error_rate",
                "response_time_ms",
            }
            missing = required_thresholds - set(value.keys())
            if missing:
                error_msg = FlextPluginConstants.PluginMessages.MISSING_REQUIRED_THRESHOLDS.format(
                    missing=missing
                )
                raise ValueError(error_msg)

            for key, threshold in value.items():
                if (
                    key.endswith("_percent")
                    and not 0 <= threshold <= FlextConstants.Validation.MAX_PERCENTAGE
                ):
                    error_msg = FlextPluginConstants.PluginMessages.PERCENTAGE_THRESHOLD_MUST_BE_0_100.format(
                        key=key
                    )
                    raise ValueError(error_msg)
                if threshold < 0:
                    error_msg = FlextPluginConstants.PluginMessages.THRESHOLD_CANNOT_BE_NEGATIVE.format(
                        key=key
                    )
                    raise ValueError(error_msg)

            return value

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
        keywords: FlextPluginTypes.Core.StringList = Field(
            default_factory=list,
            description="Plugin keywords",
        )
        maintainers: FlextPluginTypes.Core.StringList = Field(
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
        input_data: dict[str, FlextPluginTypes.Core.AnyDict] = Field(
            default_factory=dict,
            description="Input data for execution",
        )
        context: dict[str, FlextPluginTypes.Core.AnyDict] = Field(
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
        data: FlextPluginTypes.Core.AnyDict = Field(
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
        plugins_affected: FlextPluginTypes.Core.StringList = Field(
            default_factory=list,
            description="List of affected plugin names",
        )
        execution_time_ms: float = Field(
            default=0.0,
            description="Operation execution time in milliseconds",
        )
        details: dict[str, FlextPluginTypes.Core.AnyDict] = Field(
            default_factory=dict,
            description="Additional operation details",
        )
        errors: FlextPluginTypes.Core.StringList = Field(
            default_factory=list,
            description="List of error messages",
        )
        completed_at: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Operation completion timestamp",
        )


__all__ = [
    # Main unified class
    "FlextPluginModels",
]
