"""FLEXT Plugin Implementations - Single CONSOLIDATED Class Following FLEXT Patterns.

This module implements the CONSOLIDATED implementation pattern with a single FlextPluginImplementations
class containing ALL plugin implementation definitions as nested classes. Maintains backward
compatibility through property re-exports and follows FLEXT architectural standards.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    MutableMapping,
)
from typing import override

from flext_plugin import c, m, p, r, t, u


class FlextPluginImplementations:
    """Single CONSOLIDATED class containing ALL plugin implementations.

    Consolidates ALL implementation definitions into one class following FLEXT patterns.
    Individual implementations available as nested classes for organization while maintaining
    backward compatibility through direct exports.

    This approach follows FLEXT architectural standards for single consolidated classes
    per module while preserving existing API surface for seamless migration.
    """

    class ConcreteConfigBase:
        config: t.MutableJsonMapping

        def get_config(self) -> t.JsonMapping:
            return self.config

    class ConcretePlugin(ConcreteConfigBase):
        """Concrete implementation of the FlextPlugin interface.

        This class implements the abstract FlextPlugin interface from flext-core,
        providing actual plugin functionality while using m.Plugin
        for domain logic and state management.

        Attributes:
        name: Plugin name
        _version: Plugin version
        _entity: Domain entity for business logic
        logger: Plugin logger
        _initialized: Initialization state

        """

        @override
        def __init__(
            self,
            name: str,
            version: str,
            entity: m.Plugin.Entity | None = None,
        ) -> None:
            """Initialize concrete plugin.

            Args:
            name: Plugin name
            version: Plugin version
            entity: Optional domain entity for business logic

            """
            super().__init__()
            self.name = name
            self._version = version
            self._entity = entity
            self.logger = u.fetch_logger(f"plugin.{self.name}")
            self._initialized = False
            self.config: t.MutableJsonMapping = {}

        @property
        def version(self) -> str:
            """Get plugin version."""
            return self._version

        def configure(self, settings: t.JsonMapping) -> p.Result[None]:
            """Configure component with provided settings."""
            try:
                self.config.update(settings)
                return r[None].ok(None)
            except c.EXC_BROAD_IO_TYPE as e:
                self.logger.exception(f"Failed to configure plugin {self.name}")
                return r[None].fail_op("Configuration", e)

        def fetch_info(self) -> t.JsonMapping:
            """Get plugin information.

            Returns:
            Dictionary containing plugin metadata

            """
            return {
                "name": self.name,
                "version": self._version,
                "initialized": self._initialized,
                "entity_present": self._entity is not None,
            }

        def initialize(self, context: t.JsonMapping) -> p.Result[None]:
            """Initialize plugin with context.

            Args:
                context: Plugin runtime context

            Returns:
                r indicating success or failure

            """
            try:
                if context:
                    configure_result = self.configure(context)
                    if configure_result.failure:
                        return r[None].fail(
                            configure_result.error or "Context configuration failed"
                        )
                self.logger.info(f"Initializing plugin {self.name} v{self.version}")
                if self._entity:
                    validation = self._entity.validate_business_rules()
                    if validation.failure:
                        return r[None].fail(validation.error or "Validation failed")
                    self._entity.is_enabled = True
                    self.logger.info(f"Plugin entity {self.name} activated")
                self._initialized = True
                return r[None].ok(None)
            except c.EXC_BROAD_IO_TYPE as e:
                self.logger.exception(f"Failed to initialize plugin {self.name}")
                return r[None].fail_op("Initialization", e)

        def shutdown(self) -> p.Result[None]:
            """Shutdown plugin and release resources.

            Returns:
            r indicating success or failure

            """
            try:
                self.logger.info(f"Shutting down plugin {self.name}")
                if self._entity:
                    self._entity.is_enabled = False
                    self.logger.info(f"Plugin entity {self.name} deactivated")
                self._initialized = False
                return r[None].ok(None)
            except c.EXC_BROAD_IO_TYPE as e:
                self.logger.exception(f"Failed to shutdown plugin {self.name}")
                return r[None].fail_op("Shutdown", e)

    class ConcretePluginRegistry:
        """Concrete implementation of plugin registry.

        Manages plugin registration, discovery, and lifecycle.
        """

        def __init__(self) -> None:
            """Initialize plugin registry."""
            self.plugins: MutableMapping[str, m.Plugin.Entity] = {}
            self.logger = u.fetch_logger("plugin.registry")

        def fetch_plugin(
            self,
            plugin_name: str,
        ) -> m.Plugin.Entity | None:
            """Fetch a plugin by name.

            Args:
                plugin_name: Name of plugin to retrieve

            Returns:
                Plugin instance or None if not found

            """
            return self.plugins.get(plugin_name)

        def list_plugins(self) -> t.SequenceOf[m.Plugin.Entity]:
            """List all registered plugin names.

            Returns:
            List of registered plugin instances

            """
            return list(self.plugins.values())

        def register_plugin(self, plugin: t.JsonValue) -> p.Result[bool]:
            """Register a plugin via protocol interface."""
            if isinstance(plugin, m.Plugin.Entity):
                return self.register(plugin).map(lambda _: True)
            return r[bool].fail("Invalid plugin type for registration")

        def register(self, plugin: m.Plugin.Entity) -> p.Result[None]:
            """Register a plugin.

            Args:
                plugin: Plugin instance to register

            Returns:
                r indicating registration success or failure

            """
            plugin_name = plugin.name
            if plugin_name in self.plugins:
                return r[None].fail(f"Plugin {plugin_name} already registered")
            self.plugins[plugin_name] = plugin
            self.logger.info("Registered plugin %s", plugin_name)
            return r[None].ok(None)

        def unregister(self, plugin_name: str) -> p.Result[None]:
            """Unregister a plugin by name.

            Args:
                plugin_name: Name of plugin to unregister

            Returns:
                r indicating success or not found error

            """
            if plugin_name not in self.plugins:
                return r[None].fail(f"Plugin {plugin_name} not found")
            del self.plugins[plugin_name]
            self.logger.info("Unregistered plugin %s", plugin_name)
            return r[None].ok(None)


__all__: list[str] = ["FlextPluginImplementations"]
