"""FLEXT Plugin Implementations - Single CONSOLIDATED Class Following FLEXT Patterns.

This module implements the CONSOLIDATED implementation pattern with a single FlextPluginImplementations
class containing ALL plugin implementation definitions as nested classes. Maintains backward
compatibility through property re-exports and follows FLEXT architectural standards.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Protocol, cast, override

from flext_core import FlextLogger, FlextProtocols, FlextResult, FlextTypes

from flext_plugin.entities import FlextPluginEntities


class FlextPluginImplementations:
    """Single CONSOLIDATED class containing ALL plugin implementations.

    Consolidates ALL implementation definitions into one class following FLEXT patterns.
    Individual implementations available as nested classes for organization while maintaining
    backward compatibility through direct exports.

    This approach follows FLEXT architectural standards for single consolidated classes
    per module while preserving existing API surface for seamless migration.
    """

    # Define minimal protocols for types that don't exist in flext-core yet
    class FlextPluginLoaderProtocol(Protocol):
        """Protocol for plugin loader interface."""

        def load_plugin(self, plugin_path: str | Path) -> FlextResult[object]:
            """Load plugin from path."""
            ...

    class FlextPluginRegistryProtocol(Protocol):
        """Protocol for plugin registry interface."""

        def register(self, plugin: object) -> FlextResult[None]:
            """Register a plugin."""
            ...

        def get_plugin(self, plugin_name: str) -> FlextResult[object]:
            """Get plugin by name."""
            ...

    # Type aliases for cleaner code
    FlextPluginLoader = FlextPluginLoaderProtocol
    FlextPluginEntities.Registry = FlextPluginRegistryProtocol

    class ConcretePlugin:
        """Concrete implementation of the FlextPlugin interface.

        This class implements the abstract FlextPlugin interface from flext-core,
        providing actual plugin functionality while using FlextPluginEntities.Entity
        for domain logic and state management.

        Attributes:
          _name: Plugin name
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
            entity: FlextPluginEntities.Entity | None = None,
        ) -> None:
            """Initialize concrete plugin.

            Args:
                name: Plugin name
                version: Plugin version
                entity: Optional domain entity for business logic

            """
            self._name = name
            self._version = version
            self._entity = entity
            self.logger = FlextLogger(f"plugin.{name}")
            self._initialized = False
            self._config: FlextTypes.Dict = {}

        @property
        def name(self) -> str:
            """Get plugin name."""
            return self._name

        @property
        def version(self) -> str:
            """Get plugin version."""
            return self._version

        def configure(self, config: FlextTypes.Dict) -> FlextResult[None]:
            """Configure component with provided settings."""
            try:
                # Store configuration
                self._config: FlextTypes.Dict = config
                return FlextResult[None].ok(None)
            except Exception as e:
                self.logger.exception(f"Failed to configure plugin {self.name}")
                return FlextResult[None].fail(f"Configuration failed: {e!s}")

        def get_config(self) -> FlextTypes.Dict:
            """Get current configuration."""
            return getattr(self, "_config", {})

        def initialize(
            self,
            _context: FlextProtocols.PluginContext,
        ) -> FlextResult[None]:
            """Initialize plugin with context.

            Args:
                context: Plugin runtime context
            Returns:
                FlextResult indicating success or failure

            """
            try:
                self.logger.info(f"Initializing plugin {self.name} v{self.version}")
                # Validate entity if present
                if self._entity:
                    validation = self._entity.validate_business_rules()
                    if not validation.success:
                        return validation
                    # Activate entity
                    if self._entity.activate():
                        self.logger.info(f"Plugin entity {self.name} activated")
                    else:
                        self.logger.warning(f"Plugin entity {self.name} already active")
                self._initialized = True
                return FlextResult[None].ok(None)
            except Exception as e:
                self.logger.exception(f"Failed to initialize plugin {self.name}")
                return FlextResult[None].fail(f"Initialization failed: {e!s}")

        def shutdown(self) -> FlextResult[None]:
            """Shutdown plugin and release resources.

            Returns:
                FlextResult indicating success or failure

            """
            try:
                self.logger.info(f"Shutting down plugin {self.name}")
                # Deactivate entity if present
                if self._entity:
                    if self._entity.deactivate():
                        self.logger.info(f"Plugin entity {self.name} deactivated")
                    else:
                        self.logger.warning(
                            f"Plugin entity {self.name} already inactive"
                        )
                self._initialized = False
                return FlextResult[None].ok(None)
            except Exception as e:
                self.logger.exception(f"Failed to shutdown plugin {self.name}")
                return FlextResult[None].fail(f"Shutdown failed: {e!s}")

        def get_info(self) -> FlextTypes.Dict:
            """Get plugin information.

            Returns:
                Dictionary containing plugin metadata

            """
            return {
                "name": self._name,
                "version": self._version,
                "initialized": self._initialized,
                "entity_present": self._entity is not None,
            }

    class ConcreteExecutablePlugin(ConcretePlugin):
        """Concrete implementation of executable plugin.

        Extends ConcretePlugin with execution capabilities as defined
        in the FlextExecutablePlugin interface.
        """

        @override
        def __init__(
            self,
            name: str,
            version: str,
            operations: FlextTypes.Dict | None = None,
            entity: FlextPluginEntities.Entity | None = None,
        ) -> None:
            """Initialize executable plugin.

            Args:
                name: Plugin name
                version: Plugin version
                operations: Supported operations mapping
                entity: Optional domain entity

            """
            super().__init__(name, version, entity)
            self._operations = operations or {}

        def execute(
            self,
            operation: str,
            _params: Mapping[str, object],
        ) -> FlextResult[object]:
            """Execute a plugin operation.

            Args:
                operation: Operation name to execute
                params: Operation parameters
            Returns:
                FlextResult containing operation result or error

            """
            if not self._initialized:
                return FlextResult[object].fail("Plugin not initialized")
            if operation not in self._operations:
                return FlextResult[object].fail(f"Unsupported operation: {operation}")
            try:
                self.logger.info(
                    f"Executing operation {operation} on plugin {self.name}"
                )
                # Record execution in entity if present
                if self._entity:
                    self._entity.record_execution(0.0, success=True)
                # Execute operation (simplified for example)
                result = self._operations[operation]
                return FlextResult[object].ok(result)
            except Exception as e:
                self.logger.exception(f"Operation {operation} failed")
                # Record error in entity if present
                if self._entity:
                    self._entity.record_error(str(e))
                return FlextResult[object].fail(f"Operation failed: {e!s}")

        def get_supported_operations(self) -> FlextTypes.StringList:
            """Get list of supported operations.

            Returns:
                List of operation names

            """
            return list(self._operations.keys())

    class ConcreteDataPlugin(ConcretePlugin):
        """Concrete implementation of data processing plugin.

        Implements the FlextDataPlugin interface for data extraction,
        transformation, and loading operations.
        """

        @override
        def __init__(
            self,
            name: str,
            version: str,
            connection_config: FlextTypes.Dict | None = None,
            entity: FlextPluginEntities.Entity | None = None,
        ) -> None:
            """Initialize data plugin.

            Args:
                name: Plugin name
                version: Plugin version
                connection_config: Connection configuration
                entity: Optional domain entity

            """
            super().__init__(name, version, entity)
            self._connection_config = connection_config or {}
            self._connection_valid = False

        def validate_config(self, config: Mapping[str, object]) -> FlextResult[None]:
            """Validate plugin configuration.

            Args:
                config: Configuration to validate
            Returns:
                FlextResult indicating validation success or errors

            """
            required_fields = ["host", "port", "database"]
            missing_fields = [f for f in required_fields if f not in config]
            if missing_fields:
                return FlextResult[None].fail(
                    f"Missing required fields: {missing_fields}"
                )
            # Additional validation logic here
            self._connection_config.update(config)
            return FlextResult[None].ok(None)

        def test_connection(self) -> FlextResult[None]:
            """Test connection to data source/destination.

            Returns:
                FlextResult indicating connection success or failure

            """
            try:
                self.logger.info(f"Testing connection for plugin {self.name}")
                # Simplified connection test
                if not self._connection_config:
                    return FlextResult[None].fail(
                        "No connection configuration provided"
                    )
                # Actual connection test would go here
                self._connection_valid = True
                return FlextResult[None].ok(None)
            except Exception as e:
                self.logger.exception("Connection test failed")
                self._connection_valid = False
                return FlextResult[None].fail(f"Connection failed: {e!s}")

    class ConcreteTransformPlugin(ConcretePlugin):
        """Concrete implementation of data transformation plugin.

        Implements the FlextTransformPlugin interface for data
        transformation operations like DBT models.
        """

        @override
        def __init__(
            self,
            name: str,
            version: str,
            schema: FlextTypes.Dict | None = None,
            entity: FlextPluginEntities.Entity | None = None,
        ) -> None:
            """Initialize transform plugin.

            Args:
                name: Plugin name
                version: Plugin version
                schema: Transformation schema
                entity: Optional domain entity

            """
            super().__init__(name, version, entity)
            self._schema = schema or {}

        def transform(self, data: object) -> FlextResult[object]:
            """Transform input data.

            Args:
                data: Input data to transform
            Returns:
                FlextResult containing transformed data or error

            """
            try:
                self.logger.info(f"Transforming data with plugin {self.name}")
                # Simplified transformation logic
                if not isinstance(data, dict):
                    return FlextResult[object].fail("Input data must be a dictionary")
                # Apply transformation based on schema
                transformed: FlextTypes.Dict = dict[str, object](
                    cast("FlextTypes.Dict", data)
                )
                transformed["_transformed_by"] = self._name
                transformed["_transform_version"] = self._version
                return FlextResult[object].ok(transformed)
            except Exception as e:
                self.logger.exception("Transformation failed")
                return FlextResult[object].fail(f"Transform failed: {e!s}")

        def get_schema(self) -> FlextResult[Mapping[str, object]]:
            """Get transformation schema.

            Returns:
                FlextResult containing schema definition

            """
            if not self._schema:
                return FlextResult[Mapping[str, object]].fail("No schema defined")
            return FlextResult[Mapping[str, object]].ok(self._schema)

    class LoggerAdapter(FlextProtocols.LoggerProtocol):
        """Adapter to make FlextLogger compatible with LoggerProtocol."""

        @override
        def __init__(self, logger: FlextLogger) -> None:
            """Initialize with FlextLogger instance."""
            self.logger = logger

        def critical(
            self, message: str, *args: object, **kwargs: object
        ) -> FlextResult[None]:
            """Log critical message."""
            self.logger.critical(message, *args, **kwargs)
            return FlextResult[None].ok(None)

        def error(
            self, message: str, *args: object, **kwargs: object
        ) -> FlextResult[None]:
            """Log error message."""
            self.logger.error(message, *args, **kwargs)
            return FlextResult[None].ok(None)

        def warning(
            self, message: str, *args: object, **kwargs: object
        ) -> FlextResult[None]:
            """Log warning message."""
            self.logger.warning(message, *args, **kwargs)
            return FlextResult[None].ok(None)

        def info(
            self, message: str, *args: object, **kwargs: object
        ) -> FlextResult[None]:
            """Log info message."""
            self.logger.info(message, *args, **kwargs)
            return FlextResult[None].ok(None)

        def debug(
            self, message: str, *args: object, **kwargs: object
        ) -> FlextResult[None]:
            """Log debug message."""
            self.logger.debug(message, *args, **kwargs)
            return FlextResult[None].ok(None)

        def trace(
            self, message: str, *args: object, **kwargs: object
        ) -> FlextResult[None]:
            """Log trace message."""
            self.logger.debug(
                message, *args, **kwargs
            )  # structlog doesn't have trace, use debug
            return FlextResult[None].ok(None)

        def exception(
            self, message: str, *, exc_info: bool = True, **kwargs: object
        ) -> None:
            """Log exception message."""
            self.logger.error(message, exc_info=exc_info, **kwargs)

    class ConcretePluginContext:
        """Concrete implementation of plugin runtime context.

        Provides plugins with access to system services, configuration,
        and logging infrastructure.
        """

        @override
        def __init__(
            self,
            logger: FlextLogger,
            config: FlextTypes.Dict | None = None,
            services: FlextTypes.Dict | None = None,
        ) -> None:
            """Initialize the instance.

            Args:
                logger: Structured logger for plugin
                config: Plugin configuration
                services: Available services

            """
            self.logger = logger
            self._config: FlextTypes.Dict = config or {}
            self._services = services or {}

        @property
        def logger(self) -> FlextLogger:
            """Get logger for plugin."""
            return self.logger

        def get_config(self) -> FlextTypes.Dict:
            """Get configuration for plugin."""
            return dict[str, object](self._config)

        def get_logger(self) -> FlextProtocols.LoggerProtocol:
            """Get logger instance for plugin."""
            return LoggerAdapter(self.logger)

        def get_service(self, service_name: str) -> FlextResult[object]:
            """Get service by name from container.

            Args:
                service_name: Name of service to retrieve
            Returns:
                FlextResult with service instance or not found error

            """
            if service_name not in self._services:
                return FlextResult[object].fail(f"Service not found: {service_name}")
            return FlextResult[object].ok(self._services[service_name])

    class ConcretePluginRegistry(FlextPluginEntities.Registry):
        """Concrete implementation of plugin registry.

        Manages plugin registration, discovery, and lifecycle.
        """

        @override
        def __init__(self) -> None:
            """Initialize plugin registry."""
            self._plugins: FlextTypes.Dict = {}
            self.logger = FlextLogger("plugin.registry")

        def register(self, plugin: object) -> FlextResult[None]:
            """Register a plugin.

            Args:
                plugin: Plugin instance to register
            Returns:
                FlextResult indicating registration success or failure

            """
            # Since FlextPlugin protocol doesn't have name/version attributes,
            # we generate a unique name based on plugin ID
            plugin_id = id(plugin)
            plugin_name = f"plugin_{plugin_id}"
            if plugin_name in self._plugins:
                return FlextResult[None].fail(
                    f"Plugin {plugin_name} already registered"
                )
            self._plugins[plugin_name] = plugin
            self.logger.info(f"Registered plugin {plugin_name}")
            return FlextResult[None].ok(None)

        def unregister(self, plugin_name: str) -> FlextResult[None]:
            """Unregister a plugin by name.

            Args:
                plugin_name: Name of plugin to unregister
            Returns:
                FlextResult indicating success or not found error

            """
            if plugin_name not in self._plugins:
                return FlextResult[None].fail(f"Plugin {plugin_name} not found")
            del self._plugins[plugin_name]
            self.logger.info(f"Unregistered plugin {plugin_name}")
            return FlextResult[None].ok(None)

        def get_plugin(self, plugin_name: str) -> FlextResult[object]:
            """Get plugin by name.

            Args:
                plugin_name: Name of plugin to retrieve
            Returns:
                FlextResult containing plugin or not found error

            """
            if plugin_name not in self._plugins:
                return FlextResult[object].fail(f"Plugin {plugin_name} not found")
            return FlextResult[object].ok(self._plugins[plugin_name])

        def list_plugins(self) -> FlextTypes.StringList:
            """List all registered plugin names.

            Returns:
                List of registered plugin names

            """
            return list(self._plugins.keys())

    class ConcretePluginLoader(FlextPluginLoader):
        """Concrete implementation of plugin loader.

        Handles dynamic plugin loading and discovery.
        """

        @override
        def __init__(
            self, registry: FlextPluginEntities.Registry | None = None
        ) -> None:
            """Initialize plugin loader.

            Args:
                registry: Optional plugin registry to use

            Returns:
                object: Description of return value.

            """
            self._registry = (
                registry or FlextPluginImplementations.ConcretePluginRegistry()
            )
            self.logger = FlextLogger("plugin.loader")

        def load_plugin(self, plugin_path: str | Path) -> FlextResult[object]:
            """Load plugin from path.

            Args:
                plugin_path: Path to plugin module or package
            Returns:
                FlextResult containing loaded plugin or load error

            """
            try:
                self.logger.info(f"Loading plugin from {plugin_path}")
                # Simplified plugin loading - actual implementation would
                # dynamically import and instantiate plugin
                concrete_plugin = FlextPluginImplementations.ConcretePlugin(
                    name=f"loaded-from-{plugin_path}",
                    version="1.0.0",
                )
                # Create FlextPluginEntities.Entity for registration
                plugin_entity = FlextPluginEntities.Entity.create(
                    name=concrete_plugin.name,
                    plugin_version=concrete_plugin.version,
                )
                # Register loaded plugin
                reg_result: FlextResult[None] = self._registry.register(plugin_entity)
                if not reg_result.success:
                    return FlextResult[object].fail(
                        f"Failed to register loaded plugin: {reg_result.error}",
                    )
                return FlextResult[object].ok(concrete_plugin)
            except Exception as e:
                self.logger.exception(f"Failed to load plugin from {plugin_path}")
                return FlextResult[object].fail(f"Load failed: {e!s}")

        def discover_plugins(
            self,
            search_path: str,
        ) -> FlextResult[FlextTypes.StringList]:
            """Discover available plugins in path.

            Args:
                search_path: Directory to search for plugins
            Returns:
                FlextResult containing list of discovered plugin paths

            """
            try:
                self.logger.info(f"Discovering plugins in {search_path}")
                # Simplified discovery - actual implementation would
                # scan directory for valid plugin packages
                discovered = [
                    f"{search_path}/plugin1",
                    f"{search_path}/plugin2",
                ]
                return FlextResult[FlextTypes.StringList].ok(discovered)
            except Exception as e:
                self.logger.exception(f"Plugin discovery failed in {search_path}")
                return FlextResult[FlextTypes.StringList].fail(
                    f"Discovery failed: {e!s}",
                )


# Backward compatibility exports - direct access to nested classes
ConcretePlugin = FlextPluginImplementations.ConcretePlugin
ConcreteExecutablePlugin = FlextPluginImplementations.ConcreteExecutablePlugin
ConcreteDataPlugin = FlextPluginImplementations.ConcreteDataPlugin
ConcreteTransformPlugin = FlextPluginImplementations.ConcreteTransformPlugin
LoggerAdapter = FlextPluginImplementations.LoggerAdapter
ConcretePluginContext = FlextPluginImplementations.ConcretePluginContext
ConcretePluginRegistry = FlextPluginImplementations.ConcretePluginRegistry
ConcretePluginLoader = FlextPluginImplementations.ConcretePluginLoader


__all__ = [
    "ConcreteDataPlugin",
    "ConcreteExecutablePlugin",
    # Backward compatibility exports
    "ConcretePlugin",
    "ConcretePluginContext",
    "ConcretePluginLoader",
    "ConcretePluginRegistry",
    "ConcreteTransformPlugin",
    # CONSOLIDATED class (FLEXT pattern)
    "FlextPluginImplementations",
    "LoggerAdapter",
]
