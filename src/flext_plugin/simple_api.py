"""FLEXT Plugin Simple API - Factory functions and convenience methods for plugins.

This module provides simplified factory functions for creating plugin entities,
configurations, and metadata objects. These functions serve as convenience
wrappers around the domain entities, providing sensible defaults and
simplified parameter interfaces for common plugin creation scenarios.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from flext_core import FlextTypes

from flext_plugin.entities import (
    FlextPlugin,
    FlextPluginConfig,
    FlextPluginMetadata,
    FlextPluginRegistry,
)
from flext_plugin.flext_plugin_models import PluginStatus


def create_flext_plugin(
    name: str,
    version: str,
    *,
    config: FlextTypes.Core.Dict | None = None,
) -> FlextPlugin:
    """Create a new FlextPlugin entity with automatic ID generation and timestamps.

    Factory function that creates a properly initialized FlextPlugin domain entity
    with automatic UUID generation and timestamp management. This function provides
    a simplified interface for plugin creation while ensuring all required fields
    are properly initialized and validated.

    """
    config = config or {}
    config["created_at"] = datetime.now(UTC)

    return FlextPlugin.create(
        name=name,
        plugin_version=version,
        entity_id=str(uuid.uuid4()),
        config=config,
    )


def create_flext_plugin_config(
    plugin_name: str,
    config_data: FlextTypes.Core.Dict | None = None,
) -> FlextPluginConfig:
    """Create a new FlextPluginConfig entity.

    Args:
      plugin_name: Name of the plugin this config belongs to
      config_data: Configuration data

    Returns:
      New FlextPluginConfig entity

    """
    return FlextPluginConfig.create(
        plugin_name=plugin_name,
        entity_id=str(uuid.uuid4()),
        config_data=config_data,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )


def create_flext_plugin_metadata(
    plugin_name: str,
    *,
    metadata: FlextTypes.Core.Dict | None = None,
    entry_point: str = "",
) -> FlextPluginMetadata:
    """Create a new FlextPluginMetadata entity.

    Args:
      plugin_name: Name of the plugin this metadata belongs to
      metadata: Metadata dict containing tags, categories, URLs, license info
      entry_point: Plugin entry point (defaults to plugin_name if not provided)

    Returns:
      New FlextPluginMetadata entity

    """
    metadata = metadata or {}
    metadata["created_at"] = datetime.now(UTC)

    # Use plugin_name as entry_point if not provided
    final_entry_point = entry_point or plugin_name

    return FlextPluginMetadata.create(
        name=plugin_name,
        entry_point=final_entry_point,
        entity_id=str(uuid.uuid4()),
        metadata=metadata,
    )


def create_flext_plugin_registry(
    name: str,
    plugins: dict[str, FlextPlugin] | None = None,
) -> FlextPluginRegistry:
    """Create a new FlextPluginRegistry entity.

    Args:
      name: Registry name
      plugins: Dictionary of registered plugins (name -> plugin)

    Returns:
      New FlextPluginRegistry entity

    """
    return FlextPluginRegistry.create(
        name=name,
        entity_id=str(uuid.uuid4()),
        plugins=plugins,
        created_at=datetime.now(UTC),
    )


def create_plugin_from_dict(plugin_data: FlextTypes.Core.Dict) -> FlextPlugin:
    """Create a FlextPlugin entity from dictionary data with comprehensive validation.

    Factory function that creates a FlextPlugin entity from dictionary input,
    providing comprehensive validation and type conversion. This function is
    particularly useful for creating plugins from external data sources such
    as configuration files, API responses, or serialized data.

    """

    # Helper function for validation
    def _handle_value_error(error: str) -> None:
        """Handle value error by raising appropriate exception."""
        raise ValueError(error)

    try:
        # Extract required fields with validation
        name_obj = plugin_data.get("name", "")
        if not name_obj:
            msg = "Plugin name is required"
            _handle_value_error(msg)
        name = str(name_obj)

        version_obj = plugin_data.get("version", "")
        if not version_obj:
            msg = "Plugin version is required"
            _handle_value_error(msg)
        version = str(version_obj)

        # Extract optional fields
        description = str(plugin_data.get("description", ""))
        author = str(plugin_data.get("author", ""))
        dependencies = plugin_data.get("dependencies", [])
        metadata = plugin_data.get("metadata", {})

        # Handle status conversion
        status_str = plugin_data.get("status", "inactive")
        try:
            status = PluginStatus(str(status_str))
        except ValueError:
            status = PluginStatus.INACTIVE

        return create_flext_plugin(
            name=name,
            version=version,
            config={
                "description": description,
                "author": author,
                "dependencies": dependencies,
                "metadata": metadata,
                "status": status,
            },
        )

    except (RuntimeError, ValueError, TypeError) as e:
        error_msg: str = f"Failed to create plugin from dictionary: {e}"
        raise ValueError(error_msg) from e


def create_plugin_config_from_dict(
    plugin_name: str,
    config_dict: FlextTypes.Core.Dict,
) -> FlextPluginConfig:
    """Create a FlextPluginConfig from dictionary data.

    Args:
      plugin_name: Name of the plugin
      config_dict: Dictionary containing configuration data

    Returns:
      New FlextPluginConfig entity

    Raises:
      ValueError: If plugin name is empty

    """
    if not plugin_name:
        msg = "Plugin name is required"
        raise ValueError(msg)

    return create_flext_plugin_config(
        plugin_name=plugin_name,
        config_data=config_dict,
    )


# Backwards compatibility aliases
create_plugin = create_flext_plugin
create_plugin_config = create_flext_plugin_config
create_plugin_metadata = create_flext_plugin_metadata
create_plugin_registry = create_flext_plugin_registry

__all__ = [
    "create_flext_plugin",
    "create_flext_plugin_config",
    "create_flext_plugin_metadata",
    "create_flext_plugin_registry",
    # Legacy aliases
    "create_plugin",
    "create_plugin_config",
    "create_plugin_config_from_dict",
    "create_plugin_from_dict",
    "create_plugin_metadata",
    "create_plugin_registry",
]
