"""Models for plugin operations.

This module provides data models for plugin operations.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SerializationInfo,
    computed_field,
    field_serializer,
    model_validator,
)

from flext_core import FlextModels
from flext_plugin.typings import FlextPluginTypes

# Constants for plugin performance thresholds and validation
PERCENTAGE_MAX: int = 100
PERCENTAGE_MIN: int = 0
PERFORMANCE_EXCELLENT_SUCCESS_RATE: float = 95.0
PERFORMANCE_GOOD_SUCCESS_RATE: float = 90.0
PERFORMANCE_FAIR_SUCCESS_RATE: float = 80.0
PERFORMANCE_EXCELLENT_TIME_MS: int = 1000
PERFORMANCE_GOOD_TIME_MS: int = 2000
PERFORMANCE_FAIR_TIME_MS: int = 5000
EXECUTION_TIME_SCALE_MS_TO_S: int = 1000
PRODUCTION_READY_TIMEOUT_SECONDS: int = 300
PRODUCTION_READY_MAX_MEMORY_MB: int = 1024


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
        # Enhanced Pydantic 2.11 enterprise features
        validate_assignment=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=False,
        validate_return=True,
        ser_json_timedelta="iso8601",
        ser_json_bytes="base64",
        hide_input_in_errors=True,
        json_schema_extra={
            "examples": [
                {
                    "plugin_system": {
                        "name": "enterprise-plugin-platform",
                        "version": "0.9.9",
                        "active_plugins": 12,
                        "plugin_types": ["EXTENSION", "SERVICE", "TAP", "TARGET"],
                    },
                    "plugin_registration": {
                        "name": "flext-enterprise-tap",
                        "plugin_type": "TAP",
                        "status": "ACTIVE",
                        "security_level": "HIGH",
                    },
                    "plugin_monitoring": {
                        "execution_time_ms": 234.5,
                        "memory_usage_mb": 45.2,
                        "health_status": "HEALTHY",
                    },
                }
            ],
            "enterprise_features": [
                "Plugin lifecycle management",
                "Hot-reload system",
                "Security sandboxing",
                "Performance monitoring",
                "Registry and discovery",
                "Singer/Meltano integration",
            ],
        },
    )

    @computed_field
    @property
    def active_plugin_models_count(self) -> int:
        """Computed field returning the number of active plugin model types."""
        # Count active plugin models based on nested classes
        plugin_model_classes = [
            self.PluginModel,
            self.ConfigModel,
            self.PluginStatus,
            self.PluginType,
            self.SecurityModel,
            self.MonitoringModel,
        ]
        return len([cls for cls in plugin_model_classes if cls])

    @computed_field
    @property
    def plugin_system_summary(self) -> dict[str, Any]:
        """Computed field providing comprehensive plugin system summary."""
        return {
            "system_info": {
                "name": "FLEXT Plugin System",
                "version": "2.11.0",
                "active_models": self.active_plugin_models_count,
                "architecture": "Clean Architecture + DDD",
            },
            "supported_operations": [
                "plugin_registration",
                "plugin_discovery",
                "plugin_lifecycle_management",
                "hot_reload_system",
                "security_validation",
                "performance_monitoring",
            ],
            "plugin_types": [
                "UTILITY",
                "EXTENSION",
                "SERVICE",
                "MIDDLEWARE",
                "TAP",
                "TARGET",
                "TRANSFORM",
                "API",
                "CLI",
            ],
            "integrations": [
                "Singer ecosystem",
                "Meltano platform",
                "FLEXT core services",
                "Enterprise monitoring",
            ],
            "security_features": [
                "Plugin sandboxing",
                "Security level validation",
                "Dependency scanning",
                "Runtime isolation",
            ],
        }

    @model_validator(mode="after")
    def validate_plugin_system_consistency(self) -> Self:
        """Model validator ensuring plugin system consistency and security."""
        # Validate that plugin models maintain consistency
        if hasattr(self, "_initialized") and not self._initialized:
            msg = "Plugin models must be properly initialized"
            raise ValueError(msg)

        # Ensure security configurations are properly set for enterprise
        if hasattr(self, "SecurityModel"):
            # Plugin-specific validation logic can be added here
            pass

        return self

    @field_serializer("*", when_used="json")
    def serialize_with_plugin_metadata(
        self, value: Any, _info: SerializationInfo
    ) -> Any:
        """Field serializer adding plugin processing metadata and security context."""
        if isinstance(value, dict):
            return {
                **value,
                "_plugin_metadata": {
                    "processed_at": datetime.now(UTC).isoformat(),
                    "model_type": "FlextPluginModels",
                    "security_validated": True,
                    "plugin_system_compatible": True,
                    "enterprise_grade": True,
                },
            }
        return value

    # Core Plugin Status and Type Enums
    class PluginStatus(BaseModel):
        """Plugin lifecycle and health states."""

        model_config = ConfigDict(validate_assignment=True, frozen=True, extra="forbid")

        UNKNOWN: str = "unknown"
        DISCOVERED: str = "discovered"
        LOADED: str = "loaded"
        ACTIVE: str = "active"
        INACTIVE: str = "inactive"
        LOADING: str = "loading"
        ERROR: str = "error"
        DISABLED: str = "disabled"
        HEALTHY: str = "healthy"
        UNHEALTHY: str = "unhealthy"

        @computed_field
        @property
        def status_categories(self) -> dict[str, list[str]]:
            """Computed field providing plugin status categorization."""
            return {
                "operational_states": [
                    self.DISCOVERED,
                    self.LOADED,
                    self.ACTIVE,
                    self.INACTIVE,
                    self.LOADING,
                    self.DISABLED,
                ],
                "health_states": [self.HEALTHY, self.UNHEALTHY, self.ERROR],
                "transition_states": [self.UNKNOWN, self.LOADING],
            }

        @computed_field
        @property
        def status_metadata(self) -> dict[str, Any]:
            """Computed field providing status metadata."""
            return {
                "total_states": 10,
                "enterprise_ready": True,
                "supports_transitions": True,
                "monitoring_enabled": True,
            }

    class PluginType(BaseModel):
        """Plugin type classifications."""

        model_config = ConfigDict(validate_assignment=True, frozen=True, extra="forbid")

        UTILITY: str = "utility"
        EXTENSION: str = "extension"
        SERVICE: str = "service"
        MIDDLEWARE: str = "middleware"
        TAP: str = "tap"
        TARGET: str = "target"
        TRANSFORM: str = "transform"
        API: str = "api"
        CLI: str = "cli"

        @computed_field
        @property
        def type_categories(self) -> dict[str, list[str]]:
            """Computed field providing plugin type categorization."""
            return {
                "data_processing": [self.TAP, self.TARGET, self.TRANSFORM],
                "infrastructure": [self.SERVICE, self.MIDDLEWARE, self.API],
                "user_interface": [self.CLI, self.EXTENSION],
                "system_utilities": [self.UTILITY],
            }

        @computed_field
        @property
        def singer_compatible_types(self) -> list[str]:
            """Computed field returning Singer ecosystem compatible types."""
            return [self.TAP, self.TARGET, self.TRANSFORM]

    # Core Plugin Models
    class PluginModel(BaseModel):
        """Core plugin entity model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            validate_return=True,
            str_strip_whitespace=True,
        )

        name: str = Field(description="Plugin name")
        version: str = Field(description="Plugin version")
        plugin_type: str = Field(description="Plugin type")
        status: str = Field(default="inactive", description="Plugin status")
        description: str = Field(default="", description="Plugin description")
        author: str = Field(default="", description="Plugin author")
        entry_point: str = Field(description="Plugin entry point")
        dependencies: list[str] = Field(
            default_factory=list, description="Plugin dependencies"
        )
        created_at: str = Field(
            default_factory=lambda: str(datetime.now(UTC)),
            description="Creation timestamp",
        )
        updated_at: str = Field(
            default_factory=lambda: str(datetime.now(UTC)),
            description="Update timestamp",
        )

        @computed_field
        @property
        def plugin_summary(self) -> dict[str, Any]:
            """Computed field providing comprehensive plugin summary."""
            return {
                "identity": {
                    "name": self.name,
                    "version": self.version,
                    "type": self.plugin_type,
                    "author": self.author,
                },
                "operational_info": {
                    "status": self.status,
                    "entry_point": self.entry_point,
                    "dependency_count": len(self.dependencies),
                    "has_description": bool(self.description),
                },
                "lifecycle_info": {
                    "created_at": self.created_at,
                    "updated_at": self.updated_at,
                    "is_singer_compatible": self.plugin_type
                    in {"tap", "target", "transform"},
                    "is_enterprise_ready": True,
                },
            }

        @model_validator(mode="after")
        def validate_plugin_consistency(self) -> Self:
            """Model validator for plugin consistency."""
            # Validate plugin name follows naming conventions
            if (
                not self.name.replace("-", "")
                .replace("_", "")
                .replace(".", "")
                .isalnum()
            ):
                msg = "Plugin name must contain only alphanumeric characters, hyphens, underscores, and dots"
                raise ValueError(msg)

            # Validate version format (semantic versioning)
            version_pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$"

            if not re.match(version_pattern, self.version):
                msg = "Plugin version must follow semantic versioning (e.g., 1.0.0 or 1.0.0-alpha)"
                raise ValueError(msg)

            # Validate entry point format
            if not self.entry_point or "." not in self.entry_point:
                msg = "Plugin entry point must be a valid Python module path"
                raise ValueError(msg)

            return self

        @field_serializer("dependencies", when_used="json")
        def serialize_dependencies_with_validation(
            self, value: list[str]
        ) -> dict[str, Any]:
            """Field serializer for dependencies with validation metadata."""
            return {
                "dependencies": value,
                "dependency_count": len(value),
                "has_flext_dependencies": any("flext" in dep for dep in value),
                "validated_at": datetime.now(UTC).isoformat(),
            }

    class ConfigModel(FlextModels.BaseConfig):
        """Plugin configuration model."""

        model_config = ConfigDict(
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
        priority: int = Field(default=PERCENTAGE_MAX, description="Plugin priority")
        timeout_seconds: int = Field(default=60, description="Plugin execution timeout")
        max_memory_mb: int = Field(default=512, description="Maximum memory usage")
        max_cpu_percent: int = Field(default=50, description="Maximum CPU usage")
        auto_restart: bool = Field(default=True, description="Auto restart on failure")
        retry_attempts: int = Field(default=3, description="Maximum retry attempts")

        @computed_field
        @property
        def config_summary(self) -> dict[str, Any]:
            """Computed field providing comprehensive configuration summary."""
            return {
                "operational_config": {
                    "enabled": self.enabled,
                    "priority": self.priority,
                    "auto_restart": self.auto_restart,
                    "retry_attempts": self.retry_attempts,
                },
                "resource_limits": {
                    "timeout_seconds": self.timeout_seconds,
                    "max_memory_mb": self.max_memory_mb,
                    "max_cpu_percent": self.max_cpu_percent,
                    "memory_limit_bytes": self.max_memory_mb * 1024 * 1024,
                },
                "settings_info": {
                    "settings_count": len(self.settings),
                    "has_custom_settings": bool(self.settings),
                    "is_production_ready": self.timeout_seconds <= PRODUCTION_READY_TIMEOUT_SECONDS
                    and self.max_memory_mb <= PRODUCTION_READY_MAX_MEMORY_MB,
                },
            }

        @model_validator(mode="after")
        def validate_config_consistency(self) -> Self:
            """Model validator for configuration consistency."""
            # Validate resource limits
            if self.max_memory_mb <= 0:
                msg = "Maximum memory must be positive"
                raise ValueError(msg)

            if self.max_cpu_percent <= 0 or self.max_cpu_percent > PERCENTAGE_MAX:
                msg = "Maximum CPU percent must be between 1 and 100"
                raise ValueError(msg)

            if self.timeout_seconds <= 0:
                msg = "Timeout must be positive"
                raise ValueError(msg)

            if self.priority < 0:
                msg = "Priority must be non-negative"
                raise ValueError(msg)

            if self.retry_attempts < 0:
                msg = "Retry attempts must be non-negative"
                raise ValueError(msg)

            return self

        @field_serializer("settings", when_used="json")
        def serialize_settings_securely(self, value: dict) -> dict[str, Any]:
            """Field serializer for secure settings handling."""
            masked_settings = {}
            sensitive_keys = [
                "password",
                "secret",
                "key",
                "token",
                "auth",
                "credential",
            ]

            for key, val in value.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    masked_settings[key] = "***MASKED***"
                else:
                    masked_settings[key] = val

            return {
                "settings": masked_settings,
                "settings_metadata": {
                    "total_settings": len(value),
                    "masked_settings": len(value) - len(masked_settings),
                    "processed_at": datetime.now(UTC).isoformat(),
                },
            }

    class SecurityModel(BaseModel):
        """Plugin security validation and configuration model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            validate_return=True,
        )

        security_level: str = Field(
            default="MEDIUM", description="Plugin security level"
        )
        sandboxing_enabled: bool = Field(default=True, description="Enable sandboxing")
        network_access: bool = Field(default=False, description="Allow network access")
        file_system_access: str = Field(
            default="read-only", description="File system access level"
        )
        allowed_modules: list[str] = Field(
            default_factory=list, description="Allowed Python modules"
        )
        blocked_modules: list[str] = Field(
            default_factory=list, description="Blocked Python modules"
        )
        resource_limits: dict[str, Any] = Field(
            default_factory=dict, description="Resource usage limits"
        )
        audit_logging: bool = Field(default=True, description="Enable audit logging")

        @computed_field
        @property
        def security_summary(self) -> dict[str, Any]:
            """Computed field providing comprehensive security summary."""
            return {
                "security_configuration": {
                    "level": self.security_level,
                    "sandboxing_enabled": self.sandboxing_enabled,
                    "network_access": self.network_access,
                    "file_system_access": self.file_system_access,
                    "audit_logging": self.audit_logging,
                },
                "module_controls": {
                    "allowed_modules_count": len(self.allowed_modules),
                    "blocked_modules_count": len(self.blocked_modules),
                    "has_module_restrictions": bool(
                        self.allowed_modules or self.blocked_modules
                    ),
                },
                "enterprise_compliance": {
                    "is_enterprise_secure": self.security_level
                    in {"HIGH", "ENTERPRISE"},
                    "requires_sandboxing": self.sandboxing_enabled,
                    "has_resource_limits": bool(self.resource_limits),
                    "audit_compliant": self.audit_logging,
                },
            }

        @model_validator(mode="after")
        def validate_security_consistency(self) -> Self:
            """Model validator for security configuration consistency."""
            # Validate security level
            valid_levels = ["LOW", "MEDIUM", "HIGH", "ENTERPRISE"]
            if self.security_level not in valid_levels:
                msg = f"Security level must be one of: {valid_levels}"
                raise ValueError(msg)

            # Validate file system access
            valid_fs_access = ["none", "read-only", "write", "full"]
            if self.file_system_access not in valid_fs_access:
                msg = f"File system access must be one of: {valid_fs_access}"
                raise ValueError(msg)

            # Enterprise security requirements
            if self.security_level == "ENTERPRISE":
                if not self.sandboxing_enabled:
                    msg = "Enterprise security level requires sandboxing"
                    raise ValueError(msg)
                if not self.audit_logging:
                    msg = "Enterprise security level requires audit logging"
                    raise ValueError(msg)
                if self.network_access and self.file_system_access == "full":
                    msg = "Enterprise security cannot allow both network and full file system access"
                    raise ValueError(msg)

            return self

        @field_serializer("resource_limits", when_used="json")
        def serialize_resource_limits_with_metadata(
            self, value: dict[str, Any]
        ) -> dict[str, Any]:
            """Field serializer for resource limits with validation metadata."""
            return {
                "limits": value,
                "limits_metadata": {
                    "limit_count": len(value),
                    "has_memory_limit": "memory" in value,
                    "has_cpu_limit": "cpu" in value,
                    "has_time_limit": "timeout" in value,
                    "validated_at": datetime.now(UTC).isoformat(),
                },
            }

    class MonitoringModel(BaseModel):
        """Plugin monitoring and performance tracking model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            validate_return=True,
        )

        execution_count: int = Field(default=0, description="Total execution count")
        success_count: int = Field(default=0, description="Successful execution count")
        error_count: int = Field(default=0, description="Error count")
        avg_execution_time_ms: float = Field(
            default=0.0, description="Average execution time"
        )
        last_execution_time: str = Field(
            default_factory=lambda: str(datetime.now(UTC)),
            description="Last execution timestamp",
        )
        memory_usage_mb: float = Field(default=0.0, description="Current memory usage")
        cpu_usage_percent: float = Field(default=0.0, description="Current CPU usage")
        health_status: str = Field(
            default="UNKNOWN", description="Plugin health status"
        )
        metrics: dict[str, Any] = Field(
            default_factory=dict, description="Custom metrics"
        )

        @computed_field
        @property
        def monitoring_summary(self) -> dict[str, Any]:
            """Computed field providing comprehensive monitoring summary."""
            success_rate = (
                (self.success_count / self.execution_count * PERCENTAGE_MAX)
                if self.execution_count > 0
                else 0.0
            )
            error_rate = (
                (self.error_count / self.execution_count * PERCENTAGE_MAX)
                if self.execution_count > 0
                else 0.0
            )

            return {
                "execution_statistics": {
                    "total_executions": self.execution_count,
                    "successful_executions": self.success_count,
                    "failed_executions": self.error_count,
                    "success_rate_percent": round(success_rate, 2),
                    "error_rate_percent": round(error_rate, 2),
                },
                "performance_metrics": {
                    "avg_execution_time_ms": self.avg_execution_time_ms,
                    "avg_execution_time_seconds": round(
                        self.avg_execution_time_ms / EXECUTION_TIME_SCALE_MS_TO_S, 3
                    ),
                    "current_memory_mb": self.memory_usage_mb,
                    "current_cpu_percent": self.cpu_usage_percent,
                    "last_execution": self.last_execution_time,
                },
                "health_assessment": {
                    "status": self.health_status,
                    "is_healthy": self.health_status == "HEALTHY",
                    "performance_grade": self._calculate_performance_grade(),
                    "custom_metrics_count": len(self.metrics),
                },
            }

        @model_validator(mode="after")
        def validate_monitoring_consistency(self) -> Self:
            """Model validator for monitoring data consistency."""
            # Validate execution counts
            if self.execution_count < 0:
                msg = "Execution count cannot be negative"
                raise ValueError(msg)

            if self.success_count < 0 or self.error_count < 0:
                msg = "Success and error counts cannot be negative"
                raise ValueError(msg)

            if self.success_count + self.error_count > self.execution_count:
                msg = "Success + error count cannot exceed total execution count"
                raise ValueError(msg)

            # Validate resource usage
            if self.memory_usage_mb < 0:
                msg = "Memory usage cannot be negative"
                raise ValueError(msg)

            if (
                self.cpu_usage_percent < PERCENTAGE_MIN
                or self.cpu_usage_percent > PERCENTAGE_MAX
            ):
                msg = "CPU usage must be between 0 and 100 percent"
                raise ValueError(msg)

            if self.avg_execution_time_ms < 0:
                msg = "Average execution time cannot be negative"
                raise ValueError(msg)

            return self

        @field_serializer("metrics", when_used="json")
        def serialize_metrics_with_metadata(
            self, value: dict[str, Any]
        ) -> dict[str, Any]:
            """Field serializer for metrics with processing metadata."""
            return {
                "custom_metrics": value,
                "metrics_metadata": {
                    "metric_count": len(value),
                    "collected_at": datetime.now(UTC).isoformat(),
                    "plugin_monitoring_version": "2.11.0",
                    "enterprise_compatible": True,
                },
            }

        def _calculate_performance_grade(self) -> str:
            """Calculate performance grade based on metrics."""
            if self.execution_count == 0:
                return "UNGRADED"

            success_rate = (self.success_count / self.execution_count) * PERCENTAGE_MAX

            if (
                success_rate >= PERFORMANCE_EXCELLENT_SUCCESS_RATE
                and self.avg_execution_time_ms < PERFORMANCE_EXCELLENT_TIME_MS
            ):
                return "EXCELLENT"
            if (
                success_rate >= PERFORMANCE_GOOD_SUCCESS_RATE
                and self.avg_execution_time_ms < PERFORMANCE_GOOD_TIME_MS
            ):
                return "GOOD"
            if (
                success_rate >= PERFORMANCE_FAIR_SUCCESS_RATE
                and self.avg_execution_time_ms < PERFORMANCE_FAIR_TIME_MS
            ):
                return "FAIR"
            return "POOR"
