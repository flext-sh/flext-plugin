"""FLEXT Plugin Config - Plugin system configuration management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_core import r, u as u_core
from flext_core.config import FlextConfig
from pydantic import Field
from pydantic_settings import SettingsConfigDict


@FlextConfig.auto_register("plugin")
class FlextPluginConfig(FlextConfig.AutoConfig):
    """Plugin system configuration management using AutoConfig pattern.

    **ARCHITECTURAL PATTERN**: Zero-Boilerplate Auto-Registration

    This class uses FlextConfig.AutoConfig for automatic:
    - Singleton pattern (thread-safe)
    - Namespace registration (accessible via config.plugin)
    - Environment variable loading from FLEXT_PLUGIN_* variables
    - .env file loading (production/development)
    - Automatic type conversion and validation via Pydantic v2
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_PLUGIN_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
        validate_default=True,
        frozen=False,
        arbitrary_types_allowed=True,
        strict=False,
    )

    # Pydantic fields
    plugin_name: str = Field(
        default="",
        description="Name of the plugin this config belongs to",
    )
    config_data: dict[str, object] = Field(
        default_factory=dict,
        description="Plugin configuration data",
    )
    enabled: bool = Field(default=True, description="Whether plugin is enabled")
    settings: dict[str, object] = Field(
        default_factory=dict,
        description="Plugin settings",
    )
    dependencies: list[str] = Field(
        default_factory=list,
        description="Plugin dependencies",
    )
    priority: int = Field(default=100, description="Plugin execution priority")
    max_memory_mb: int = Field(default=512, description="Maximum memory usage in MB")
    max_cpu_percent: int = Field(default=50, description="Maximum CPU usage percentage")
    timeout_seconds: int = Field(default=30, description="Plugin execution timeout")
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Configuration creation timestamp",
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Configuration last update timestamp",
    )

    @classmethod
    def create(
        cls,
        *,
        plugin_name: str,
        entity_id: str | None = None,
        config_data: dict[str, object] | None = None,
        **kwargs: object,
    ) -> FlextPluginConfig:
        """Create plugin config entity with proper validation."""
        entity_id = entity_id or u_core.Generators.generate_entity_id()

        # Create instance data
        instance_data: dict[str, object] = {
            "id": entity_id,
            "version": kwargs.get("version", 1),
            "metadata": kwargs.get("entity_metadata", {}),
            "plugin_name": plugin_name,
            "config_data": config_data or {},
            "enabled": kwargs.get("enabled", True),
            "settings": kwargs.get("settings", {}),
            "dependencies": kwargs.get("dependencies", []),
            "priority": kwargs.get("priority", 100),
            "max_memory_mb": kwargs.get(
                "max_memory_mb",
                512,
            ),
            "max_cpu_percent": kwargs.get(
                "max_cpu_percent",
                50,
            ),
            "timeout_seconds": kwargs.get(
                "timeout_seconds",
                30,
            ),
            "created_at": kwargs.get("created_at", datetime.now(UTC)),
            "updated_at": kwargs.get("updated_at"),
        }

        return cls.model_validate(instance_data)

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(UTC)

    def validate_business_rules(self) -> r[None]:
        """Validate domain rules for plugin config entity."""
        if not self.plugin_name or not self.plugin_name.strip():
            return r[None].fail("Plugin name is required and cannot be empty")
        if self.max_memory_mb <= 0:
            return r[None].fail("Maximum memory must be positive")
        cpu_percentage_max = 100
        if self.max_cpu_percent < 0 or self.max_cpu_percent > cpu_percentage_max:
            return r[None].fail("CPU percentage must be between 0 and 100")
        if self.timeout_seconds <= 0:
            return r[None].fail("Timeout must be positive")
        return r[None].ok(None)


__all__ = ["FlextPluginConfig"]
