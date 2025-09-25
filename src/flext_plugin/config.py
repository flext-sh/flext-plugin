"""FLEXT Plugin Configuration - Plugin system settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_core import FlextConfig, FlextModels, FlextResult, FlextTypes


class FlextPluginDiscoveryConfig(FlextModels.Config):
    """Plugin discovery configuration."""

    enabled: bool = Field(
        default=True,
        description="Enable plugin discovery",
    )
    plugin_directories: list[str] = Field(
        default_factory=lambda: ["plugins", "~/.flext/plugins"],
        description="Directories to search for plugins",
    )
    auto_discover: bool = Field(
        default=True,
        description="Automatically discover plugins on startup",
    )
    discovery_interval_seconds: int = Field(
        default=300,
        description="Plugin discovery interval in seconds",
        gt=0,
        le=3600,
    )
    include_system_plugins: bool = Field(
        default=True,
        description="Include system-level plugins",
    )

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Validate plugin discovery configuration."""
        if not self.plugin_directories:
            return FlextResult[None].fail("At least one plugin directory required")
        if self.discovery_interval_seconds < 1:
            return FlextResult[None].fail("Discovery interval must be positive")
        return FlextResult[None].ok(None)


class FlextPluginLoadingConfig(FlextModels.Config):
    """Plugin loading configuration."""

    lazy_loading: bool = Field(
        default=True,
        description="Enable lazy plugin loading",
    )
    max_load_time_seconds: int = Field(
        default=30,
        description="Maximum plugin load time in seconds",
        gt=0,
        le=300,
    )
    validate_on_load: bool = Field(
        default=True,
        description="Validate plugins on load",
    )
    fail_fast: bool = Field(
        default=False,
        description="Fail immediately on plugin load errors",
    )
    isolation_mode: str = Field(
        default="process",
        description="Plugin isolation mode: process, thread, or none",
        pattern="^(Union[Union[process, thread], none])$",
    )

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Validate plugin loading configuration."""
        valid_modes = {"process", "thread", "none"}
        if self.isolation_mode not in valid_modes:
            return FlextResult[None].fail(
                f"Invalid isolation mode: {self.isolation_mode}",
            )
        if self.max_load_time_seconds < 1:
            return FlextResult[None].fail("Max load time must be positive")
        return FlextResult[None].ok(None)


class FlextPluginSecurityConfig(FlextModels.Config):
    """Plugin security configuration."""

    verify_signatures: bool = Field(
        default=True,
        description="Verify plugin signatures",
    )
    allowed_sources: list[str] = Field(
        default_factory=lambda: ["official", "trusted"],
        description="Allowed plugin sources",
    )
    sandbox_enabled: bool = Field(
        default=True,
        description="Enable plugin sandboxing",
    )
    max_memory_mb: int = Field(
        default=512,
        description="Maximum plugin memory usage in MB",
        gt=0,
        le=4096,
    )
    max_cpu_percent: int = Field(
        default=50,
        description="Maximum plugin CPU usage percentage",
        gt=0,
        le=100,
    )

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Validate plugin security configuration."""
        if not self.allowed_sources:
            return FlextResult[None].fail("At least one allowed source required")
        if self.max_memory_mb < 1:
            return FlextResult[None].fail("Max memory must be positive")
        max_cpu_percent = 100
        if self.max_cpu_percent < 1 or self.max_cpu_percent > max_cpu_percent:
            return FlextResult[None].fail("CPU percent must be between 1 and 100")
        return FlextResult[None].ok(None)


class FlextPluginConfig(FlextConfig):
    """Complete plugin system configuration using FlextConfig patterns.

    Provides comprehensive plugin discovery, loading, security, and
    lifecycle management configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_PLUGIN_",
        case_sensitive=False,
    )

    # Structured configuration using value objects
    discovery: FlextPluginDiscoveryConfig = Field(
        default_factory=FlextPluginDiscoveryConfig,
        description="Plugin discovery configuration",
    )
    loading: FlextPluginLoadingConfig = Field(
        default_factory=FlextPluginLoadingConfig,
        description="Plugin loading configuration",
    )
    security: FlextPluginSecurityConfig = Field(
        default_factory=FlextPluginSecurityConfig,
        description="Plugin security configuration",
    )

    # Hot reload configuration
    hot_reload_enabled: bool = Field(
        default=True,
        description="Enable plugin hot reloading",
    )
    hot_reload_interval_seconds: int = Field(
        default=5,
        description="Hot reload check interval in seconds",
        gt=0,
        le=3600,
    )

    # Plugin registry configuration
    registry_path: str | None = Field(
        default=None,
        description="Plugin registry file path",
    )
    enable_remote_registry: bool = Field(
        default=False,
        description="Enable remote plugin registry",
    )

    # Project identification
    project_name: str = Field(
        default="flext-plugin",
        description="Project name",
    )
    project_version: str = Field(
        default="0.9.0",
        description="Project version",
    )

    def validate_domain_rules(self: object) -> FlextResult[None]:
        """Validate complete plugin configuration."""
        validations = [
            ("Discovery", self.discovery.validate_business_rules()),
            ("Loading", self.loading.validate_business_rules()),
            ("Security", self.security.validate_business_rules()),
        ]

        for section_name, validation_result in validations:
            if not validation_result.success:
                return FlextResult[None].fail(
                    f"{section_name} validation failed: {validation_result.error}",
                )

        # Validate hot reload configuration
        if self.hot_reload_enabled and self.hot_reload_interval_seconds < 1:
            return FlextResult[None].fail("Hot reload interval must be positive")

        return FlextResult[None].ok(None)

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Alias to validate_domain_rules for business rule validation."""
        return self.validate_domain_rules()

    @classmethod
    def create_with_defaults(
        cls,
        **overrides: FlextTypes.Core.Dict,
    ) -> FlextPluginConfig:
        """Create configuration with intelligent defaults."""
        defaults = {
            "discovery": FlextPluginDiscoveryConfig(),
            "loading": FlextPluginLoadingConfig(),
            "security": FlextPluginSecurityConfig(),
            "hot_reload_enabled": True,
            "hot_reload_interval_seconds": 5,
            "registry_path": None,
            "enable_remote_registry": False,
            "project_name": "flext-plugin",
            "project_version": "0.9.0",
        }
        defaults.update(overrides)
        return cls.model_validate(defaults)


__all__: FlextTypes.Core.StringList = [
    "FlextPluginConfig",
    "FlextPluginDiscoveryConfig",
    "FlextPluginLoadingConfig",
    "FlextPluginSecurityConfig",
]
