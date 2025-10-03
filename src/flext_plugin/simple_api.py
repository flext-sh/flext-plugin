"""FLEXT Plugin Simple API - Factory functions and convenience methods for plugins.

This module provides simplified factory functions for creating plugin entities,
configurations, and metadata objects. These functions serve as convenience
wrappers around the domain entities, providing sensible defaults and
simplified parameter interfaces for common plugin creation scenarios.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import contextlib
import uuid
from datetime import UTC, datetime

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextTypes,
)
from flext_plugin.entities import (
    FlextPlugin,
    FlextPluginConfig,
    FlextPluginMetadata,
    FlextPluginRegistry,
)
from flext_plugin.models import PluginStatus


class FlextPluginSimpleApi:
    """Unified class providing factory functions and convenience methods for plugins.

    This class serves as a namespace for simplified factory functions that create
    plugin entities, configurations, and metadata objects. It provides convenience
    wrappers around the domain entities with sensible defaults and simplified
    parameter interfaces for common plugin creation scenarios.

    Integrates flext-core components:
    - FlextLogger for structured logging
    - FlextResult for consistent error handling
    - FlextTypes for type safety

    All methods are static and can be used without instantiating the class.
    """

    _logger = FlextLogger(__name__)

    @staticmethod
    def create_flext_plugin(
        name: str,
        version: str,
        *,
        config: FlextTypes.Dict | None = None,
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

    @staticmethod
    def create_flext_plugin_config(
        plugin_name: str,
        config_data: FlextTypes.Dict | None = None,
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
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat(),
        )

    @staticmethod
    def create_flext_plugin_metadata(
        plugin_name: str,
        *,
        metadata: FlextTypes.Dict | None = None,
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

    @staticmethod
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

    @staticmethod
    def create_plugin_from_dict(
        plugin_data: FlextTypes.Dict,
    ) -> FlextResult[FlextPlugin]:
        """Create a FlextPlugin entity from dictionary data with comprehensive validation.

        Factory function that creates a FlextPlugin entity from dictionary input,
        providing comprehensive validation and type conversion. This function is
        particularly useful for creating plugins from external data sources such
        as configuration files, API responses, or serialized data.

        Returns:
            FlextResult containing the created plugin or error details.

        """
        try:
            # Extract required fields with validation
            name_obj = plugin_data.get("name", "")
            if not name_obj:
                return FlextResult[FlextPlugin].fail("Plugin name is required")

            name = str(name_obj)
            version_obj = plugin_data.get("version", "")
            if not version_obj:
                return FlextResult[FlextPlugin].fail("Plugin version is required")

            version = str(version_obj)

            # Validate status if provided
            status_str = plugin_data.get("status", "inactive")
            with contextlib.suppress(ValueError):
                PluginStatus(str(status_str))

            plugin = FlextPluginSimpleApi.create_flext_plugin(
                name=name,
                version=version,
                config={
                    "description": str(plugin_data.get("description", "")),
                    "author": str(plugin_data.get("author", "")),
                    "dependencies": plugin_data.get("dependencies", []),
                    "metadata": plugin_data.get("metadata", {}),
                    "status": status_str,
                },
            )

            FlextPluginSimpleApi._logger.info(
                "Plugin created from dictionary",
                extra={"plugin_name": name, "version": version},
            )

            return FlextResult[FlextPlugin].ok(plugin)

        except Exception as e:
            error_msg = f"Failed to create plugin from dictionary: {e}"
            FlextPluginSimpleApi._logger.error(
                "Plugin creation failed",
                extra={"error": error_msg, "data_keys": list(plugin_data.keys())},
            )
            return FlextResult[FlextPlugin].fail(error_msg)

    @staticmethod
    def create_plugin_config_from_dict(
        plugin_name: str,
        config_dict: FlextTypes.Dict,
    ) -> FlextResult[FlextPluginConfig]:
        """Create a FlextPluginConfig from dictionary data.

        Args:
            plugin_name: Name of the plugin
            config_dict: Dictionary containing configuration data

        Returns:
            FlextResult containing the new config entity or error details.

        """
        if not plugin_name:
            return FlextResult[FlextPluginConfig].fail("Plugin name is required")

        try:
            config = FlextPluginSimpleApi.create_flext_plugin_config(
                plugin_name=plugin_name,
                config_data=config_dict,
            )

            FlextPluginSimpleApi._logger.info(
                "Plugin config created from dictionary",
                extra={"plugin_name": plugin_name},
            )

            return FlextResult[FlextPluginConfig].ok(config)

        except Exception as e:
            error_msg = f"Failed to create plugin config: {e}"
            FlextPluginSimpleApi._logger.error(
                "Plugin config creation failed",
                extra={"plugin_name": plugin_name, "error": error_msg},
            )
            return FlextResult[FlextPluginConfig].fail(error_msg)


__all__ = [
    "FlextPluginSimpleApi",
]
