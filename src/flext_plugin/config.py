"""FLEXT Plugin Configuration - Plugin system settings using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import Self

from pydantic import Field, field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from flext_core import FlextConfig, FlextModels, FlextResult
from flext_plugin.constants import FlextPluginConstants


class FlextPluginConfig(FlextConfig):
    """Single Pydantic 2 Settings class for flext-plugin extending FlextConfig.

    Follows standardized pattern:
    - Extends FlextConfig from flext-core
    - No nested classes within Config
    - All defaults from FlextPluginConstants
    - Uses enhanced singleton pattern with inverse dependency injection
    - Uses Pydantic 2.11+ features (field_validator, model_validator)
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_PLUGIN_",
        case_sensitive=False,
        extra="allow",
        # Inherit enhanced Pydantic 2.11+ features from FlextConfig
        validate_assignment=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "title": "FLEXT Plugin Configuration",
            "description": "Plugin system configuration extending FlextConfig",
        },
    )

    # Plugin Discovery Configuration using FlextPluginConstants for defaults
    discovery_enabled: bool = Field(
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
        gt=0,
        le=3600,
        description="Plugin discovery interval in seconds",
    )

    include_system_plugins: bool = Field(
        default=True,
        description="Include system-level plugins",
    )

    # Plugin Loading Configuration using FlextPluginConstants for defaults
    loading_enabled: bool = Field(
        default=True,
        description="Enable plugin loading",
    )

    lazy_loading: bool = Field(
        default=True,
        description="Enable lazy plugin loading",
    )

    max_load_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum plugin load retries",
    )

    load_timeout_seconds: int = Field(
        default=30,
        gt=0,
        le=300,
        description="Plugin load timeout in seconds",
    )

    dependency_resolution: bool = Field(
        default=True,
        description="Enable plugin dependency resolution",
    )

    # Plugin Security Configuration using FlextPluginConstants for defaults
    security_enabled: bool = Field(
        default=True,
        description="Enable plugin security checks",
    )

    require_signatures: bool = Field(
        default=False,
        description="Require plugin signatures",
    )

    sandbox_enabled: bool = Field(
        default=True,
        description="Enable plugin sandboxing",
    )

    allowed_imports: list[str] = Field(
        default_factory=lambda: ["flext_core", "flext_plugin"],
        description="Allowed import modules for plugins",
    )

    restricted_operations: list[str] = Field(
        default_factory=lambda: ["file_write", "network_access"],
        description="Restricted operations for plugins",
    )

    # Hot Reload Configuration using FlextPluginConstants for defaults
    hot_reload_enabled: bool = Field(
        default=True,
        description="Enable plugin hot reloading",
    )

    hot_reload_interval_seconds: int = Field(
        default=5,
        gt=0,
        le=3600,
        description="Hot reload check interval in seconds",
    )

    # Plugin Registry Configuration using FlextPluginConstants for defaults
    registry_path: str | None = Field(
        default=None,
        description="Plugin registry file path",
    )

    enable_remote_registry: bool = Field(
        default=False,
        description="Enable remote plugin registry",
    )

    remote_registry_url: str | None = Field(
        default=None,
        description="Remote plugin registry URL",
    )

    # Performance Configuration using FlextPluginConstants for defaults
    max_concurrent_loads: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Maximum concurrent plugin loads",
    )

    memory_limit_mb: int = Field(
        default=512,
        gt=0,
        description="Memory limit per plugin in MB",
    )

    execution_timeout_seconds: int = Field(
        default=60,
        gt=0,
        description="Plugin execution timeout in seconds",
    )

    # Project Identification
    project_name: str = Field(
        default="flext-plugin",
        description="Project name",
    )

    project_version: str = Field(
        default="0.9.0",
        description="Project version",
    )

    # Pydantic 2.11+ field validators
    @field_validator("plugin_directories")
    @classmethod
    def validate_plugin_directories(cls, v: list[str]) -> list[str]:
        """Validate plugin directories are specified."""
        if not v:
            msg = "At least one plugin directory required"
            raise ValueError(msg)
        return v

    @field_validator("discovery_interval_seconds")
    @classmethod
    def validate_discovery_interval(cls, v: int) -> int:
        """Validate discovery interval is reasonable."""
        if v < 1:
            msg = "Discovery interval must be positive"
            raise ValueError(msg)
        return v

    @field_validator("allowed_imports")
    @classmethod
    def validate_allowed_imports(cls, v: list[str]) -> list[str]:
        """Validate allowed imports list."""
        if not v:
            msg = "At least one allowed import required for security"
            raise ValueError(msg)
        return v

    @field_validator("remote_registry_url")
    @classmethod
    def validate_remote_registry_url(cls, v: str | None) -> str | None:
        """Validate remote registry URL format."""
        if v is not None and v.strip():
            # Use flext-core URL validation
            result = FlextModels.create_validated_url(v.strip())
            if result.is_failure:
                msg = f"Invalid remote registry URL: {result.error}"
                raise ValueError(msg)
            return str(result.unwrap())
        return v

    @model_validator(mode="after")
    def validate_plugin_configuration_consistency(self) -> Self:
        """Validate plugin configuration consistency."""
        # Validate security configuration consistency
        if self.security_enabled and not self.allowed_imports:
            msg = "Security mode requires at least one allowed import"
            raise ValueError(msg)

        # Validate remote registry configuration
        if self.enable_remote_registry and not self.remote_registry_url:
            msg = "Remote registry requires URL when enabled"
            raise ValueError(msg)

        # Validate hot reload configuration
        if self.hot_reload_enabled and self.hot_reload_interval_seconds < 1:
            msg = "Hot reload interval must be positive when enabled"
            raise ValueError(msg)

        # Validate loading configuration
        if self.loading_enabled and self.max_load_retries < 0:
            msg = "Max load retries cannot be negative"
            raise ValueError(msg)

        # Validate performance configuration
        if (
            self.max_concurrent_loads
            > FlextPluginConstants.Performance.MAX_CONCURRENT_LOADS_WARNING_THRESHOLD
        ):
            warnings.warn(
                f"High concurrent loads ({self.max_concurrent_loads}) may impact performance",
                UserWarning,
                stacklevel=2,
            )

        return self

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate plugin system business rules."""
        try:
            # Validate discovery rules
            if self.discovery_enabled and not self.plugin_directories:
                return FlextResult[None].fail("Plugin discovery requires directories")

            # Validate loading rules
            if self.loading_enabled and self.load_timeout_seconds <= 0:
                return FlextResult[None].fail("Load timeout must be positive")

            # Validate security rules
            if (
                self.security_enabled
                and self.sandbox_enabled
                and not self.allowed_imports
            ):
                return FlextResult[None].fail(
                    "Sandboxed security requires allowed imports"
                )

            # Validate performance rules
            if (
                self.memory_limit_mb
                < FlextPluginConstants.Performance.MINIMUM_MEMORY_LIMIT_MB
            ):
                return FlextResult[None].fail("Memory limit too low (minimum 64MB)")

            if (
                self.execution_timeout_seconds
                > FlextPluginConstants.Performance.MAXIMUM_EXECUTION_TIMEOUT_SECONDS
            ):
                return FlextResult[None].fail(
                    "Execution timeout too high (maximum 1 hour)"
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Business rules validation failed: {e}")

    def get_discovery_config(self) -> dict[str, object]:
        """Get plugin discovery configuration context."""
        return {
            "enabled": self.discovery_enabled,
            "directories": self.plugin_directories,
            "auto_discover": self.auto_discover,
            "interval_seconds": self.discovery_interval_seconds,
            "include_system": self.include_system_plugins,
        }

    def get_loading_config(self) -> dict[str, object]:
        """Get plugin loading configuration context."""
        return {
            "enabled": self.loading_enabled,
            "lazy_loading": self.lazy_loading,
            "max_retries": self.max_load_retries,
            "timeout_seconds": self.load_timeout_seconds,
            "dependency_resolution": self.dependency_resolution,
        }

    def get_security_config(self) -> dict[str, object]:
        """Get plugin security configuration context."""
        return {
            "enabled": self.security_enabled,
            "require_signatures": self.require_signatures,
            "sandbox_enabled": self.sandbox_enabled,
            "allowed_imports": self.allowed_imports,
            "restricted_operations": self.restricted_operations,
        }

    def get_registry_config(self) -> dict[str, object]:
        """Get plugin registry configuration context."""
        return {
            "registry_path": self.registry_path,
            "enable_remote": self.enable_remote_registry,
            "remote_url": self.remote_registry_url,
        }

    def get_performance_config(self) -> dict[str, object]:
        """Get plugin performance configuration context."""
        return {
            "max_concurrent_loads": self.max_concurrent_loads,
            "memory_limit_mb": self.memory_limit_mb,
            "execution_timeout_seconds": self.execution_timeout_seconds,
        }

    @classmethod
    def create_for_environment(
        cls, environment: str, **overrides: object
    ) -> FlextPluginConfig:
        """Create configuration for specific environment using enhanced singleton pattern."""
        return cls.get_or_create_shared_instance(
            project_name="flext-plugin", environment=environment, **overrides
        )

    @classmethod
    def create_default(cls) -> FlextPluginConfig:
        """Create default configuration instance using enhanced singleton pattern."""
        return cls.get_or_create_shared_instance(project_name="flext-plugin")

    @classmethod
    def create_for_development(cls) -> FlextPluginConfig:
        """Create configuration optimized for development using enhanced singleton pattern."""
        return cls.get_or_create_shared_instance(
            project_name="flext-plugin",
            hot_reload_enabled=True,
            hot_reload_interval_seconds=2,
            security_enabled=False,
            sandbox_enabled=False,
            max_concurrent_loads=2,
            memory_limit_mb=256,
        )

    @classmethod
    def create_for_production(cls) -> FlextPluginConfig:
        """Create configuration optimized for production using enhanced singleton pattern."""
        return cls.get_or_create_shared_instance(
            project_name="flext-plugin",
            hot_reload_enabled=False,
            security_enabled=True,
            sandbox_enabled=True,
            require_signatures=True,
            max_concurrent_loads=10,
            memory_limit_mb=1024,
        )

    @classmethod
    def get_global_instance(cls) -> FlextPluginConfig:
        """Get the global singleton instance using enhanced FlextConfig pattern."""
        return cls.get_or_create_shared_instance(project_name="flext-plugin")

    @classmethod
    def reset_global_instance(cls) -> None:
        """Reset the global FlextPluginConfig instance (mainly for testing)."""
        # Use the enhanced FlextConfig reset mechanism
        cls.reset_shared_instance()


__all__ = [
    "FlextPluginConfig",
]
