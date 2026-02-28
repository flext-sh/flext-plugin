"""FLEXT Plugin Config - Plugin system configuration management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_core import FlextSettings, r, u
from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import SettingsConfigDict

from flext_plugin.typings import t


@FlextSettings.auto_register("plugin")
class FlextPluginSettings(FlextSettings):
    """Plugin system configuration management.

    **ARCHITECTURAL PATTERN**: BaseSettings Configuration

    This class provides:
    - Environment variable support via FLEXT_PLUGIN_* prefix
    - Namespace registration (accessible via FlextSettings.get_namespace)
    - Pydantic v2 validation and type safety
    - Complete plugin system configuration
    """

    # Use FlextSettings.resolve_env_file() to ensure all FLEXT configs use same .env
    model_config = SettingsConfigDict(
        env_prefix="FLEXT_PLUGIN_",
        env_file=FlextSettings.resolve_env_file(),
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
    config_data: t.Plugin.ConfigDict = Field(
        default_factory=dict,
        description="Plugin configuration data",
    )
    enabled: bool = Field(default=True, description="Whether plugin is enabled")
    settings: t.Plugin.SettingsDict = Field(
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
    timeout_seconds: float = Field(default=30.0, description="Plugin execution timeout")
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Configuration creation timestamp",
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Configuration last update timestamp",
    )

    class CreateOptions(BaseModel):
        """Options for strict plugin settings creation."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        version: str = "1"
        entity_metadata: t.Plugin.MetadataDict = Field(default_factory=dict)
        enabled: bool = True
        settings: t.Plugin.SettingsDict = Field(default_factory=dict)
        dependencies: list[str] = Field(default_factory=list)
        priority: int = 100
        max_memory_mb: int = 512
        max_cpu_percent: int = 50
        timeout_seconds: float = 30.0
        created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
        updated_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        plugin_name: str,
        entity_id: str | None = None,
        config_data: t.Plugin.ConfigDict | None = None,
        options: CreateOptions | None = None,
    ) -> FlextPluginSettings:
        """Create plugin config entity with proper validation."""
        entity_id = entity_id or u.generate("entity")
        create_options = options if options is not None else cls.CreateOptions()

        # Create instance data
        instance_data = {
            "id": entity_id,
            "version": create_options.version,
            "metadata": create_options.entity_metadata,
            "plugin_name": plugin_name,
            "config_data": config_data or {},
            "enabled": create_options.enabled,
            "settings": create_options.settings,
            "dependencies": create_options.dependencies,
            "priority": create_options.priority,
            "max_memory_mb": create_options.max_memory_mb,
            "max_cpu_percent": create_options.max_cpu_percent,
            "timeout_seconds": create_options.timeout_seconds,
            "created_at": create_options.created_at,
            "updated_at": create_options.updated_at,
        }

        return cls.model_validate(instance_data)

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(UTC)

    def validate_business_rules(self) -> r[bool]:
        """Validate domain rules for plugin config entity."""
        if not self.plugin_name or not self.plugin_name.strip():
            return r[bool].fail("Plugin name is required and cannot be empty")
        if self.max_memory_mb <= 0:
            return r[bool].fail("Maximum memory must be positive")
        cpu_percentage_max = 100
        if self.max_cpu_percent < 0 or self.max_cpu_percent > cpu_percentage_max:
            return r[bool].fail("CPU percentage must be between 0 and 100")
        if self.timeout_seconds <= 0:
            return r[bool].fail("Timeout must be positive")
        return r[bool].ok(value=True)


__all__ = ["FlextPluginSettings"]
