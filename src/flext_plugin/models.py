"""FLEXT Plugin Models - Plugin system data models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import types
from datetime import datetime
from pathlib import Path
from typing import Annotated, Self

from flext_cli import FlextCliModels, u
from flext_plugin import c, p, r, t


class FlextPluginModels(FlextCliModels):
    """Plugin domain models extending flext-core patterns.

    Provides standardized models for all plugin operations including plugin
    entities, configurations, execution results, and monitoring data.

    All models inherit flext-core validation and patterns following
    Railway-Oriented Programming with r[T] error handling.
    """

    class Plugin:
        """Plugin domain namespace."""

        class Entity(FlextCliModels.Entity):
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
                c.Plugin.Type,
                u.Field(
                    description="Plugin type classification",
                ),
            ] = c.Plugin.Type.UTILITY
            is_enabled: Annotated[bool, u.Field(description="Plugin enabled state")] = (
                True
            )
            metadata: Annotated[
                t.JsonMapping,
                u.Field(
                    description="Extensible plugin metadata",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))

            @classmethod
            def create(cls, **kwargs: p.AttributeProbe) -> Self:
                """Factory method validated by the entity contract itself."""
                payload: dict[str, p.AttributeProbe] = dict(kwargs)
                entity_id = payload.pop("entity_id", None)
                if entity_id is not None and "unique_id" not in payload:
                    payload["unique_id"] = entity_id
                payload["metadata"] = t.json_mapping_adapter().validate_python(
                    payload.get("metadata") or {},
                )
                return cls.model_validate(payload)

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
                metadata = dict(self.metadata)
                if "error_count" not in metadata:
                    metadata["error_count"] = 0
                if "last_error" not in metadata:
                    metadata["last_error"] = ""
                error_count = u.to_int(
                    metadata.get("error_count", 0),
                )
                metadata["error_count"] = error_count + 1
                metadata["last_error"] = error_message
                self.metadata = t.json_mapping_adapter().validate_python(
                    metadata,
                )

            def record_execution(self, execution_time: float, *, success: bool) -> None:
                """Record plugin execution metrics.

                Args:
                    execution_time: Time taken for execution in seconds
                    success: Whether the execution was successful

                """
                metadata = dict(self.metadata)
                if "execution_count" not in metadata:
                    metadata["execution_count"] = 0
                if "total_execution_time" not in metadata:
                    metadata["total_execution_time"] = 0.0
                if "success_count" not in metadata:
                    metadata["success_count"] = 0
                if "failure_count" not in metadata:
                    metadata["failure_count"] = 0

                exec_count = u.to_int(
                    metadata.get("execution_count", 0),
                )
                total_time = u.to_float(
                    metadata.get("total_execution_time", 0.0),
                )
                metadata["execution_count"] = exec_count + 1
                metadata["total_execution_time"] = total_time + execution_time

                if success:
                    success_count = u.to_int(
                        metadata.get("success_count", 0),
                    )
                    metadata["success_count"] = success_count + 1
                else:
                    failure_count = u.to_int(
                        metadata.get("failure_count", 0),
                    )
                    metadata["failure_count"] = failure_count + 1

                self.metadata = t.json_mapping_adapter().validate_python(
                    metadata,
                )

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

                # Plugin type validity is enforced by Pydantic via c.Plugin.Type StrEnum.
                return r[bool].ok(value=True)

        class DiscoveryData(FlextCliModels.Value):
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
                t.JsonMapping,
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

        class PluginMetadata(FlextCliModels.Value):
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
                t.JsonMapping,
                u.Field(
                    description="Additional metadata",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))

        class PluginRegistry(FlextCliModels.Value):
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
                t.JsonMapping,
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


m: type[FlextPluginModels] = FlextPluginModels

__all__: list[str] = ["FlextPluginModels", "m"]
