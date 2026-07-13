"""FLEXT Plugin Models - Plugin system data models.

from flext_plugin import u
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import types
from datetime import datetime
from pathlib import Path
from typing import Annotated, Self

from flext_cli import m, u
from flext_plugin import c, p, t


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
            ] = c.Plugin.DEFAULT_PLUGIN_VERSION
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
                """Create an entity validated by the entity contract itself."""
                payload: t.MutableMappingKV[str, p.AttributeProbe] = dict(kwargs)
                entity_id = payload.pop("entity_id", None)
                if entity_id is not None and "unique_id" not in payload:
                    payload["unique_id"] = entity_id
                payload["metadata"] = t.json_mapping_adapter().validate_python(
                    payload.get("metadata") or {},
                )
                entity: Self = cls.model_validate(payload)
                return entity

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
                t.JsonMapping,
                u.Field(
                    description="Additional metadata",
                ),
            ] = u.Field(default_factory=lambda: types.MappingProxyType({}))

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


m = FlextPluginModels

__all__: list[str] = ["FlextPluginModels", "m"]
