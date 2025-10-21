"""FLEXT Plugin Domain Entities - Domain-Driven Design patterns for plugin system.

This module provides domain entities following Domain-Driven Design patterns with
Pydantic v2 validation. Entities represent core plugin domain concepts with identity
and lifecycle.

Architecture Layer: 1 (Domain)
=============================
Domain layer with pure business logic, no infrastructure dependencies.

Domain Concepts:
- Plugin: Core plugin entity with identity and lifecycle
- PluginRegistry: Aggregate root managing collection of plugins
- Domain Events: Significant domain occurrences

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, ClassVar, Self, TypeVar
from uuid import uuid4

from flext_core import FlextModels, FlextResult
from pydantic import ConfigDict, Field

T = TypeVar("T")

# Constants
SEMANTIC_VERSION_PARTS = 3


class FlextPluginEntities:
    """Domain entities for plugin system following Domain-Driven Design patterns.

    Provides core domain entities with Pydantic validation and FlextResult error
    handling. All entities follow railway-oriented programming patterns and are
    designed for composition and extensibility.

    Nested Classes:
    ===============
    - Plugin: Core plugin entity with lifecycle (Entity pattern)
    - PluginConfig: Plugin configuration value object (Value pattern)
    - PluginMetadata: Plugin metadata value object (Value pattern)
    - PluginRegistry: Collection aggregate root (AggregateRoot pattern)
    - DomainEvents: Significant plugin domain events (Event pattern)

    Architecture: Layer 1 (Domain)
    =============================
    Pure business logic with no infrastructure dependencies. Uses Pydantic v2
    validation and FlextCore patterns for type safety and error handling.

    Features:
    =========
    - Identity-based equality for entities
    - Immutable value objects with frozen Pydantic models
    - Aggregate root for consistency boundaries
    - Domain events for event sourcing
    - FlextResult[T] for composable error handling
    - 100% type safety with Pyrefly strict mode

    """

    # ========================================================================
    # VALUE OBJECTS - Immutable domain values
    # ========================================================================

    class PluginConfig(FlextModels.Value):
        """Plugin configuration value object - immutable configuration.

        Value object representing plugin configuration. Immutable after creation,
        compared by value, and hashable for use in collections.

        Attributes:
        name: Plugin name (unique identifier in registry)
        plugin_version: Plugin semantic version
        enabled: Whether plugin is enabled
        metadata: Additional configuration metadata
        tags: Classification tags for plugin discovery

        """

        name: str = Field(
            description="Plugin name (unique in registry)",
            min_length=1,
            max_length=255,
        )
        plugin_version: str = Field(
            description="Plugin semantic version (e.g., '1.0.0')",
            min_length=1,
            max_length=50,
        )
        enabled: bool = Field(default=True, description="Whether plugin is enabled")
        metadata: dict[str, Any] = Field(
            default_factory=dict,
            description="Additional configuration metadata",
        )
        tags: list[str] = Field(
            default_factory=list,
            description="Classification tags for discovery",
        )

        model_config: ClassVar[ConfigDict] = {
            "frozen": True,
            "validate_assignment": True,
        }

    class PluginMetadata(FlextModels.Value):
        """Plugin metadata value object - immutable plugin information.

        Represents read-only plugin information including description, author,
        and plugin type classification.

        Attributes:
        description: Human-readable plugin description
        author: Plugin author/maintainer
        plugin_type: Plugin type classification
        created_at: Creation timestamp
        updated_at: Last update timestamp

        """

        description: str = Field(
            default="",
            description="Human-readable plugin description",
        )
        author: str = Field(default="", description="Plugin author/maintainer")
        plugin_type: str = Field(
            default="extension",
            description="Plugin type (extension, service, middleware, etc.)",
        )
        created_at: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Creation timestamp",
        )
        updated_at: datetime | None = Field(
            default=None,
            description="Last update timestamp",
        )

        model_config: ClassVar[ConfigDict] = {
            "frozen": True,
            "validate_assignment": True,
        }

    class PluginExecutionResult(FlextModels.Value):
        """Plugin execution result value object - immutable execution outcome.

        Represents the result of plugin execution with status and outcome data.

        Attributes:
        success: Whether execution succeeded
        result_data: Execution result data
        error_message: Error message if execution failed
        execution_time_ms: Execution time in milliseconds

        """

        success: bool = Field(description="Whether execution succeeded")
        result_data: dict[str, Any] = Field(
            default_factory=dict,
            description="Execution result data",
        )
        error_message: str = Field(
            default="",
            description="Error message if execution failed",
        )
        execution_time_ms: float = Field(
            ge=0,
            description="Execution time in milliseconds",
        )

        model_config: ClassVar[ConfigDict] = {
            "frozen": True,
            "validate_assignment": True,
        }

    # ========================================================================
    # ENTITIES - Domain objects with identity and lifecycle
    # ========================================================================

    class Plugin(FlextModels.Entity):
        """Plugin entity - core domain entity with identity and lifecycle.

        Represents a plugin with identity (id), lifecycle (created_at, updated_at),
        and mutable state. Compared by identity (id), not by value.

        Attributes:
        id: Unique plugin identifier
        config: Plugin configuration (PluginConfig value object)
        metadata: Plugin metadata (PluginMetadata value object)
        status: Plugin status (discovered, loaded, active, etc.)
        created_at: Entity creation timestamp
        updated_at: Last entity update timestamp
        domain_data: Extensible domain-specific data

        """

        config: FlextPluginEntities.PluginConfig = Field(
            description="Plugin configuration"
        )
        metadata: FlextPluginEntities.PluginMetadata = Field(
            description="Plugin metadata"
        )
        status: str = Field(
            default="discovered",
            description="Plugin status (discovered, loaded, active, failed, etc.)",
        )
        created_at: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Creation timestamp",
        )
        updated_at: datetime | None = Field(
            default=None,
            description="Last update timestamp",
        )
        domain_data: dict[str, Any] = Field(
            default_factory=dict,
            description="Extensible domain-specific data for composition",
        )

        @classmethod
        def create(
            cls,
            *,
            name: str,
            plugin_version: str,
            config: FlextPluginEntities.PluginConfig | None = None,
            metadata: FlextPluginEntities.PluginMetadata | None = None,
            entity_id: str | None = None,
        ) -> Self:
            """Factory method to create a new Plugin entity.

            Args:
            name: Plugin name
            plugin_version: Plugin version
            config: Plugin configuration (auto-created if None)
            metadata: Plugin metadata (auto-created if None)
            entity_id: Entity ID (auto-generated if None)

            Returns:
            New Plugin entity instance

            """
            final_id = entity_id or str(uuid4())
            final_config = config or FlextPluginEntities.PluginConfig(
                name=name,
                plugin_version=plugin_version,
            )
            final_metadata = metadata or FlextPluginEntities.PluginMetadata()

            return cls(
                id=final_id,
                config=final_config,
                metadata=final_metadata,
                status="discovered",
            )

        def update_status(self, new_status: str) -> FlextResult[None]:
            """Update plugin status following business rules.

            Valid status transitions:
            - discovered -> loaded -> active -> deactivated
            - any -> failed

            Args:
            new_status: New status value

            Returns:
            FlextResult indicating success or validation failure

            """
            valid_statuses = {
                "discovered",
                "loaded",
                "active",
                "deactivated",
                "failed",
            }
            if new_status not in valid_statuses:
                return FlextResult.fail(f"Invalid status: {new_status}")

            self.status = new_status
            self.updated_at = datetime.now(UTC)
            return FlextResult.ok(None)

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate plugin domain business rules.

            Business Rules:
            - Plugin name must not be empty
            - Plugin version must follow semantic versioning
            - Status must be valid

            Returns:
            FlextResult indicating validation success or failure

            """
            if not self.config.name.strip():
                return FlextResult.fail("Plugin name cannot be empty")

            # Basic semantic version validation (X.Y.Z)
            version_parts = self.config.plugin_version.split(".")
            if len(version_parts) != SEMANTIC_VERSION_PARTS or not all(
                p.isdigit() for p in version_parts
            ):
                return FlextResult.fail(
                    f"Invalid semantic version: {self.config.plugin_version}",
                )

            valid_statuses = {
                "discovered",
                "loaded",
                "active",
                "deactivated",
                "failed",
            }
            if self.status not in valid_statuses:
                return FlextResult.fail(f"Invalid plugin status: {self.status}")

            return FlextResult.ok(None)

    # ========================================================================
    # AGGREGATE ROOTS - Consistency boundaries
    # ========================================================================

    class PluginRegistry(FlextModels.AggregateRoot):
        """Plugin registry aggregate root - manages plugin collection.

        Aggregate root for plugin lifecycle management and consistency boundary.
        Enforces transactional invariants for plugin registry operations.

        Attributes:
        id: Registry identifier
        name: Registry name
        plugins: Managed plugin collection (keyed by plugin name)
        created_at: Registry creation timestamp
        updated_at: Last update timestamp

        """

        name: str = Field(description="Registry name")
        plugins: dict[str, FlextPluginEntities.Plugin] = Field(
            default_factory=dict,
            description="Plugin collection keyed by name",
        )
        created_at: datetime = Field(
            default_factory=lambda: datetime.now(UTC),
            description="Creation timestamp",
        )
        updated_at: datetime | None = Field(
            default=None,
            description="Last update timestamp",
        )

        @classmethod
        def create(cls, *, name: str, registry_id: str | None = None) -> Self:
            """Factory method to create a new PluginRegistry.

            Args:
            name: Registry name
            registry_id: Registry ID (auto-generated if None)

            Returns:
            New PluginRegistry instance

            """
            return cls(id=registry_id or str(uuid4()), name=name)

        def register_plugin(
            self, plugin: FlextPluginEntities.Plugin
        ) -> FlextResult[None]:
            """Register a plugin in the registry.

            Business Rules:
            - Plugin name must not already exist in registry
            - Plugin must pass business rule validation

            Args:
            plugin: Plugin to register

            Returns:
            FlextResult indicating success or conflict/validation failure

            """
            # Validate plugin business rules
            validation = plugin.validate_business_rules()
            if validation.is_failure:
                return validation

            # Check for duplicate plugin names
            if plugin.config.name in self.plugins:
                return FlextResult.fail(
                    f"Plugin '{plugin.config.name}' already registered",
                )

            # Register plugin
            self.plugins[plugin.config.name] = plugin
            self.updated_at = datetime.now(UTC)
            return FlextResult.ok(None)

        def unregister_plugin(
            self, plugin_name: str
        ) -> FlextResult[FlextPluginEntities.Plugin | None]:
            """Unregister a plugin from the registry.

            Args:
            plugin_name: Name of plugin to unregister

            Returns:
            FlextResult with unregistered plugin or failure if not found

            """
            if plugin_name not in self.plugins:
                return FlextResult.fail(f"Plugin '{plugin_name}' not registered")

            plugin = self.plugins.pop(plugin_name)
            self.updated_at = datetime.now(UTC)
            return FlextResult.ok(plugin)

        def get_plugin(
            self, plugin_name: str
        ) -> FlextResult[FlextPluginEntities.Plugin | None]:
            """Retrieve a plugin from the registry.

            Args:
            plugin_name: Name of plugin to retrieve

            Returns:
            FlextResult with plugin or None if not found

            """
            plugin = self.plugins.get(plugin_name)
            if not plugin:
                return FlextResult.fail(f"Plugin '{plugin_name}' not found")
            return FlextResult.ok(plugin)

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate registry business rules.

            Business Rules:
            - Registry name must not be empty
            - All contained plugins must be valid

            Returns:
            FlextResult indicating validation success or failure

            """
            if not self.name.strip():
                return FlextResult.fail("Registry name cannot be empty")

            # Validate all plugins
            for plugin in self.plugins.values():
                validation = plugin.validate_business_rules()
                if validation.is_failure:
                    return validation

            return FlextResult.ok(None)

    # ========================================================================
    # DOMAIN EVENTS - Event sourcing events
    # ========================================================================

    class DomainEvents:
        """Significant plugin domain events for event sourcing.

        Contains event classes representing important domain occurrences that can
        be persisted for audit trails and event replay.

        """

        class PluginRegistered(FlextModels.DomainEvent):
            """Event: Plugin was registered in the registry."""

            plugin_name: str = Field(description="Name of registered plugin")
            plugin_version: str = Field(description="Version of registered plugin")

        class PluginStatusChanged(FlextModels.DomainEvent):
            """Event: Plugin status changed."""

            plugin_name: str = Field(description="Name of plugin")
            old_status: str = Field(description="Previous status")
            new_status: str = Field(description="New status")

        class PluginExecuted(FlextModels.DomainEvent):
            """Event: Plugin execution completed."""

            plugin_name: str = Field(description="Name of executed plugin")
            success: bool = Field(description="Whether execution succeeded")
            execution_time_ms: float = Field(
                ge=0,
                description="Execution time in milliseconds",
            )

        class PluginUnregistered(FlextModels.DomainEvent):
            """Event: Plugin was unregistered from the registry."""

            plugin_name: str = Field(description="Name of unregistered plugin")
            plugin_version: str = Field(
                description="Version of unregistered plugin",
            )


__all__ = ["FlextPluginEntities"]
