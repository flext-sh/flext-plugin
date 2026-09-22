"""Plugin domain models for flext-plugin.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Annotated

from flext_cli import m as cli_m, u as cli_u

from flext_plugin import t


class FlextPluginModelsPlugin:
    """Canonical namespace owner.

    Plugin domain models namespace.

    All plugin-specific Pydantic models are organized here for better
    namespace organization and to enable composition with other domain models.
    """

    class Entity(cli_m.Entity):
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
            cli_u.Field(
                ...,
                min_length=3,
                max_length=100,
                pattern="^[a-zA-Z][a-zA-Z0-9_-]*$",
                description="Plugin unique identifier name",
            ),
        ]
        plugin_version: Annotated[
            str,
            cli_u.Field(
                pattern=r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$",
                description="Plugin semantic version (X.Y.Z)",
            ),
        ] = "1.0.0"
        description: Annotated[
            str,
            cli_u.Field(
                max_length=1000, description="Plugin functionality description"
            ),
        ] = ""
        author: Annotated[
            str, cli_u.Field(max_length=200, description="Plugin author/maintainer")
        ] = ""
        plugin_type: Annotated[
            str, cli_u.Field(description="Plugin type classification")
        ] = "utility"
        is_enabled: Annotated[bool, cli_u.Field(description="Plugin enabled state")] = (
            True
        )
        metadata: Annotated[
            t.JsonMapping, cli_u.Field(description="Extensible plugin metadata")
        ] = cli_u.Field(default_factory=dict)

        @cli_u.field_validator("plugin_version", mode="before")
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

    class DiscoveryData(cli_m.Value):
        """Plugin discovery data - immutable discovery result.

        Represents discovered plugin information from various discovery methods
        (file system, entry points). Immutable value object.

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
            cli_u.Field(
                min_length=3,
                max_length=100,
                pattern="^[a-zA-Z][a-zA-Z0-9_-]*$",
                description="Plugin unique identifier name",
            ),
        ]
        version: Annotated[
            str,
            cli_u.Field(
                pattern=r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$",
                description="Plugin semantic version (X.Y.Z)",
            ),
        ]
        path: Annotated[Path, cli_u.Field(description="File system path to plugin")]
        discovery_type: Annotated[
            str, cli_u.Field(description="Type of discovered plugin")
        ]
        discovery_method: Annotated[
            str, cli_u.Field(description="Discovery method used")
        ]
        metadata: Annotated[
            t.JsonMapping, cli_u.Field(description="Extensible discovery metadata")
        ] = cli_u.Field(default_factory=dict)

        @cli_u.field_validator("version", mode="before")
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

    class Metadata(cli_m.Value):
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

        name: Annotated[str, cli_u.Field(description="Plugin unique identifier")]
        version: Annotated[str, cli_u.Field(description="Plugin semantic version")]
        description: Annotated[str, cli_u.Field(description="Plugin description")] = ""
        author: Annotated[str, cli_u.Field(description="Plugin author")] = "Unknown"
        plugin_type: Annotated[str, cli_u.Field(description="Type of plugin")] = (
            "extension"
        )
        entry_point: Annotated[str, cli_u.Field(description="Entry point for plugin")]
        dependencies: Annotated[
            t.VariadicTuple[str], cli_u.Field(description="List of plugin dependencies")
        ] = cli_u.Field(default_factory=tuple)
        metadata: Annotated[
            t.JsonMapping, cli_u.Field(description="Additional metadata")
        ] = cli_u.Field(default_factory=dict)

    class Registry(cli_m.Value):
        """Plugin registry - central plugin registry storage.

        Represents plugin registry with version tracking and plugin entries.
        Immutable value object.

        Attributes:
        version: Registry schema version
        plugins: Dictionary of registered plugins
        last_updated: Last update timestamp
        created_at: Registry creation timestamp

        """

        version: Annotated[str, cli_u.Field(description="Registry schema version")]
        plugins: Annotated[
            t.JsonMapping, cli_u.Field(description="Dictionary of registered plugins")
        ] = cli_u.Field(default_factory=dict)
        last_updated: Annotated[
            datetime, cli_u.Field(description="Last update timestamp")
        ] = cli_u.Field(default_factory=datetime.now)
        created_at: Annotated[
            datetime, cli_u.Field(description="Registry creation timestamp")
        ] = cli_u.Field(default_factory=datetime.now)


__all__: list[str] = ["FlextPluginModelsPlugin"]
