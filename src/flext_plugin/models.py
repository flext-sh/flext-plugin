"""FLEXT Plugin Models - Plugin system data models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import types
from collections.abc import Callable, Mapping
from datetime import datetime
from pathlib import Path
from typing import Annotated, Self

from flext_core import FlextModels, r
from pydantic import Field, field_validator

from flext_plugin import (
    FlextPluginConstants as c_constants,
    FlextPluginTypes as t_types,
    t,
)


class FlextPluginModels(FlextModels):
    """Plugin domain models extending flext-core patterns.

    Provides standardized models for all plugin operations including plugin
    entities, configurations, execution results, and monitoring data.

    All models inherit flext-core validation and patterns following
    Railway-Oriented Programming with r[T] error handling.
    """

    # Re-export PluginType enum from constants for convenience
    PluginType = c_constants.Plugin.PluginType

    class Plugin:
        """Plugin domain namespace."""

        class Entity(FlextModels.Entity):
            """Entity - real inheritance."""

        class Plugin(FlextModels.Entity):
            """Plugin entity - core domain entity with identity and lifecycle.

            Represents a plugin with identity, lifecycle management, and mutable state.
            Compared by identity (id), not by value.

            Attributes:
            name: Plugin unique identifier
            plugin_version: Plugin semantic version (X.Y.Z)
            description: Plugin functionality description
            author: Plugin author/maintainer
            plugin_type: Plugin type classification (from PluginType enum)
            is_enabled: Plugin enabled state
            metadata: Extensible plugin metadata

            """

            name: Annotated[
                str,
                Field(
                    ...,
                    min_length=c_constants.Plugin.PluginValidation.MIN_PLUGIN_NAME_LENGTH,
                    max_length=c_constants.Plugin.PluginValidation.MAX_PLUGIN_NAME_LENGTH,
                    pattern=c_constants.Plugin.PluginValidation.PLUGIN_NAME_PATTERN,
                    description="Plugin unique identifier name",
                ),
            ]
            plugin_version: Annotated[
                str,
                Field(
                    default="1.0.0",
                    pattern=c_constants.Plugin.PluginValidation.VERSION_PATTERN,
                    description="Plugin semantic version (X.Y.Z)",
                ),
            ]
            description: Annotated[
                str,
                Field(
                    default="",
                    max_length=c_constants.Plugin.PluginValidation.MAX_DESCRIPTION_LENGTH,
                    description="Plugin functionality description",
                ),
            ]
            author: Annotated[
                str,
                Field(
                    default="",
                    max_length=c_constants.Plugin.PluginValidation.MAX_AUTHOR_LENGTH,
                    description="Plugin author/maintainer",
                ),
            ]
            plugin_type: Annotated[
                str,
                Field(
                    default=c_constants.Plugin.PluginType.UTILITY,
                    description="Plugin type classification",
                ),
            ]
            is_enabled: Annotated[
                bool,
                Field(default=True, description="Plugin enabled state"),
            ]
            metadata: Annotated[
                dict[str, t.NormalizedValue],
                Field(
                    default_factory=dict,
                    description="Extensible plugin metadata",
                ),
            ]

            @classmethod
            def create(
                cls,
                *,
                name: str,
                plugin_version: str = "1.0.0",
                description: str = "",
                author: str = "",
                plugin_type: str = c_constants.Plugin.PluginType.UTILITY,
                is_enabled: bool = True,
                metadata: Mapping[str, t.NormalizedValue] | None = None,
                entity_id: str | None = None,
            ) -> Self:
                """Factory method to create a new Plugin entity.

                Args:
                name: Plugin name (required)
                plugin_version: Plugin semantic version
                description: Plugin description
                author: Plugin author
                plugin_type: Plugin type (from PluginType enum)
                is_enabled: Whether plugin is initially enabled
                metadata: Additional metadata
                entity_id: Entity ID (auto-generated if None)

                Returns:
                New Plugin entity instance

                """
                metadata_payload: dict[str, t.NormalizedValue] = (
                    dict(metadata.items()) if metadata else {}
                )
                payload: dict[str, t.NormalizedValue] = {
                    "name": name,
                    "plugin_version": plugin_version,
                    "description": description,
                    "author": author,
                    "plugin_type": plugin_type,
                    "is_enabled": is_enabled,
                    "metadata": metadata_payload,
                }
                if entity_id is not None:
                    payload["unique_id"] = entity_id
                return cls.model_validate(payload)

            @field_validator("plugin_type", mode="before")
            @classmethod
            def validate_plugin_type(cls, value: str) -> str:
                """Validate plugin type is a valid PluginType enum value."""
                valid_types = {
                    "tap",
                    "target",
                    "transform",
                    "extension",
                    "service",
                    "middleware",
                    "transformer",
                    "api",
                    "database",
                    "notification",
                    "authentication",
                    "authorization",
                    "utility",
                    "tool",
                    "handler",
                    "processor",
                    "core",
                    "addon",
                    "theme",
                    "language",
                }
                if value not in valid_types:
                    error_msg = f"Invalid plugin type '{value}'. Must be one of: {', '.join(sorted(valid_types))}"
                    raise ValueError(error_msg)
                return value

            @field_validator("plugin_version", mode="before")
            @classmethod
            def validate_semantic_version(cls, value: str) -> str:
                """Validate semantic version format (X.Y.Z)."""
                min_version_parts = 2
                max_version_parts = 3
                parts = value.split(".")
                if (
                    len(parts) < min_version_parts
                    or len(parts) > max_version_parts
                    or not all(p.isdigit() for p in parts if p)
                ):
                    error_msg = f"Version must be semantic format X.Y.Z, got: {value}"
                    raise ValueError(error_msg)
                return value

            def disable(self) -> r[bool]:
                """Disable the plugin.

                Returns:
                r[bool] indicating success or failure

                """
                if not self.is_enabled:
                    return r[bool].fail("Plugin is already disabled")
                self.is_enabled = False
                return r[bool].ok(value=True)

            def enable(self) -> r[bool]:
                """Enable the plugin.

                Returns:
                r[bool] indicating success or failure

                """
                if self.is_enabled:
                    return r[bool].fail("Plugin is already enabled")
                self.is_enabled = True
                return r[bool].ok(value=True)

            def record_error(self, error_message: str) -> None:
                """Record plugin error.

                Args:
                    error_message: Error message to record

                """
                if "error_count" not in self.metadata:
                    self.metadata["error_count"] = 0
                if "last_error" not in self.metadata:
                    self.metadata["last_error"] = ""

                error_count_val = self.metadata.get("error_count", 0)
                error_count = (
                    int(error_count_val)
                    if isinstance(error_count_val, (int, float, str))
                    else 0
                )
                self.metadata["error_count"] = error_count + 1
                self.metadata["last_error"] = error_message

            def record_execution(self, execution_time: float, *, success: bool) -> None:
                """Record plugin execution metrics.

                Args:
                    execution_time: Time taken for execution in seconds
                    success: Whether the execution was successful

                """
                # Update metadata with execution info - use proper type narrowing
                if "execution_count" not in self.metadata:
                    self.metadata["execution_count"] = 0
                if "total_execution_time" not in self.metadata:
                    self.metadata["total_execution_time"] = 0.0
                if "success_count" not in self.metadata:
                    self.metadata["success_count"] = 0
                if "failure_count" not in self.metadata:
                    self.metadata["failure_count"] = 0

                exec_count_val = self.metadata.get("execution_count", 0)
                exec_count = (
                    int(exec_count_val)
                    if isinstance(exec_count_val, (int, float, str))
                    else 0
                )
                total_time_val = self.metadata.get("total_execution_time", 0.0)
                total_time = (
                    float(total_time_val)
                    if isinstance(total_time_val, (int, float, str))
                    else 0.0
                )
                self.metadata["execution_count"] = exec_count + 1
                self.metadata["total_execution_time"] = total_time + execution_time

                if success:
                    success_count_val = self.metadata.get("success_count", 0)
                    success_count = (
                        int(success_count_val)
                        if isinstance(success_count_val, (int, float, str))
                        else 0
                    )
                    self.metadata["success_count"] = success_count + 1
                else:
                    failure_count_val = self.metadata.get("failure_count", 0)
                    failure_count = (
                        int(failure_count_val)
                        if isinstance(failure_count_val, (int, float, str))
                        else 0
                    )
                    self.metadata["failure_count"] = failure_count + 1

            def validate_business_rules(self) -> r[bool]:
                """Validate plugin business rules.

                Business Rules:
                - Plugin name must not be empty
                - Plugin version must follow semantic versioning (X.Y.Z)
                - Plugin type must be valid

                Returns:
                r[bool] indicating validation success or failure

                """
                min_version_parts = 2
                max_version_parts = 3
                if not self.name or not self.name.strip():
                    return r[bool].fail("Plugin name cannot be empty")

                # Validate semantic version
                version_parts = self.plugin_version.split(".")
                if (
                    len(version_parts) < min_version_parts
                    or len(version_parts) > max_version_parts
                ):
                    return r[bool].fail(
                        f"Invalid semantic version: {self.plugin_version}",
                    )
                if not all(part.isdigit() for part in version_parts if part):
                    return r[bool].fail(
                        f"Version parts must be numeric: {self.plugin_version}",
                    )

                # Validate plugin type
                valid_types = {
                    "tap",
                    "target",
                    "transform",
                    "extension",
                    "service",
                    "middleware",
                    "transformer",
                    "api",
                    "database",
                    "notification",
                    "authentication",
                    "authorization",
                    "utility",
                    "tool",
                    "handler",
                    "processor",
                    "core",
                    "addon",
                    "theme",
                    "language",
                }
                if self.plugin_type not in valid_types:
                    return r[bool].fail(f"Invalid plugin type: {self.plugin_type}")

                return r[bool].ok(value=True)

        class ExecutionResult(FlextModels.Value):
            """Plugin execution result - immutable execution outcome.

            Represents the result of a plugin execution including success status,
            output data, and execution metrics.

            Attributes:
            success: Whether execution succeeded
            data: Execution output data
            error: Error message if execution failed
            execution_time_ms: Execution time in milliseconds

            """

            success: Annotated[bool, Field(description="Whether execution succeeded")]
            data: Annotated[
                dict[str, t.NormalizedValue],
                Field(
                    default_factory=dict,
                    description="Execution output data",
                ),
            ]
            error: Annotated[
                str,
                Field(
                    default="",
                    description="Error message if execution failed",
                ),
            ]
            execution_time_ms: Annotated[
                float,
                Field(
                    default=0.0,
                    ge=0,
                    description="Execution time in milliseconds",
                ),
            ]

        class DiscoveryData(FlextModels.Value):
            """Plugin discovery data - immutable discovery result.

            Represents discovered plugin information from various discovery methods
            (file system, entry points, etc_constants.). Immutable value object.

            Attributes:
            name: Plugin unique identifier name
            version: Plugin semantic version (X.Y.Z)
            path: File system path to plugin
            discovery_type: Type of discovered plugin (file, directory, entry_point)
            discovery_method: Discovery method used (file_system, entry_points)
            metadata: Extensible discovery metadata

            """

            name: Annotated[
                str,
                Field(
                    min_length=c_constants.Plugin.PluginValidation.MIN_PLUGIN_NAME_LENGTH,
                    max_length=c_constants.Plugin.PluginValidation.MAX_PLUGIN_NAME_LENGTH,
                    pattern=c_constants.Plugin.PluginValidation.PLUGIN_NAME_PATTERN,
                    description="Plugin unique identifier name",
                ),
            ]
            version: Annotated[
                str,
                Field(
                    pattern=c_constants.Plugin.PluginValidation.VERSION_PATTERN,
                    description="Plugin semantic version (X.Y.Z)",
                ),
            ]
            path: Annotated[Path, Field(description="File system path to plugin")]
            discovery_type: Annotated[
                t_types.Plugin.DiscoveryTypeLiteral,
                Field(
                    description="Type of discovered plugin",
                ),
            ]
            discovery_method: Annotated[
                t_types.Plugin.DiscoveryMethodLiteral,
                Field(
                    description="Discovery method used",
                ),
            ]
            metadata: Annotated[
                dict[str, t.NormalizedValue],
                Field(
                    default_factory=dict,
                    description="Extensible discovery metadata",
                ),
            ]

            @field_validator("version", mode="before")
            @classmethod
            def validate_version(cls, value: str) -> str:
                """Validate semantic version format."""
                min_parts = 2
                max_parts = 3
                parts = value.split(".")
                if (
                    len(parts) < min_parts
                    or len(parts) > max_parts
                    or not all(p.isdigit() for p in parts if p)
                ):
                    error_msg = f"Version must be semantic format X.Y.Z, got: {value}"
                    raise ValueError(error_msg)
                return value

        class LoadData(FlextModels.Value):
            """Plugin load data - immutable load result.

            Represents successfully loaded plugin information including the loaded
            module object and load metadata. Immutable value object.

            Attributes:
            name: Plugin unique identifier name
            version: Plugin semantic version
            path: File system path to plugin
            module: The loaded Python module object
            load_type: Type of loaded plugin (file, directory, entry_point)
            loaded_at: Timestamp when plugin was loaded
            entry_file: Entry file path for directory-based plugins

            """

            name: Annotated[
                str,
                Field(
                    min_length=c_constants.Plugin.PluginValidation.MIN_PLUGIN_NAME_LENGTH,
                    max_length=c_constants.Plugin.PluginValidation.MAX_PLUGIN_NAME_LENGTH,
                    description="Plugin unique identifier name",
                ),
            ]
            version: Annotated[
                str,
                Field(
                    pattern=c_constants.Plugin.PluginValidation.VERSION_PATTERN,
                    description="Plugin semantic version (X.Y.Z)",
                ),
            ]
            path: Annotated[Path, Field(description="File system path to plugin")]
            module: Annotated[
                types.ModuleType,
                Field(
                    description="The loaded Python module object",
                ),
            ]
            load_type: Annotated[
                t_types.Plugin.LoadTypeLiteral,
                Field(
                    description="Type of loaded plugin",
                ),
            ]
            loaded_at: Annotated[
                datetime,
                Field(description="Timestamp when plugin was loaded"),
            ]
            entry_file: Annotated[
                Path | None,
                Field(
                    default=None,
                    description="Entry file path for directory-based plugins",
                ),
            ]

        class ReloadRecord(FlextModels.Value):
            """Plugin reload record - immutable reload history entry.

            Records information about a plugin reload event including timing,
            success/failure status, and optional error details. Immutable value object.

            Attributes:
            plugin_name: Name of reloaded plugin
            plugin_path: Path to reloaded plugin
            timestamp: When reload occurred
            success: Whether reload succeeded
            error: Error message if reload failed
            duration_ms: Reload duration in milliseconds

            """

            plugin_name: Annotated[str, Field(description="Name of reloaded plugin")]
            plugin_path: Annotated[Path, Field(description="Path to reloaded plugin")]
            timestamp: Annotated[datetime, Field(description="When reload occurred")]
            success: Annotated[bool, Field(description="Whether reload succeeded")]
            error: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Error message if reload failed",
                ),
            ]
            duration_ms: Annotated[
                float,
                Field(
                    default=0.0,
                    ge=0,
                    description="Reload duration in milliseconds",
                ),
            ]

        class PluginMetadata(FlextModels.Value):
            """Plugin metadata - immutable metadata value object.

            Represents complete metadata about a plugin including discovery
            and description information. Immutable value object.

            Attributes:
            name: Plugin unique identifier
            version: Plugin semantic version
            description: Plugin description
            author: Plugin author
            plugin_type: Type of plugin (extension, transformer, etc_constants.)
            entry_point: Entry point for plugin
            dependencies: List of plugin dependencies
            metadata: Additional metadata dictionary

            """

            name: Annotated[str, Field(description="Plugin unique identifier")]
            version: Annotated[str, Field(description="Plugin semantic version")]
            description: Annotated[
                str,
                Field(default="", description="Plugin description"),
            ]
            author: Annotated[
                str,
                Field(default="Unknown", description="Plugin author"),
            ]
            plugin_type: Annotated[
                str,
                Field(default="extension", description="Type of plugin"),
            ]
            entry_point: Annotated[str, Field(description="Entry point for plugin")]
            dependencies: Annotated[
                list[str],
                Field(
                    default_factory=list,
                    description="List of plugin dependencies",
                ),
            ]
            metadata: Annotated[
                dict[str, t.NormalizedValue],
                Field(
                    default_factory=dict,
                    description="Additional metadata",
                ),
            ]

        class EventData(FlextModels.Value):
            """Event data - immutable event information.

            Represents structured event data with context and metadata.
            Immutable value object.

            Attributes:
            event_type: Type of event
            plugin_name: Associated plugin name
            timestamp: When event occurred
            data: Event-specific data

            """

            event_type: Annotated[str, Field(description="Type of event")]
            plugin_name: Annotated[str, Field(description="Associated plugin name")]
            timestamp: Annotated[datetime, Field(description="When event occurred")]
            data: Annotated[
                dict[str, t.NormalizedValue],
                Field(
                    default_factory=dict,
                    description="Event-specific data",
                ),
            ]

        class ValidationResult(FlextModels.Value):
            """Validation result - immutable validation outcome.

            Represents result of plugin validation including status and details.
            Immutable value object.

            Attributes:
            is_valid: Whether validation passed
            errors: List of validation errors
            warnings: List of validation warnings
            details: Additional validation details

            """

            is_valid: Annotated[bool, Field(description="Whether validation passed")]
            errors: Annotated[
                list[str],
                Field(
                    default_factory=list,
                    description="List of validation errors",
                ),
            ]
            warnings: Annotated[
                list[str],
                Field(
                    default_factory=list,
                    description="List of validation warnings",
                ),
            ]
            details: Annotated[
                dict[str, t.NormalizedValue],
                Field(
                    default_factory=dict,
                    description="Additional validation details",
                ),
            ]

        class SecurityReport(FlextModels.Value):
            """Security report - immutable security scan result.

            Represents security scanning results for plugins.
            Immutable value object.

            Attributes:
            is_safe: Whether plugin passed security checks
            violations: List of security violations
            warnings: List of security warnings
            analysis_time: When analysis was performed

            """

            is_safe: Annotated[
                bool,
                Field(description="Whether plugin passed security checks"),
            ]
            violations: Annotated[
                list[str],
                Field(
                    default_factory=list,
                    description="List of security violations",
                ),
            ]
            warnings: Annotated[
                list[str],
                Field(
                    default_factory=list,
                    description="List of security warnings",
                ),
            ]
            analysis_time: Annotated[
                datetime,
                Field(description="When analysis was performed"),
            ]

        class WatcherConfig(FlextModels.Value):
            """Watcher configuration - file system monitoring config.

            Represents file watcher configuration for hot reload.
            Immutable value object.

            Attributes:
            watch_path: Path being watched
            watch_interval: Polling interval in seconds
            callback: Callback function reference (Any for flexibility)
            active: Whether watcher is active
            last_modified: File modification tracking
            created_at: Configuration creation time

            """

            watch_path: Annotated[str, Field(description="Path being watched")]
            watch_interval: Annotated[
                float,
                Field(description="Polling interval in seconds"),
            ]
            callback: Annotated[
                Callable[..., object] | None,
                Field(
                    default=None,
                    description="Callback function reference",
                ),
            ]
            active: Annotated[
                bool,
                Field(default=False, description="Whether watcher is active"),
            ]
            last_modified: Annotated[
                dict[str, t.NormalizedValue],
                Field(
                    default_factory=dict,
                    description="File modification tracking",
                ),
            ]
            created_at: Annotated[
                datetime,
                Field(description="Configuration creation time"),
            ]

        class SandboxConfig(FlextModels.Value):
            """Sandbox configuration - plugin execution sandbox settings.

            Represents security sandbox configuration for plugin execution.
            Immutable value object.

            Attributes:
            plugin_name: Name of plugin to sandbox
            max_memory_mb: Maximum memory in MB
            max_execution_time: Maximum execution time in seconds
            allowed_modules: Allowed import modules
            network_access: Whether network access allowed
            file_system_access: File system access level
            environment_variables: Environment variable settings

            """

            plugin_name: Annotated[str, Field(description="Name of plugin to sandbox")]
            max_memory_mb: Annotated[int, Field(description="Maximum memory in MB")]
            max_execution_time: Annotated[
                int,
                Field(
                    description="Maximum execution time in seconds",
                ),
            ]
            allowed_modules: Annotated[
                list[str],
                Field(
                    description="Allowed import modules",
                ),
            ]
            network_access: Annotated[
                bool,
                Field(description="Whether network access allowed"),
            ]
            file_system_access: Annotated[
                str,
                Field(description="File system access level"),
            ]
            environment_variables: Annotated[
                dict[str, str],
                Field(
                    description="Environment variable settings",
                ),
            ]

        class PluginRegistry(FlextModels.Value):
            """Plugin registry - central plugin registry storage.

            Represents plugin registry with version tracking and plugin entries.
            Immutable value object.

            Attributes:
            version: Registry schema version
            plugins: Dictionary of registered plugins
            last_updated: Last update timestamp
            created_at: Registry creation timestamp

            """

            version: Annotated[str, Field(description="Registry schema version")]
            plugins: Annotated[
                dict[str, t.NormalizedValue],
                Field(
                    default_factory=dict,
                    description="Dictionary of registered plugins",
                ),
            ]
            last_updated: Annotated[
                datetime,
                Field(
                    default_factory=datetime.now,
                    description="Last update timestamp",
                ),
            ]
            created_at: Annotated[
                datetime,
                Field(
                    default_factory=datetime.now,
                    description="Registry creation timestamp",
                ),
            ]

        class PluginConfig(FlextModels.Value):
            """Plugin configuration model.

            Represents configuration for a plugin with key-value pairs.
            """

            plugin_name: Annotated[str, Field(description="Plugin name")]
            settings: Annotated[
                dict[str, t.NormalizedValue],
                Field(
                    default_factory=dict,
                    description="Configuration settings",
                ),
            ]

        class Registry(FlextModels.Value):
            """Plugin registry model.

            Represents a registry of plugins with metadata.
            """

            plugins: Annotated[
                dict[str, t.NormalizedValue],
                Field(
                    default_factory=dict,
                    description="Dictionary of registered plugins",
                ),
            ]
            last_updated: Annotated[
                datetime,
                Field(
                    default_factory=datetime.now,
                    description="Last update timestamp",
                ),
            ]
            created_at: Annotated[
                datetime,
                Field(
                    default_factory=datetime.now,
                    description="Registry creation timestamp",
                ),
            ]


m = FlextPluginModels

__all__ = ["FlextPluginModels", "m"]
