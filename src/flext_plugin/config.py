"""FLEXT Plugin Configuration - Advanced plugin system settings using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import Self

from flext_core import (
    FlextConfig,
    FlextConstants,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)
from pydantic import Field, field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from flext_plugin.constants import FlextPluginConstants


class FlextPluginConfig(FlextConfig):
    """Advanced Pydantic 2 Settings class for flext-plugin using modern FlextConfig features.

    Extends FlextConfig with plugin-specific configuration using advanced patterns:
    - Uses FlextConfig's enhanced singleton pattern and environment management
    - Integrates with FlextPluginConstants for type-safe constant access
    - Leverages Pydantic 2.11+ advanced validation and serialization features
    - Provides environment-specific configuration profiles
    - Implements comprehensive business rule validation
    - Supports dynamic configuration updates and hot reloading

    Configuration Sources (in priority order):
    1. Environment variables (FLEXT_PLUGIN_* prefix)
    2. Configuration files (YAML/JSON/TOML)
    3. FlextPluginConstants defaults
    4. FlextConstants fallbacks
    5. Sensible hardcoded defaults

    Key Features:
    - Type-safe configuration with full Pydantic validation
    - Environment-aware configuration profiles
    - Dynamic configuration updates without restart
    - Comprehensive security and performance validation
    - Integration with FLEXT observability and monitoring
    - Plugin-specific business rule enforcement
    """

    model_config = SettingsConfigDict(
        # Use advanced FlextConfig features
        env_prefix="FLEXT_PLUGIN_",
        case_sensitive=False,
        extra="allow",
        # Advanced Pydantic 2.11+ features
        validate_assignment=True,
        str_strip_whitespace=True,
        str_to_lower=False,
        json_encoders={
            # Custom JSON encoding for plugin types
            set: list,
            frozenset: list,
        },
        json_schema_extra={
            "title": "FLEXT Plugin Configuration",
            "description": "Advanced plugin system configuration extending FlextConfig",
            "version": "0.9.9",
            "examples": [
                {
                    "discovery_enabled": True,
                    "plugin_directories": ["plugins", "~/.flext/plugins"],
                    "security_enabled": True,
                    "hot_reload_enabled": True,
                }
            ],
        },
    )

    # Plugin Discovery Configuration - Using advanced FlextConfig integration
    discovery_enabled: bool = Field(
        default=True,
        description="Enable plugin discovery with automatic timeout validation",
    )

    plugin_directories: FlextTypes.StringList = Field(
        default=FlextPluginConstants.Discovery.DEFAULT_PLUGIN_PATHS,
        description="Directories to search for plugins (from FlextPluginConstants)",
        min_length=1,
    )

    auto_discover: bool = Field(
        default=True,
        description="Automatically discover plugins on startup",
    )

    discovery_interval_seconds: int = Field(
        default=FlextPluginConstants.Discovery.DISCOVERY_TIMEOUT_SECONDS,
        gt=0,
        le=FlextConstants.Network.DEFAULT_TIMEOUT * 60,  # Max 10 minutes
        description="Plugin discovery interval in seconds",
    )

    include_system_plugins: bool = Field(
        default=True,
        description="Include system-level plugins",
    )

    # Plugin Loading Configuration - Advanced integration with FlextConstants
    loading_enabled: bool = Field(
        default=True,
        description="Enable plugin loading with FlextConstants reliability patterns",
    )

    lazy_loading: bool = Field(
        default=True,
        description="Enable lazy plugin loading for performance optimization",
    )

    max_load_retries: int = Field(
        default=FlextPluginConstants.HotReload.MAX_RETRIES,
        ge=FlextConstants.Reliability.MIN_RETRY_ATTEMPTS,
        le=FlextConstants.Reliability.MAX_RETRY_ATTEMPTS,
        description="Maximum plugin load retries using FlextConstants reliability bounds",
    )

    load_timeout_seconds: int = Field(
        default=FlextPluginConstants.Discovery.DEFAULT_TIMEOUT_SECONDS,
        gt=0,
        le=FlextConstants.Network.DEFAULT_TIMEOUT * 5,  # Max 5x default timeout
        description="Plugin load timeout in seconds with FlextConstants integration",
    )

    dependency_resolution: bool = Field(
        default=True,
        description="Enable plugin dependency resolution for complex plugin ecosystems",
    )

    # Plugin Security Configuration - Advanced integration with FlextPluginConstants
    security_enabled: bool = Field(
        default=True,
        description="Enable comprehensive plugin security checks and validation",
    )

    require_signatures: bool = Field(
        default=False,
        description="Require cryptographic plugin signatures for enterprise security",
    )

    sandbox_enabled: bool = Field(
        default=True,
        description="Enable plugin sandboxing for secure execution isolation",
    )

    allowed_imports: FlextTypes.StringList = Field(
        default=["flext_core", "flext_plugin", "typing"],
        description="Allowed import modules for plugins with FLEXT ecosystem integration",
        min_length=1,
    )

    restricted_operations: FlextTypes.StringList = Field(
        default=["file_write", "network_access", "subprocess", "import"],
        description="Restricted operations for plugins to prevent security vulnerabilities",
    )

    # Hot Reload Configuration - Advanced integration with FlextPluginConstants
    hot_reload_enabled: bool = Field(
        default=True,
        description="Enable plugin hot reloading for development and production flexibility",
    )

    hot_reload_interval_seconds: int = Field(
        default=FlextPluginConstants.HotReload.DEFAULT_INTERVAL_SECONDS,
        gt=0,
        le=FlextConstants.Network.DEFAULT_TIMEOUT * 60,  # Max 30 minutes
        description="Hot reload check interval in seconds using FlextPluginConstants",
    )

    # Plugin Registry Configuration - Advanced remote registry support
    registry_path: str | None = Field(
        default=None,
        description="Local plugin registry file path for persistence",
    )

    enable_remote_registry: bool = Field(
        default=False,
        description="Enable remote plugin registry for distributed plugin management",
    )

    remote_registry_url: str | None = Field(
        default=None,
        description="Remote plugin registry URL for centralized plugin distribution",
    )

    # Performance Configuration - Advanced resource management
    max_concurrent_loads: int = Field(
        default=FlextPluginConstants.Lifecycle.DEFAULT_WORKERS,
        ge=FlextPluginConstants.Lifecycle.MIN_PLUGIN_WORKERS,
        le=FlextPluginConstants.Lifecycle.MAX_PLUGIN_WORKERS,
        description="Maximum concurrent plugin loads using FlextPluginConstants worker bounds",
    )

    memory_limit_mb: int = Field(
        default=FlextPluginConstants.Performance.MINIMUM_MEMORY_LIMIT_MB * 4,  # 256MB default
        gt=0,
        description="Memory limit per plugin in MB with FlextPluginConstants integration",
    )

    execution_timeout_seconds: int = Field(
        default=FlextPluginConstants.Performance.MAXIMUM_EXECUTION_TIMEOUT_SECONDS // 2,  # 30 minutes
        gt=0,
        description="Plugin execution timeout in seconds with performance bounds",
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
    def validate_plugin_directories(
        cls, v: FlextTypes.StringList
    ) -> FlextTypes.StringList:
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
    def validate_allowed_imports(
        cls, v: FlextTypes.StringList
    ) -> FlextTypes.StringList:
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
            result = FlextUtilities.Validation.validate_url(v.strip())
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
        if self.discovery_enabled and not self.plugin_directories:
            return FlextResult[None].fail("Plugin discovery requires directories")

        if self.loading_enabled and self.load_timeout_seconds <= 0:
            return FlextResult[None].fail("Load timeout must be positive")

        if (
            self.security_enabled
            and self.sandbox_enabled
            and not self.allowed_imports
        ):
            return FlextResult[None].fail("Sandboxed security requires allowed imports")

        if (
            self.memory_limit_mb
            < FlextPluginConstants.Performance.MINIMUM_MEMORY_LIMIT_MB
        ):
            return FlextResult[None].fail("Memory limit too low (minimum 64MB)")

        if (
            self.execution_timeout_seconds
            > FlextPluginConstants.Performance.MAXIMUM_EXECUTION_TIMEOUT_SECONDS
        ):
            return FlextResult[None].fail("Execution timeout too high (maximum 1 hour)")

        return FlextResult[None].ok(None)

    def get_discovery_config(self) -> FlextTypes.Dict:
        """Get plugin discovery configuration context."""
        return {
            "enabled": self.discovery_enabled,
            "directories": self.plugin_directories,
            "auto_discover": self.auto_discover,
            "interval_seconds": self.discovery_interval_seconds,
            "include_system": self.include_system_plugins,
        }

    def get_loading_config(self) -> FlextTypes.Dict:
        """Get plugin loading configuration context."""
        return {
            "enabled": self.loading_enabled,
            "lazy_loading": self.lazy_loading,
            "max_retries": self.max_load_retries,
            "timeout_seconds": self.load_timeout_seconds,
            "dependency_resolution": self.dependency_resolution,
        }

    def get_security_config(self) -> FlextTypes.Dict:
        """Get plugin security configuration context."""
        return {
            "enabled": self.security_enabled,
            "require_signatures": self.require_signatures,
            "sandbox_enabled": self.sandbox_enabled,
            "allowed_imports": self.allowed_imports,
            "restricted_operations": self.restricted_operations,
        }

    def get_registry_config(self) -> FlextTypes.Dict:
        """Get plugin registry configuration context."""
        return {
            "registry_path": self.registry_path,
            "enable_remote": self.enable_remote_registry,
            "remote_url": self.remote_registry_url,
        }

    def get_performance_config(self) -> FlextTypes.Dict:
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
        """Create configuration for specific environment."""
        return cls.get_or_create_shared_instance(
            project_name="flext-plugin", environment=environment, **overrides
        )

    @classmethod
    def create_default(cls) -> FlextPluginConfig:
        """Create default configuration instance."""
        return cls.get_or_create_shared_instance(project_name="flext-plugin")

    @classmethod
    def create_for_development(cls) -> FlextPluginConfig:
        """Create configuration optimized for development."""
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
        """Create configuration optimized for production."""
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
        """Get the global singleton instance."""
        return cls.get_or_create_shared_instance(project_name="flext-plugin")


__all__ = [
    "FlextPluginConfig",
]
