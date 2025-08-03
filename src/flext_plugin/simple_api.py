"""FLEXT Plugin Simple API - Factory functions and convenience methods for plugin entity creation.

This module provides simplified factory functions for creating plugin entities,
configurations, and metadata objects. These functions serve as convenience
wrappers around the domain entities, providing sensible defaults and
simplified parameter interfaces for common plugin creation scenarios.

The simple API abstracts the complexity of direct entity construction while
maintaining full compatibility with the underlying domain model. All functions
return properly initialized domain entities that integrate seamlessly with
the broader FLEXT plugin management system.

Key Functions:
    - create_flext_plugin: Create plugin entities with configuration
    - create_flext_plugin_config: Create plugin configuration entities
    - create_flext_plugin_metadata: Create plugin metadata entities
    - create_flext_plugin_registry: Create plugin registry collections

Factory Patterns:
    - Automatic ID generation using UUID4 for entity uniqueness
    - Timestamp management for creation and modification tracking
    - Default value handling for optional parameters
    - Type validation and conversion for data integrity

Example:
    >>> from flext_plugin.simple_api import create_flext_plugin
    >>> 
    >>> # Create plugin with minimal configuration
    >>> plugin = create_flext_plugin(
    ...     name="data-processor",
    ...     version="1.0.0",
    ...     config={
    ...         "description": "Processes data efficiently",
    ...         "author": "FLEXT Team"
    ...     }
    ... )
    >>> print(f"Created plugin: {plugin.name} v{plugin.plugin_version}")

Integration:
    - Built on domain entities for architectural consistency
    - Provides backward compatibility through function aliases
    - Supports dictionary-based plugin creation for external integration
    - Maintains enterprise-grade validation and error handling

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from flext_plugin.core.types import PluginStatus
from flext_plugin.domain.entities import (
    FlextPlugin,
    FlextPluginConfig,
    FlextPluginMetadata,
    FlextPluginRegistry,
)


def create_flext_plugin(
    name: str,
    version: str,
    *,
    config: dict[str, object] | None = None,
) -> FlextPlugin:
    """Create a new FlextPlugin entity with automatic ID generation and timestamp management.
    
    Factory function that creates a properly initialized FlextPlugin domain entity
    with automatic UUID generation and timestamp management. This function provides
    a simplified interface for plugin creation while ensuring all required fields
    are properly initialized and validated.
    
    The function handles entity initialization complexity, providing sensible defaults
    and proper integration with the domain model. All created plugins are ready for
    registration and use within the FLEXT plugin management system.

    Args:
        name: Unique plugin identifier name, must be non-empty string
        version: Plugin version string, should follow semantic versioning
        config: Optional configuration dict containing:
            - description: Human-readable plugin description
            - author: Plugin developer or organization name
            - dependencies: List of plugin dependencies
            - metadata: Additional plugin metadata
            - status: Plugin lifecycle status (defaults to INACTIVE)

    Returns:
        Fully initialized FlextPlugin domain entity with generated ID and timestamps

    Example:
        >>> plugin = create_flext_plugin(
        ...     name="data-processor",
        ...     version="1.2.0",
        ...     config={
        ...         "description": "Advanced data processing plugin",
        ...         "author": "FLEXT Development Team",
        ...         "dependencies": ["flext-core", "flext-db"]
        ...     }
        ... )
        >>> print(f"Plugin {plugin.name} v{plugin.plugin_version} created")

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
    """Create a FlextPlugin entity from dictionary data with comprehensive validation.
    
    Factory function that creates a FlextPlugin entity from dictionary input,
    providing comprehensive validation and type conversion. This function is
    particularly useful for creating plugins from external data sources such
    as configuration files, API responses, or serialized data.
    
    The function performs robust validation of required fields, handles type
    conversion where appropriate, and provides meaningful error messages for
    debugging and troubleshooting plugin creation issues.

    Args:
        plugin_data: Dictionary containing plugin information with expected keys:
            - name (required): Plugin identifier string
            - version (required): Plugin version string  
            - description (optional): Human-readable description
            - author (optional): Plugin developer or organization
            - dependencies (optional): List of plugin dependencies
            - metadata (optional): Additional metadata dictionary
            - status (optional): Plugin status string (defaults to "inactive")

    Returns:
        Fully initialized FlextPlugin domain entity created from dictionary data

    Raises:
        KeyError: If required fields ('name' or 'version') are missing from input
        ValueError: If plugin data is invalid, empty, or contains invalid values

    Example:
        >>> plugin_data = {
        ...     "name": "oracle-connector",
        ...     "version": "2.1.0",
        ...     "description": "Oracle database connectivity plugin",
        ...     "author": "FLEXT Team",
        ...     "dependencies": ["cx_Oracle", "sqlalchemy"],
        ...     "status": "inactive"
        ... }
        >>> plugin = create_plugin_from_dict(plugin_data)
        >>> print(f"Created {plugin.name} from dictionary data")
    
    Validation Process:
        1. Required field validation (name, version)
        2. Type conversion and normalization
        3. Status enum validation with fallback
        4. Configuration object assembly
        5. Entity creation with proper error handling

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
            status = PluginStatus(status_str)
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
