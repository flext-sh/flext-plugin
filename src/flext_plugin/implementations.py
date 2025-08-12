"""FLEXT Plugin Concrete Implementations - Clean Architecture Implementation Layer.

This module provides concrete implementations of the abstract plugin interfaces
defined in flext-core. These implementations bridge the gap between the pure
abstractions in flext-core and the domain entities in flext-plugin.

Architecture Principles:
    - Implements flext_core.interfaces.FlextPlugin and related interfaces
    - Uses composition with FlextPluginEntity for domain logic
    - Maintains clean separation between interface and implementation
    - Provides concrete plugin lifecycle management

Implementation Classes:
    - ConcretePlugin: Basic plugin implementation
    - ConcreteExecutablePlugin: Plugin with execution capabilities
    - ConcreteDataPlugin: Data processing plugin implementation
    - ConcreteTransformPlugin: Data transformation plugin
    - ConcretePluginContext: Runtime context implementation
    - ConcretePluginRegistry: Plugin registry implementation
    - ConcretePluginLoader: Plugin loading implementation

Example:
    >>> from flext_plugin.implementations import ConcretePlugin
    >>> plugin = ConcretePlugin(
    ...     name="my-plugin",
    ...     version="1.0.0",
    ...     entity=plugin_entity  # Domain entity for business logic
    ... )
    >>> result = plugin.initialize(context)
    >>> if result.success:
    ...     print(f"Plugin {plugin.name} initialized")

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import (
    FlextPlugin,
    FlextPluginContext,
    FlextPluginLoader,
    FlextPluginRegistry,
    FlextResult,
    get_logger,
)

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from structlog.stdlib import BoundLogger

    from flext_plugin.domain.entities import FlextPluginEntity


class ConcretePlugin(FlextPlugin):
    """Concrete implementation of the FlextPlugin interface.

    This class implements the abstract FlextPlugin interface from flext-core,
    providing actual plugin functionality while using FlextPluginEntity
    for domain logic and state management.

    Attributes:
        _name: Plugin name
        _version: Plugin version
        _entity: Domain entity for business logic
        _logger: Plugin logger
        _initialized: Initialization state

    """

    def __init__(
        self,
        name: str,
        version: str,
        entity: FlextPluginEntity | None = None,
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
        self._logger = get_logger(f"plugin.{name}")
        self._initialized = False

    @property
    def name(self) -> str:
        """Get plugin name."""
        return self._name

    @property
    def version(self) -> str:
        """Get plugin version."""
        return self._version

    def initialize(self, _context: FlextPluginContext) -> FlextResult[None]:
        """Initialize plugin with context.

        Args:
            context: Plugin runtime context

        Returns:
            FlextResult indicating success or failure

        """
        try:
            self._logger.info(f"Initializing plugin {self.name} v{self.version}")

            # Validate entity if present
            if self._entity:
                validation = self._entity.validate_business_rules()
                if not validation.success:
                    return validation

                # Activate entity
                if self._entity.activate():
                    self._logger.info(f"Plugin entity {self.name} activated")
                else:
                    self._logger.warning(f"Plugin entity {self.name} already active")

            self._initialized = True
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception(f"Failed to initialize plugin {self.name}")
            return FlextResult.fail(f"Initialization failed: {e!s}")

    def shutdown(self) -> FlextResult[None]:
        """Shutdown plugin and release resources.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            self._logger.info(f"Shutting down plugin {self.name}")

            # Deactivate entity if present
            if self._entity:
                if self._entity.deactivate():
                    self._logger.info(f"Plugin entity {self.name} deactivated")
                else:
                    self._logger.warning(f"Plugin entity {self.name} already inactive")

            self._initialized = False
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception(f"Failed to shutdown plugin {self.name}")
            return FlextResult.fail(f"Shutdown failed: {e!s}")


