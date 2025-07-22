"""FLEXT Plugin Configuration - Modern Python 3.13 with unified patterns.

REFACTORED:
    Uses flext-core unified configuration mixins with types and constants.
Zero tolerance for duplication.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flext_core import Field
from flext_core.config import get_container
from flext_core.config.unified_config import (
    BaseConfigMixin,
    LoggingConfigMixin,
    MonitoringConfigMixin,
    OracleConfigMixin,
    PerformanceConfigMixin,
)
from flext_core.domain.constants import ConfigDefaults, FlextFramework
from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from flext_core.config.base import DIContainer


class PluginSettings(
    BaseConfigMixin,
    LoggingConfigMixin,
    MonitoringConfigMixin,
    PerformanceConfigMixin,
    OracleConfigMixin,
    BaseSettings,
):
    """FLEXT Plugin configuration settings using unified configuration mixins.

    All settings can be overridden via environment variables with the
    prefix FLEXT_PLUGIN_ (e.g., FLEXT_PLUGIN_DISCOVERY_TIMEOUT).
    Uses flext-core unified configuration mixins with DI support.
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_PLUGIN_",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
        use_enum_values=True,
    )

    # Project identification (inherits from BaseConfigMixin but override with
    # Plugin-specific values)
    project_name: str = Field(
        default="flext-infrastructure.plugins.flext-plugin",
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
        description="Project name",
    )
    project_version: str = Field(
        default=FlextFramework.VERSION,
        description="Project version",
    )

    # Plugin Discovery Configuration
    plugin_directory: Path = Field(
        default_factory=lambda: Path.cwd() / "plugins",
        description="Directory to search for plugins",
    )
    additional_plugin_paths: list[Path] = Field(
        default_factory=list,
        description="Additional plugin search paths",
    )
    discovery_timeout: int = Field(
        5,
        ge=1,
        le=60,
        description="Plugin discovery timeout in seconds",
    )
    discovery_pattern: str = Field(
        "*.py",
        description="File pattern for plugin discovery",
    )
    exclude_patterns: list[str] = Field(
        default_factory=lambda: ["__pycache__", "*.pyc", ".git", ".pytest_cache"],
        description="Patterns to exclude from discovery",
    )

    # Plugin Loading Configuration
    load_timeout: int = Field(
        30,
        ge=1,
        le=300,
        description="Plugin loading timeout in seconds",
    )
    max_concurrent_loads: int = Field(
        10,
        ge=1,
        le=100,
        description="Maximum concurrent plugin loads",
    )
    enable_lazy_loading: bool = Field(True, description="Enable lazy plugin loading")
    cache_loaded_plugins: bool = Field(
        True,
        description="Cache loaded plugins in memory",
    )

    # Hot Reload Configuration
    hot_reload_enabled: bool = Field(
        False,
        description="Enable hot reload functionality",
    )
    hot_reload_poll_interval: int = Field(
        1000,
        ge=100,
        le=10000,
        description="Hot reload poll interval in milliseconds",
    )

    # Security Configuration
    verify_signatures: bool = Field(True, description="Verify plugin signatures")
    allowed_imports: list[str] = Field(
        default_factory=lambda: [
            "requests",
            "pandas",
            "numpy",
            "pydantic",
            "click",
        ],
        description="Allowed Python imports for plugins",
    )

    # Note: health_check_enabled inherited from MonitoringConfigMixin
    # Additional plugin-specific health check configuration
    plugin_health_check_interval: int = Field(
        30,
        ge=10,
        le=300,
        description="Plugin-specific health check interval in seconds",
    )

    # Cache and Storage Configuration
    registry_cache_dir: Path = Field(
        default_factory=lambda: Path.cwd() / ".flext" / "plugin_cache",
        description="Directory for plugin registry cache",
    )
    hot_reload_state_backup_dir: Path = Field(
        default_factory=lambda: Path.cwd() / ".flext" / "hot_reload_backup",
        description="Directory for hot reload state backups",
    )

    # Additional Plugin-specific Configuration
    log_plugin_events: bool = Field(True, description="Log plugin lifecycle events")

    # Note: Most common settings now inherited from mixins:
    # - BaseConfigMixin: project_name, project_version, environment, debug
    # - LoggingConfigMixin: log_level, log_file, log_format, log_rotation
    # - MonitoringConfigMixin: metrics_enabled, health_check_enabled, prometheus_port
    # - PerformanceConfigMixin: batch_size, timeout_seconds, retry_count

    # Note: log_level validation is now handled by LoggingConfigMixin

    def configure_dependencies(self, container: DIContainer | None = None) -> None:
        """Configure dependencies in container."""
        if container is None:
            container = get_container()

        # Register this settings instance
        container.register(PluginSettings, self)

        # Parent mixins don't have configure_dependencies method


# Convenience function for getting settings
def get_plugin_settings() -> PluginSettings:
    """Get plugin settings instance."""
    # MyPy doesn't recognize pydantic Field defaults in strict mode
    return PluginSettings()
