"""FLEXT Plugin Metadata Entity - Plugin metadata domain entity.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime

from flext_core import FlextModels, FlextResult, FlextUtilities
from pydantic import Field, field_validator


class PluginMetadata(FlextModels.Entity):
    """Plugin metadata entity containing additional plugin information."""

    # Pydantic fields for the entity
    plugin_name: str = Field(
        default="",
        description="Name of the plugin this metadata belongs to",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Plugin tags for categorization",
    )
    categories: list[str] = Field(
        default_factory=list,
        description="Plugin categories",
    )
    homepage_url: str = Field(default="", description="Plugin homepage URL")
    documentation_url: str = Field(default="", description="Plugin documentation URL")
    repository_url: str = Field(default="", description="Plugin repository URL")
    license_info: str = Field(default="", description="Plugin license information")

    # Additional fields for testing convenience
    name: str = Field(min_length=1, description="Plugin name (alias for plugin_name)")
    entry_point: str = Field(min_length=1, description="Plugin entry point")
    plugin_type: str = Field(default="", description="Plugin type")
    description: str = Field(default="", description="Plugin description")
    dependencies: list[str] = Field(
        default_factory=list,
        description="Plugin dependencies",
    )
    trusted: bool = Field(default=False, description="Whether plugin is trusted")
    homepage: str | None = Field(default=None, description="Plugin homepage (alias)")
    repository: str | None = Field(
        default=None,
        description="Plugin repository (alias)",
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Metadata creation timestamp",
    )

    @classmethod
    def create(
        cls,
        *,
        name: str,
        entry_point: str,
        entity_id: str | None = None,
        **kwargs: object,
    ) -> PluginMetadata:
        """Create plugin metadata entity with proper validation."""
        entity_id = entity_id or FlextUtilities.Generators.generate_entity_id()

        # Create instance data
        instance_data: dict[str, object] = {
            "id": entity_id,
            "version": kwargs.get("version", 1),
            "metadata": kwargs.get("entity_metadata", {}),
            "plugin_name": name,
            "name": name,
            "entry_point": entry_point,
            "plugin_type": kwargs.get("plugin_type", ""),
            "description": kwargs.get("description", ""),
            "dependencies": kwargs.get("dependencies", []),
            "trusted": kwargs.get("trusted", False),
            "homepage": kwargs.get("homepage"),
            "repository": kwargs.get("repository"),
            "tags": kwargs.get("tags", []),
            "categories": kwargs.get("categories", []),
            "homepage_url": kwargs.get("homepage_url", ""),
            "documentation_url": kwargs.get("documentation_url", ""),
            "repository_url": kwargs.get("repository_url", ""),
            "license_info": kwargs.get("license_info", ""),
        }

        return cls.model_validate(instance_data)

    @field_validator("name")
    @classmethod
    def validate_name_not_empty(cls, v: str) -> str:
        """Validate that name is not empty."""
        if not v or not v.strip():
            msg = "Plugin name cannot be empty"
            raise ValueError(msg)
        return v

    @field_validator("entry_point")
    @classmethod
    def validate_entry_point_not_empty(cls, v: str) -> str:
        """Validate that entry_point is not empty when provided."""
        if v and not v.strip():
            msg = "Plugin entry point cannot be empty"
            raise ValueError(msg)
        return v

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin metadata entity."""
        if not self.plugin_name or not self.plugin_name.strip():
            return FlextResult[None].fail("Plugin name is required and cannot be empty")
        if not self.name or not self.name.strip():
            return FlextResult[None].fail(
                "Plugin name field is required and cannot be empty",
            )
        if not self.entry_point or not self.entry_point.strip():
            return FlextResult[None].fail(
                "Plugin entry point is required and cannot be empty",
            )
        return FlextResult[None].ok(None)


__all__ = ["PluginMetadata"]
