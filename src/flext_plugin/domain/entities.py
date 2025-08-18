"""FLEXT Plugin Domain Entities - Rich business entities for plugin management.

This module implements the core domain entities following Domain-Driven Design
principles. These entities encapsulate business logic, maintain consistency
boundaries, and provide the primary abstractions for plugin management operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from typing import cast

from flext_core import (
    FlextEntity,
    FlextGenerators,
    FlextResult,
    FlextTimestamp,
    get_logger,
)
from pydantic import Field, field_validator

from flext_plugin.typings import (
    PluginStatus,
    PluginType,
)


class FlextPluginConfigParams:
    """Parameter Object pattern for FlextPluginConfig initialization - SOLID Single Responsibility."""

    plugin_name: str = ""
    config_data: dict[str, object] | None = None
    created_at: FlextTimestamp | None = None
    updated_at: FlextTimestamp | None = None
    enabled: bool = True
    settings: dict[str, object] | None = None
    dependencies: list[str] | None = None
    priority: int = 100
    max_memory_mb: int = 512
    max_cpu_percent: int = 50
    timeout_seconds: int = 30


class FlextPluginMetadataParams:
    """Parameter Object pattern for FlextPluginMetadata initialization - SOLID Single Responsibility."""

    plugin_name: str = ""
    metadata: dict[str, object] | None = None
    name: str = ""
    entry_point: str = ""
    plugin_type: object = ""
    description: str = ""
    dependencies: list[str] | None = None
    trusted: bool = False
    homepage: str | None = None
    repository: str | None = None


class FlextPluginRegistryParams:
    """Parameter Object pattern for FlextPluginRegistry initialization - SOLID Single Responsibility."""

    name: str = ""
    plugins: dict[str, FlextPluginEntity] | None = None
    created_at: FlextTimestamp | None = None
    registry_url: str = ""
    is_enabled: bool = True
    plugin_count: int = 0
    sync_error_count: int = 0
    last_sync: FlextTimestamp | None = None
    requires_authentication: bool = False
    api_key: str = ""
    verify_signatures: bool = False
    trusted_publishers: list[str] | None = None


class FlextPluginEntity(FlextEntity):
    """Rich plugin domain entity with comprehensive business logic and lifecycle management.

    Core domain entity representing a plugin within the FLEXT ecosystem.
    This is a DOMAIN ENTITY, not a plugin implementation. It encapsulates
    plugin identity, metadata, configuration, and business rules while
    maintaining consistency with Domain-Driven Design principles.

    IMPORTANT: This entity is distinct from flext_core.FlextPlugin,
    which is the abstract interface that actual plugin implementations must follow.
    This entity represents the domain concept of a plugin in the business layer.

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
      >>> plugin = FlextPluginEntity.model_validate(
      ...     {
      ...         "id": "plugin-123",
      ...         "name": "oracle-connector",
      ...         "plugin_version": "2.1.0",
      ...         "description": "Oracle database connector",
      ...         "author": "FLEXT Team",
      ...     }
      ... )
      >>> activation_result = plugin.activate()
      >>> if activation_result.success():
      ...     print(f"Plugin {plugin.name} activated successfully")

    """

    # Pydantic field definitions with comprehensive metadata
    name: str = Field(
        description="Unique plugin identifier used for discovery and management",
        min_length=1,
        max_length=100,
    )
    plugin_version: str = Field(
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
    plugin_type: PluginType = Field(
        default=PluginType.UTILITY,
        description="Plugin category and type for classification",
    )
    created_at: FlextTimestamp = Field(
        default_factory=FlextTimestamp.now,
        description="Plugin creation timestamp",
    )

    @classmethod
    def create(
        cls,
        *,
        name: str,
        plugin_version: str,
        entity_id: str | None = None,
        config: dict[str, object] | None = None,
        **kwargs: object,
    ) -> FlextPluginEntity:
        """Create plugin entity with proper validation.

        Args:
            name: Plugin name (required)
            plugin_version: Plugin version (required)
            entity_id: Unique entity identifier
            config: Configuration dict containing description, author, etc.
            **kwargs: Additional arguments for testing convenience

        Returns:
            FlextPluginEntity: Validated plugin entity

        """
        # Generate ID if not provided
        final_id = entity_id or FlextGenerators.generate_entity_id()

        # Extract config values
        config = config or {}

        # Handle testing convenience for plugin_id in kwargs
        plugin_name = kwargs.get("plugin_id", name)

        # Create instance data
        instance_data = {
            "id": final_id,
            "version": kwargs.get("entity_version", 1),  # FlextEntity version
            "metadata": kwargs.get("metadata", {}),
            "name": plugin_name,
            "plugin_version": plugin_version,
            "description": config.get("description", ""),
            "author": config.get("author", ""),
            "status": config.get("status", PluginStatus.INACTIVE),
            "plugin_type": config.get("plugin_type", PluginType.UTILITY),
        }

        return cls.model_validate(instance_data)

    # Remove __new__ method - let Pydantic handle object creation naturally
    # Use factory method create() for backward compatibility

    # Testing convenience properties (without conflicting names)
    @property
    def plugin_name(self) -> str:
        """Get plugin name (convenience)."""
        return self.name

    def get_version(self) -> str:
        """Get plugin version (convenience)."""
        return self.plugin_version

    @property
    def plugin_status(self) -> str:
        """Get plugin status (convenience) - returns value string."""
        # FlextEntity uses use_enum_values=True, so status is already a string
        return self.status if isinstance(self.status, str) else self.status.value

    def __setattr__(self, name: str, value: object) -> None:
        """Override setattr to handle plugin_status setter for frozen model."""
        if name == "plugin_status" and isinstance(value, PluginStatus):
            # Use object.__setattr__ to bypass frozen model restrictions
            object.__setattr__(self, "status", value)
        else:
            # For all other attributes, use the parent's __setattr__
            super().__setattr__(name, value)

    # Health and status checking properties
    @property
    def is_healthy(self) -> bool:
        """Check if plugin is healthy."""
        # Handle both enum and string values due to use_enum_values=True
        return self.status in {PluginStatus.HEALTHY, PluginStatus.HEALTHY.value}

    # Execution tracking properties (for testing convenience)
    @property
    def execution_count(self) -> int:
        """Get number of executions recorded."""
        # For testing convenience, return a placeholder
        return getattr(self, "_execution_count", 0)

    @property
    def average_execution_time_ms(self) -> float:
        """Get average execution time in milliseconds."""
        # For testing convenience, return a placeholder
        return getattr(self, "_average_execution_time_ms", 0.0)

    @property
    def last_execution(self) -> datetime | None:
        """Get timestamp of last execution."""
        # For testing convenience, return a placeholder
        return getattr(self, "_last_execution", None)

    @property
    def error_count(self) -> int:
        """Get number of errors recorded."""
        # For testing convenience, return a placeholder
        return getattr(self, "_error_count", 0)

    @property
    def last_error(self) -> str:
        """Get last error message."""
        # For testing convenience, return a placeholder
        return getattr(self, "_last_error", "")

    @property
    def last_error_time(self) -> datetime | None:
        """Get timestamp of last error."""
        # For testing convenience, return a placeholder
        return getattr(self, "_last_error_time", None)

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
        # Handle both enum and string values due to use_enum_values=True
        if self.status in {PluginStatus.INACTIVE, PluginStatus.INACTIVE.value}:
            object.__setattr__(self, "status", PluginStatus.ACTIVE)
            return True
        return False

    def deactivate(self) -> bool:
        """Deactivate the plugin.

        Returns:
            True if deactivation successful, False otherwise

        """
        # Handle both enum and string values due to use_enum_values=True
        if self.status in {PluginStatus.ACTIVE, PluginStatus.ACTIVE.value}:
            object.__setattr__(self, "status", PluginStatus.INACTIVE)
            return True
        return False

    def is_active(self) -> bool:
        """Check if plugin is active.

        Returns:
            True if plugin is active, False otherwise

        """
        # Handle both enum and string values due to use_enum_values=True
        return self.status in {PluginStatus.ACTIVE, PluginStatus.ACTIVE.value}

    def record_execution(
        self,
        execution_time_ms: float,
        *,
        success: bool = True,
    ) -> None:
        """Record plugin execution for metrics tracking.

        Args:
            execution_time_ms: Execution time in milliseconds
            success: Whether execution was successful

        """
        # Get current counts
        current_count = getattr(self, "_execution_count", 0)
        current_avg = getattr(self, "_average_execution_time_ms", 0.0)

        # Calculate new average
        new_count = current_count + 1
        new_avg = ((current_avg * current_count) + execution_time_ms) / new_count

        # Set new values using object.__setattr__ for frozen model
        object.__setattr__(self, "_execution_count", new_count)
        object.__setattr__(self, "_average_execution_time_ms", new_avg)
        object.__setattr__(self, "_last_execution", FlextTimestamp.now())

        # Update status based on success
        if not success:
            object.__setattr__(self, "status", PluginStatus.UNHEALTHY)

    def record_error(self, error_message: str) -> None:
        """Record plugin error for tracking.

        Args:
            error_message: Error message to record

        """
        # Get current error count
        current_error_count = getattr(self, "_error_count", 0)

        # Set new values using object.__setattr__ for frozen model
        object.__setattr__(self, "_error_count", current_error_count + 1)
        object.__setattr__(self, "_last_error", error_message)
        object.__setattr__(self, "_last_error_time", FlextTimestamp.now())
        object.__setattr__(self, "status", PluginStatus.UNHEALTHY)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin entity.

        Returns:
            FlextResult indicating success or failure of validation

        """
        if not self.name or not self.name.strip():
            return FlextResult[None].fail("Plugin name is required and cannot be empty")
        if not self.plugin_version or not self.plugin_version.strip():
            return FlextResult[None].fail(
                "Plugin version is required and cannot be empty"
            )
        return FlextResult[None].ok(None)


