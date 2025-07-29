"""FLEXT Plugin Simple API - Factory functions for easy plugin creation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Simple factory functions for creating plugin entities and configurations.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from flext_plugin.domain.entities import (
    FlextPlugin,
    FlextPluginConfig,
    FlextPluginMetadata,
    FlextPluginRegistry,
    PluginStatus,
)


def create_flext_plugin(
    name: str,
    version: str,
    description: str = "",
    author: str = "",
    dependencies: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
    status: PluginStatus = PluginStatus.INACTIVE,
) -> FlextPlugin:
    """Create a new FlextPlugin entity.

    Args:
        name: Plugin name
        version: Plugin version
        description: Plugin description
        author: Plugin author
        dependencies: List of plugin dependencies
        metadata: Additional plugin metadata
        status: Plugin status

    Returns:
        New FlextPlugin entity

    """
    return FlextPlugin(
        entity_id=str(uuid.uuid4()),
        name=name,
        version=version,
        description=description,
        author=author,
        dependencies=dependencies,
        metadata=metadata,
        status=status,
        created_at=datetime.now(),
    )


def create_flext_plugin_config(
    plugin_name: str,
    config_data: dict[str, Any] | None = None,
) -> FlextPluginConfig:
    """Create a new FlextPluginConfig entity.

    Args:
        plugin_name: Name of the plugin this config belongs to
        config_data: Configuration data

    Returns:
        New FlextPluginConfig entity

    """
    return FlextPluginConfig(
        entity_id=str(uuid.uuid4()),
        plugin_name=plugin_name,
        config_data=config_data,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def create_flext_plugin_metadata(
    plugin_name: str,
    tags: list[str] | None = None,
    categories: list[str] | None = None,
    homepage_url: str = "",
    documentation_url: str = "",
    repository_url: str = "",
    license_info: str = "",
) -> FlextPluginMetadata:
    """Create a new FlextPluginMetadata entity.

    Args:
        plugin_name: Name of the plugin this metadata belongs to
        tags: Plugin tags
        categories: Plugin categories
        homepage_url: Plugin homepage URL
        documentation_url: Plugin documentation URL
        repository_url: Plugin repository URL
        license_info: Plugin license information

    Returns:
        New FlextPluginMetadata entity

    """
    return FlextPluginMetadata(
        entity_id=str(uuid.uuid4()),
        plugin_name=plugin_name,
        tags=tags,
        categories=categories,
        homepage_url=homepage_url,
        documentation_url=documentation_url,
        repository_url=repository_url,
        license_info=license_info,
        created_at=datetime.now(),
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
    return FlextPluginRegistry(
        entity_id=str(uuid.uuid4()),
        name=name,
        plugins=plugins,
        created_at=datetime.now(),
    )


def create_plugin_from_dict(plugin_data: dict[str, Any]) -> FlextPlugin:
    """Create a FlextPlugin from dictionary data.

    Args:
        plugin_data: Dictionary containing plugin information

    Returns:
        New FlextPlugin entity

    Raises:
        KeyError: If required fields are missing
        ValueError: If plugin data is invalid

    """

    # Helper function for validation
    def _handle_value_error(error: str) -> None:
        """Handle value error by raising appropriate exception."""
        raise ValueError(error)

    try:
        # Extract required fields with validation
        name = plugin_data.get("name", "")
        if not name:
            msg = "Plugin name is required"
            _handle_value_error(msg)

        version = plugin_data.get("version", "")
        if not version:
            msg = "Plugin version is required"
            _handle_value_error(msg)

        # Extract optional fields
        description = plugin_data.get("description", "")
        author = plugin_data.get("author", "")
        dependencies = plugin_data.get("dependencies", [])
        metadata = plugin_data.get("metadata", {})

        # Handle status conversion
        status_str = plugin_data.get("status", "inactive")
        try:
            status = PluginStatus(status_str)
        except ValueError:
            status = PluginStatus.INACTIVE

        return create_flext_plugin(
            name=name,
            version=version,
            description=description,
            author=author,
            dependencies=dependencies,
            metadata=metadata,
            status=status,
        )

    except (RuntimeError, ValueError, TypeError) as e:
        msg = f"Failed to create plugin from dictionary: {e}"
        raise ValueError(msg) from e


def create_plugin_config_from_dict(
    plugin_name: str,
    config_dict: dict[str, Any],
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
