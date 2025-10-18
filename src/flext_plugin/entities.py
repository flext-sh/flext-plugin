"""FLEXT Plugin Entities - Generic extensible entity system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Generic entity system that can be extended for any domain through composition.
Uses advanced Python 3.13+ patterns, delegates to flext-core libraries, and eliminates code duplication.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Generic, TypeVar

from flext_core import FlextModels, FlextResult, FlextUtilities
from pydantic import Field, field_validator

# Generic type variables for maximum extensibility
T = TypeVar("T")


# Define base classes first to avoid forward reference issues
class _BaseEntity[T](FlextModels.Entity):
    """Generic base entity with comprehensive validation and lifecycle management."""

    # Core fields using Python 3.13+ features
    id: str = Field(description="Unique entity identifier")
    version: int = Field(default=1, description="Entity version for optimistic locking")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Extensible metadata"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Creation timestamp"
    )
    updated_at: datetime | None = Field(
        default=None, description="Last update timestamp"
    )

    # Generic domain data - extensible through composition
    domain_data: dict[str, T] = Field(
        default_factory=dict, description="Domain-specific data"
    )

    @classmethod
    def create(cls, *, entity_id: str | None = None, **kwargs: Any):
        """Generic factory method using advanced patterns."""
        final_id = entity_id or FlextUtilities.Generators.generate_entity_id()

        # Use walrus operator for efficiency
        instance_data = {
            "id": final_id,
            "version": (_version := kwargs.get("version", 1)),
            "metadata": kwargs.get("metadata", {}),
            "domain_data": kwargs.get("domain_data", {}),
            **kwargs,  # Allow arbitrary extension
        }

        return cls.model_validate(instance_data)

    def update_timestamp(self) -> None:
        """Update timestamp using walrus operator."""
        self.updated_at = datetime.now(UTC)

    def validate_business_rules(self) -> FlextResult[None]:
        """Generic validation delegating to domain-specific logic."""
        return FlextResult.ok(None)


class _BaseStatus(StrEnum):
    """Generic status enumeration with extensible patterns."""

    # Base statuses that work for any domain
    UNKNOWN = "unknown"
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DISABLED = "disabled"
    LOADING = "loading"
    ERROR = "error"

    @classmethod
    def operational_statuses(cls):
        """Get statuses representing operational states."""
        return [cls.ACTIVE, cls.HEALTHY, cls.COMPLETED]

    @classmethod
    def error_statuses(cls):
        """Get statuses representing error states."""
        return [cls.ERROR, cls.UNHEALTHY, cls.FAILED, cls.DISABLED]

    def is_operational(self) -> bool:
        """Check operational state using advanced pattern matching."""
        match self:
            case cls.ACTIVE | cls.HEALTHY | cls.COMPLETED:
                return True
            case _:
                return False

    def is_error_state(self) -> bool:
        """Check error state using pattern matching."""
        match self:
            case cls.ERROR | cls.UNHEALTHY | cls.FAILED | cls.DISABLED:
                return True
            case _:
                return False


class FlextPluginEntities:
    """Generic extensible entity system using advanced composition patterns.

    This class provides a unified, generic foundation that can be extended for any domain
    through composition rather than inheritance. Uses Python 3.13+ features for maximum efficiency.

    Key features:
    - Generic type system for domain extensibility
    - Advanced composition patterns reducing code duplication
    - Delegation to flext-core libraries following SOLID principles
    - Python 3.13+ syntax with walrus operator and pattern matching
    - Zero legacy code or fallbacks

    Usage:
        ```python
        from flext_plugin import FlextPluginEntities

        # Create any domain entity through composition
        plugin = FlextPluginEntities.Plugin.create(name="my-plugin")
        registry = FlextPluginEntities.Registry.create(name="my-registry")
        ```
    """

    # Expose base classes for composition
    Entity = _BaseEntity
    Status = _BaseStatus

    # Generic configuration entity with advanced validation
    class Config(_BaseEntity[dict[str, Any]]):
        """Generic configuration entity extensible for any domain."""

        # Core config fields - generic and extensible
        name: str = Field(description="Configuration name/identifier")
        enabled: bool = Field(
            default=True, description="Whether configuration is enabled"
        )
        settings: dict[str, Any] = Field(
            default_factory=dict, description="Configuration settings"
        )
        priority: int = Field(default=100, description="Configuration priority")

        # Resource limits - generic for any domain
        max_memory_mb: int = Field(default=512, description="Maximum memory in MB")
        max_cpu_percent: int = Field(default=50, description="Maximum CPU percentage")
        timeout_seconds: int = Field(default=30, description="Timeout in seconds")

        @field_validator("priority")
        @classmethod
        def validate_priority_range(cls, v: int) -> int:
            """Validate priority using advanced range checking."""
            if not (0 <= v <= 100):
                msg = "Priority must be between 0 and 100"
                raise ValueError(msg)
            return v

        @field_validator("max_memory_mb", "max_cpu_percent", "timeout_seconds")
        @classmethod
        def validate_positive_values(cls, v: int) -> int:
            """Generic positive value validation."""
            if v <= 0:
                msg = "Value must be positive"
                raise ValueError(msg)
            return v

        def validate_business_rules(self) -> FlextResult[None]:
            """Domain-agnostic validation delegating to field validators."""
            return FlextResult.ok(None)

    # Generic registry with advanced collection management
    class Registry(_BaseEntity[dict[str, T]], Generic[T]):
        """Generic registry for managing collections of any type."""

        name: str = Field(description="Registry identifier")
        items: dict[str, T] = Field(
            default_factory=dict, description="Registered items"
        )
        is_enabled: bool = Field(
            default=True, description="Whether registry is enabled"
        )

        # Generic counters using advanced typing
        item_count: int = Field(default=0, description="Number of registered items")
        error_count: int = Field(default=0, description="Number of errors")

        def register(self, item: T, key: str | None = None) -> FlextResult[None]:
            """Generic registration with error handling."""
            final_key = key or getattr(item, "name", getattr(item, "id", str(id(item))))

            if final_key in self.items:
                return FlextResult.fail(f"Item '{final_key}' already registered")

            self.items[final_key] = item
            self.item_count = len(self.items)
            self.update_timestamp()

            return FlextResult.ok(None)

        def unregister(self, key: str) -> FlextResult[T]:
            """Generic unregistration with return value."""
            if (item := self.items.pop(key, None)) is not None:
                self.item_count = len(self.items)
                self.update_timestamp()
                return FlextResult.ok(item)

            return FlextResult.fail(f"Item '{key}' not found")

        def get(self, key: str) -> T | None:
            """Generic item retrieval."""
            return self.items.get(key)

        def list_items(self) -> list[T]:
            """List all registered items."""
            return list(self.items.values())

        def validate_business_rules(self) -> FlextResult[None]:
            """Generic registry validation."""
            if not self.name:
                return FlextResult.fail("Registry name is required")
            return FlextResult.ok(None)

    # Generic execution entity with advanced state management
    class Execution(_BaseEntity[dict[str, Any]]):
        """Generic execution entity for tracking any kind of execution."""

        # Core execution fields
        execution_id: str = Field(description="Unique execution identifier")
        status: _BaseStatus = Field(
            default=_BaseStatus.PENDING, description="Execution status"
        )
        start_time: str = Field(
            default_factory=FlextUtilities.Generators.generate_iso_timestamp,
            description="Start timestamp",
        )
        end_time: datetime | None = Field(
            default=None, description="Completion timestamp"
        )

        # Input/output data - generic for any domain
        input_data: dict[str, Any] = Field(
            default_factory=dict, description="Execution input"
        )
        output_data: dict[str, Any] = Field(
            default_factory=dict, description="Execution output"
        )

        # Results and errors
        result: Any = Field(default=None, description="Execution result")
        error: str = Field(default="", description="Error message")

        # Performance metrics
        execution_time: float = Field(
            default=0.0, description="Execution duration in seconds"
        )

        @property
        def is_running(self) -> bool:
            """Check if execution is running."""
            return self.status == _BaseStatus.LOADING

        @property
        def is_completed(self) -> bool:
            """Check if execution is completed."""
            return self.status in {_BaseStatus.COMPLETED, _BaseStatus.FAILED}

        def mark_started(self) -> None:
            """Mark execution as started."""
            self.status = _BaseStatus.LOADING
            self.start_time = FlextUtilities.Generators.generate_iso_timestamp()

        def mark_completed(
            self, *, success: bool = True, error_message: str | None = None
        ) -> None:
            """Mark execution as completed using advanced patterns."""
            self.end_time = datetime.now(UTC)
            self.status = _BaseStatus.COMPLETED if success else _BaseStatus.FAILED

            if error_message and not success:
                self.error = error_message

        def update_resource_usage(
            self, memory_mb: float = 0.0, cpu_time_ms: float = 0.0
        ) -> None:
            """Update resource usage tracking."""
            self.output_data.update({
                "resource_usage": {
                    "memory_mb": memory_mb,
                    "cpu_time_ms": cpu_time_ms,
                    "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                }
            })

    # Domain-specific compositions - these extend the generic base through composition
    # Plugin-specific composition using the generic entities
    class Plugin(_BaseEntity[dict[str, Any]]):
        """Plugin entity composed from generic entities."""

        # Plugin-specific fields
        name: str = Field(description="Plugin name", min_length=1, max_length=100)
        version: str = Field(description="Plugin version", min_length=1, max_length=50)
        description: str = Field(default="", description="Plugin description")
        author: str = Field(default="", description="Plugin author")

        # Composed status and type using generic enums
        status: _BaseStatus = Field(default=_BaseStatus.INACTIVE)
        plugin_type: str = Field(default="utility", description="Plugin type")

        # Runtime metrics
        execution_count: int = Field(default=0, description="Execution count")
        error_count: int = Field(default=0, description="Error count")

        @classmethod
        def create(cls, *, name: str, version: str, **kwargs: Any):
            """Create plugin using generic factory with domain-specific logic."""
            return super().create(
                name=name,
                version=version,
                domain_data={"plugin_specific": kwargs},
                **kwargs,
            )

        def is_active(self) -> bool:
            """Check if plugin is active using generic status."""
            return self.status == _BaseStatus.ACTIVE

        def activate(self) -> bool:
            """Activate plugin."""
            if self.status == _BaseStatus.INACTIVE:
                self.status = _BaseStatus.ACTIVE
                return True
            return False

        def deactivate(self) -> bool:
            """Deactivate plugin."""
            if self.status == _BaseStatus.ACTIVE:
                self.status = _BaseStatus.INACTIVE
                return True
            return False

        def validate_business_rules(self) -> FlextResult[None]:
            """Domain-specific validation."""
            if not self.name or not self.version:
                return FlextResult.fail("Plugin name and version are required")
            return FlextResult.ok(None)

    # Plugin Registry composition
    class PluginRegistry(Registry[Plugin]):
        """Plugin registry composed from generic registry."""

        registry_url: str = Field(default="", description="Registry URL")
        requires_authentication: bool = Field(
            default=False, description="Authentication required"
        )
        trusted_publishers: list[str] = Field(
            default_factory=list, description="Trusted publishers"
        )

        @property
        def is_available(self) -> bool:
            """Check availability using composition."""
            return self.is_enabled and bool(self.registry_url)

    # Plugin Execution composition
    class PluginExecution(Execution):
        """Plugin execution composed from generic execution."""

        plugin_name: str = Field(description="Plugin name")
        plugin_id: str = Field(description="Plugin identifier")

        @property
        def memory_usage_mb(self) -> float:
            """Get memory usage with advanced error handling."""
            if resource_usage := self.output_data.get("resource_usage"):
                return float(resource_usage.get("memory_mb", 0.0))
            return 0.0

        @property
        def cpu_time_ms(self) -> float:
            """Get CPU time with advanced error handling."""
            if resource_usage := self.output_data.get("resource_usage"):
                return float(resource_usage.get("cpu_time_ms", 0.0))
            return 0.0


__all__ = ["FlextPluginEntities"]
