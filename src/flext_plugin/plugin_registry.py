"""FLEXT Plugin Registry Entity - Plugin registry domain entity.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime

from flext_core import FlextModels, FlextResult, FlextUtilities
from pydantic import Field

from flext_plugin.plugin import Plugin


class PluginRegistry(FlextModels.Entity):
    """Plugin registry entity managing registered plugins."""

    # Pydantic fields
    name: str = Field(default="", description="Registry name")
    plugins: dict[str, Plugin] = Field(
        default_factory=dict,
        description="Dictionary of registered plugins",
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Registry creation timestamp",
    )

    # Registry configuration fields for testing convenience
    registry_url: str = Field(default="", description="Registry URL")
    is_enabled: bool = Field(default=True, description="Whether registry is enabled")
    plugin_count: int = Field(default=0, description="Number of plugins in registry")
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
        **kwargs: object,
    ) -> PluginRegistry:
        """Create plugin registry entity with proper validation."""
        entity_id = entity_id or FlextUtilities.Generators.generate_entity_id()

        # Create instance data
        instance_data: dict[str, object] = {
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

    def record_sync(self, *, success: bool, plugin_count: int | None = None) -> None:
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

    def register_plugin(self, plugin: Plugin) -> bool:
        """Register a plugin in the registry."""
        if plugin.is_valid() and plugin.name not in self.plugins:
            self.plugins[plugin.name] = plugin
            return True
        return False

    def register(self, plugin: Plugin) -> FlextResult[None]:
        """Register a plugin in the registry with FlextResult return type."""
        if self.register_plugin(plugin):
            return FlextResult[None].ok(None)
        return FlextResult[None].fail(f"Failed to register plugin {plugin.name}")

    def unregister_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unregister a plugin from the registry."""
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            return FlextResult[bool].ok(True)
        return FlextResult[bool].fail(f"Plugin '{plugin_name}' not found")

    def get_plugin(self, plugin_name: str) -> Plugin | None:
        """Get a plugin by name."""
        return self.plugins.get(plugin_name)

    def get(self, plugin_name: str) -> Plugin | None:
        """Get a plugin by name (alias for get_plugin)."""
        return self.get_plugin(plugin_name)

    def unregister(self, plugin_name: str) -> FlextResult[bool]:
        """Unregister a plugin (alias for unregister_plugin)."""
        return self.unregister_plugin(plugin_name)

    def list_plugins(self) -> list[Plugin]:
        """List all registered plugins."""
        return list(self.plugins.values())

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain rules for plugin registry entity."""
        if not self.name or not self.name.strip():
            return FlextResult[None].fail(
                "Registry name is required and cannot be empty",
            )
        return FlextResult[None].ok(None)


__all__ = ["PluginRegistry"]
