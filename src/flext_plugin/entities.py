"""FLEXT Plugin Entities - Plugin domain entities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Self, cast

from flext_core import FlextLogger, FlextModels, FlextResult, FlextTypes, FlextUtilities
from pydantic import Field, field_validator

from flext_plugin.config import FlextPluginConfig
from flext_plugin.constants import FlextPluginConstants
from flext_plugin.types import FlextPluginTypes


class FlextPluginEntities:
    """Unified container for all plugin domain entities following flext standards.

    This class contains all domain entities for the plugin system, following the
    [Project][Module] pattern where each entity is a nested class within the main
    FlextPluginEntities class.

    Usage:
        ```python
        from flext_plugin import FlextPluginEntities

        # Create plugin entity
        plugin = FlextPluginEntities.Plugin.create(
            name="my-plugin", plugin_version="1.0.0"
        )

        # Create plugin config
        config = FlextPluginEntities.Config.create(
            plugin_name="my-plugin", config_data={"setting": "value"}
        )
        ```
    """

    class PluginStatus(StrEnum):
        """Plugin lifecycle and operational status enumeration."""

        UNKNOWN = FlextPluginConstants.Lifecycle.STATUS_UNKNOWN
        DISCOVERED = FlextPluginConstants.Lifecycle.STATUS_DISCOVERED
        LOADED = FlextPluginConstants.Lifecycle.STATUS_LOADED
        ACTIVE = FlextPluginConstants.Lifecycle.STATUS_ACTIVE
        INACTIVE = FlextPluginConstants.Lifecycle.STATUS_INACTIVE
        LOADING = FlextPluginConstants.Lifecycle.STATUS_LOADING
        ERROR = FlextPluginConstants.Lifecycle.STATUS_ERROR
        DISABLED = FlextPluginConstants.Lifecycle.STATUS_DISABLED
        HEALTHY = FlextPluginConstants.Lifecycle.STATUS_HEALTHY
        UNHEALTHY = FlextPluginConstants.Lifecycle.STATUS_UNHEALTHY

        @classmethod
        def get_operational_statuses(cls) -> list[Self]:
            """Get statuses representing operational states."""
            return [cls.ACTIVE, cls.HEALTHY, cls.LOADED]

        @classmethod
        def get_error_statuses(cls) -> list[Self]:
            """Get statuses representing error states."""
            return [cls.ERROR, cls.UNHEALTHY, cls.DISABLED]

        def is_operational(self) -> bool:
            """Check if status represents operational state."""
            return self in self.get_operational_statuses()

        def is_error_state(self) -> bool:
            """Check if status represents error state."""
            return self in self.get_error_statuses()

    class PluginType(StrEnum):
        """Plugin type classification for platform organization."""

        # Singer ETL Types
        TAP = FlextPluginConstants.Types.TYPE_TAP
        TARGET = FlextPluginConstants.Types.TYPE_TARGET
        TRANSFORM = FlextPluginConstants.Types.TYPE_TRANSFORM

        # Architecture Types
        EXTENSION = FlextPluginConstants.Types.TYPE_EXTENSION
        SERVICE = FlextPluginConstants.Types.TYPE_SERVICE
        MIDDLEWARE = FlextPluginConstants.Types.TYPE_MIDDLEWARE
        TRANSFORMER = FlextPluginConstants.Types.TYPE_TRANSFORMER

        # Integration Types
        API = FlextPluginConstants.Types.TYPE_API
        DATABASE = FlextPluginConstants.Types.TYPE_DATABASE
        NOTIFICATION = FlextPluginConstants.Types.TYPE_NOTIFICATION
        AUTHENTICATION = FlextPluginConstants.Types.TYPE_AUTHENTICATION
        AUTHORIZATION = FlextPluginConstants.Types.TYPE_AUTHORIZATION

        # Utility Types
        UTILITY = FlextPluginConstants.Types.TYPE_UTILITY
        TOOL = FlextPluginConstants.Types.TYPE_TOOL
        HANDLER = FlextPluginConstants.Types.TYPE_HANDLER
        PROCESSOR = FlextPluginConstants.Types.TYPE_PROCESSOR

        # Additional Types
        CORE = FlextPluginConstants.Types.TYPE_CORE
        ADDON = FlextPluginConstants.Types.TYPE_ADDON
        THEME = FlextPluginConstants.Types.TYPE_THEME
        LANGUAGE = FlextPluginConstants.Types.TYPE_LANGUAGE

        @classmethod
        def get_etl_types(cls) -> list[Self]:
            """Get ETL-related plugin types."""
            return [cls.TAP, cls.TARGET, cls.TRANSFORM]

        @classmethod
        def get_architectural_types(cls) -> list[Self]:
            """Get architectural plugin types."""
            return [cls.EXTENSION, cls.SERVICE, cls.MIDDLEWARE, cls.TRANSFORMER]

        def is_etl_plugin(self) -> bool:
            """Check if this is an ETL plugin type."""
            return self in self.get_etl_types()

        def is_architectural_plugin(self) -> bool:
            """Check if this is an architectural plugin type."""
            return self in self.get_architectural_types()

    class Config(FlextModels.Entity):
        """Plugin configuration entity for managing plugin settings and parameters."""

        # Pydantic fields
        plugin_name: str = Field(
            default="",
            description="Name of the plugin this config belongs to",
        )
        config_data: FlextPluginTypes.Core.ConfigDict = Field(
            default_factory=dict,
            description="Plugin configuration data",
        )
        enabled: bool = Field(default=True, description="Whether plugin is enabled")
        settings: FlextPluginTypes.Core.SettingsDict = Field(
            default_factory=dict,
            description="Plugin settings",
        )
        dependencies: FlextPluginTypes.Core.StringList = Field(
            default_factory=list,
            description="Plugin dependencies",
        )
        priority: int = Field(default=100, description="Plugin execution priority")
        max_memory_mb: int = Field(
            default=512, description="Maximum memory usage in MB"
        )
        max_cpu_percent: int = Field(
            default=50, description="Maximum CPU usage percentage"
        )
        timeout_seconds: int = Field(default=30, description="Plugin execution timeout")
        created_at: datetime = Field(
            default_factory=datetime.now,
            description="Configuration creation timestamp",
        )
        updated_at: datetime | None = Field(
            default=None,
            description="Configuration last update timestamp",
        )

        @classmethod
        def create(
            cls,
            *,
            plugin_name: str,
            entity_id: str | None = None,
            config_data: FlextPluginTypes.Core.ConfigDict | None = None,
            **kwargs: object,
        ) -> FlextPluginEntities.Config:
            """Create plugin config entity with proper validation."""
            entity_id = entity_id or FlextUtilities.Generators.generate_entity_id()

            # Create instance data
            instance_data: FlextPluginTypes.Core.PluginDict = {
                "id": entity_id,
                "version": kwargs.get("version", 1),
                "metadata": kwargs.get("entity_metadata", {}),
                "plugin_name": plugin_name,
                "config_data": config_data or {},
                "enabled": kwargs.get("enabled", True),
                "settings": kwargs.get("settings", {}),
                "dependencies": kwargs.get("dependencies", []),
                "priority": kwargs.get("priority", 100),
                "max_memory_mb": kwargs.get(
                    "max_memory_mb", FlextPluginConfig.Performance().max_memory_mb
                ),
                "max_cpu_percent": kwargs.get(
                    "max_cpu_percent", FlextPluginConfig.Performance().max_cpu_percent
                ),
                "timeout_seconds": kwargs.get(
                    "timeout_seconds", FlextPluginConfig.Security().max_execution_time
                ),
                "created_at": kwargs.get("created_at", datetime.now(UTC)),
                "updated_at": kwargs.get("updated_at"),
            }

            return cls.model_validate(instance_data)

        def is_valid(self) -> bool:
            """Validate plugin config entity state."""
            return bool(self.plugin_name)

        def update_timestamp(self) -> None:
            """Update the updated_at timestamp."""
            setattr(self, "updated_at", datetime.now(UTC))

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate domain rules for plugin config entity."""
            if not self.plugin_name or not self.plugin_name.strip():
                return FlextResult[None].fail(
                    "Plugin name is required and cannot be empty"
                )
            if self.max_memory_mb <= 0:
                return FlextResult[None].fail("Maximum memory must be positive")
            if (
                self.max_cpu_percent < 0
                or self.max_cpu_percent
                > FlextPluginConstants.Performance.MAX_CPU_PERCENTAGE
            ):
                return FlextResult[None].fail(
                    "CPU percentage must be between 0 and 100"
                )
            if self.timeout_seconds <= 0:
                return FlextResult[None].fail("Timeout must be positive")
            return FlextResult[None].ok(None)

    class Plugin(FlextModels.Entity):
        """Rich plugin domain entity with comprehensive business logic and lifecycle management.

        Core domain entity representing a plugin within the FLEXT ecosystem.
        This is a DOMAIN ENTITY, not a plugin implementation. It encapsulates
        plugin identity, metadata, configuration, and business rules while
        maintaining consistency with Domain-Driven Design principles.
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
        status: FlextPluginEntities.PluginStatus = Field(
            alias="status",
            default=FlextPluginConstants.Lifecycle.STATUS_INACTIVE,
            description="Current plugin lifecycle and operational status",
        )
        plugin_type: FlextPluginEntities.PluginType = Field(
            alias="plugin_type",
            default=FlextPluginConstants.Types.TYPE_UTILITY,
            description="Plugin category and type for classification",
        )
        created_at: datetime = Field(
            default_factory=datetime.now,
            description="Plugin creation timestamp",
        )

        @classmethod
        def create(
            cls,
            *,
            name: str,
            plugin_version: str,
            entity_id: str | None = None,
            config: FlextPluginTypes.Core.ConfigDict | None = None,
            **kwargs: object,
        ) -> FlextPluginEntities.Plugin:
            """Create plugin entity with proper validation.

            Args:
                name: Plugin name (required)
                plugin_version: Plugin version (required)
                entity_id: Unique entity identifier
                config: Configuration dict[str, object] containing description, author, etc.
                **kwargs: Additional arguments for testing convenience

            Returns:
                FlextPluginEntities.Plugin: Validated plugin entity

            """
            # Generate ID if not provided
            entity_id = entity_id or FlextUtilities.Generators.generate_entity_id()

            # Extract config values
            config = config or {}

            # Create instance data
            instance_data: FlextPluginTypes.Core.PluginDict = {
                "id": entity_id,
                "version": kwargs.get("entity_version", 1),
                "metadata": kwargs.get("metadata", {}),
                "name": name,
                "plugin_version": plugin_version,
                "description": config.get("description", kwargs.get("description", "")),
                "author": config.get("author", kwargs.get("author", "")),
                "status": config.get(
                    "status",
                    kwargs.get(
                        "status", FlextPluginConstants.Lifecycle.STATUS_INACTIVE
                    ),
                ),
                "plugin_type": config.get(
                    "plugin_type",
                    kwargs.get("plugin_type", FlextPluginConstants.Types.TYPE_UTILITY),
                ),
            }

            return cls.model_validate(instance_data)

        # Testing convenience properties

        def is_valid(self) -> bool:
            """Validate plugin entity state."""
            return bool(self.name and self.plugin_version)

        def activate(self) -> bool:
            """Activate the plugin."""
            if self.status in {
                FlextPluginConstants.Lifecycle.STATUS_INACTIVE,
                FlextPluginConstants.Lifecycle.STATUS_INACTIVE.value,
            }:
                setattr(self, "status", FlextPluginConstants.Lifecycle.STATUS_ACTIVE)
                return True
            return False

        def deactivate(self) -> bool:
            """Deactivate the plugin."""
            if self.status in {
                FlextPluginConstants.Lifecycle.STATUS_ACTIVE,
                FlextPluginConstants.Lifecycle.STATUS_HEALTHY,
            }:
                setattr(self, "status", FlextPluginConstants.Lifecycle.STATUS_INACTIVE)
                return True
            return False

        def is_active(self) -> bool:
            """Check if plugin is active."""
            return self.status in {
                FlextPluginEntities.PluginStatus.ACTIVE,
                FlextPluginEntities.PluginStatus.ACTIVE.value,
            }

        def record_execution(
            self,
            execution_time_ms: float,
            *,
            success: bool = True,
        ) -> None:
            """Record plugin execution for metrics tracking."""
            current_count = getattr(self, "_execution_count", 0)
            current_avg = getattr(self, "_average_execution_time_ms", 0.0)

            new_count = current_count + 1
            new_avg = ((current_avg * current_count) + execution_time_ms) / new_count

            setattr(self, "_execution_count", new_count)
            setattr(self, "_average_execution_time_ms", new_avg)
            setattr(
                self,
                "_last_execution",
                FlextUtilities.Generators.generate_iso_timestamp(),
            )

            if not success:
                setattr(self, "status", FlextPluginEntities.PluginStatus.UNHEALTHY)

        def record_error(self, error_message: str) -> None:
            """Record plugin error for tracking."""
            current_error_count = getattr(self, "_error_count", 0)

            setattr(self, "_error_count", current_error_count + 1)
            setattr(self, "_last_error", error_message)
            setattr(
                self,
                "_last_error_time",
                FlextUtilities.Generators.generate_iso_timestamp(),
            )
            setattr(self, "status", FlextPluginEntities.PluginStatus.UNHEALTHY)

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate domain rules for plugin entity."""
            if not self.name or not self.name.strip():
                return FlextResult[None].fail(
                    "Plugin name is required and cannot be empty"
                )
            if not self.plugin_version or not self.plugin_version.strip():
                return FlextResult[None].fail(
                    "Plugin version is required and cannot be empty",
                )
            return FlextResult[None].ok(None)

    class Metadata(FlextModels.Entity):
        """Plugin metadata entity containing additional plugin information."""

        # Pydantic fields for the entity
        plugin_name: str = Field(
            default="",
            description="Name of the plugin this metadata belongs to",
        )
        tags: FlextTypes.StringList = Field(
            default_factory=list,
            description="Plugin tags for categorization",
        )
        categories: FlextTypes.StringList = Field(
            default_factory=list,
            description="Plugin categories",
        )
        homepage_url: str = Field(default="", description="Plugin homepage URL")
        documentation_url: str = Field(
            default="", description="Plugin documentation URL"
        )
        repository_url: str = Field(default="", description="Plugin repository URL")
        license_info: str = Field(default="", description="Plugin license information")

        # Additional fields for testing convenience
        name: str = Field(
            min_length=1, description="Plugin name (alias for plugin_name)"
        )
        entry_point: str = Field(min_length=1, description="Plugin entry point")
        plugin_type: str = Field(default="", description="Plugin type")
        description: str = Field(default="", description="Plugin description")
        dependencies: FlextPluginTypes.Core.StringList = Field(
            default_factory=list,
            description="Plugin dependencies",
        )
        trusted: bool = Field(default=False, description="Whether plugin is trusted")
        homepage: str | None = Field(
            default=None, description="Plugin homepage (alias)"
        )
        repository: str | None = Field(
            default=None,
            description="Plugin repository (alias)",
        )
        created_at: datetime = Field(
            default_factory=datetime.now,
            description="Metadata creation timestamp",
        )

        @classmethod
        def create(
            cls,
            *,
            name: str,
            entry_point: str,
            entity_id: str | None = None,
            **kwargs: object,
        ) -> FlextPluginEntities.Metadata:
            """Create plugin metadata entity with proper validation."""
            entity_id = entity_id or FlextUtilities.Generators.generate_entity_id()

            # Create instance data
            instance_data: FlextPluginTypes.Core.PluginDict = {
                "id": entity_id,
                "version": kwargs.get("version", 1),
                "metadata": kwargs.get("entity_metadata", {}),
                "plugin_name": name,
                "name": name,
                "entry_point": entry_point,
                "plugin_type": kwargs.get("plugin_type", ""),
                "description": kwargs.get("description", ""),
                "dependencies": kwargs.get("dependencies", []),
                "trusted": kwargs.get("trusted", False),
                "homepage": kwargs.get("homepage"),
                "repository": kwargs.get("repository"),
                "tags": kwargs.get("tags", []),
                "categories": kwargs.get("categories", []),
                "homepage_url": kwargs.get("homepage_url", ""),
                "documentation_url": kwargs.get("documentation_url", ""),
                "repository_url": kwargs.get("repository_url", ""),
                "license_info": kwargs.get("license_info", ""),
            }

            return cls.model_validate(instance_data)

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
            if v and not v.strip():
                msg = "Plugin entry point cannot be empty"
                raise ValueError(msg)
            return v

        def is_valid(self) -> bool:
            """Validate plugin metadata entity state."""
            return bool(self.plugin_name)

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate domain rules for plugin metadata entity."""
            if not self.plugin_name or not self.plugin_name.strip():
                return FlextResult[None].fail(
                    "Plugin name is required and cannot be empty"
                )
            if not self.name or not self.name.strip():
                return FlextResult[None].fail(
                    "Plugin name field is required and cannot be empty",
                )
            if not self.entry_point or not self.entry_point.strip():
                return FlextResult[None].fail(
                    "Plugin entry point is required and cannot be empty",
                )
            return FlextResult[None].ok(None)

    class Registry(FlextModels.Entity):
        """Plugin registry entity managing registered plugins."""

        # Pydantic fields
        name: str = Field(default="", description="Registry name")
        plugins: dict[str, FlextPluginEntities.Plugin] = Field(
            default_factory=dict,
            description="Dictionary of registered plugins",
        )
        created_at: datetime = Field(
            default_factory=datetime.now,
            description="Registry creation timestamp",
        )

        # Registry configuration fields for testing convenience
        registry_url: str = Field(default="", description="Registry URL")
        is_enabled: bool = Field(
            default=True, description="Whether registry is enabled"
        )
        plugin_count: int = Field(
            default=0, description="Number of plugins in registry"
        )
        sync_error_count: int = Field(default=0, description="Number of sync errors")
        last_sync: str | None = Field(default=None, description="Last sync timestamp")

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
        trusted_publishers: FlextTypes.StringList = Field(
            default_factory=list,
            description="List of trusted publishers",
        )

        @classmethod
        def create(
            cls,
            *,
            name: str,
            entity_id: str | None = None,
            **kwargs: object,
        ) -> FlextPluginEntities.Registry:
            """Create plugin registry entity with proper validation."""
            entity_id = entity_id or FlextUtilities.Generators.generate_entity_id()

            # Create instance data
            instance_data: FlextPluginTypes.Core.PluginDict = {
                "id": entity_id,
                "version": kwargs.get("version", 1),
                "metadata": kwargs.get("entity_metadata", {}),
                "name": name,
                "plugins": kwargs.get("plugins", {}),
                "registry_url": kwargs.get("registry_url", ""),
                "is_enabled": kwargs.get("is_enabled", True),
                "plugin_count": kwargs.get("plugin_count", 0),
                "sync_error_count": kwargs.get("sync_error_count", 0),
                "last_sync": kwargs.get("last_sync"),
                "requires_authentication": kwargs.get("requires_authentication", False),
                "api_key": kwargs.get("api_key", ""),
                "verify_signatures": kwargs.get("verify_signatures", False),
                "trusted_publishers": kwargs.get("trusted_publishers", []),
            }

            return cls.model_validate(instance_data)

        @property
        def is_available(self) -> bool:
            """Check if registry is available (enabled and has URL)."""
            return self.is_enabled and bool(self.registry_url)

        def record_sync(
            self, *, success: bool, plugin_count: int | None = None
        ) -> None:
            """Record sync attempt results."""
            setattr(
                self,
                "last_sync",
                FlextUtilities.Generators.generate_iso_timestamp(),
            )

            if success and plugin_count is not None:
                setattr(self, "plugin_count", plugin_count)
            elif not success:
                setattr(self, "sync_error_count", self.sync_error_count + 1)

        def is_valid(self) -> bool:
            """Validate plugin registry entity state."""
            return bool(self.name)

        def register_plugin(self, plugin: FlextPluginEntities.Plugin) -> bool:
            """Register a plugin in the registry."""
            if plugin.is_valid() and plugin.name not in self.plugins:
                self.plugins[plugin.name] = plugin
                return True
            return False

        def register(self, plugin: FlextPluginEntities.Plugin) -> FlextResult[None]:
            """Register a plugin in the registry with FlextResult return type."""
            if self.register_plugin(plugin):
                return FlextResult[None].ok(None)
            return FlextResult[None].fail(f"Failed to register plugin {plugin.name}")

        def unregister_plugin(self, plugin_name: str) -> bool:
            """Unregister a plugin from the registry."""
            if plugin_name in self.plugins:
                del self.plugins[plugin_name]
                return True
            return False

        def get_plugin(self, plugin_name: str) -> FlextPluginEntities.Plugin | None:
            """Get a plugin by name."""
            return self.plugins.get(plugin_name)

        def list_plugins(self) -> list[FlextPluginEntities.Plugin]:
            """List all registered plugins."""
            return list(self.plugins.values())

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate domain rules for plugin registry entity."""
            if not self.name or not self.name.strip():
                return FlextResult[None].fail(
                    "Registry name is required and cannot be empty",
                )
            return FlextResult[None].ok(None)

    class Execution(FlextModels.Entity):
        """Plugin execution entity for tracking plugin executions."""

        # Pydantic fields
        plugin_name: str = Field(
            default="",
            description="Name of the plugin being executed",
        )
        plugin_id: str = Field(
            default="",
            description="Plugin identifier",
        )
        execution_id: str = Field(
            default="",
            description="Execution identifier",
        )
        start_time: str = Field(
            default_factory=FlextUtilities.Generators.generate_iso_timestamp,
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
        input_data: FlextPluginTypes.Core.InputDict = Field(
            default_factory=dict,
            description="Input data for execution",
        )
        output_data: FlextPluginTypes.Core.OutputDict = Field(
            default_factory=dict,
            description="Output data from execution",
        )

        @classmethod
        def create(
            cls,
            *,
            plugin_name: str = "",
            execution_config: FlextPluginTypes.Core.ConfigDict | None = None,
            entity_id: str | None = None,
            **kwargs: object,
        ) -> FlextPluginEntities.Execution:
            """Create plugin execution entity with proper validation."""
            final_id = entity_id or FlextUtilities.Generators.generate_entity_id()
            execution_config = execution_config or {}

            # Create instance data with all required fields including base entity fields
            instance_data: FlextPluginTypes.Core.PluginDict = {
                "id": final_id,
                "version": kwargs.get("version", 1),
                "metadata": kwargs.get("metadata", {}),
                "plugin_name": plugin_name,
                "plugin_id": kwargs.get("plugin_id", plugin_name),
                "execution_id": kwargs.get("execution_id", final_id),
                "start_time": execution_config.get(
                    "start_time",
                    FlextUtilities.Generators.generate_iso_timestamp(),
                ),
                "end_time": execution_config.get("end_time"),
                "status": execution_config.get("status", "pending"),
                "result": execution_config.get("result"),
                "error": execution_config.get("error", ""),
                "error_message": execution_config.get("error_message"),
                "input_data": kwargs.get("input_data", {}),
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
                "FlextTypes.Dict",
                self.output_data.get("resource_usage", {}),
            )
            memory_value = resource_usage.get("memory_mb", 0.0)
            if isinstance(memory_value, (int, float)):
                return float(memory_value)
            if isinstance(memory_value, str):
                try:
                    return float(memory_value)
                except ValueError as e:
                    logger = FlextLogger(__name__)
                    logger.exception(
                        f"Invalid memory value '{memory_value}' for plugin execution",
                    )
                    msg = f"Invalid memory value: {memory_value}"
                    raise ValueError(msg) from e
            return 0.0

        @property
        def cpu_time_ms(self) -> float:
            """Get CPU time in milliseconds from resource tracking."""
            resource_usage = cast(
                "FlextTypes.Dict",
                self.output_data.get("resource_usage", {}),
            )
            cpu_value = resource_usage.get("cpu_time_ms", 0.0)
            if isinstance(cpu_value, (int, float)):
                return float(cpu_value)
            if isinstance(cpu_value, str):
                try:
                    return float(cpu_value)
                except ValueError as e:
                    logger = FlextLogger(__name__)
                    logger.exception(
                        f"Invalid CPU time value '{cpu_value}' for plugin execution",
                    )
                    msg = f"Invalid CPU time value: {cpu_value}"
                    raise ValueError(msg) from e
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
            setattr(self, "status", "running")
            setattr(
                self,
                "start_time",
                FlextUtilities.Generators.generate_iso_timestamp(),
            )

        def mark_completed(
            self,
            *,
            success: bool = True,
            error_message: str | None = None,
        ) -> None:
            """Mark execution as completed."""
            setattr(
                self,
                "end_time",
                FlextUtilities.Generators.generate_iso_timestamp(),
            )
            if success:
                setattr(self, "status", "completed")
            else:
                setattr(self, "status", "failed")
                if error_message:
                    setattr(self, "error", error_message)
                    setattr(self, "error_message", error_message)

        def update_resource_usage(
            self,
            memory_mb: float = 0.0,
            cpu_time_ms: float = 0.0,
        ) -> None:
            """Update resource usage tracking."""
            current_output = dict[str, object](self.output_data)
            current_output.update(
                {
                    "resource_usage": {
                        "memory_mb": memory_mb,
                        "cpu_time_ms": cpu_time_ms,
                        "timestamp": str(
                            FlextUtilities.Generators.generate_iso_timestamp(),
                        ),
                    },
                },
            )
            setattr(self, "output_data", current_output)

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate domain rules for plugin execution entity."""
            if not self.plugin_name:
                return FlextResult[None].fail("Plugin name is required")
            return FlextResult[None].ok(None)


__all__ = ["FlextPluginEntities"]
