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
    ...     config={"description": "Processes data efficiently"},
    ... )
    >>> result = plugin.activate()
    >>> if result.success():
    ...     print(f"Plugin {plugin.name} is now active")

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_core import FlextEntity, FlextEntityId, FlextResult
from flext_core.utilities import FlextGenerators
from pydantic import Field, field_validator

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
        ...         "author": "FLEXT Team",
        ...     },
        ... )
        >>> activation_result = plugin.activate()
        >>> if activation_result.success():
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

        # Handle backward compatibility for plugin_id in kwargs
        plugin_name = kwargs.get("plugin_id", name)

        # Initialize FlextEntity base with ONLY base fields
        super().__init__(id=final_entity_id)

        # Set business fields directly (frozen model workaround)
        object.__setattr__(self, "name", plugin_name)
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
    def plugin_status(self) -> str:
        """Get plugin status (compatibility) - returns value string."""
        return self.status.value

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
        return self.status == PluginStatus.HEALTHY

    # Execution tracking properties (for backward compatibility)
    @property
    def execution_count(self) -> int:
        """Get number of executions recorded."""
        # For backward compatibility, return a placeholder
        return getattr(self, "_execution_count", 0)

    @property
    def average_execution_time_ms(self) -> float:
        """Get average execution time in milliseconds."""
        # For backward compatibility, return a placeholder
        return getattr(self, "_average_execution_time_ms", 0.0)

    @property
    def last_execution(self) -> datetime | None:
        """Get timestamp of last execution."""
        # For backward compatibility, return a placeholder
        return getattr(self, "_last_execution", None)

    @property
    def error_count(self) -> int:
        """Get number of errors recorded."""
        # For backward compatibility, return a placeholder
        return getattr(self, "_error_count", 0)

    @property
    def last_error(self) -> str:
        """Get last error message."""
        # For backward compatibility, return a placeholder
        return getattr(self, "_last_error", "")

    @property
    def last_error_time(self) -> datetime | None:
        """Get timestamp of last error."""
        # For backward compatibility, return a placeholder
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
        object.__setattr__(self, "_last_execution", datetime.now(UTC))

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
        object.__setattr__(self, "_last_error_time", datetime.now(UTC))
        object.__setattr__(self, "status", PluginStatus.UNHEALTHY)

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

    # Pydantic fields
    plugin_name: str = Field(
        default="",
        description="Name of the plugin this config belongs to",
    )
    config_data: dict[str, object] = Field(
        default_factory=dict,
        description="Configuration data",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Last update timestamp",
    )

    # Configuration fields for backward compatibility
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

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        *,
        plugin_name: str = "",
        config_data: dict[str, object] | None = None,
        created_at: datetime | None = None,  # noqa: ARG002
        updated_at: datetime | None = None,
        enabled: bool = True,
        settings: dict[str, object] | None = None,
        dependencies: list[str] | None = None,
        priority: int = 100,
        max_memory_mb: int = 512,
        max_cpu_percent: int = 50,
        timeout_seconds: int = 30,
        **kwargs: object,  # noqa: ARG002
    ) -> None:
        """Initialize plugin configuration entity.

        Args:
            entity_id: Unique entity identifier
            plugin_name: Name of the plugin this config belongs to
            config_data: Configuration data
            created_at: Creation timestamp
            updated_at: Last update timestamp
            enabled: Whether plugin configuration is enabled
            settings: Plugin settings
            dependencies: Plugin dependencies
            priority: Plugin priority
            max_memory_mb: Maximum memory usage in MB
            max_cpu_percent: Maximum CPU usage percentage
            timeout_seconds: Timeout in seconds
            **kwargs: Additional keyword arguments for backward compatibility

        """
        # FlextEntity expects keyword argument 'id'
        final_id = entity_id or FlextGenerators.generate_entity_id()

        # Initialize FlextEntity base with ONLY base fields
        super().__init__(id=final_id)

        # Set business fields directly (frozen model workaround)
        object.__setattr__(self, "plugin_name", plugin_name)
        object.__setattr__(self, "config_data", config_data or {})
        object.__setattr__(self, "updated_at", updated_at or datetime.now(UTC))
        object.__setattr__(self, "enabled", enabled)
        object.__setattr__(self, "settings", settings or {})
        object.__setattr__(self, "dependencies", dependencies or [])
        object.__setattr__(self, "priority", priority)
        object.__setattr__(self, "max_memory_mb", max_memory_mb)
        object.__setattr__(self, "max_cpu_percent", max_cpu_percent)
        object.__setattr__(self, "timeout_seconds", timeout_seconds)

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
        object.__setattr__(self, "updated_at", datetime.now(UTC))

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

    # Additional fields for backward compatibility
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

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        *,
        plugin_name: str = "",
        metadata: dict[str, object] | None = None,
        name: str = "",
        entry_point: str = "",
        plugin_type: object = "",
        description: str = "",
        dependencies: list[str] | None = None,
        trusted: bool = False,
        homepage: str | None = None,
        repository: str | None = None,
        **kwargs: object,  # noqa: ARG002
    ) -> None:
        """Initialize plugin metadata entity.

        Args:
            entity_id: Unique entity identifier
            plugin_name: Name of the plugin this metadata belongs to
            metadata: Metadata dict containing tags, categories, URLs, license
            name: Plugin name (alias for plugin_name)
            entry_point: Plugin entry point
            plugin_type: Plugin type (PluginType enum or string)
            description: Plugin description
            dependencies: Plugin dependencies
            trusted: Whether plugin is trusted
            homepage: Plugin homepage (alias)
            repository: Plugin repository (alias)
            **kwargs: Additional keyword arguments for backward compatibility

        """
        # Import PluginType here to avoid circular imports

        # FlextEntity expects keyword argument 'id'
        final_id = entity_id or FlextGenerators.generate_entity_id()

        # Extract from metadata dict
        metadata = metadata or {}

        # Handle plugin_type conversion
        plugin_type_value = ""
        if hasattr(plugin_type, "value"):  # PluginType enum
            plugin_type_value = plugin_type.value
        elif isinstance(plugin_type, str):
            plugin_type_value = plugin_type

        # Use name parameter or fall back to plugin_name
        final_name = name or plugin_name

        # Extract values from metadata dict when not provided directly
        final_entry_point = entry_point or metadata.get("entry_point", "")
        final_description = description or metadata.get("description", "")

        # For FlextPluginMetadata, we need to use standard Pydantic initialization
        # to ensure validation works properly for required fields
        super().__init__(
            id=final_id,
            plugin_name=final_name,
            name=final_name,
            entry_point=final_entry_point,
            plugin_type=plugin_type_value,
            description=final_description,
            dependencies=dependencies or [],
            trusted=trusted,
            homepage=homepage,
            repository=repository,
            tags=metadata.get("tags", []),
            categories=metadata.get("categories", []),
            homepage_url=metadata.get("homepage_url", ""),
            documentation_url=metadata.get("documentation_url", ""),
            repository_url=metadata.get("repository_url", ""),
            license_info=metadata.get("license_info", ""),
        )

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
        if v is not None and v != "" and not v.strip():
            msg = "Plugin entry point cannot be empty"
            raise ValueError(msg)
        return v

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

    # Pydantic fields
    name: str = Field(default="", description="Registry name")
    plugins: dict[str, FlextPlugin] = Field(
        default_factory=dict,
        description="Dictionary of registered plugins",
    )

    # Registry configuration fields for backward compatibility
    registry_url: str = Field(default="", description="Registry URL")
    is_enabled: bool = Field(default=True, description="Whether registry is enabled")
    plugin_count: int = Field(default=0, description="Number of plugins in registry")
    sync_error_count: int = Field(default=0, description="Number of sync errors")
    last_sync: datetime | None = Field(default=None, description="Last sync timestamp")

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

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        *,
        name: str = "",
        plugins: dict[str, FlextPlugin] | None = None,
        created_at: datetime | None = None,  # noqa: ARG002
        registry_url: str = "",
        is_enabled: bool = True,
        plugin_count: int = 0,
        sync_error_count: int = 0,
        last_sync: datetime | None = None,
        requires_authentication: bool = False,
        api_key: str = "",
        verify_signatures: bool = False,
        trusted_publishers: list[str] | None = None,
        **kwargs: object,  # noqa: ARG002
    ) -> None:
        """Initialize plugin registry entity.

        Args:
            entity_id: Unique entity identifier
            name: Registry name
            plugins: Dictionary of registered plugins (name -> plugin)
            created_at: Creation timestamp
            registry_url: Registry URL
            is_enabled: Whether registry is enabled
            plugin_count: Number of plugins in registry
            sync_error_count: Number of sync errors
            last_sync: Last sync timestamp
            requires_authentication: Whether authentication is required
            api_key: API key for authentication
            verify_signatures: Whether to verify signatures
            trusted_publishers: List of trusted publishers
            **kwargs: Additional keyword arguments for backward compatibility

        """
        # FlextEntity expects keyword argument 'id'
        final_id = entity_id or FlextGenerators.generate_entity_id()

        # Initialize FlextEntity base with ONLY base fields
        super().__init__(id=final_id)

        # Set business fields directly (frozen model workaround)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "plugins", plugins or {})
        object.__setattr__(self, "registry_url", registry_url)
        object.__setattr__(self, "is_enabled", is_enabled)
        object.__setattr__(self, "plugin_count", plugin_count)
        object.__setattr__(self, "sync_error_count", sync_error_count)
        object.__setattr__(self, "last_sync", last_sync)
        object.__setattr__(self, "requires_authentication", requires_authentication)
        object.__setattr__(self, "api_key", api_key)
        object.__setattr__(self, "verify_signatures", verify_signatures)
        object.__setattr__(self, "trusted_publishers", trusted_publishers or [])

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
        object.__setattr__(self, "last_sync", datetime.now(UTC))

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
    start_time: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
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

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        *,
        plugin_name: str = "",
        execution_config: dict[str, object] | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize plugin execution entity.

        Args:
            entity_id: Unique entity identifier
            plugin_name: Name of the plugin being executed
            execution_config: Execution configuration dictionary
            **kwargs: Additional keyword arguments for backward compatibility

        """
        # FlextEntity expects keyword argument 'id'
        final_id = entity_id or FlextGenerators.generate_entity_id()

        # Extract from execution_config dict
        execution_config = execution_config or {}

        # Initialize FlextEntity base with ONLY base fields
        super().__init__(id=final_id)

        # Handle backward compatibility - tests may pass plugin_id
        if "plugin_id" in kwargs:
            plugin_name = plugin_name or kwargs["plugin_id"]
        execution_id = kwargs.get("execution_id", final_id)
        input_data = kwargs.get("input_data", {})

        # Set business fields directly (frozen model workaround)
        object.__setattr__(self, "plugin_name", plugin_name)
        object.__setattr__(self, "plugin_id", kwargs.get("plugin_id", plugin_name))
        object.__setattr__(self, "execution_id", execution_id)
        object.__setattr__(
            self,
            "start_time",
            execution_config.get("start_time", datetime.now(UTC)),
        )
        object.__setattr__(self, "end_time", execution_config.get("end_time"))
        object.__setattr__(self, "status", execution_config.get("status", "pending"))
        object.__setattr__(self, "result", execution_config.get("result"))
        object.__setattr__(self, "error", execution_config.get("error", ""))
        object.__setattr__(self, "error_message", execution_config.get("error_message"))
        object.__setattr__(self, "input_data", input_data)
        object.__setattr__(self, "output_data", execution_config.get("output_data", {}))

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
        resource_usage = self.output_data.get("resource_usage", {})
        return resource_usage.get("memory_mb", 0.0)

    @property
    def cpu_time_ms(self) -> float:
        """Get CPU time in milliseconds from resource tracking."""
        resource_usage = self.output_data.get("resource_usage", {})
        return resource_usage.get("cpu_time_ms", 0.0)

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
        object.__setattr__(self, "start_time", datetime.now(UTC))

    def mark_completed(
        self,
        success: bool = True,
        error_message: str | None = None,
    ) -> None:
        """Mark execution as completed.

        Args:
            success: Whether execution was successful
            error_message: Error message if execution failed

        """
        object.__setattr__(self, "end_time", datetime.now(UTC))
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
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            },
        )
        object.__setattr__(self, "output_data", current_output)

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