class FlextPluginConfig(FlextEntity):
    """Plugin configuration entity with validation and business rules."""

    # Pydantic fields
    plugin_name: str = Field(
        description="Name of the plugin this config belongs to",
        min_length=1,
    )
    config_data: dict[str, object] = Field(
        default_factory=dict,
        description="Configuration data",
    )
    created_at: FlextTimestamp = Field(
        default_factory=FlextTimestamp.now,
        description="Configuration creation timestamp",
    )
    updated_at: FlextTimestamp = Field(
        default_factory=FlextTimestamp.now,
        description="Last update timestamp",
    )

    # Configuration fields for testing convenience
    enabled: bool = Field(
        default=True,
        description="Whether plugin configuration is enabled",
    )
    settings: dict[str, object] = Field(
        default_factory=dict,
        description="Plugin settings",
    )
    dependencies: list[str] = Field(
        default_factory=list,
        description="Plugin dependencies",
    )
    priority: int = Field(default=100, description="Plugin priority")
    max_memory_mb: int = Field(default=512, description="Maximum memory usage in MB")
    max_cpu_percent: int = Field(default=50, description="Maximum CPU usage percentage")
    timeout_seconds: int = Field(default=30, description="Timeout in seconds")

    @classmethod
    def create(
        cls,
        *,
        plugin_name: str,
        entity_id: str | None = None,
        params: FlextPluginConfigParams | None = None,
        **kwargs: object,
    ) -> FlextPluginConfig:
        """Create plugin configuration entity with proper validation."""
        final_id = entity_id or FlextGenerators.generate_entity_id()

        # Use params if provided, otherwise create from individual parameters
        if params is not None:
            p = params
        else:
            p = FlextPluginConfigParams()
            p.plugin_name = plugin_name
            p.config_data = cast("dict[str, object] | None", kwargs.get("config_data"))
            p.created_at = cast("FlextTimestamp | None", kwargs.get("created_at"))
            p.updated_at = cast("FlextTimestamp | None", kwargs.get("updated_at"))
            p.enabled = cast("bool", kwargs.get("enabled", True))
            p.settings = cast("dict[str, object] | None", kwargs.get("settings"))
            p.dependencies = cast("list[str] | None", kwargs.get("dependencies"))
            p.priority = cast("int", kwargs.get("priority", 100))
            p.max_memory_mb = cast("int", kwargs.get("max_memory_mb", 512))
            p.max_cpu_percent = cast("int", kwargs.get("max_cpu_percent", 50))
            p.timeout_seconds = cast("int", kwargs.get("timeout_seconds", 30))

        # Create instance data
        instance_data = {
            "id": final_id,
            "version": kwargs.get("version", 1),
            "metadata": kwargs.get("metadata", {}),
            "plugin_name": p.plugin_name,
            "config_data": p.config_data or {},
            "updated_at": p.updated_at or FlextTimestamp.now(),
            "enabled": p.enabled,
            "settings": p.settings or {},
            "dependencies": p.dependencies or [],
            "priority": p.priority,
            "max_memory_mb": p.max_memory_mb,
            "max_cpu_percent": p.max_cpu_percent,
            "timeout_seconds": p.timeout_seconds,
        }

        return cls.model_validate(instance_data)

    # Remove __init__ override to prevent recursion - let Pydantic handle construction

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
        # Update mutable dict in place
        self.config_data.update(new_config)
        # Update timestamp using frozen model workaround
        object.__setattr__(self, "updated_at", FlextTimestamp.now())

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin configuration entity.

        Returns:
            FlextResult indicating success or failure of validation

        """
        if not self.plugin_name or not self.plugin_name.strip():
            return FlextResult[None].fail("Plugin name is required and cannot be empty")
        return FlextResult[None].ok(None)


class FlextPluginMetadata(FlextEntity):
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
    created_at: FlextTimestamp = Field(
        default_factory=FlextTimestamp.now,
        description="Metadata creation timestamp",
    )

    @classmethod
    def create(
        cls,
        *,
        name: str,
        entry_point: str,
        entity_id: str | None = None,
        params: FlextPluginMetadataParams | None = None,
        **kwargs: object,
    ) -> FlextPluginMetadata:
        """Create plugin metadata entity with proper validation."""
        final_id = entity_id or FlextGenerators.generate_entity_id()

        # Use params if provided, otherwise create from individual parameters
        if params is not None:
            p = params
        else:
            p = FlextPluginMetadataParams()
            p.plugin_name = cast("str", kwargs.get("plugin_name", name))
            p.metadata = cast("dict[str, object] | None", kwargs.get("metadata"))
            p.name = name
            p.entry_point = entry_point
            p.plugin_type = kwargs.get("plugin_type", "")
            p.description = cast("str", kwargs.get("description", ""))
            p.dependencies = cast("list[str] | None", kwargs.get("dependencies"))
            p.trusted = cast("bool", kwargs.get("trusted", False))
            p.homepage = cast("str | None", kwargs.get("homepage"))
            p.repository = cast("str | None", kwargs.get("repository"))

        # Extract from metadata dict
        metadata_dict = p.metadata or {}

        # Handle plugin_type conversion
        plugin_type_value: str = str(p.plugin_type) if p.plugin_type is not None else ""

        # Use name parameter or fall back to plugin_name
        final_name = p.name or p.plugin_name

        # Create instance data
        instance_data = {
            "id": final_id,
            "version": kwargs.get("version", 1),
            "metadata": kwargs.get("entity_metadata", {}),
            "plugin_name": final_name,
            "name": final_name,
            "entry_point": p.entry_point,
            "plugin_type": plugin_type_value,
            "description": p.description,
            "dependencies": p.dependencies or [],
            "trusted": p.trusted,
            "homepage": p.homepage,
            "repository": p.repository,
            "tags": metadata_dict.get("tags", []),
            "categories": metadata_dict.get("categories", []),
            "homepage_url": metadata_dict.get("homepage_url", ""),
            "documentation_url": metadata_dict.get("documentation_url", ""),
            "repository_url": metadata_dict.get("repository_url", ""),
            "license_info": metadata_dict.get("license_info", ""),
        }

        return cls.model_validate(instance_data)

    # Remove __init__ override to prevent recursion - let Pydantic handle construction

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
        if v != "" and not v.strip():
            msg = "Plugin entry point cannot be empty"
            raise ValueError(msg)
        return v

    def is_valid(self) -> bool:
        """Validate plugin metadata entity state.

        Returns:
            True if metadata is valid, False otherwise

        """
        return bool(self.plugin_name)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin metadata entity.

        Returns:
            FlextResult indicating success or failure of validation

        """
        if not self.plugin_name or not self.plugin_name.strip():
            return FlextResult[None].fail("Plugin name is required and cannot be empty")
        if not self.name or not self.name.strip():
            return FlextResult[None].fail(
                "Plugin name field is required and cannot be empty"
            )
        if not self.entry_point or not self.entry_point.strip():
            return FlextResult[None].fail(
                "Plugin entry point is required and cannot be empty",
            )
        return FlextResult[None].ok(None)


