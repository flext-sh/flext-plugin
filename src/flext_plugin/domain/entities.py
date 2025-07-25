"""FLEXT Plugin Domain Entities - Core plugin business entities.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Core domain entities for plugin management system.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from flext_core import FlextEntity, FlextEntityId


class PluginStatus(Enum):
    """Plugin status enumeration."""

    INACTIVE = "inactive"
    ACTIVE = "active"
    LOADING = "loading"
    ERROR = "error"
    DISABLED = "disabled"


class FlextPlugin(FlextEntity):
    """Plugin entity representing a plugin in the system."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        name: str = "",
        version: str = "",
        description: str = "",
        author: str = "",
        dependencies: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        status: PluginStatus = PluginStatus.INACTIVE,
        created_at: datetime | None = None,
    ) -> None:
        """Initialize plugin entity.

        Args:
            entity_id: Unique entity identifier
            name: Plugin name
            version: Plugin version
            description: Plugin description
            author: Plugin author
            dependencies: List of plugin dependencies
            metadata: Additional plugin metadata
            status: Plugin status
            created_at: Creation timestamp

        """
        super().__init__(entity_id)
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.dependencies = dependencies or []
        self.metadata = metadata or {}
        self.status = status
        self.created_at = created_at or datetime.now()

    def is_valid(self) -> bool:
        """Validate plugin entity state.

        Returns:
            True if plugin is valid, False otherwise

        """
        return bool(self.name and self.version)

    def activate(self) -> bool:
        """Activate the plugin.

        Returns:
            True if activation successful, False otherwise

        """
        if self.status == PluginStatus.INACTIVE:
            self.status = PluginStatus.ACTIVE
            return True
        return False

    def deactivate(self) -> bool:
        """Deactivate the plugin.

        Returns:
            True if deactivation successful, False otherwise

        """
        if self.status == PluginStatus.ACTIVE:
            self.status = PluginStatus.INACTIVE
            return True
        return False

    def is_active(self) -> bool:
        """Check if plugin is active.

        Returns:
            True if plugin is active, False otherwise

        """
        return self.status == PluginStatus.ACTIVE


class FlextPluginConfig(FlextEntity):
    """Plugin configuration entity."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        plugin_name: str = "",
        config_data: dict[str, Any] | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        """Initialize plugin configuration entity.

        Args:
            entity_id: Unique entity identifier
            plugin_name: Name of the plugin this config belongs to
            config_data: Configuration data
            created_at: Creation timestamp
            updated_at: Last update timestamp

        """
        super().__init__(entity_id)
        self.plugin_name = plugin_name
        self.config_data = config_data or {}
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def is_valid(self) -> bool:
        """Validate plugin configuration entity state.

        Returns:
            True if configuration is valid, False otherwise

        """
        return bool(self.plugin_name)

    def update_config(self, new_config: dict[str, Any]) -> None:
        """Update configuration data.

        Args:
            new_config: New configuration data

        """
        self.config_data.update(new_config)
        self.updated_at = datetime.now()


class FlextPluginMetadata(FlextEntity):
    """Plugin metadata entity containing additional plugin information."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        plugin_name: str = "",
        tags: list[str] | None = None,
        categories: list[str] | None = None,
        homepage_url: str = "",
        documentation_url: str = "",
        repository_url: str = "",
        license_info: str = "",
        created_at: datetime | None = None,
    ) -> None:
        """Initialize plugin metadata entity.

        Args:
            entity_id: Unique entity identifier
            plugin_name: Name of the plugin this metadata belongs to
            tags: Plugin tags
            categories: Plugin categories
            homepage_url: Plugin homepage URL
            documentation_url: Plugin documentation URL
            repository_url: Plugin repository URL
            license_info: Plugin license information
            created_at: Creation timestamp

        """
        super().__init__(entity_id)
        self.plugin_name = plugin_name
        self.tags = tags or []
        self.categories = categories or []
        self.homepage_url = homepage_url
        self.documentation_url = documentation_url
        self.repository_url = repository_url
        self.license_info = license_info
        self.created_at = created_at or datetime.now()

    def is_valid(self) -> bool:
        """Validate plugin metadata entity state.

        Returns:
            True if metadata is valid, False otherwise

        """
        return bool(self.plugin_name)


class FlextPluginRegistry(FlextEntity):
    """Plugin registry entity managing registered plugins."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        name: str = "",
        plugins: dict[str, FlextPlugin] | None = None,
        created_at: datetime | None = None,
    ) -> None:
        """Initialize plugin registry entity.

        Args:
            entity_id: Unique entity identifier
            name: Registry name
            plugins: Dictionary of registered plugins (name -> plugin)
            created_at: Creation timestamp

        """
        super().__init__(entity_id)
        self.name = name
        self.plugins = plugins or {}
        self.created_at = created_at or datetime.now()

    def is_valid(self) -> bool:
        """Validate plugin registry entity state.

        Returns:
            True if registry is valid, False otherwise

        """
        return bool(self.name)

    def register_plugin(self, plugin: FlextPlugin) -> bool:
        """Register a plugin in the registry.

        Args:
            plugin: Plugin to register

        Returns:
            True if registration successful, False otherwise

        """
        if plugin.is_valid() and plugin.name not in self.plugins:
            self.plugins[plugin.name] = plugin
            return True
        return False

    def unregister_plugin(self, plugin_name: str) -> bool:
        """Unregister a plugin from the registry.

        Args:
            plugin_name: Name of plugin to unregister

        Returns:
            True if unregistration successful, False otherwise

        """
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            return True
        return False

    def get_plugin(self, plugin_name: str) -> FlextPlugin | None:
        """Get a plugin by name.

        Args:
            plugin_name: Name of plugin to get

        Returns:
            Plugin if found, None otherwise

        """
        return self.plugins.get(plugin_name)

    def list_plugins(self) -> list[FlextPlugin]:
        """List all registered plugins.

        Returns:
            List of all registered plugins

        """
        return list(self.plugins.values())


# Backwards compatibility aliases
Plugin = FlextPlugin
PluginConfig = FlextPluginConfig
PluginMetadata = FlextPluginMetadata
PluginRegistry = FlextPluginRegistry