class ConcreteExecutablePlugin(ConcretePlugin):
    """Concrete implementation of executable plugin.

    Extends ConcretePlugin with execution capabilities as defined
    in the FlextExecutablePlugin interface.
    """

    def __init__(
        self,
        name: str,
        version: str,
        operations: dict[str, object] | None = None,
        entity: FlextPluginEntity | None = None,
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

    def execute(self, operation: str, _params: Mapping[str, object]) -> FlextResult[object]:
        """Execute a plugin operation.

        Args:
            operation: Operation name to execute
            params: Operation parameters

        Returns:
            FlextResult containing operation result or error

        """
        if not self._initialized:
            return FlextResult.fail("Plugin not initialized")

        if operation not in self._operations:
            return FlextResult.fail(f"Unsupported operation: {operation}")

        try:
            self._logger.info(f"Executing operation {operation} on plugin {self.name}")

            # Record execution in entity if present
            if self._entity:
                self._entity.record_execution(0.0, success=True)

            # Execute operation (simplified for example)
            result = self._operations[operation]
            return FlextResult.ok(result)

        except Exception as e:
            self._logger.exception(f"Operation {operation} failed")

            # Record error in entity if present
            if self._entity:
                self._entity.record_error(str(e))

            return FlextResult.fail(f"Operation failed: {e!s}")

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

    def __init__(
        self,
        name: str,
        version: str,
        connection_config: dict[str, object] | None = None,
        entity: FlextPluginEntity | None = None,
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
            return FlextResult.fail(f"Missing required fields: {missing_fields}")

        # Additional validation logic here
        self._connection_config.update(config)
        return FlextResult.ok(None)

    def test_connection(self) -> FlextResult[None]:
        """Test connection to data source/destination.

        Returns:
            FlextResult indicating connection success or failure

        """
        try:
            self._logger.info(f"Testing connection for plugin {self.name}")

            # Simplified connection test
            if not self._connection_config:
                return FlextResult.fail("No connection configuration provided")

            # Actual connection test would go here
            self._connection_valid = True
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception("Connection test failed")
            self._connection_valid = False
            return FlextResult.fail(f"Connection failed: {e!s}")


class ConcreteTransformPlugin(ConcretePlugin):
    """Concrete implementation of data transformation plugin.

    Implements the FlextTransformPlugin interface for data
    transformation operations like DBT models.
    """

    def __init__(
        self,
        name: str,
        version: str,
        schema: dict[str, object] | None = None,
        entity: FlextPluginEntity | None = None,
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
            self._logger.info(f"Transforming data with plugin {self.name}")

            # Simplified transformation logic
            if not isinstance(data, dict):
                return FlextResult.fail("Input data must be a dictionary")

            # Apply transformation based on schema
            transformed = dict(data)  # Copy input
            transformed["_transformed_by"] = self.name
            transformed["_transform_version"] = self.version

            return FlextResult.ok(transformed)

        except Exception as e:
            self._logger.exception("Transformation failed")
            return FlextResult.fail(f"Transform failed: {e!s}")

    def get_schema(self) -> FlextResult[Mapping[str, object]]:
        """Get transformation schema.

        Returns:
            FlextResult containing schema definition

        """
        if not self._schema:
            return FlextResult.fail("No schema defined")

        return FlextResult.ok(self._schema)


class ConcretePluginContext(FlextPluginContext):
    """Concrete implementation of plugin runtime context.

    Provides plugins with access to system services, configuration,
    and logging infrastructure.
    """

    def __init__(
        self,
        logger: BoundLogger,
        config: dict[str, object] | None = None,
        services: dict[str, object] | None = None,
    ) -> None:
        """Initialize plugin context.

        Args:
            logger: Structured logger for plugin
            config: Plugin configuration
            services: Available services

        """
        self._logger = logger
        self._config = config or {}
        self._services = services or {}

    @property
    def logger(self) -> BoundLogger:
        """Get logger for plugin."""
        return self._logger

    @property
    def config(self) -> Mapping[str, object]:
        """Get plugin configuration."""
        return self._config

    def get_service(self, service_name: str) -> FlextResult[object]:
        """Get service by name from container.

        Args:
            service_name: Name of service to retrieve

        Returns:
            FlextResult with service instance or not found error

        """
        if service_name not in self._services:
            return FlextResult.fail(f"Service not found: {service_name}")

        return FlextResult.ok(self._services[service_name])


class ConcretePluginRegistry(FlextPluginRegistry):
    """Concrete implementation of plugin registry.

    Manages plugin registration, discovery, and lifecycle.
    """

    def __init__(self) -> None:
        """Initialize plugin registry."""
        self._plugins: dict[str, FlextPlugin] = {}
        self._logger = get_logger("plugin.registry")

    def register(self, plugin: FlextPlugin) -> FlextResult[None]:
        """Register a plugin.

        Args:
            plugin: Plugin instance to register

        Returns:
            FlextResult indicating registration success or failure

        """
        if plugin.name in self._plugins:  # type: ignore[attr-defined]
            return FlextResult.fail(f"Plugin {plugin.name} already registered")  # type: ignore[attr-defined]

        self._plugins[plugin.name] = plugin  # type: ignore[attr-defined]
        self._logger.info(f"Registered plugin {plugin.name} v{plugin.version}")  # type: ignore[attr-defined]
        return FlextResult.ok(None)

    def unregister(self, plugin_name: str) -> FlextResult[None]:
        """Unregister a plugin by name.

        Args:
            plugin_name: Name of plugin to unregister

        Returns:
            FlextResult indicating success or not found error

        """
        if plugin_name not in self._plugins:
            return FlextResult.fail(f"Plugin {plugin_name} not found")

        del self._plugins[plugin_name]
        self._logger.info(f"Unregistered plugin {plugin_name}")
        return FlextResult.ok(None)

    def get_plugin(self, plugin_name: str) -> FlextResult[FlextPlugin]:
        """Get plugin by name.

        Args:
            plugin_name: Name of plugin to retrieve

        Returns:
            FlextResult containing plugin or not found error

        """
        if plugin_name not in self._plugins:
            return FlextResult.fail(f"Plugin {plugin_name} not found")

        return FlextResult.ok(self._plugins[plugin_name])

    def list_plugins(self) -> list[str]:
        """List all registered plugin names.

        Returns:
            List of registered plugin names

        """
        return list(self._plugins.keys())


class ConcretePluginLoader(FlextPluginLoader):
    """Concrete implementation of plugin loader.

    Handles dynamic plugin loading and discovery.
    """

    def __init__(self, registry: FlextPluginRegistry | None = None) -> None:
        """Initialize plugin loader.

        Args:
            registry: Optional plugin registry to use

        """
        self._registry = registry or ConcretePluginRegistry()  # type: ignore[abstract]
        self._logger = get_logger("plugin.loader")

    def load_plugin(self, plugin_path: str | Path) -> FlextResult[FlextPlugin]:
        """Load plugin from path.

        Args:
            plugin_path: Path to plugin module or package

        Returns:
            FlextResult containing loaded plugin or load error

        """
        try:
            self._logger.info(f"Loading plugin from {plugin_path}")

            # Simplified plugin loading - actual implementation would
            # dynamically import and instantiate plugin
            plugin = ConcretePlugin(  # type: ignore[abstract]
                name=f"loaded-from-{plugin_path}",
                version="1.0.0",
            )

            # Register loaded plugin
            reg_result = self._registry.register(plugin)  # type: ignore[attr-defined]
            if not reg_result.success:
                return FlextResult.fail(f"Failed to register loaded plugin: {reg_result.error}")

            return FlextResult.ok(plugin)

        except Exception as e:
            self._logger.exception(f"Failed to load plugin from {plugin_path}")
            return FlextResult.fail(f"Load failed: {e!s}")

    def discover_plugins(self, search_path: str) -> FlextResult[list[str]]:
        """Discover available plugins in path.

        Args:
            search_path: Directory to search for plugins

        Returns:
            FlextResult containing list of discovered plugin paths

        """
        try:
            self._logger.info(f"Discovering plugins in {search_path}")

            # Simplified discovery - actual implementation would
            # scan directory for valid plugin packages
            discovered = [
                f"{search_path}/plugin1",
                f"{search_path}/plugin2",
            ]

            return FlextResult.ok(discovered)

        except Exception as e:
            self._logger.exception(f"Plugin discovery failed in {search_path}")
            return FlextResult.fail(f"Discovery failed: {e!s}")
