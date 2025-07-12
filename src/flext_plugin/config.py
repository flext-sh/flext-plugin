"""FLEXT Plugin Configuration - Modern Python 3.13 + Clean Architecture + DI.

REFACTORED:
    Uses flext-core BaseSettings with types and constants.
Zero tolerance for duplication.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict

from flext_core.config import BaseSettings, get_container, singleton
from flext_core.domain.constants import FlextFramework


@singleton()
class PluginSettings(BaseSettings):
    """FLEXT Plugin configuration settings with environment variable support.

    All settings can be overridden via environment variables with the
    prefix FLEXT_PLUGIN_ (e.g., FLEXT_PLUGIN_DISCOVERY_TIMEOUT).
    Uses flext-core BaseSettings foundation with DI support.
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

    # Project identification
    project_name: str = Field("flext-plugin", description="Project name")
    project_version: str = Field(FlextFramework.VERSION, description="Project version")

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
    discovery_pattern: str = Field("*.py", description="File pattern for plugin discovery")
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
    cache_loaded_plugins: bool = Field(True, description="Cache loaded plugins in memory")

    # Hot Reload Configuration
    hot_reload_enabled: bool = Field(False, description="Enable hot reload functionality")
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

    # Health Check Configuration
    health_check_enabled: bool = Field(True, description="Enable plugin health checks")
    health_check_interval: int = Field(
        30,
        ge=10,
        le=300,
        description="Health check interval in seconds",
    )

    # Logging Configuration
    log_plugin_events: bool = Field(True, description="Log plugin lifecycle events")
    log_level: str = Field("INFO", description="Plugin system log level")

    # Environment and debugging
    environment: str = Field("development", description="Environment name")
    debug: bool = Field(False, description="Debug mode")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            msg = f"Log level must be one of {valid_levels}"
            raise ValueError(msg)
        return v.upper()

    def configure_dependencies(self, container: object = None) -> None:
        """Configure dependencies in container."""
        if container is None:
            container = get_container()

        # Register this settings instance
        container.register(PluginSettings, self)

        # Call parent configuration
        super().configure_dependencies(container)


# Convenience function for getting settings
def get_plugin_settings() -> PluginSettings:
    """Get plugin settings instance."""
    return PluginSettings()
