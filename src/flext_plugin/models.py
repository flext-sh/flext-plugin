"""FLEXT Plugin Models - Plugin system data models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal, Self

from flext_core import FlextModels, FlextResult
from pydantic import Field, field_validator

from flext_plugin.constants import FlextPluginConstants


class FlextPluginModels:
    """Plugin domain models extending flext-core patterns.

    Provides standardized models for all plugin operations including plugin
    entities, configurations, execution results, and monitoring data.

    All models inherit flext-core validation and patterns following
    Railway-Oriented Programming with FlextResult[T] error handling.
    """

    # Re-export PluginType enum from constants for convenience
    class PluginType(FlextPluginConstants.PluginType):
        """PluginType - real inheritance."""

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

        name: str = Field(
            ...,
            min_length=FlextPluginConstants.PluginValidation.MIN_PLUGIN_NAME_LENGTH,
            max_length=FlextPluginConstants.PluginValidation.MAX_PLUGIN_NAME_LENGTH,
            pattern=FlextPluginConstants.PluginValidation.PLUGIN_NAME_PATTERN,
            description="Plugin unique identifier name",
        )
        plugin_version: str = Field(
            default="1.0.0",
            pattern=FlextPluginConstants.PluginValidation.VERSION_PATTERN,
            description="Plugin semantic version (X.Y.Z)",
        )
        description: str = Field(
            default="",
            max_length=FlextPluginConstants.PluginValidation.MAX_DESCRIPTION_LENGTH,
            description="Plugin functionality description",
        )
        author: str = Field(
            default="",
            max_length=FlextPluginConstants.PluginValidation.MAX_AUTHOR_LENGTH,
            description="Plugin author/maintainer",
        )
        plugin_type: str = Field(
            default=FlextPluginConstants.PluginType.UTILITY,
            description="Plugin type classification",
        )
        is_enabled: bool = Field(default=True, description="Plugin enabled state")
        metadata: dict[str, object] = Field(
            default_factory=dict,
            description="Extensible plugin metadata",
        )

        @field_validator("plugin_version", mode="before")
        @classmethod
        def validate_semantic_version(cls, value: str) -> str:
            """Validate semantic version format (X.Y.Z)."""
            min_version_parts = 2
            max_version_parts = 3
            if isinstance(value, str):
                parts = value.split(".")
                if (
                    len(parts) < min_version_parts
                    or len(parts) > max_version_parts
                    or not all(p.isdigit() for p in parts if p)
                ):
                    error_msg = f"Version must be semantic format X.Y.Z, got: {value}"
                    raise ValueError(error_msg)
            return value

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

        @classmethod
        def create(
            cls,
            *,
            name: str,
            plugin_version: str = "1.0.0",
            description: str = "",
            author: str = "",
            plugin_type: str = FlextPluginConstants.PluginType.UTILITY,
            is_enabled: bool = True,
            metadata: dict[str, object] | None = None,
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
            return cls(
                id=entity_id,
                name=name,
                plugin_version=plugin_version,
                description=description,
                author=author,
                plugin_type=plugin_type,
                is_enabled=is_enabled,
                metadata=metadata or {},
            )

        def enable(self) -> FlextResult[None]:
            """Enable the plugin.

            Returns:
            FlextResult indicating success or failure

            """
            if self.is_enabled:
                return FlextResult.fail("Plugin is already enabled")
            self.is_enabled = True
            return FlextResult.ok(None)

        def disable(self) -> FlextResult[None]:
            """Disable the plugin.

            Returns:
            FlextResult indicating success or failure

            """
            if not self.is_enabled:
                return FlextResult.fail("Plugin is already disabled")
            self.is_enabled = False
            return FlextResult.ok(None)

        def record_execution(self, execution_time: float, success: bool) -> None:
            """Record plugin execution metrics.

            Args:
                execution_time: Time taken for execution in seconds
                success: Whether the execution was successful

            """
            # Update metadata with execution info
            if "execution_count" not in self.metadata:
                self.metadata["execution_count"] = 0
            if "total_execution_time" not in self.metadata:
                self.metadata["total_execution_time"] = 0.0
            if "success_count" not in self.metadata:
                self.metadata["success_count"] = 0
            if "failure_count" not in self.metadata:
                self.metadata["failure_count"] = 0

            self.metadata["execution_count"] += 1
            self.metadata["total_execution_time"] += execution_time
            if success:
                self.metadata["success_count"] += 1
            else:
                self.metadata["failure_count"] += 1

        def record_error(self, error_message: str) -> None:
            """Record plugin error.

            Args:
                error_message: Error message to record

            """
            if "error_count" not in self.metadata:
                self.metadata["error_count"] = 0
            if "last_error" not in self.metadata:
                self.metadata["last_error"] = ""

            self.metadata["error_count"] += 1
            self.metadata["last_error"] = error_message

        def activate(self) -> bool:
            """Activate the plugin (legacy method).

            Returns:
                True if activated, False if already active

            """
            if self.is_enabled:
                return False
            self.is_enabled = True
            return True

        def deactivate(self) -> bool:
            """Deactivate the plugin (legacy method).

            Returns:
                True if deactivated, False if already inactive

            """
            if not self.is_enabled:
                return False
            self.is_enabled = False
            return True

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate plugin business rules.

            Business Rules:
            - Plugin name must not be empty
            - Plugin version must follow semantic versioning (X.Y.Z)
            - Plugin type must be valid

            Returns:
            FlextResult indicating validation success or failure

            """
            min_version_parts = 2
            max_version_parts = 3
            if not self.name or not self.name.strip():
                return FlextResult.fail("Plugin name cannot be empty")

            # Validate semantic version
            version_parts = self.plugin_version.split(".")
            if (
                len(version_parts) < min_version_parts
                or len(version_parts) > max_version_parts
            ):
                return FlextResult.fail(
                    f"Invalid semantic version: {self.plugin_version}",
                )
            if not all(part.isdigit() for part in version_parts if part):
                return FlextResult.fail(
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
                return FlextResult.fail(f"Invalid plugin type: {self.plugin_type}")

            return FlextResult.ok(None)

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

        success: bool = Field(description="Whether execution succeeded")
        data: dict[str, object] = Field(
            default_factory=dict,
            description="Execution output data",
        )
        error: str = Field(
            default="",
            description="Error message if execution failed",
        )
        execution_time_ms: float = Field(
            default=0.0,
            ge=0,
            description="Execution time in milliseconds",
        )

    class DiscoveryData(FlextModels.Value):
        """Plugin discovery data - immutable discovery result.

        Represents discovered plugin information from various discovery methods
        (file system, entry points, etc.). Immutable value object.

        Attributes:
        name: Plugin unique identifier name
        version: Plugin semantic version (X.Y.Z)
        path: File system path to plugin
        discovery_type: Type of discovered plugin (file, directory, entry_point)
        discovery_method: Discovery method used (file_system, entry_points)
        metadata: Extensible discovery metadata

        """

        name: str = Field(
            min_length=FlextPluginConstants.PluginValidation.MIN_PLUGIN_NAME_LENGTH,
            max_length=FlextPluginConstants.PluginValidation.MAX_PLUGIN_NAME_LENGTH,
            pattern=FlextPluginConstants.PluginValidation.PLUGIN_NAME_PATTERN,
            description="Plugin unique identifier name",
        )
        version: str = Field(
            pattern=FlextPluginConstants.PluginValidation.VERSION_PATTERN,
            description="Plugin semantic version (X.Y.Z)",
        )
        path: Path = Field(description="File system path to plugin")
        discovery_type: Literal["file", "directory", "entry_point"] = Field(
            description="Type of discovered plugin",
        )
        discovery_method: Literal["file_system", "entry_points"] = Field(
            description="Discovery method used",
        )
        metadata: dict[str, object] = Field(
            default_factory=dict,
            description="Extensible discovery metadata",
        )

        @field_validator("version", mode="before")
        @classmethod
        def validate_version(cls, value: str) -> str:
            """Validate semantic version format."""
            min_parts = 2
            max_parts = 3
            if isinstance(value, str):
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

        name: str = Field(
            min_length=FlextPluginConstants.PluginValidation.MIN_PLUGIN_NAME_LENGTH,
            max_length=FlextPluginConstants.PluginValidation.MAX_PLUGIN_NAME_LENGTH,
            description="Plugin unique identifier name",
        )
        version: str = Field(
            pattern=FlextPluginConstants.PluginValidation.VERSION_PATTERN,
            description="Plugin semantic version (X.Y.Z)",
        )
        path: Path = Field(description="File system path to plugin")
        module: Any = Field(description="The loaded Python module object")
        load_type: Literal["file", "directory", "entry_point"] = Field(
            description="Type of loaded plugin",
        )
        loaded_at: datetime = Field(description="Timestamp when plugin was loaded")
        entry_file: Path | None = Field(
            default=None,
            description="Entry file path for directory-based plugins",
        )

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

        plugin_name: str = Field(description="Name of reloaded plugin")
        plugin_path: Path = Field(description="Path to reloaded plugin")
        timestamp: datetime = Field(description="When reload occurred")
        success: bool = Field(description="Whether reload succeeded")
        error: str | None = Field(
            default=None,
            description="Error message if reload failed",
        )
        duration_ms: float = Field(
            default=0.0,
            ge=0,
            description="Reload duration in milliseconds",
        )

    class PluginMetadata(FlextModels.Value):
        """Plugin metadata - immutable metadata value object.

        Represents complete metadata about a plugin including discovery
        and description information. Immutable value object.

        Attributes:
        name: Plugin unique identifier
        version: Plugin semantic version
        description: Plugin description
        author: Plugin author
        plugin_type: Type of plugin (extension, transformer, etc.)
        entry_point: Entry point for plugin
        dependencies: List of plugin dependencies
        metadata: Additional metadata dictionary

        """

        name: str = Field(description="Plugin unique identifier")
        version: str = Field(description="Plugin semantic version")
        description: str = Field(default="", description="Plugin description")
        author: str = Field(default="Unknown", description="Plugin author")
        plugin_type: str = Field(default="extension", description="Type of plugin")
        entry_point: str = Field(description="Entry point for plugin")
        dependencies: list[str] = Field(
            default_factory=list,
            description="List of plugin dependencies",
        )
        metadata: dict[str, object] = Field(
            default_factory=dict,
            description="Additional metadata",
        )

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

        event_type: str = Field(description="Type of event")
        plugin_name: str = Field(description="Associated plugin name")
        timestamp: datetime = Field(description="When event occurred")
        data: dict[str, object] = Field(
            default_factory=dict,
            description="Event-specific data",
        )

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

        is_valid: bool = Field(description="Whether validation passed")
        errors: list[str] = Field(
            default_factory=list,
            description="List of validation errors",
        )
        warnings: list[str] = Field(
            default_factory=list,
            description="List of validation warnings",
        )
        details: dict[str, object] = Field(
            default_factory=dict,
            description="Additional validation details",
        )

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

        is_safe: bool = Field(description="Whether plugin passed security checks")
        violations: list[str] = Field(
            default_factory=list,
            description="List of security violations",
        )
        warnings: list[str] = Field(
            default_factory=list,
            description="List of security warnings",
        )
        analysis_time: datetime = Field(description="When analysis was performed")

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

        watch_path: str = Field(description="Path being watched")
        watch_interval: float = Field(description="Polling interval in seconds")
        callback: Any = Field(default=None, description="Callback function reference")
        active: bool = Field(default=False, description="Whether watcher is active")
        last_modified: dict[str, object] = Field(
            default_factory=dict,
            description="File modification tracking",
        )
        created_at: datetime = Field(description="Configuration creation time")

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

        plugin_name: str = Field(description="Name of plugin to sandbox")
        max_memory_mb: int = Field(description="Maximum memory in MB")
        max_execution_time: int = Field(description="Maximum execution time in seconds")
        allowed_modules: list[str] = Field(
            description="Allowed import modules",
        )
        network_access: bool = Field(description="Whether network access allowed")
        file_system_access: str = Field(description="File system access level")
        environment_variables: dict[str, str] = Field(
            description="Environment variable settings",
        )

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

        version: str = Field(description="Registry schema version")
        plugins: dict[str, object] = Field(
            default_factory=dict,
            description="Dictionary of registered plugins",
        )
        last_updated: datetime = Field(
            default_factory=datetime.now,
            description="Last update timestamp",
        )
        created_at: datetime = Field(
            default_factory=datetime.now,
            description="Registry creation timestamp",
        )

    class Config(FlextModels.Value):
        """Plugin configuration model.

        Represents configuration for a plugin with key-value pairs.
        """

        plugin_name: str = Field(description="Plugin name")
        settings: dict[str, object] = Field(
            default_factory=dict,
            description="Configuration settings",
        )

    class Registry(FlextModels.Value):
        """Plugin registry model.

        Represents a registry of plugins with metadata.
        """

        plugins: dict[str, object] = Field(
            default_factory=dict,
            description="Dictionary of registered plugins",
        )
        last_updated: datetime = Field(
            default_factory=datetime.now,
            description="Last update timestamp",
        )
        created_at: datetime = Field(
            default_factory=datetime.now,
            description="Registry creation timestamp",
        )


__all__ = ["FlextPluginModels"]
