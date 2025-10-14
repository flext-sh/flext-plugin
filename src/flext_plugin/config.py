"""FLEXT Plugin Config - Plugin system configuration management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextCore
from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict

from flext_plugin.constants import FlextPluginConstants


class FlextPluginConfig(FlextCore.Config):
    """Plugin system configuration management extending FlextCore.Config.

    Provides comprehensive configuration management for all plugin system operations
    including discovery, loading, execution, security, and monitoring settings.

    Usage:
        ```python
        from flext_plugin import FlextPluginConfig

        # Load configuration
        config = FlextPluginConfig()

        # Access plugin-specific settings
        plugin_paths = config.discovery.plugin_paths
        security_level = config.security.default_level
        performance_limits = config.performance.max_memory_mb
        ```
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_PLUGIN_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_assignment=True,
    )

    class Discovery:
        """Plugin discovery configuration settings."""

        plugin_paths: FlextCore.Types.StringList = Field(
            default_factory=lambda: FlextPluginConstants.Discovery.DEFAULT_PLUGIN_PATHS,
            description="Paths to search for plugins",
        )
        timeout_seconds: int = Field(
            default=FlextPluginConstants.Discovery.DEFAULT_TIMEOUT_SECONDS,
            description="Discovery timeout in seconds",
        )
        enable_validation: bool = Field(
            default=True,
            description="Enable plugin validation during discovery",
        )
        enable_security_scan: bool = Field(
            default=True,
            description="Enable security scanning during discovery",
        )
        recursive_search: bool = Field(
            default=True,
            description="Search subdirectories recursively",
        )
        file_extensions: FlextCore.Types.StringList = Field(
            default_factory=lambda: [
                FlextPluginConstants.Files.PYTHON_EXTENSION,
                FlextPluginConstants.Files.YAML_CONFIG_EXTENSION,
                FlextPluginConstants.Files.JSON_CONFIG_EXTENSION,
                FlextPluginConstants.Files.TOML_CONFIG_EXTENSION,
            ],
            description="File extensions to consider for plugins",
        )

        @field_validator("plugin_paths")
        @classmethod
        def validate_plugin_paths(
            cls, v: FlextCore.Types.StringList
        ) -> FlextCore.Types.StringList:
            """Validate plugin paths are not empty."""
            if not v:
                raise ValueError(
                    FlextPluginConstants.PluginMessages.AT_LEAST_ONE_PLUGIN_PATH_MUST_BE_SPECIFIED
                )
            return v

        @field_validator("timeout_seconds")
        @classmethod
        def validate_timeout(cls, v: int) -> int:
            """Validate timeout is positive."""
            if v <= 0:
                raise ValueError(
                    FlextPluginConstants.PluginMessages.TIMEOUT_MUST_BE_POSITIVE
                )
            return v

    class Security:
        """Plugin security configuration settings."""

        default_level: str = Field(
            default=FlextPluginConstants.PluginSecurity.DEFAULT_SECURITY_LEVEL,
            description="Default security level for plugins",
        )
        enable_sandboxing: bool = Field(
            default=True,
            description="Enable plugin sandboxing",
        )
        require_signature_verification: bool = Field(
            default=False,
            description="Require signature verification for plugins",
        )
        allowed_imports: FlextCore.Types.StringList = Field(
            default_factory=lambda: FlextPluginConstants.Security.DEFAULT_ALLOWED_IMPORTS,
            description="Allowed import modules for plugins",
        )
        blocked_imports: FlextCore.Types.StringList = Field(
            default_factory=lambda: FlextPluginConstants.Security.DEFAULT_BLOCKED_IMPORTS,
            description="Blocked import modules for plugins",
        )
        network_access: bool = Field(
            default=False,
            description="Allow network access for plugins",
        )
        file_system_access: bool = Field(
            default=False,
            description="Allow file system access for plugins",
        )
        max_execution_time: int = Field(
            default=FlextPluginConstants.PluginPerformance.READY_TIMEOUT_SECONDS,
            description="Maximum execution time in seconds",
        )

        @field_validator("default_level")
        @classmethod
        def validate_security_level(cls, v: str) -> str:
            """Validate security level is valid."""
            if v.upper() not in FlextPluginConstants.PluginSecurity.SECURITY_LEVELS:
                raise ValueError(
                    FlextPluginConstants.PluginMessages.INVALID_SECURITY_LEVEL.format(
                        level=v
                    )
                )
            return v.upper()

    class Performance:
        """Plugin performance configuration settings."""

        max_memory_mb: int = Field(
            default=FlextPluginConstants.PluginPerformance.READY_MAX_MEMORY_MB,
            description="Maximum memory usage in MB",
        )
        max_cpu_percent: int = Field(
            default=FlextPluginConstants.PluginPerformance.DEFAULT_MAX_CPU_PERCENT,
            description="Maximum CPU usage percentage",
        )
        max_concurrent_plugins: int = Field(
            default=FlextPluginConstants.PluginPerformance.DEFAULT_MAX_CONCURRENT_PLUGINS,
            description="Maximum number of concurrent plugins",
        )
        enable_resource_monitoring: bool = Field(
            default=True,
            description="Enable resource usage monitoring",
        )
        performance_thresholds: dict[str, float] = Field(
            default_factory=lambda: {
                "excellent_success_rate": FlextPluginConstants.PluginPerformance.EXCELLENT_SUCCESS_RATE,
                "good_success_rate": FlextPluginConstants.PluginPerformance.GOOD_SUCCESS_RATE,
                "fair_success_rate": FlextPluginConstants.PluginPerformance.FAIR_SUCCESS_RATE,
            },
            description="Performance threshold configuration",
        )

        @field_validator("max_memory_mb")
        @classmethod
        def validate_memory_limit(cls, v: int) -> int:
            """Validate memory limit is reasonable."""
            if v < FlextPluginConstants.PluginPerformance.MINIMUM_MEMORY_LIMIT_MB:
                raise ValueError(
                    FlextPluginConstants.PluginMessages.MEMORY_LIMIT_TOO_LOW
                )
            if v > FlextPluginConstants.PluginPerformance.READY_MAX_MEMORY_MB:
                raise ValueError(
                    FlextPluginConstants.PluginMessages.MEMORY_LIMIT_EXCEEDS_MAXIMUM
                )
            return v

        @field_validator("max_cpu_percent")
        @classmethod
        def validate_cpu_percent(cls, v: int) -> int:
            """Validate CPU percentage is valid."""
            if (
                not FlextPluginConstants.PluginPerformance.PERCENTAGE_MIN
                <= v
                <= FlextPluginConstants.PluginPerformance.PERCENTAGE_MAX
            ):
                raise ValueError(
                    FlextPluginConstants.PluginMessages.CPU_PERCENTAGE_MUST_BE_BETWEEN_0_AND_100
                )
            return v

    class HotReload:
        """Plugin hot reload configuration settings."""

        enabled: bool = Field(
            default=True,
            description="Enable hot reload functionality",
        )
        watch_interval: float = Field(
            default=FlextPluginConstants.HotReload.DEFAULT_INTERVAL_SECONDS,
            description="File watching interval in seconds",
        )
        debounce_ms: int = Field(
            default=FlextPluginConstants.HotReload.DEBOUNCE_MS,
            description="Debounce time in milliseconds",
        )
        max_retries: int = Field(
            default=FlextPluginConstants.HotReload.MAX_RETRIES,
            description="Maximum retry attempts for failed reloads",
        )
        enable_rollback: bool = Field(
            default=True,
            description="Enable rollback on reload failure",
        )
        watch_paths: FlextCore.Types.StringList = Field(
            default_factory=list,
            description="Additional paths to watch for changes",
        )

        @field_validator("watch_interval")
        @classmethod
        def validate_watch_interval(cls, v: float) -> float:
            """Validate watch interval is positive."""
            if v <= 0:
                raise ValueError(
                    FlextPluginConstants.PluginMessages.WATCH_INTERVAL_MUST_BE_POSITIVE
                )
            return v

        @field_validator("debounce_ms")
        @classmethod
        def validate_debounce(cls, v: int) -> int:
            """Validate debounce time is non-negative."""
            if v < 0:
                raise ValueError(
                    FlextPluginConstants.PluginMessages.DEBOUNCE_TIME_CANNOT_BE_NEGATIVE
                )
            return v

    class Monitoring:
        """Plugin monitoring configuration settings."""

        enabled: bool = Field(
            default=True,
            description="Enable monitoring functionality",
        )
        metrics_enabled: bool = Field(
            default=True,
            description="Enable metrics collection",
        )
        health_checks_enabled: bool = Field(
            default=True,
            description="Enable health checks",
        )
        performance_tracking: bool = Field(
            default=True,
            description="Enable performance tracking",
        )
        error_tracking: bool = Field(
            default=True,
            description="Enable error tracking",
        )
        log_level: str = Field(
            default=FlextPluginConstants.Monitoring.DEFAULT_LOG_LEVEL,
            description="Logging level for plugin operations",
        )
        retention_days: int = Field(
            default=FlextPluginConstants.Monitoring.DEFAULT_RETENTION_DAYS,
            description="Data retention period in days",
        )

        @field_validator("log_level")
        @classmethod
        def validate_log_level(cls, v: str) -> str:
            """Validate log level is valid."""
            if v.upper() not in FlextPluginConstants.Monitoring.LOG_LEVELS:
                raise ValueError(
                    FlextPluginConstants.PluginMessages.INVALID_LOG_LEVEL.format(
                        level=v
                    )
                )
            return v.upper()

        @field_validator("retention_days")
        @classmethod
        def validate_retention_days(cls, v: int) -> int:
            """Validate retention days is reasonable."""
            if (
                not FlextPluginConstants.Monitoring.MIN_RETENTION_DAYS
                <= v
                <= FlextPluginConstants.Monitoring.MAX_RETENTION_DAYS
            ):
                raise ValueError(
                    FlextPluginConstants.PluginMessages.RETENTION_DAYS_MUST_BE_BETWEEN_1_AND_365
                )
            return v

    class Registry:
        """Plugin registry configuration settings."""

        enabled: bool = Field(
            default=True,
            description="Enable plugin registry functionality",
        )
        registry_url: str | None = Field(
            default=None,
            description="Remote registry URL",
        )
        require_authentication: bool = Field(
            default=False,
            description="Require authentication for registry access",
        )
        api_key: str | None = Field(
            default=None,
            description="API key for registry authentication",
        )
        verify_signatures: bool = Field(
            default=False,
            description="Verify plugin signatures",
        )
        trusted_publishers: FlextCore.Types.StringList = Field(
            default_factory=list,
            description="List of trusted plugin publishers",
        )
        sync_interval: int = Field(
            default=FlextPluginConstants.Registry.DEFAULT_SYNC_INTERVAL,
            description="Registry sync interval in seconds",
        )

        @field_validator("sync_interval")
        @classmethod
        def validate_sync_interval(cls, v: int) -> int:
            """Validate sync interval is positive."""
            if v <= 0:
                raise ValueError(
                    FlextPluginConstants.PluginMessages.SYNC_INTERVAL_MUST_BE_POSITIVE
                )
            return v

    # Configuration sections
    discovery: Discovery = Field(default_factory=Discovery)
    security: Security = Field(default_factory=Security)
    performance: Performance = Field(default_factory=Performance)
    hot_reload: HotReload = Field(default_factory=HotReload)
    monitoring: Monitoring = Field(default_factory=Monitoring)
    registry: Registry = Field(default_factory=Registry)

    def get_plugin_paths(self) -> FlextCore.Types.StringList:
        """Get all configured plugin paths."""
        return self.discovery.plugin_paths

    def is_security_enabled(self) -> bool:
        """Check if security features are enabled."""
        return (
            self.security.enable_sandboxing
            or self.security.require_signature_verification
        )

    def is_monitoring_enabled(self) -> bool:
        """Check if monitoring features are enabled."""
        return self.monitoring.enabled and (
            self.monitoring.metrics_enabled
            or self.monitoring.health_checks_enabled
            or self.monitoring.performance_tracking
        )

    def get_performance_limits(self) -> FlextCore.Types.Dict:
        """Get performance limit configuration."""
        return {
            "max_memory_mb": self.performance.max_memory_mb,
            "max_cpu_percent": self.performance.max_cpu_percent,
            "max_concurrent_plugins": self.performance.max_concurrent_plugins,
            "max_execution_time": self.security.max_execution_time,
        }

    def validate_configuration(self) -> bool:
        """Validate the entire configuration."""
        try:
            # Validate all sections
            self.discovery.model_validate(self.discovery.model_dump())
            self.security.model_validate(self.security.model_dump())
            self.performance.model_validate(self.performance.model_dump())
            self.hot_reload.model_validate(self.hot_reload.model_dump())
            self.monitoring.model_validate(self.monitoring.model_dump())
            self.registry.model_validate(self.registry.model_dump())
            return True
        except Exception:
            return False


__all__ = ["FlextPluginConfig"]
