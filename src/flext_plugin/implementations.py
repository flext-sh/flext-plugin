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

from flext_core import FlextLogger, FlextResult

from flext_plugin.models import FlextPluginModels
from flext_plugin.protocols import FlextPluginProtocols


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

        def load_plugin(self, _plugin_path: str | Path) -> FlextResult[object]:
            """Load plugin from path."""
            ...

    class FlextPluginRegistryProtocol(Protocol):
        """Protocol for plugin registry interface."""

        def register(self, _plugin: object) -> FlextResult[None]:
            """Register a plugin."""
            ...

        def get_plugin(self, _plugin_name: str) -> FlextResult[object]:
            """Get plugin by name."""
            ...

    # Type aliases for cleaner code
    FlextPluginLoader = FlextPluginLoaderProtocol

    class ConcretePlugin:
        """Concrete implementation of the FlextPlugin interface.

        This class implements the abstract FlextPlugin interface from flext-core,
        providing actual plugin functionality while using FlextPluginModels.Plugin
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
            entity: FlextPluginModels.Plugin | None = None,
        ) -> None:
            """Initialize concrete plugin.

            Args:
            name: Plugin name
            version: Plugin version
            entity: Optional domain entity for business logic

            """
            super().__init__()
            self._name = name
            self._version = version
            self._entity = entity
            self.logger = FlextLogger(f"plugin.{self.name}")
            self._initialized = False
            self._config: dict[str, object] = {}

        @property
        def name(self) -> str:
            """Get plugin name."""
            return self._name

        @property
        def version(self) -> str:
            """Get plugin version."""
            return self._version

        def configure(self, config: dict[str, object]) -> FlextResult[None]:
            """Configure component with provided settings."""
            try:
                # Store configuration
                self._config.update(config)
                return FlextResult[None].ok(None)
            except Exception as e:
                self.logger.exception(f"Failed to configure plugin {self.name}")
                return FlextResult[None].fail(f"Configuration failed: {e!s}")

        def get_config(self) -> dict[str, object]:
            """Get current configuration."""
            return getattr(self, "_config", {})

        def initialize(
            self,
            _context: dict[str, object],
        ) -> FlextResult[None]:
            """Initialize plugin with context.

            Args:
                _context: Plugin runtime context

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
                    self._entity.is_enabled = True
                    self.logger.info(f"Plugin entity {self.name} activated")
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
                            f"Plugin entity {self.name} already inactive",
                        )
                self._initialized = False
                return FlextResult[None].ok(None)
            except Exception as e:
                self.logger.exception(f"Failed to shutdown plugin {self.name}")
                return FlextResult[None].fail(f"Shutdown failed: {e!s}")

        def get_info(self) -> dict[str, object]:
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
            operations: dict[str, object] | None = None,
            entity: FlextPluginModels.Plugin | None = None,
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
                _params: Operation parameters

            Returns:
                FlextResult containing operation result or error

            """
            if not self._initialized:
                return FlextResult[object].fail("Plugin not initialized")
            if operation not in self._operations:
                return FlextResult[object].fail(f"Unsupported operation: {operation}")
            try:
                self.logger.info(
                    f"Executing operation {operation} on plugin {self.name}",
                )
                # Record execution in entity if present
                if self._entity:
                    self._entity.record_execution(0.0, success=True)
                # Execute operation (simplified for example)
                result = self._operations[operation]
                return FlextResult[object].ok(result)
            except Exception as e:
                self.logger.exception("Operation %s failed", operation)
                # Record error in entity if present
                if self._entity:
                    self._entity.record_error(str(e))
                return FlextResult[object].fail(f"Operation failed: {e!s}")

        def get_supported_operations(self) -> list[str]:
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
            connection_config: dict[str, object] | None = None,
            entity: FlextPluginModels.Plugin | None = None,
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
                    f"Missing required fields: {missing_fields}",
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
                        "No connection configuration provided",
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
            schema: dict[str, object] | None = None,
            entity: FlextPluginModels.Plugin | None = None,
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
                transformed: dict[str, object] = dict[str, object](
                    cast("dict[str, object]", data),
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

    class LoggerAdapter(FlextPluginProtocols.LoggerProtocol):
        """Adapter to make FlextLogger compatible with LoggerProtocol."""

        @override
        def __init__(self, logger: FlextLogger) -> None:
            """Initialize with FlextLogger instance."""
            self.logger = logger  # Simple adapter, no super() needed

        def critical(self, message: str, *_args: object, **_kwargs: object) -> None:
            """Log critical message."""
            self.logger.critical(message)

        def error(self, message: str, *_args: object, **_kwargs: object) -> None:
            """Log error message."""
            self.logger.error(message)

        def warning(self, message: str, *_args: object, **_kwargs: object) -> None:
            """Log warning message."""
            self.logger.warning(message)

        def info(self, message: str, *_args: object, **_kwargs: object) -> None:
            """Log info message."""
            self.logger.info(message)

        def debug(self, message: str, *_args: object, **_kwargs: object) -> None:
            """Log debug message."""
            self.logger.debug(message)

        def trace(self, message: str, *_args: object, **_kwargs: object) -> None:
            """Log trace message."""
            self.logger.debug(message)  # structlog doesn't have trace, use debug

        def log(
            self,
            level: str,
            message: str,
            _context: dict[str, object] | None = None,
        ) -> None:
            """Log a message with optional context."""
            getattr(self.logger, level.lower(), self.logger.debug)(message)

        def exception(
            self,
            message: str,
            *,
            _exc_info: bool = True,
            **_kwargs: object,
        ) -> None:
            """Log exception message."""
            self.logger.error(message)

    class ConcretePluginContext:
        """Concrete implementation of plugin runtime context.

        Provides plugins with access to system services, configuration,
        and logging infrastructure.
        """

        @override
        def __init__(
            self,
            logger: FlextLogger,
            config: dict[str, object] | None = None,
            services: dict[str, object] | None = None,
        ) -> None:
            """Initialize the instance.

            Args:
                logger: Structured logger for plugin
                config: Plugin configuration
                services: Available services

            """
            super().__init__()
            self._logger = logger
            self._config: dict[str, object] = config or {}
            self._services = services or {}

        @property
        def logger(self) -> FlextLogger:
            """Get logger for plugin."""
            return self._logger

        def get_config(self) -> dict[str, object]:
            """Get configuration for plugin."""
            return dict[str, object](self._config)

        def get_logger(self) -> FlextPluginProtocols.LoggerProtocol:
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

    class ConcretePluginRegistry:
        """Concrete implementation of plugin registry.

        Manages plugin registration, discovery, and lifecycle.
        """

        def __init__(self) -> None:
            """Initialize plugin registry."""
            self.plugins: dict[str, FlextPluginModels.Plugin] = {}
            self._logger = FlextLogger("plugin.registry")

        def register(self, plugin: FlextPluginModels.Plugin) -> FlextResult[None]:
            """Register a plugin.

            Args:
                plugin: Plugin instance to register

            Returns:
                FlextResult indicating registration success or failure

            """
            plugin_name = plugin.name
            if plugin_name in self.plugins:
                return FlextResult[None].fail(
                    f"Plugin {plugin_name} already registered",
                )
            self.plugins[plugin_name] = plugin
            self._logger.info("Registered plugin %s", plugin_name)
            return FlextResult[None].ok(None)

        def unregister(self, plugin_name: str) -> FlextResult[None]:
            """Unregister a plugin by name.

            Args:
                plugin_name: Name of plugin to unregister

            Returns:
                FlextResult indicating success or not found error

            """
            if plugin_name not in self.plugins:
                return FlextResult[None].fail(f"Plugin {plugin_name} not found")
            del self.plugins[plugin_name]
            self._logger.info("Unregistered plugin %s", plugin_name)
            return FlextResult[None].ok(None)

        def get_plugin(self, plugin_name: str) -> FlextPluginModels.Plugin | None:
            """Get plugin by name.

            Args:
                plugin_name: Name of plugin to retrieve

            Returns:
                Plugin instance or None if not found

            """
            return self.plugins.get(plugin_name)

        def list_plugins(self) -> list[FlextPluginModels.Plugin]:
            """List all registered plugin names.

            Returns:
            List of registered plugin instances

            """
            return list(self.plugins.values())

    class ConcretePluginLoader(FlextPluginLoader):
        """Concrete implementation of plugin loader.

        Handles dynamic plugin loading and discovery.
        """

        @override
        def __init__(self, registry: object | None = None) -> None:
            """Initialize plugin loader.

            Args:
            registry: Optional plugin registry to use

            """
            super().__init__()
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
                self.logger.info("Loading plugin from %s", plugin_path)
                # Simplified plugin loading - actual implementation would
                # dynamically import and instantiate plugin
                concrete_plugin = FlextPluginImplementations.ConcretePlugin(
                    name=f"loaded-from-{plugin_path}",
                    version="1.0.0",
                )
                # Create FlextPluginModels.Plugin for registration
                plugin_entity = FlextPluginModels.Plugin.create(
                    name=concrete_plugin.name,
                    plugin_version=concrete_plugin.version,
                )
                # Register loaded plugin
                reg_result: FlextResult[None] = cast(
                    "ConcretePluginRegistry",
                    self._registry,
                ).register(plugin_entity)
                if not reg_result.success:
                    return FlextResult[object].fail(
                        f"Failed to register loaded plugin: {reg_result.error}",
                    )
                return FlextResult[object].ok(concrete_plugin)
            except Exception as e:
                self.logger.exception("Failed to load plugin from %s", plugin_path)
                return FlextResult[object].fail(f"Load failed: {e!s}")

        def discover_plugins(
            self,
            search_path: str,
        ) -> FlextResult[list[str]]:
            """Discover available plugins in path.

            Args:
                search_path: Directory to search for plugins

            Returns:
                FlextResult containing list of discovered plugin paths

            """
            try:
                self.logger.info("Discovering plugins in %s", search_path)
                # Simplified discovery - actual implementation would
                # scan directory for valid plugin packages
                discovered = [
                    f"{search_path}/plugin1",
                    f"{search_path}/plugin2",
                ]
                return FlextResult[list[str]].ok(discovered)
            except Exception as e:
                self.logger.exception("Plugin discovery failed in %s", search_path)
                return FlextResult[list[str]].fail(
                    f"Discovery failed: {e!s}",
                )


# Backward compatibility exports - direct access to nested classes
# Plugin implementation classes with real inheritance
class ConcretePlugin(FlextPluginImplementations.ConcretePlugin):
    """ConcretePlugin - real inheritance from FlextPluginImplementations.ConcretePlugin."""


class ConcreteExecutablePlugin(FlextPluginImplementations.ConcreteExecutablePlugin):
    """ConcreteExecutablePlugin - real inheritance from ConcreteExecutablePlugin."""


class ConcreteDataPlugin(FlextPluginImplementations.ConcreteDataPlugin):
    """ConcreteDataPlugin - real inheritance from ConcreteDataPlugin."""


class ConcreteTransformPlugin(FlextPluginImplementations.ConcreteTransformPlugin):
    """ConcreteTransformPlugin - real inheritance from ConcreteTransformPlugin."""


class LoggerAdapter(FlextPluginImplementations.LoggerAdapter):
    """LoggerAdapter - real inheritance from LoggerAdapter."""


class ConcretePluginContext(FlextPluginImplementations.ConcretePluginContext):
    """ConcretePluginContext - real inheritance from ConcretePluginContext."""


class ConcretePluginRegistry(FlextPluginImplementations.ConcretePluginRegistry):
    """ConcretePluginRegistry - real inheritance from ConcretePluginRegistry."""


class ConcretePluginLoader(FlextPluginImplementations.ConcretePluginLoader):
    """ConcretePluginLoader - real inheritance from ConcretePluginLoader."""


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
