"""FLEXT Plugin Simple API - Factory functions for easy plugin creation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Simple factory functions for creating plugin entities and configurations.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

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
    *,
    config: dict[str, object] | None = None,
) -> FlextPlugin:
    """Create a new FlextPlugin entity.

    Args:
        name: Plugin name
        version: Plugin version
        config: Configuration dict containing description, author, dependencies,
            metadata, status

    Returns:
        New FlextPlugin entity

    """
    config = config or {}
    config["created_at"] = datetime.now(UTC)

    return FlextPlugin(
        entity_id=str(uuid.uuid4()),
        name=name,
        version=version,
        config=config,
    )


def create_flext_plugin_config(
    plugin_name: str,
    config_data: dict[str, object] | None = None,
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
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )


def create_flext_plugin_metadata(
    plugin_name: str,
    *,
    metadata: dict[str, object] | None = None,
) -> FlextPluginMetadata:
    """Create a new FlextPluginMetadata entity.

    Args:
        plugin_name: Name of the plugin this metadata belongs to
        metadata: Metadata dict containing tags, categories, URLs, license info

    Returns:
        New FlextPluginMetadata entity

    """
    metadata = metadata or {}
    metadata["created_at"] = datetime.now(UTC)

    return FlextPluginMetadata(
        entity_id=str(uuid.uuid4()),
        plugin_name=plugin_name,
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
    return FlextPluginRegistry(
        entity_id=str(uuid.uuid4()),
        name=name,
        plugins=plugins,
        created_at=datetime.now(UTC),
    )


def create_plugin_from_dict(plugin_data: dict[str, object]) -> FlextPlugin:
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
    config_dict: dict[str, object],
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
