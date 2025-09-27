"""Models for plugin operations.

This module provides data models for plugin operations.
"""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import Field

from flext_core import FlextModels
from flext_plugin.typings import FlextPluginTypes


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

    # Core Plugin Status and Type Enums
    class PluginStatus(FlextModels.BaseModel):
        """Plugin lifecycle and health states."""

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

    class PluginType(FlextModels.BaseModel):
        """Plugin type classifications."""

        UTILITY: str = "utility"
        EXTENSION: str = "extension"
        SERVICE: str = "service"
        MIDDLEWARE: str = "middleware"
        TAP: str = "tap"
        TARGET: str = "target"
        TRANSFORM: str = "transform"
        API: str = "api"
        CLI: str = "cli"

    # Core Plugin Models
    class PluginModel(FlextModels.BaseModel):
        """Core plugin entity model."""

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

    class ConfigModel(FlextModels.BaseConfig):
        """Plugin configuration model."""

        enabled: bool = Field(default=True, description="Plugin enabled state")
        settings: FlextPluginTypes.Core.SettingsDict = Field(
            default_factory=dict, description="Plugin settings"
        )
        priority: int = Field(default=100, description="Plugin priority")
        timeout_seconds: int = Field(default=60, description="Plugin execution timeout")
        max_memory_mb: int = Field(default=512, description="Maximum memory usage")
        max_cpu_percent: int = Field(default=50, description="Maximum CPU usage")
        auto_restart: bool = Field(default=True, description="Auto restart on failure")
        retry_attempts: int = Field(default=3, description="Maximum retry attempts")
