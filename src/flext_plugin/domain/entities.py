"""FLEXT Plugin Domain Entities - Core plugin business entities.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Core domain entities for plugin management system.
"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_core import FlextEntity, FlextEntityId

from flext_plugin.core.types import PluginStatus


class FlextPlugin(FlextEntity):
    """Plugin entity representing a plugin in the system."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        *,
        name: str = "",
        version: str = "",
        config: dict[str, object] | None = None,
    ) -> None:
        """Initialize plugin entity.

        Args:
            entity_id: Unique entity identifier
            name: Plugin name
            version: Plugin version
            config: Configuration dict containing description, author, dependencies,
                metadata, status, created_at

        """
        super().__init__(entity_id)
        self.name = name
        self.version = version

        # Extract from config dict
        config = config or {}
        self.description = config.get("description", "")
        self.author = config.get("author", "")
        self.dependencies = config.get("dependencies", [])
        self.metadata = config.get("metadata", {})
        self.status = config.get("status", PluginStatus.INACTIVE)
        self.created_at = config.get("created_at", datetime.now(UTC))

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
        *,
        plugin_name: str = "",
        config_data: dict[str, object] | None = None,
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
        self.created_at = created_at or datetime.now(UTC)
        self.updated_at = updated_at or datetime.now(UTC)

    def is_valid(self) -> bool:
        """Validate plugin configuration entity state.

        Returns:
            True if configuration is valid, False otherwise

        """
        return bool(self.plugin_name)

    def update_config(self, new_config: dict[str, object]) -> None:
        """Update configuration data.

        Args:
            new_config: New configuration data

        """
        self.config_data.update(new_config)
        self.updated_at = datetime.now(UTC)


class FlextPluginMetadata(FlextEntity):
    """Plugin metadata entity containing additional plugin information."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        *,
        plugin_name: str = "",
        metadata: dict[str, object] | None = None,
    ) -> None:
        """Initialize plugin metadata entity.

        Args:
            entity_id: Unique entity identifier
            plugin_name: Name of the plugin this metadata belongs to
            metadata: Metadata dict containing tags, categories, URLs, license,
                created_at

        """
        super().__init__(entity_id)
        self.plugin_name = plugin_name

        # Extract from metadata dict
        metadata = metadata or {}
        self.tags = metadata.get("tags", [])
        self.categories = metadata.get("categories", [])
        self.homepage_url = metadata.get("homepage_url", "")
        self.documentation_url = metadata.get("documentation_url", "")
        self.repository_url = metadata.get("repository_url", "")
        self.license_info = metadata.get("license_info", "")
        self.created_at = metadata.get("created_at", datetime.now(UTC))

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
        *,
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
        self.created_at = created_at or datetime.now(UTC)

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


# Additional domain entities
class FlextPluginExecution(FlextEntity):
    """Plugin execution entity for tracking plugin executions."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        *,
        plugin_name: str = "",
        execution_config: dict[str, object] | None = None,
    ) -> None:
        """Initialize plugin execution entity."""
        super().__init__(entity_id)
        self.plugin_name = plugin_name

        # Extract from execution_config dict
        execution_config = execution_config or {}
        self.start_time = execution_config.get("start_time", datetime.now(UTC))
        self.end_time = execution_config.get("end_time")
        self.status = execution_config.get("status", "pending")
        self.result = execution_config.get("result")
        self.error = execution_config.get("error", "")

    def is_valid(self) -> bool:
        """Validate plugin execution entity state."""
        return bool(self.plugin_name)


# Backwards compatibility aliases
Plugin = FlextPlugin
PluginConfig = FlextPluginConfig
PluginConfiguration = FlextPluginConfig  # Additional alias for tests
PluginMetadata = FlextPluginMetadata
PluginRegistry = FlextPluginRegistry
PluginInstance = FlextPlugin  # Alias for compatibility
PluginExecution = FlextPluginExecution