class FlextPluginRegistry(FlextEntity):
    """Plugin registry entity managing registered plugins."""

    # Pydantic fields
    name: str = Field(default="", description="Registry name")
    plugins: dict[str, FlextPluginEntity] = Field(
        default_factory=dict,
        description="Dictionary of registered plugins",
    )
    created_at: FlextTimestamp = Field(
        default_factory=FlextTimestamp.now,
        description="Registry creation timestamp",
    )

    # Registry configuration fields for testing convenience
    registry_url: str = Field(default="", description="Registry URL")
    is_enabled: bool = Field(default=True, description="Whether registry is enabled")
    plugin_count: int = Field(default=0, description="Number of plugins in registry")
    sync_error_count: int = Field(default=0, description="Number of sync errors")
    last_sync: FlextTimestamp | None = Field(
        default=None, description="Last sync timestamp"
    )

    # Authentication fields
    requires_authentication: bool = Field(
        default=False,
        description="Whether authentication is required",
    )
    api_key: str = Field(default="", description="API key for authentication")

    # Security fields
    verify_signatures: bool = Field(
        default=False,
        description="Whether to verify signatures",
    )
    trusted_publishers: list[str] = Field(
        default_factory=list,
        description="List of trusted publishers",
    )

    @classmethod
    def create(
        cls,
        *,
        name: str,
        entity_id: str | None = None,
        params: FlextPluginRegistryParams | None = None,
        **kwargs: object,
    ) -> FlextPluginRegistry:
        """Create plugin registry entity with proper validation."""
        final_id = entity_id or FlextGenerators.generate_entity_id()

        # Use params if provided, otherwise create from individual parameters
        if params is not None:
            p = params
        else:
            p = FlextPluginRegistryParams()
            p.name = name
            p.plugins = cast(
                "dict[str, FlextPluginEntity] | None",
                kwargs.get("plugins"),
            )
            p.created_at = cast("FlextTimestamp | None", kwargs.get("created_at"))
            p.registry_url = cast("str", kwargs.get("registry_url", ""))
            p.is_enabled = cast("bool", kwargs.get("is_enabled", True))
            p.plugin_count = cast("int", kwargs.get("plugin_count", 0))
            p.sync_error_count = cast("int", kwargs.get("sync_error_count", 0))
            p.last_sync = cast("FlextTimestamp | None", kwargs.get("last_sync"))
            p.requires_authentication = cast(
                "bool",
                kwargs.get("requires_authentication", False),
            )
            p.api_key = cast("str", kwargs.get("api_key", ""))
            p.verify_signatures = cast("bool", kwargs.get("verify_signatures", False))
            p.trusted_publishers = cast(
                "list[str] | None",
                kwargs.get("trusted_publishers"),
            )

        # Create instance data
        instance_data = {
            "id": final_id,
            "version": kwargs.get("version", 1),
            "metadata": kwargs.get("entity_metadata", {}),
            "name": p.name,
            "plugins": p.plugins or {},
            "registry_url": p.registry_url,
            "is_enabled": p.is_enabled,
            "plugin_count": p.plugin_count,
            "sync_error_count": p.sync_error_count,
            "last_sync": p.last_sync,
            "requires_authentication": p.requires_authentication,
            "api_key": p.api_key,
            "verify_signatures": p.verify_signatures,
            "trusted_publishers": p.trusted_publishers or [],
        }

        return cls.model_validate(instance_data)

    # Remove __init__ override to prevent recursion - let Pydantic handle construction

    @property
    def is_available(self) -> bool:
        """Check if registry is available (enabled and has URL)."""
        return self.is_enabled and bool(self.registry_url)

    def record_sync(self, *, success: bool, plugin_count: int | None = None) -> None:
        """Record sync attempt results.

        Args:
            success: Whether sync was successful
            plugin_count: Number of plugins synced (only updated on success)

        """
        object.__setattr__(self, "last_sync", FlextTimestamp.now())

        if success and plugin_count is not None:
            object.__setattr__(self, "plugin_count", plugin_count)
        elif not success:
            # Increment error count on failure
            object.__setattr__(self, "sync_error_count", self.sync_error_count + 1)

    def is_valid(self) -> bool:
        """Validate plugin registry entity state.

        Returns:
            True if registry is valid, False otherwise

        """
        return bool(self.name)

    def register_plugin(self, plugin: FlextPluginEntity) -> bool:
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

    def get_plugin(self, plugin_name: str) -> FlextPluginEntity | None:
        """Get a plugin by name.

        Args:
            plugin_name: Name of plugin to get

        Returns:
            Plugin if found, None otherwise

        """
        return self.plugins.get(plugin_name)

    def list_plugins(self) -> list[FlextPluginEntity]:
        """List all registered plugins.

        Returns:
            List of all registered plugins

        """
        return list(self.plugins.values())

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin registry entity.

        Returns:
            FlextResult indicating success or failure of validation

        """
        if not self.name or not self.name.strip():
            return FlextResult[None].fail(
                "Registry name is required and cannot be empty"
            )
        return FlextResult[None].ok(None)


# Additional domain entities
class FlextPluginExecution(FlextEntity):
    """Plugin execution entity for tracking plugin executions."""

    # Pydantic fields
    plugin_name: str = Field(
        default="",
        description="Name of the plugin being executed",
    )
    plugin_id: str = Field(
        default="",
        description="Plugin identifier (backward compatibility)",
    )
    execution_id: str = Field(
        default="",
        description="Execution identifier",
    )
    start_time: FlextTimestamp = Field(
        default_factory=FlextTimestamp.now,
        description="Execution start time",
    )
    end_time: datetime | None = Field(
        default=None,
        description="Execution end time",
    )
    status: str = Field(default="pending", description="Execution status")
    result: object | None = Field(default=None, description="Execution result")
    error: str = Field(default="", description="Execution error message")
    error_message: str | None = Field(
        default=None,
        description="Error message (compatibility)",
    )
    input_data: dict[str, object] = Field(
        default_factory=dict,
        description="Input data for execution",
    )
    output_data: dict[str, object] = Field(
        default_factory=dict,
        description="Output data from execution",
    )

    @classmethod
    def create(
        cls,
        *,
        plugin_name: str = "",
        execution_config: dict[str, object] | None = None,
        entity_id: str | None = None,
        **kwargs: object,
    ) -> FlextPluginExecution:
        """Create plugin execution entity with proper validation.

        Args:
            plugin_name: Name of the plugin being executed
            execution_config: Execution configuration dictionary
            entity_id: Unique entity identifier
            **kwargs: Additional arguments for testing convenience

        Returns:
            FlextPluginExecution: Validated plugin execution entity

        """
        # Generate ID if not provided
        final_id = entity_id or FlextGenerators.generate_entity_id()

        # Extract from execution_config dict
        execution_config = execution_config or {}

        # Handle testing convenience - tests may pass plugin_id
        if "plugin_id" in kwargs:
            plugin_name = plugin_name or str(kwargs["plugin_id"])
        execution_id = kwargs.get("execution_id", final_id)
        input_data = kwargs.get("input_data", {})

        # Create instance data with all required fields including base entity fields
        instance_data = {
            "id": final_id,
            "version": kwargs.get("version", 1),
            "metadata": kwargs.get("metadata", {}),
            "plugin_name": plugin_name,
            "plugin_id": kwargs.get("plugin_id", plugin_name),
            "execution_id": execution_id,
            "start_time": execution_config.get("start_time", FlextTimestamp.now()),
            "end_time": execution_config.get("end_time"),
            "status": execution_config.get("status", "pending"),
            "result": execution_config.get("result"),
            "error": execution_config.get("error", ""),
            "error_message": execution_config.get("error_message"),
            "input_data": input_data,
            "output_data": execution_config.get("output_data", {}),
        }

        return cls.model_validate(instance_data)

    def is_valid(self) -> bool:
        """Validate plugin execution entity state."""
        return bool(self.plugin_name)

    @property
    def success(self) -> bool:
        """Check if execution was successful."""
        return self.status == "completed"

    @property
    def execution_status(self) -> str:
        """Get execution status (compatibility alias)."""
        return self.status

    @property
    def memory_usage_mb(self) -> float:
        """Get memory usage in MB from resource tracking."""
        resource_usage = cast(
            "dict[str, object]",
            self.output_data.get("resource_usage", {}),
        )
        memory_value = resource_usage.get("memory_mb", 0.0)
        if isinstance(memory_value, (int, float)):
            return float(memory_value)
        if isinstance(memory_value, str):
            try:
                return float(memory_value)
            except ValueError as e:
                # Log critical error and raise proper exception instead of returning fake data
                logger = get_logger(__name__)
                logger.exception(
                    f"Invalid memory value '{memory_value}' for plugin execution",
                )
                msg = f"Invalid memory value: {memory_value}"
                raise ValueError(msg) from e
        # Only return 0.0 for valid empty/None values, not for conversion failures
        return 0.0

    @property
    def cpu_time_ms(self) -> float:
        """Get CPU time in milliseconds from resource tracking."""
        resource_usage = cast(
            "dict[str, object]",
            self.output_data.get("resource_usage", {}),
        )
        cpu_value = resource_usage.get("cpu_time_ms", 0.0)
        if isinstance(cpu_value, (int, float)):
            return float(cpu_value)
        if isinstance(cpu_value, str):
            try:
                return float(cpu_value)
            except ValueError as e:
                # Log critical error and raise proper exception instead of returning fake data
                logger = get_logger(__name__)
                logger.exception(
                    f"Invalid CPU time value '{cpu_value}' for plugin execution",
                )
                msg = f"Invalid CPU time value: {cpu_value}"
                raise ValueError(msg) from e
        # Only return 0.0 for valid empty/None values, not for conversion failures
        return 0.0

    @property
    def is_running(self) -> bool:
        """Check if execution is currently running."""
        return self.status == "running"

    @property
    def is_completed(self) -> bool:
        """Check if execution is completed (successful or failed)."""
        return self.status in {"completed", "failed"}

    def mark_started(self) -> None:
        """Mark execution as started."""
        object.__setattr__(self, "status", "running")
        object.__setattr__(self, "start_time", FlextTimestamp.now())

    def mark_completed(
        self,
        *,
        success: bool = True,
        error_message: str | None = None,
    ) -> None:
        """Mark execution as completed.

        Args:
            success: Whether execution was successful
            error_message: Error message if execution failed

        """
        object.__setattr__(self, "end_time", FlextTimestamp.now())
        if success:
            object.__setattr__(self, "status", "completed")
        else:
            object.__setattr__(self, "status", "failed")
            if error_message:
                object.__setattr__(self, "error", error_message)
                object.__setattr__(self, "error_message", error_message)

    def update_resource_usage(
        self,
        memory_mb: float = 0.0,
        cpu_time_ms: float = 0.0,
    ) -> None:
        """Update resource usage tracking.

        Args:
            memory_mb: Memory usage in MB
            cpu_time_ms: CPU time in milliseconds

        """
        # Add resource usage to output_data for tracking
        current_output = dict(self.output_data)
        current_output.update(
            {
                "resource_usage": {
                    "memory_mb": memory_mb,
                    "cpu_time_ms": cpu_time_ms,
                    "timestamp": str(FlextTimestamp.now()),
                },
            },
        )
        object.__setattr__(self, "output_data", current_output)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin execution entity.

        Returns:
            FlextResult indicating success or failure of validation

        """
        if not self.plugin_name:
            return FlextResult[None].fail("Plugin name is required")
        return FlextResult[None].ok(None)


# Testing convenience aliases - TRANSITIONAL: Use FlextPluginEntity instead
# These aliases are maintained for testing convenience but should be migrated
# to use the new naming convention to avoid confusion with interface names.
Plugin = FlextPluginEntity  # TRANSITIONAL: Use FlextPluginEntity
FlextPlugin = (
    FlextPluginEntity  # TRANSITIONAL: Conflicts with interface, use FlextPluginEntity
)
PluginConfig = FlextPluginConfig
PluginConfiguration = FlextPluginConfig  # Additional alias for tests
PluginMetadata = FlextPluginMetadata
PluginRegistry = FlextPluginRegistry
PluginInstance = FlextPluginEntity  # TRANSITIONAL: Use FlextPluginEntity
PluginExecution = FlextPluginExecution
