"""FLEXT Plugin Models - Plugin system data models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import types
from collections.abc import (
    Callable,
    Mapping,
)
from datetime import datetime
from pathlib import Path
from typing import Annotated, ClassVar, Self

from flext_cli import m
from flext_core import u

from flext_plugin import c, p, r, t


class FlextPluginModels(m):
    """Plugin domain models extending flext-core patterns.

    Provides standardized models for all plugin operations including plugin
    entities, configurations, execution results, and monitoring data.

    All models inherit flext-core validation and patterns following
    Railway-Oriented Programming with r[T] error handling.
    """

    class Plugin:
        """Plugin domain namespace."""

        class Entity(m.Entity):
            """Entity - real inheritance."""

            _flext_enforcement_exempt: ClassVar[bool] = True

        class Plugin(m.Entity):
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

            _flext_enforcement_exempt: ClassVar[bool] = True

            name: Annotated[
                str,
                u.Field(
                    ...,
                    min_length=c.Plugin.PluginValidation.MIN_PLUGIN_NAME_LENGTH,
                    max_length=c.Plugin.PluginValidation.MAX_PLUGIN_NAME_LENGTH,
                    pattern=c.Plugin.PluginValidation.PLUGIN_NAME_PATTERN,
                    description="Plugin unique identifier name",
                ),
            ]
            plugin_version: Annotated[
                str,
                u.Field(
                    pattern=c.Plugin.PluginValidation.VERSION_PATTERN,
                    description="Plugin semantic version (X.Y.Z)",
                ),
            ] = "1.0.0"
            description: Annotated[
                str,
                u.Field(
                    max_length=c.Plugin.PluginValidation.MAX_DESCRIPTION_LENGTH,
                    description="Plugin functionality description",
                ),
            ] = ""
            author: Annotated[
                str,
                u.Field(
                    max_length=c.Plugin.PluginValidation.MAX_AUTHOR_LENGTH,
                    description="Plugin author/maintainer",
                ),
            ] = ""
            plugin_type: Annotated[
                str,
                u.Field(
                    description="Plugin type classification",
                ),
            ] = c.Plugin.PluginType.UTILITY
            is_enabled: Annotated[bool, u.Field(description="Plugin enabled state")] = (
                True
            )
            metadata: Annotated[
                t.MutableFlatContainerMapping,
                u.Field(
                    description="Extensible plugin metadata",
                ),
            ] = u.Field(default_factory=dict)

            @classmethod
            def create(
                cls,
                *,
                name: str,
                plugin_version: str = "1.0.0",
                description: str = "",
                author: str = "",
                plugin_type: str = c.Plugin.PluginType.UTILITY,
                is_enabled: bool = True,
                metadata: Mapping[str, t.Container] | None = None,
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
                metadata_payload: Mapping[str, t.Container] = (
                    dict(metadata.items()) if metadata else {}
                )
                payload: t.MutableFlatContainerMapping = {
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

            @u.field_validator("plugin_type", mode="before")
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

            @u.field_validator("plugin_version", mode="before")
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

            def disable(self) -> p.Result[bool]:
                """Disable the plugin.

                Returns:
                r[bool] indicating success or failure

                """
                if not self.is_enabled:
                    return r[bool].fail("Plugin is already disabled")
                self.is_enabled = False
                return r[bool].ok(value=True)

            def enable(self) -> p.Result[bool]:
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

                error_count = u.to_int(
                    self.metadata.get("error_count", 0),
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

                exec_count = u.to_int(
                    self.metadata.get("execution_count", 0),
                )
                total_time = u.to_float(
                    self.metadata.get("total_execution_time", 0.0),
                )
                self.metadata["execution_count"] = exec_count + 1
                self.metadata["total_execution_time"] = total_time + execution_time

                if success:
                    success_count = u.to_int(
                        self.metadata.get("success_count", 0),
                    )
                    self.metadata["success_count"] = success_count + 1
                else:
                    failure_count = u.to_int(
                        self.metadata.get("failure_count", 0),
                    )
                    self.metadata["failure_count"] = failure_count + 1

            def validate_business_rules(self) -> p.Result[bool]:
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

        class ExecutionResult(m.Value):
            """Plugin execution result - immutable execution outcome.

            Represents the result of a plugin execution including success status,
            output data, and execution metrics.

            Attributes:
            success: Whether execution succeeded
            data: Execution output data
            error: Error message if execution failed
            execution_time_ms: Execution time in milliseconds

            """

            _flext_enforcement_exempt: ClassVar[bool] = True

            success: Annotated[bool, u.Field(description="Whether execution succeeded")]
            data: Annotated[
                Mapping[str, t.Container],
                u.Field(
                    description="Execution output data",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))
            error: Annotated[
                str,
                u.Field(
                    description="Error message if execution failed",
                ),
            ] = ""
            execution_time_ms: Annotated[
                t.NonNegativeFloat,
                u.Field(
                    description="Execution time in milliseconds",
                ),
            ] = 0.0

        class DiscoveryData(m.Value):
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
                u.Field(
                    min_length=c.Plugin.PluginValidation.MIN_PLUGIN_NAME_LENGTH,
                    max_length=c.Plugin.PluginValidation.MAX_PLUGIN_NAME_LENGTH,
                    pattern=c.Plugin.PluginValidation.PLUGIN_NAME_PATTERN,
                    description="Plugin unique identifier name",
                ),
            ]
            version: Annotated[
                str,
                u.Field(
                    pattern=c.Plugin.PluginValidation.VERSION_PATTERN,
                    description="Plugin semantic version (X.Y.Z)",
                ),
            ]
            path: Annotated[Path, u.Field(description="File system path to plugin")]
            discovery_type: Annotated[
                c.Plugin.DiscoveryTypeLiteral,
                u.Field(
                    description="Type of discovered plugin",
                ),
            ]
            discovery_method: Annotated[
                c.Plugin.DiscoveryMethodLiteral,
                u.Field(
                    description="Discovery method used",
                ),
            ]
            metadata: Annotated[
                Mapping[str, t.Container],
                u.Field(
                    description="Extensible discovery metadata",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))

            @u.field_validator("version", mode="before")
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

        class LoadData(m.Value):
            """Plugin load data - immutable load result.

            Represents successfully loaded plugin information including the loaded
            module t.Container and load metadata. Immutable value object.

            Attributes:
            name: Plugin unique identifier name
            version: Plugin semantic version
            path: File system path to plugin
            module: The loaded Python module t.Container
            load_type: Type of loaded plugin (file, directory, entry_point)
            loaded_at: Timestamp when plugin was loaded
            entry_file: Entry file path for directory-based plugins

            """

            name: Annotated[
                str,
                u.Field(
                    min_length=c.Plugin.PluginValidation.MIN_PLUGIN_NAME_LENGTH,
                    max_length=c.Plugin.PluginValidation.MAX_PLUGIN_NAME_LENGTH,
                    description="Plugin unique identifier name",
                ),
            ]
            version: Annotated[
                str,
                u.Field(
                    pattern=c.Plugin.PluginValidation.VERSION_PATTERN,
                    description="Plugin semantic version (X.Y.Z)",
                ),
            ]
            path: Annotated[Path, u.Field(description="File system path to plugin")]
            module: Annotated[
                types.ModuleType,
                u.Field(
                    description="The loaded Python module t.Container",
                ),
            ]
            load_type: Annotated[
                c.Plugin.LoadTypeLiteral,
                u.Field(
                    description="Type of loaded plugin",
                ),
            ]
            loaded_at: Annotated[
                datetime,
                u.Field(description="Timestamp when plugin was loaded"),
            ]
            entry_file: Annotated[
                Path | None,
                u.Field(
                    description="Entry file path for directory-based plugins",
                ),
            ] = None

        class ReloadRecord(m.Value):
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

            plugin_name: Annotated[str, u.Field(description="Name of reloaded plugin")]
            plugin_path: Annotated[Path, u.Field(description="Path to reloaded plugin")]
            timestamp: Annotated[datetime, u.Field(description="When reload occurred")]
            success: Annotated[bool, u.Field(description="Whether reload succeeded")]
            error: Annotated[
                str | None,
                u.Field(
                    description="Error message if reload failed",
                ),
            ] = None
            duration_ms: Annotated[
                t.NonNegativeFloat,
                u.Field(
                    description="Reload duration in milliseconds",
                ),
            ] = 0.0

        class PluginMetadata(m.Value):
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

            name: Annotated[str, u.Field(description="Plugin unique identifier")]
            version: Annotated[str, u.Field(description="Plugin semantic version")]
            description: Annotated[str, u.Field(description="Plugin description")] = ""
            author: Annotated[str, u.Field(description="Plugin author")] = "Unknown"
            plugin_type: Annotated[str, u.Field(description="Type of plugin")] = (
                "extension"
            )
            entry_point: Annotated[str, u.Field(description="Entry point for plugin")]
            dependencies: Annotated[
                t.StrSequence,
                u.Field(
                    description="List of plugin dependencies",
                ),
            ] = u.Field(default_factory=tuple)
            metadata: Annotated[
                Mapping[str, t.Container],
                u.Field(
                    description="Additional metadata",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))

        class EventData(m.Value):
            """Event data - immutable event information.

            Represents structured event data with context and metadata.
            Immutable value object.

            Attributes:
            event_type: Type of event
            plugin_name: Associated plugin name
            timestamp: When event occurred
            data: Event-specific data

            """

            event_type: Annotated[str, u.Field(description="Type of event")]
            plugin_name: Annotated[str, u.Field(description="Associated plugin name")]
            timestamp: Annotated[datetime, u.Field(description="When event occurred")]
            data: Annotated[
                Mapping[str, t.Container],
                u.Field(
                    description="Event-specific data",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))

        class ValidationResult(m.Value):
            """Validation result - immutable validation outcome.

            Represents result of plugin validation including status and details.
            Immutable value object.

            Attributes:
            valid: Whether validation passed
            errors: List of validation errors
            warnings: List of validation warnings
            details: Additional validation details

            """

            _flext_enforcement_exempt: ClassVar[bool] = True

            valid: Annotated[bool, u.Field(description="Whether validation passed")]
            errors: Annotated[
                t.StrSequence,
                u.Field(
                    description="List of validation errors",
                ),
            ] = u.Field(default_factory=tuple)
            warnings: Annotated[
                t.StrSequence,
                u.Field(
                    description="List of validation warnings",
                ),
            ] = u.Field(default_factory=tuple)
            details: Annotated[
                Mapping[str, t.Container],
                u.Field(
                    description="Additional validation details",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))

        class SecurityReport(m.Value):
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
                u.Field(description="Whether plugin passed security checks"),
            ]
            violations: Annotated[
                t.StrSequence,
                u.Field(
                    description="List of security violations",
                ),
            ] = u.Field(default_factory=tuple)
            warnings: Annotated[
                t.StrSequence,
                u.Field(
                    description="List of security warnings",
                ),
            ] = u.Field(default_factory=tuple)
            analysis_time: Annotated[
                datetime,
                u.Field(description="When analysis was performed"),
            ]

        class WatcherConfig(m.Value):
            """Watcher configuration - file system monitoring settings.

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

            watch_path: Annotated[str, u.Field(description="Path being watched")]
            watch_interval: Annotated[
                t.PositiveFloat,
                u.Field(description="Polling interval in seconds"),
            ]
            callback: Annotated[
                Callable[..., t.Container] | None,
                u.Field(
                    description="Callback function reference",
                ),
            ] = None
            active: Annotated[
                bool, u.Field(description="Whether watcher is active")
            ] = False
            last_modified: Annotated[
                Mapping[str, t.Container],
                u.Field(
                    description="File modification tracking",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))
            created_at: Annotated[
                datetime,
                u.Field(description="Configuration creation time"),
            ]

        class SandboxConfig(m.Value):
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

            plugin_name: Annotated[
                str, u.Field(description="Name of plugin to sandbox")
            ]
            max_memory_mb: Annotated[
                t.PositiveInt,
                u.Field(description="Maximum memory in MB"),
            ]
            max_execution_time: Annotated[
                t.PositiveInt,
                u.Field(
                    description="Maximum execution time in seconds",
                ),
            ]
            allowed_modules: Annotated[
                t.StrSequence,
                u.Field(
                    description="Allowed import modules",
                ),
            ]
            network_access: Annotated[
                bool,
                u.Field(description="Whether network access allowed"),
            ]
            file_system_access: Annotated[
                str,
                u.Field(description="File system access level"),
            ]
            environment_variables: Annotated[
                t.StrMapping,
                u.Field(
                    description="Environment variable settings",
                ),
            ]

        class PluginRegistry(m.Value):
            """Plugin registry - central plugin registry storage.

            Represents plugin registry with version tracking and plugin entries.
            Immutable value object.

            Attributes:
            version: Registry schema version
            plugins: Dictionary of registered plugins
            last_updated: Last update timestamp
            created_at: Registry creation timestamp

            """

            version: Annotated[str, u.Field(description="Registry schema version")]
            plugins: Annotated[
                Mapping[str, t.Container],
                u.Field(
                    description="Dictionary of registered plugins",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))
            last_updated: Annotated[
                datetime,
                u.Field(
                    description="Last update timestamp",
                ),
            ] = u.Field(default_factory=datetime.now)
            created_at: Annotated[
                datetime,
                u.Field(
                    description="Registry creation timestamp",
                ),
            ] = u.Field(default_factory=datetime.now)

        class PluginConfig(m.Value):
            """Plugin configuration model.

            Represents configuration for a plugin with key-value pairs.
            """

            plugin_name: Annotated[str, u.Field(description="Plugin name")]
            config: Annotated[
                Mapping[str, t.Container],
                u.Field(
                    description="Configuration settings",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))

        class Registry(m.Value):
            """Plugin registry model.

            Represents a registry of plugins with metadata.
            """

            plugins: Annotated[
                Mapping[str, t.Container],
                u.Field(
                    description="Dictionary of registered plugins",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))
            last_updated: Annotated[
                datetime,
                u.Field(
                    description="Last update timestamp",
                ),
            ] = u.Field(default_factory=datetime.now)
            created_at: Annotated[
                datetime,
                u.Field(
                    description="Registry creation timestamp",
                ),
            ] = u.Field(default_factory=datetime.now)


m = FlextPluginModels

__all__: list[str] = ["FlextPluginModels", "m"]
