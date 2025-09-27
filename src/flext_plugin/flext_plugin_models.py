"""FLEXT Plugin Models - Single CONSOLIDATED Class Following FLEXT Patterns.

This module implements the CONSOLIDATED model pattern with a single FlextPluginModels
class containing ALL plugin model definitions as nested classes. Maintains backward
compatibility through property re-exports and follows FLEXT architectural standards.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from datetime import datetime
from enum import StrEnum

from pydantic import ConfigDict, Extra, Field, field_validator

from flext_core import FlextModels, FlextTypes
from flext_plugin.constants import FlextPluginConstants
from flext_plugin.type_definitions import PluginConfigData


class FlextPluginModels(FlextModels.Entity):
    """Single CONSOLIDATED class containing ALL plugin models.

    Consolidates ALL model definitions into one class following FLEXT patterns.
    Individual models available as nested classes for organization while maintaining
    backward compatibility through direct exports.

    This approach follows FLEXT architectural standards for single consolidated classes
    per module while preserving existing API surface for seamless migration.
    """

    class Status(StrEnum):
        """Plugin lifecycle and health states."""

        UNKNOWN = "unknown"
        DISCOVERED = "discovered"
        LOADED = "loaded"
        ACTIVE = "active"
        INACTIVE = "inactive"
        LOADING = "loading"
        ERROR = "error"
        DISABLED = "disabled"
        HEALTHY = "healthy"
        UNHEALTHY = "unhealthy"

    class Type(StrEnum):
        """Supported plugin categories for the platform."""

        # Singer ETL Types
        TAP = "tap"
        TARGET = "target"
        TRANSFORM = "transform"

        # Architecture Types
        EXTENSION = "extension"
        SERVICE = "service"
        MIDDLEWARE = "middleware"
        TRANSFORMER = "transformer"

        # Integration Types
        API = "api"
        DATABASE = "database"
        NOTIFICATION = "notification"
        AUTHENTICATION = "authentication"
        AUTHORIZATION = "authorization"

        # Utility Types
        UTILITY = "utility"
        TOOL = "tool"
        HANDLER = "handler"
        PROCESSOR = "processor"

        # Additional Types
        CORE = "core"
        ADDON = "addon"
        THEME = "theme"
        LANGUAGE = "language"

    class ConfigModel(FlextModels.Value):
        """Pydantic model for plugin configuration."""

        model_config = ConfigDict(
            extra=Extra.allow,
            validate_assignment=True,
            str_strip_whitespace=True,
        )

        name: str = Field(
            ...,
            min_length=FlextPluginConstants.MIN_PLUGIN_NAME_LENGTH,
            max_length=FlextPluginConstants.MAX_PLUGIN_NAME_LENGTH,
            pattern=FlextPluginConstants.VALID_PLUGIN_NAME_PATTERN,
            description="Plugin name following naming conventions",
        )
        version: str = Field(
            default="1.0.0",
            description="Plugin version in semantic versioning format",
        )
        description: str = Field(default="", description="Plugin description")
        author: str = Field(default="", description="Plugin author")
        plugin_type: FlextPluginModels.Type = Field(
            default_factory=lambda: FlextPluginModels.Type.UTILITY,
            description="Plugin type category",
        )
        status: FlextPluginModels.Status = Field(
            default_factory=lambda: FlextPluginModels.Status.INACTIVE,
            description="Current plugin status",
        )
        enabled: bool = Field(default=True, description="Whether the plugin is enabled")
        auto_start: bool = Field(
            default=False,
            description="Whether to automatically start the plugin",
        )
        dependencies: FlextTypes.Core.StringList = Field(
            default_factory=list,
            description="List of plugin dependencies",
        )
        tags: FlextTypes.Core.StringList = Field(
            default_factory=list,
            description="Plugin tags for categorization",
        )
        config: dict[str, PluginConfigData] = Field(
            default_factory=dict,
            description="Plugin-specific configuration",
        )

        @field_validator("name")
        @classmethod
        def validate_name(cls, v: str) -> str:
            """Validate plugin name format."""
            if not re.match(FlextPluginConstants.VALID_PLUGIN_NAME_PATTERN, v):
                error_msg = f"Plugin name '{v}' does not match required pattern"
                raise ValueError(error_msg)
            return v

    class MetadataModel(FlextModels.Entity):
        """Pydantic model for plugin metadata."""

        model_config = ConfigDict(
            extra=Extra.allow,
            validate_assignment=True,
        )

        plugin_id: str = Field(..., description="Unique plugin identifier")
        created_at: datetime = Field(
            default_factory=datetime.now,
            description="Plugin creation timestamp",
        )
        updated_at: datetime | None = Field(
            default=None,
            description="Last update timestamp",
        )
        homepage: str | None = Field(default=None, description="Plugin homepage URL")
        repository: str | None = Field(
            default=None,
            description="Plugin repository URL",
        )
        documentation: str | None = Field(
            default=None,
            description="Plugin documentation URL",
        )
        license: str | None = Field(default=None, description="Plugin license")
        keywords: FlextTypes.Core.StringList = Field(
            default_factory=list,
            description="Plugin keywords",
        )
        maintainers: FlextTypes.Core.StringList = Field(
            default_factory=list,
            description="Plugin maintainers",
        )
        platform_version: str | None = Field(
            default=None,
            description="Required platform version",
        )
        python_version: str | None = Field(
            default=None,
            description="Required Python version",
        )

    class PluginModel(FlextModels.Value):
        """Complete Pydantic model for a FLEXT plugin."""

        model_config = ConfigDict(
            extra=Extra.allow,
            validate_assignment=True,
        )

        config: FlextPluginModels.ConfigModel = Field(
            ...,
            description="Plugin configuration",
        )
        metadata: FlextPluginModels.MetadataModel = Field(
            ...,
            description="Plugin metadata",
        )
        runtime_data: dict[str, PluginConfigData] = Field(
            default_factory=dict,
            description="Runtime-specific data",
        )

        @property
        def name(self: object) -> str:
            """Get plugin name from configuration."""
            return self.config.name

        @property
        def version(self: object) -> str:
            """Get plugin version from configuration."""
            return self.config.version

        @property
        def plugin_type(self: object) -> FlextPluginModels.Type:
            """Get plugin type from configuration."""
            return self.config.plugin_type

        @property
        def status(self: object) -> FlextPluginModels.Status:
            """Get plugin status from configuration."""
            return self.config.status

    class ExecutionContextModel(FlextModels.Entity):
        """Pydantic model for plugin execution context."""

        model_config = ConfigDict(
            extra=Extra.allow,
            validate_assignment=True,
        )

        plugin_id: str = Field(..., description="Plugin identifier")
        execution_id: str = Field(..., description="Unique execution identifier")
        input_data: dict[str, PluginConfigData] = Field(
            default_factory=dict,
            description="Input data for execution",
        )
        context: dict[str, PluginConfigData] = Field(
            default_factory=dict,
            description="Execution context data",
        )
        timeout_seconds: int | None = Field(
            default=None,
            description="Execution timeout in seconds",
        )
        started_at: datetime = Field(
            default_factory=datetime.now,
            description="Execution start timestamp",
        )

    class ExecutionResultModel(FlextModels.Entity):
        """Pydantic model for plugin execution results."""

        model_config = ConfigDict(
            extra=Extra.allow,
            validate_assignment=True,
        )

        success: bool = Field(default=False, description="Whether execution succeeded")
        data: PluginConfigData = Field(
            default=None,
            description="Execution output data",
        )
        error: str = Field(default="", description="Error message if execution failed")
        plugin_name: str = Field(default="", description="Name of the executed plugin")
        execution_time: float = Field(
            default=0.0,
            description="Execution time in seconds",
        )
        execution_id: str = Field(default="", description="Unique execution identifier")
        completed_at: datetime = Field(
            default_factory=datetime.now,
            description="Execution completion timestamp",
        )

        @property
        def duration_ms(self: object) -> float:
            """Get execution time in milliseconds."""
            return self.execution_time * 1000

        def is_failure(self: object) -> bool:
            """Return True if execution failed."""
            return not self.success

    class ManagerResultModel(FlextModels.Entity):
        """Pydantic model for plugin manager operation results."""

        model_config = ConfigDict(
            extra=Extra.allow,
            validate_assignment=True,
        )

        operation: str = Field(..., description="Operation name")
        success: bool = Field(default=False, description="Whether operation succeeded")
        plugins_affected: FlextTypes.Core.StringList = Field(
            default_factory=list,
            description="List of affected plugin names",
        )
        execution_time_ms: float = Field(
            default=0.0,
            description="Operation execution time in milliseconds",
        )
        details: dict[str, PluginConfigData] = Field(
            default_factory=dict,
            description="Additional operation details",
        )
        errors: FlextTypes.Core.StringList = Field(
            default_factory=list,
            description="List of error messages",
        )
        completed_at: datetime = Field(
            default_factory=datetime.now,
            description="Operation completion timestamp",
        )


# Export consolidated class and individual models for backward compatibility
PluginStatus = FlextPluginModels.Status
PluginType = FlextPluginModels.Type
FlextPluginConfigModel = FlextPluginModels.ConfigModel
FlextPluginMetadataModel = FlextPluginModels.MetadataModel
FlextPluginModel = FlextPluginModels.PluginModel
PluginExecutionContextModel = FlextPluginModels.ExecutionContextModel
PluginExecutionResultModel = FlextPluginModels.ExecutionResultModel
PluginManagerResultModel = FlextPluginModels.ManagerResultModel

__all__ = [
    # Legacy backward compatibility exports
    "FlextPluginConfigModel",
    "FlextPluginMetadataModel",
    "FlextPluginModel",
    # CONSOLIDATED class (FLEXT pattern)
    "FlextPluginModels",
    "PluginExecutionContextModel",
    "PluginExecutionResultModel",
    "PluginManagerResultModel",
    "PluginStatus",
    "PluginType",
]
