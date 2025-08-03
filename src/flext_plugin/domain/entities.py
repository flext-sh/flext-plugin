"""FLEXT Plugin Domain Entities - Rich business entities for plugin management.

This module implements the core domain entities following Domain-Driven Design
principles. These entities encapsulate business logic, maintain consistency
boundaries, and provide the primary abstractions for plugin management operations.

Key Entities:
    - FlextPlugin: Core plugin entity with lifecycle management
    - FlextPluginConfig: Plugin configuration with validation
    - FlextPluginMetadata: Plugin descriptive information
    - FlextPluginRegistry: Aggregate managing plugin collections

Architecture:
    These entities form the domain layer of the Clean Architecture,
    containing rich business logic and enforcing domain rules.
    They integrate with flext-core patterns while maintaining
    plugin-specific business semantics.

Domain Rules:
    - Plugin names must be unique within a registry
    - Plugin status transitions follow defined lifecycle rules
    - Configuration changes trigger validation and events
    - Registry maintains consistency across plugin operations

Example:
    >>> plugin = FlextPlugin(
    ...     name="data-processor",
    ...     version="1.0.0",
    ...     config={"description": "Processes data efficiently"}
    ... )
    >>> result = plugin.activate()
    >>> if result.is_success():
    ...     print(f"Plugin {plugin.name} is now active")

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_core import FlextEntity, FlextEntityId, FlextResult
from flext_core.utilities import FlextGenerators
from pydantic import Field

from flext_plugin.core.types import PluginStatus


class FlextPlugin(FlextEntity):
    """Rich plugin entity with comprehensive business logic and lifecycle management.

    Core domain entity representing a plugin within the FLEXT ecosystem.
    Encapsulates plugin identity, metadata, configuration, and business rules
    while maintaining consistency with Domain-Driven Design principles.

    This entity serves as the primary abstraction for plugin operations,
    including lifecycle management, validation, activation/deactivation,
    and integration with the broader FLEXT platform services.

    Business Rules:
        - Plugin names must be non-empty and unique within a registry
        - Version strings must follow semantic versioning patterns
        - Status transitions must follow defined lifecycle rules
        - Configuration changes require validation before application

    Lifecycle States:
        DISCOVERED → LOADED → ACTIVE ↔ INACTIVE
                           ↓
                        ERROR → DISABLED

    Attributes:
        name: Unique plugin identifier within the system
        plugin_version: Semantic version string (e.g., "1.2.3")
        description: Human-readable plugin description
        author: Plugin developer or organization name
        status: Current plugin lifecycle status

    Domain Events:
        The entity generates domain events for:
        - Plugin activation/deactivation
        - Configuration changes
        - Status transitions
        - Error conditions

    Example:
        >>> plugin = FlextPlugin(
        ...     name="oracle-connector",
        ...     version="2.1.0",
        ...     config={
        ...         "description": "Oracle database connector",
        ...         "author": "FLEXT Team"
        ...     }
        ... )
        >>> activation_result = plugin.activate()
        >>> if activation_result.is_success():
        ...     print(f"Plugin {plugin.name} activated successfully")

    """

    # Pydantic field definitions with comprehensive metadata
    name: str = Field(
        default="",
        description="Unique plugin identifier used for discovery and management",
        min_length=1,
        max_length=100,
    )
    plugin_version: str = Field(
        default="",
        description="Semantic version string following semver format (e.g., '1.2.3')",
        min_length=1,
        max_length=50,
    )
    description: str = Field(
        default="",
        description="Human-readable description of plugin functionality",
        max_length=500,
    )
    author: str = Field(
        default="",
        description="Plugin developer or organization name",
        max_length=100,
    )
    status: PluginStatus = Field(
        default=PluginStatus.INACTIVE,
        description="Current plugin lifecycle and operational status",
    )

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        *,
        name: str = "",
        version: str = "",
        config: dict[str, object] | None = None,
        metadata: object = None,  # noqa: ARG002
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
        final_entity_id = entity_id or FlextGenerators.generate_entity_id()

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
        created_at: datetime | None = None,  # noqa: ARG002
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
        created_at: datetime | None = None,  # noqa: ARG002
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
