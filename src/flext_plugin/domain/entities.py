"""FLEXT Plugin Domain Entities - Core plugin business entities.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Core domain entities for plugin management system.
"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_core import FlextEntity, FlextEntityId, FlextResult
from flext_core.utilities import FlextGenerators
from pydantic import Field

from flext_plugin.core.types import PluginStatus


class FlextPlugin(FlextEntity):
    """Plugin entity representing a plugin in the system."""

    # Define Pydantic fields for proper type recognition
    name: str = Field(default="", description="Plugin name")
    plugin_version: str = Field(default="", description="Plugin version")
    description: str = Field(default="", description="Plugin description")
    author: str = Field(default="", description="Plugin author")
    status: PluginStatus = Field(
        default=PluginStatus.INACTIVE, description="Plugin status",
    )

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        *,
        name: str = "",
        version: str = "",
        config: dict[str, object] | None = None,
        metadata: object = None,
        **kwargs: object,  # Accept additional arguments for backward compatibility
    ) -> None:
        """Initialize plugin entity.

        Args:
            entity_id: Unique entity identifier
            name: Plugin name
            version: Plugin version
            config: Configuration dict containing description, author, dependencies,
                metadata, status, created_at
            metadata: Plugin metadata object
            **kwargs: Additional arguments for backward compatibility

        """
        # Generate ID if not provided
        final_entity_id = (
            entity_id or FlextGenerators.generate_entity_id()
        )

        # Extract config values
        config = config or {}

        # Initialize FlextEntity base first
        super().__init__(id=final_entity_id)

        # Set plugin-specific fields using object.__setattr__ for frozen models
        object.__setattr__(self, "name", kwargs.get("plugin_id", name))
        object.__setattr__(self, "plugin_version", version)
        object.__setattr__(self, "description", config.get("description", ""))
        object.__setattr__(self, "author", config.get("author", ""))
        object.__setattr__(self, "status", config.get("status", PluginStatus.INACTIVE))

    # Backward compatibility properties (without conflicting names)
    @property
    def plugin_name(self) -> str:
        """Get plugin name (compatibility)."""
        return self.name

    def get_version(self) -> str:
        """Get plugin version (compatibility)."""
        return self.plugin_version

    @property
    def plugin_status(self) -> PluginStatus:
        """Get plugin status (compatibility)."""
        return self.status

    def is_valid(self) -> bool:
        """Validate plugin entity state.

        Returns:
            True if plugin is valid, False otherwise

        """
        return bool(self.name and self.plugin_version)

    def activate(self) -> bool:
        """Activate the plugin.

        Returns:
            True if activation successful, False otherwise

        """
        if self.status == PluginStatus.INACTIVE:
            object.__setattr__(self, "status", PluginStatus.ACTIVE)
            return True
        return False

    def deactivate(self) -> bool:
        """Deactivate the plugin.

        Returns:
            True if deactivation successful, False otherwise

        """
        if self.status == PluginStatus.ACTIVE:
            object.__setattr__(self, "status", PluginStatus.INACTIVE)
            return True
        return False

    def is_active(self) -> bool:
        """Check if plugin is active.

        Returns:
            True if plugin is active, False otherwise

        """
        return self.status == PluginStatus.ACTIVE

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin entity.

        Returns:
            FlextResult indicating success or failure of validation

        """
        if not self.name:
            return FlextResult.fail("Plugin name is required")
        if not self.plugin_version:
            return FlextResult.fail("Plugin version is required")
        return FlextResult.ok(None)


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
        # FlextEntity expects keyword argument 'id'
        final_id = entity_id or FlextGenerators.generate_entity_id()
        super().__init__(id=final_id)
        self.plugin_name = plugin_name
        self.config_data = config_data or {}
        # created_at is automatically handled by FlextEntity base class
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

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin configuration entity.

        Returns:
            FlextResult indicating success or failure of validation

        """
        if not self.plugin_name:
            return FlextResult.fail("Plugin name is required")
        return FlextResult.ok(None)


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
        # FlextEntity expects keyword argument 'id'
        final_id = entity_id or FlextGenerators.generate_entity_id()
        super().__init__(id=final_id)
        self.plugin_name = plugin_name

        # Extract from metadata dict
        metadata = metadata or {}
        self.tags = metadata.get("tags", [])
        self.categories = metadata.get("categories", [])
        self.homepage_url = metadata.get("homepage_url", "")
        self.documentation_url = metadata.get("documentation_url", "")
        self.repository_url = metadata.get("repository_url", "")
        self.license_info = metadata.get("license_info", "")
        # created_at is automatically handled by FlextEntity base class

    def is_valid(self) -> bool:
        """Validate plugin metadata entity state.

        Returns:
            True if metadata is valid, False otherwise

        """
        return bool(self.plugin_name)

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin metadata entity.

        Returns:
            FlextResult indicating success or failure of validation

        """
        if not self.plugin_name:
            return FlextResult.fail("Plugin name is required")
        return FlextResult.ok(None)


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
        # FlextEntity expects keyword argument 'id'
        final_id = entity_id or FlextGenerators.generate_entity_id()
        super().__init__(id=final_id)
        self.name = name
        self.plugins = plugins or {}
        # created_at is automatically handled by FlextEntity base class

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

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin registry entity.

        Returns:
            FlextResult indicating success or failure of validation

        """
        if not self.name:
            return FlextResult.fail("Registry name is required")
        return FlextResult.ok(None)


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
        # FlextEntity expects keyword argument 'id'
        final_id = entity_id or FlextGenerators.generate_entity_id()
        super().__init__(id=final_id)
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

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin execution entity.

        Returns:
            FlextResult indicating success or failure of validation

        """
        if not self.plugin_name:
            return FlextResult.fail("Plugin name is required")
        return FlextResult.ok(None)


# Backwards compatibility aliases
Plugin = FlextPlugin
PluginConfig = FlextPluginConfig
PluginConfiguration = FlextPluginConfig  # Additional alias for tests
PluginMetadata = FlextPluginMetadata
PluginRegistry = FlextPluginRegistry
PluginInstance = FlextPlugin  # Alias for compatibility
PluginExecution = FlextPluginExecution
