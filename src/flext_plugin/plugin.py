"""FLEXT Plugin Entity - Plugin domain entity.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from flext_core import FlextModels, FlextResult, FlextUtilities
from pydantic import Field, field_validator

from flext_plugin.constants import FlextPluginConstants


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
    def get_operational_statuses(cls) -> list[PluginStatus]:
        """Get statuses representing operational states."""
        return [cls.ACTIVE, cls.HEALTHY, cls.LOADED]

    @classmethod
    def get_error_statuses(cls) -> list[PluginStatus]:
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
    def get_etl_types(cls) -> list[PluginType]:
        """Get ETL-related plugin types."""
        return [cls.TAP, cls.TARGET, cls.TRANSFORM]

    @classmethod
    def get_architectural_types(cls) -> list[PluginType]:
        """Get architectural plugin types."""
        return [cls.EXTENSION, cls.SERVICE, cls.MIDDLEWARE, cls.TRANSFORMER]

    def is_etl_plugin(self) -> bool:
        """Check if this is an ETL plugin type."""
        return self in self.get_etl_types()

    def is_architectural_plugin(self) -> bool:
        """Check if this is an architectural plugin type."""
        return self in self.get_architectural_types()


class Plugin(FlextModels.Entity):
    """Rich plugin domain entity with comprehensive business logic and lifecycle management.

    Core domain entity representing a plugin within the FLEXT ecosystem.
    This is a DOMAIN ENTITY, not a plugin implementation. It encapsulates
    plugin identity, metadata, configuration, and business rules while
    maintaining consistency with Domain-Driven Design principles.
    """

    # Pydantic field definitions with comprehensive metadata
    name: str = Field(
        description="Unique plugin identifier used for discovery and management",
        min_length=1,
        max_length=100,
    )
    plugin_version: str = Field(
        description="Semantic version string following semver format (e.g., '1.2.3')",
        min_length=1,
        max_length=50,
    )
    description: str = Field(
        default="",
        description="Human-readable description of plugin functionality",
        max_length=500,
    )
    author: str = Field(
        default="",
        description="Plugin developer or organization name",
        max_length=100,
    )
    status: PluginStatus = Field(
        alias="status",
        description="Current plugin lifecycle and operational status",
    )
    plugin_type: PluginType = Field(
        alias="plugin_type",
        description="Plugin category and type for classification",
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Plugin creation timestamp",
    )

    @field_validator("status", mode="before")
    @classmethod
    def set_default_status(cls, v: object) -> object:
        """Set default status if not provided."""
        if v is None:
            return PluginStatus.INACTIVE
        return v

    @field_validator("plugin_type", mode="before")
    @classmethod
    def set_default_plugin_type(cls, v: object) -> object:
        """Set default plugin type if not provided."""
        if v is None:
            return PluginType.UTILITY
        return v

    # Runtime metrics (optional, populated during execution)
    is_healthy: bool = Field(
        default=True,
        description="Current health status of the plugin",
    )
    execution_count: int = Field(
        default=0,
        description="Total number of executions performed",
    )
    average_execution_time_ms: float = Field(
        default=0.0,
        description="Average execution time in milliseconds",
    )
    error_count: int = Field(
        default=0,
        description="Total number of execution errors",
    )

    @classmethod
    def create(
        cls,
        *,
        name: str,
        plugin_version: str,
        entity_id: str | None = None,
        config: dict[str, object] | None = None,
        **kwargs: object,
    ) -> Plugin:
        """Create plugin entity with proper validation.

        Args:
            name: Plugin name (required)
            plugin_version: Plugin version (required)
            entity_id: Unique entity identifier
            config: Configuration dict[str, object] containing description, author, etc.
            **kwargs: Additional arguments for testing convenience

        Returns:
            Plugin: Validated plugin entity

        """
        # Generate ID if not provided
        entity_id = entity_id or FlextUtilities.Generators.generate_entity_id()

        # Extract config values
        config = config or {}

        # Create instance data
        instance_data: dict[str, object] = {
            "id": entity_id,
            "version": kwargs.get("entity_version", 1),
            "metadata": kwargs.get("metadata", {}),
            "name": name,
            "plugin_version": plugin_version,
            "description": config.get("description", kwargs.get("description", "")),
            "author": config.get("author", kwargs.get("author", "")),
            "status": config.get(
                "status",
                kwargs.get("status", FlextPluginConstants.Lifecycle.STATUS_INACTIVE),
            ),
            "plugin_type": config.get(
                "plugin_type",
                kwargs.get("plugin_type", FlextPluginConstants.Types.TYPE_UTILITY),
            ),
        }

        return cls.model_validate(instance_data)

    def activate(self) -> bool:
        """Activate the plugin."""
        if self.status in {
            FlextPluginConstants.Lifecycle.STATUS_INACTIVE,
            PluginStatus.INACTIVE,
        }:
            setattr(self, "status", PluginStatus.ACTIVE)
            return True
        return False

    def deactivate(self) -> bool:
        """Deactivate the plugin."""
        if self.status in {
            FlextPluginConstants.Lifecycle.STATUS_ACTIVE,
            PluginStatus.ACTIVE,
        }:
            setattr(self, "status", PluginStatus.INACTIVE)
            return True
        return False

    def is_active(self) -> bool:
        """Check if plugin is active."""
        return self.status in {
            PluginStatus.ACTIVE,
            PluginStatus.ACTIVE.value,
        }

    @property
    def active(self) -> bool:
        """Check if plugin is active (backward compatibility)."""
        return self.is_active()

    def record_execution(
        self,
        execution_time_ms: float,
        *,
        success: bool = True,
    ) -> None:
        """Record plugin execution for metrics tracking."""
        current_count = getattr(self, "_execution_count", 0)
        current_avg = getattr(self, "_average_execution_time_ms", 0.0)

        new_count = current_count + 1
        new_avg = ((current_avg * current_count) + execution_time_ms) / new_count

        setattr(self, "_execution_count", new_count)
        setattr(self, "_average_execution_time_ms", new_avg)
        setattr(
            self,
            "_last_execution",
            FlextUtilities.Generators.generate_iso_timestamp(),
        )

        if not success:
            setattr(self, "status", PluginStatus.UNHEALTHY)

    def record_error(self, error_message: str) -> None:
        """Record plugin error for tracking."""
        current_error_count = getattr(self, "_error_count", 0)

        setattr(self, "_error_count", current_error_count + 1)
        setattr(self, "_last_error", error_message)
        setattr(
            self,
            "_last_error_time",
            FlextUtilities.Generators.generate_iso_timestamp(),
        )
        setattr(self, "status", PluginStatus.UNHEALTHY)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin entity."""
        if not self.name or not self.name.strip():
            return FlextResult[None].fail("Plugin name is required and cannot be empty")
        if not self.plugin_version or not self.plugin_version.strip():
            return FlextResult[None].fail(
                "Plugin version is required and cannot be empty",
            )
        return FlextResult[None].ok(None)


__all__ = ["Plugin", "PluginStatus", "PluginType"]
