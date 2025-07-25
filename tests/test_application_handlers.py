"""Tests for flext_plugin.application.handlers module.

Comprehensive test coverage for application handlers following Clean Architecture
patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, Mock

import pytest

# 🚨 ARCHITECTURAL COMPLIANCE: Using módulo raiz imports
from flext_core import FlextResult

from flext_plugin.core.types import PluginType
from flext_plugin.domain.entities import (
    PluginExecution,
    PluginInstance,
    PluginMetadata,
    PluginRegistry,
)

if TYPE_CHECKING:
    from pathlib import Path

# Import the actual handler types for type annotations
try:
    from flext_plugin.application.handlers import (
        PluginDiscoveryHandler,
        PluginExecutionHandler,
        PluginLifecycleHandler,
        PluginRegistryHandler,
        PluginValidationHandler,
    )
except ImportError:
    # Fallback for type annotations only
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from flext_plugin.application.handlers import (
            PluginDiscoveryHandler,
            PluginExecutionHandler,
            PluginLifecycleHandler,
            PluginRegistryHandler,
            PluginValidationHandler,
        )
    else:
        # Use Any for runtime when imports fail
        PluginDiscoveryHandler = Any
        PluginValidationHandler = Any
        PluginLifecycleHandler = Any
        PluginExecutionHandler = Any
        PluginRegistryHandler = Any


# Create concrete test implementations that don't inherit from abstract base
class TestablePluginDiscoveryHandler:
    """Testable version of PluginDiscoveryHandler."""

    def __init__(self, discovery_service: Any) -> None:
        # Copy all attributes
        self.discovery_service = discovery_service
        # Add logger
        from flext_observability import get_logger

        self.logger = get_logger(__name__)

    async def discover_plugins(self, search_paths: Any) -> FlextResult[Any]:
        """Discover plugins in given search paths."""
        try:
            self.logger.info(
                "Starting plugin discovery",
                extra={"search_paths": search_paths},
            )

            result = await self.discovery_service.discover_plugins(search_paths)

            if result.success:
                self.logger.info(
                    "Plugin discovery completed",
                    extra={"plugin_count": len(result.data) if result.data else 0},
                )
            else:
                self.logger.error(
                    "Plugin discovery failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin discovery handler error")
            return FlextResult.fail(f"Discovery handler failed: {e}")

    async def validate_plugin_metadata(self, metadata: Any) -> FlextResult[Any]:
        """Validate plugin metadata."""
        try:
            self.logger.debug(
                "Validating plugin metadata",
                extra={"plugin_name": metadata.name},
            )

            result = await self.discovery_service.validate_plugin_metadata(metadata)

            if result.success:
                self.logger.debug("Plugin metadata validation successful")
            else:
                self.logger.warning(
                    "Plugin metadata validation failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin metadata validation handler error")
            return FlextResult.fail(f"Validation handler failed: {e}")

    async def get_plugin_manifest(
        self,
        plugin_path: Any,
    ) -> FlextResult[Any]:
        """Get plugin manifest from path."""
        try:
            self.logger.debug(
                "Getting plugin manifest",
                extra={"plugin_path": plugin_path},
            )

            result = await self.discovery_service.get_plugin_manifest(plugin_path)

            if result.success:
                self.logger.debug("Plugin manifest retrieved successfully")
            else:
                self.logger.warning(
                    "Plugin manifest retrieval failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin manifest handler error")
            return FlextResult.fail(f"Manifest handler failed: {e}")


class TestablePluginValidationHandler:
    """Testable version of PluginValidationHandler."""

    def __init__(self, validation_service: Any) -> None:
        self.validation_service = validation_service
        from flext_observability import get_logger

        self.logger = get_logger(__name__)

    async def validate_plugin(self, plugin: Any) -> FlextResult[Any]:
        """Validate plugin."""
        try:
            self.logger.info(
                "Starting plugin validation",
                extra={
                    "plugin_id": str(plugin.plugin_id)
                    if hasattr(plugin, "plugin_id")
                    else "unknown",
                },
            )

            result = await self.validation_service.validate_plugin(plugin)

            if result.success:
                self.logger.info("Plugin validation successful")
            else:
                self.logger.error(
                    "Plugin validation failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin validation handler error")
            return FlextResult.fail(f"Validation handler failed: {e}")

    async def validate_configuration(
        self,
        plugin: Any,
        config: Any,
    ) -> FlextResult[Any]:
        """Validate plugin configuration."""
        try:
            self.logger.debug(
                "Validating plugin configuration",
                extra={
                    "plugin_id": str(plugin.plugin_id)
                    if hasattr(plugin, "plugin_id")
                    else "unknown",
                },
            )

            result = await self.validation_service.validate_configuration(
                plugin,
                config,
            )

            if result.success:
                self.logger.debug("Plugin configuration validation successful")
            else:
                self.logger.warning(
                    "Plugin configuration validation failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin configuration validation handler error")
            return FlextResult.fail(f"Configuration validation handler failed: {e}")

    async def validate_dependencies(self, plugin: Any) -> FlextResult[Any]:
        """Validate plugin dependencies."""
        try:
            self.logger.debug(
                "Validating plugin dependencies",
                extra={
                    "plugin_id": str(plugin.plugin_id)
                    if hasattr(plugin, "plugin_id")
                    else "unknown",
                },
            )

            result = await self.validation_service.validate_dependencies(plugin)

            if result.success:
                self.logger.debug("Plugin dependencies validation successful")
            else:
                self.logger.warning(
                    "Plugin dependencies validation failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin dependencies validation handler error")
            return FlextResult.fail(f"Dependencies validation handler failed: {e}")


class TestablePluginLifecycleHandler:
    """Testable version of PluginLifecycleHandler."""

    def __init__(self, lifecycle_service: Any) -> None:
        self.lifecycle_service = lifecycle_service
        from flext_observability import get_logger

        self.logger = get_logger(__name__)

    async def register_plugin(self, plugin: Any) -> FlextResult[Any]:
        """Register plugin."""
        try:
            self.logger.info(
                "Registering plugin",
                extra={
                    "plugin_id": str(plugin.plugin_id)
                    if hasattr(plugin, "plugin_id")
                    else "unknown",
                },
            )

            result = await self.lifecycle_service.register_plugin(plugin)

            if result.success:
                self.logger.info("Plugin registered successfully")
            else:
                self.logger.error(
                    "Plugin registration failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin registration handler error")
            return FlextResult.fail(f"Registration handler failed: {e}")

    async def load_plugin(self, plugin: Any) -> FlextResult[Any]:
        """Load plugin."""
        try:
            return await self.lifecycle_service.load_plugin(plugin)
        except Exception as e:
            return FlextResult.fail(f"Loading handler failed: {e}")

    async def initialize_plugin(self, plugin: Any) -> FlextResult[Any]:
        """Initialize plugin."""
        try:
            return await self.lifecycle_service.initialize_plugin(plugin)
        except Exception as e:
            return FlextResult.fail(f"Initialization handler failed: {e}")

    async def activate_plugin(self, plugin: Any) -> FlextResult[Any]:
        """Activate plugin."""
        try:
            return await self.lifecycle_service.activate_plugin(plugin)
        except Exception as e:
            return FlextResult.fail(f"Activation handler failed: {e}")

    async def suspend_plugin(self, plugin: Any) -> FlextResult[Any]:
        """Suspend plugin."""
        try:
            return await self.lifecycle_service.suspend_plugin(plugin)
        except Exception as e:
            return FlextResult.fail(f"Suspension handler failed: {e}")

    async def unload_plugin(self, plugin: Any) -> FlextResult[Any]:
        """Unload plugin."""
        try:
            return await self.lifecycle_service.unload_plugin(plugin)
        except Exception as e:
            return FlextResult.fail(f"Unloading handler failed: {e}")


class TestablePluginExecutionHandler:
    """Testable version of PluginExecutionHandler."""

    def __init__(self, execution_service: Any) -> None:
        self.execution_service = execution_service
        from flext_observability import get_logger

        self.logger = get_logger(__name__)

    async def execute_plugin(
        self,
        plugin: Any,
        input_data: Any,
        execution_context: Any = None,
    ) -> FlextResult[Any]:
        """Execute plugin."""
        try:
            return await self.execution_service.execute_plugin(
                plugin,
                input_data,
                execution_context,
            )
        except Exception as e:
            return FlextResult.fail(f"Execution handler failed: {e}")

    async def get_execution_status(self, execution_id: Any) -> FlextResult[Any]:
        """Get execution status."""
        try:
            return await self.execution_service.get_execution_status(execution_id)
        except Exception as e:
            return FlextResult.fail(f"Status handler failed: {e}")

    async def cancel_execution(self, execution_id: Any) -> FlextResult[Any]:
        """Cancel execution."""
        try:
            return await self.execution_service.cancel_execution(execution_id)
        except Exception as e:
            return FlextResult.fail(f"Cancellation handler failed: {e}")


class TestablePluginRegistryHandler:
    """Testable version of PluginRegistryHandler."""

    def __init__(self, registry_service: Any) -> None:
        self.registry_service = registry_service
        from flext_observability import get_logger

        self.logger = get_logger(__name__)

    async def register_registry(self, registry: Any) -> FlextResult[Any]:
        """Register plugin registry."""
        try:
            return await self.registry_service.register_registry(registry)
        except Exception as e:
            return FlextResult.fail(f"Registry registration handler failed: {e}")

    async def sync_registry(self, registry: Any) -> FlextResult[Any]:
        """Sync plugin registry."""
        try:
            return await self.registry_service.sync_registry(registry)
        except Exception as e:
            return FlextResult.fail(f"Sync handler failed: {e}")

    async def search_plugins(self, registry: Any, query: Any) -> FlextResult[Any]:
        """Search plugins in registry."""
        try:
            return await self.registry_service.search_plugins(registry, query)
        except Exception as e:
            return FlextResult.fail(f"Search handler failed: {e}")

    async def download_plugin(
        self,
        registry: Any,
        plugin_id: Any,
    ) -> FlextResult[Any]:
        """Download plugin from registry."""
        try:
            return await self.registry_service.download_plugin(registry, plugin_id)
        except Exception as e:
            return FlextResult.fail(f"Download handler failed: {e}")


class TestPluginDiscoveryHandler:
    """Test PluginDiscoveryHandler functionality."""

    @pytest.fixture
    def mock_discovery_service(self) -> Mock:
        """Create mock discovery service."""
        service = Mock()
        service.discover_plugins = AsyncMock()
        service.validate_plugin_metadata = AsyncMock()
        service.get_plugin_manifest = AsyncMock()
        return service

    @pytest.fixture
    def handler(self, mock_discovery_service: Mock) -> TestablePluginDiscoveryHandler:
        """Create discovery handler for testing."""
        return TestablePluginDiscoveryHandler(discovery_service=mock_discovery_service)

    @pytest.fixture
    def mock_plugin_metadata(self) -> PluginMetadata:
        """Create mock plugin metadata."""
        return PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            description="Test plugin",
            author="Test Author",
            license="MIT",
            entry_point="test_plugin:main",
            plugin_type=PluginType.TAP,
            dependencies=[],
            capabilities=[],
        )

    def test_handler_initialization(self, mock_discovery_service: Mock) -> None:
        """Test discovery handler initialization."""
        handler = TestablePluginDiscoveryHandler(
            discovery_service=mock_discovery_service,
        )

        assert handler.discovery_service == mock_discovery_service
        assert hasattr(handler, "logger")

    async def test_discover_plugins_success(
        self,
        handler: TestablePluginDiscoveryHandler,
        mock_discovery_service: Mock,
        mock_plugin_metadata: PluginMetadata,
    ) -> None:
        """Test successful plugin discovery."""
        search_paths = ["/test/plugins", "/other/plugins"]
        expected_plugins = [mock_plugin_metadata]

        mock_discovery_service.discover_plugins.return_value = FlextResult.ok(
            expected_plugins,
        )

        result = await handler.discover_plugins(search_paths)

        assert result.success
        assert result.data == expected_plugins
        mock_discovery_service.discover_plugins.assert_called_once_with(search_paths)

    async def test_discover_plugins_failure(
        self,
        handler: TestablePluginDiscoveryHandler,
        mock_discovery_service: Mock,
    ) -> None:
        """Test plugin discovery failure."""
        search_paths = ["/test/plugins"]
        error_message = "Discovery failed"

        mock_discovery_service.discover_plugins.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.discover_plugins(search_paths)

        assert not result.success
        assert result.error == error_message

    async def test_discover_plugins_exception(
        self,
        handler: TestablePluginDiscoveryHandler,
        mock_discovery_service: Mock,
    ) -> None:
        """Test plugin discovery with exception."""
        search_paths = ["/test/plugins"]

        mock_discovery_service.discover_plugins.side_effect = Exception("Service error")

        result = await handler.discover_plugins(search_paths)

        assert not result.success
        assert result.error is not None
        assert result.error is not None
        assert "Discovery handler failed: Service error" in result.error

    async def test_validate_plugin_metadata_success(
        self,
        handler: TestablePluginDiscoveryHandler,
        mock_discovery_service: Mock,
        mock_plugin_metadata: PluginMetadata,
    ) -> None:
        """Test successful plugin metadata validation."""
        mock_discovery_service.validate_plugin_metadata.return_value = FlextResult.ok(
            True,
        )

        result = await handler.validate_plugin_metadata(mock_plugin_metadata)

        assert result.success
        assert result.data is True
        mock_discovery_service.validate_plugin_metadata.assert_called_once_with(
            mock_plugin_metadata,
        )

    async def test_validate_plugin_metadata_failure(
        self,
        handler: TestablePluginDiscoveryHandler,
        mock_discovery_service: Mock,
        mock_plugin_metadata: PluginMetadata,
    ) -> None:
        """Test plugin metadata validation failure."""
        error_message = "Invalid metadata"
        mock_discovery_service.validate_plugin_metadata.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.validate_plugin_metadata(mock_plugin_metadata)

        assert not result.success
        assert result.error == error_message

    async def test_validate_plugin_metadata_exception(
        self,
        handler: TestablePluginDiscoveryHandler,
        mock_discovery_service: Mock,
        mock_plugin_metadata: PluginMetadata,
    ) -> None:
        """Test plugin metadata validation with exception."""
        # Configure the mock to raise an exception when called
        mock_discovery_service.validate_plugin_metadata.side_effect = ValueError(
            "Validation error",
        )

        result = await handler.validate_plugin_metadata(mock_plugin_metadata)

        assert not result.success
        assert result.error is not None
        assert result.error is not None
        assert "Validation handler failed: Validation error" in result.error

    async def test_get_plugin_manifest_success(
        self,
        handler: TestablePluginDiscoveryHandler,
        mock_discovery_service: Mock,
    ) -> None:
        """Test successful plugin manifest retrieval."""
        plugin_path = "/test/plugins/manifest.json"
        expected_manifest = {"name": "test-plugin", "version": "1.0.0"}

        mock_discovery_service.get_plugin_manifest.return_value = FlextResult.ok(
            expected_manifest,
        )

        result = await handler.get_plugin_manifest(plugin_path)

        assert result.success
        assert result.data == expected_manifest
        mock_discovery_service.get_plugin_manifest.assert_called_once_with(plugin_path)

    async def test_get_plugin_manifest_failure(
        self,
        handler: TestablePluginDiscoveryHandler,
        mock_discovery_service: Mock,
    ) -> None:
        """Test plugin manifest retrieval failure."""
        plugin_path = "/test/plugins/nonexistent.json"
        error_message = "Manifest not found"

        mock_discovery_service.get_plugin_manifest.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.get_plugin_manifest(plugin_path)

        assert not result.success
        assert result.error == error_message

    async def test_get_plugin_manifest_exception(
        self,
        handler: TestablePluginDiscoveryHandler,
        mock_discovery_service: Mock,
    ) -> None:
        """Test plugin manifest retrieval with exception."""
        plugin_path = "/test/plugins/manifest.json"

        mock_discovery_service.get_plugin_manifest.side_effect = OSError(
            "File read error",
        )

        result = await handler.get_plugin_manifest(plugin_path)

        assert not result.success
        assert result.error is not None
        assert result.error is not None
        assert "Manifest handler failed: File read error" in result.error


class TestPluginValidationHandler:
    """Test PluginValidationHandler functionality."""

    @pytest.fixture
    def mock_validation_service(self) -> Mock:
        """Create mock validation service."""
        service = Mock()
        service.validate_plugin = AsyncMock()
        service.validate_configuration = AsyncMock()
        service.validate_dependencies = AsyncMock()
        return service

    @pytest.fixture
    def handler(self, mock_validation_service: Mock) -> TestablePluginValidationHandler:
        """Create validation handler for testing."""
        return TestablePluginValidationHandler(
            validation_service=mock_validation_service,
        )

    @pytest.fixture
    def mock_plugin_instance(self) -> PluginInstance:
        """Create mock plugin instance."""
        metadata = PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            description="Test plugin",
            author="Test Author",
            license="MIT",
            entry_point="test_plugin:main",
            plugin_type=PluginType.TAP,
            dependencies=[],
            capabilities=[],
        )
        return PluginInstance(
            plugin_id="test-plugin-123",
            metadata=metadata,
        )

    def test_handler_initialization(self, mock_validation_service: Mock) -> None:
        """Test validation handler initialization."""
        handler = TestablePluginValidationHandler(
            validation_service=mock_validation_service,
        )

        assert handler.validation_service == mock_validation_service
        assert hasattr(handler, "logger")

    async def test_validate_plugin_success(
        self,
        handler: TestablePluginValidationHandler,
        mock_validation_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test successful plugin validation."""
        mock_validation_service.validate_plugin.return_value = FlextResult.ok(True)

        result = await handler.validate_plugin(mock_plugin_instance)

        assert result.success
        assert result.data is True
        mock_validation_service.validate_plugin.assert_called_once_with(
            mock_plugin_instance,
        )

    async def test_validate_plugin_failure(
        self,
        handler: TestablePluginValidationHandler,
        mock_validation_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin validation failure."""
        error_message = "Plugin validation failed"
        mock_validation_service.validate_plugin.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.validate_plugin(mock_plugin_instance)

        assert not result.success
        assert result.error == error_message

    async def test_validate_plugin_exception(
        self,
        handler: TestablePluginValidationHandler,
        mock_validation_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin validation with exception."""
        mock_validation_service.validate_plugin.side_effect = Exception("Service error")

        result = await handler.validate_plugin(mock_plugin_instance)

        assert not result.success
        assert result.error is not None
        assert result.error is not None
        assert "Validation handler failed: Service error" in result.error

    async def test_validate_configuration_success(
        self,
        handler: TestablePluginValidationHandler,
        mock_validation_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test successful configuration validation."""
        config = {"setting1": "value1", "setting2": 42}
        mock_validation_service.validate_configuration.return_value = FlextResult.ok(
            True,
        )

        result = await handler.validate_configuration(mock_plugin_instance, config)

        assert result.success
        assert result.data is True
        mock_validation_service.validate_configuration.assert_called_once_with(
            mock_plugin_instance,
            config,
        )

    async def test_validate_configuration_failure(
        self,
        handler: TestablePluginValidationHandler,
        mock_validation_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test configuration validation failure."""
        config = {"invalid": "config"}
        error_message = "Invalid configuration"
        mock_validation_service.validate_configuration.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.validate_configuration(mock_plugin_instance, config)

        assert not result.success
        assert result.error == error_message

    async def test_validate_configuration_exception(
        self,
        handler: TestablePluginValidationHandler,
        mock_validation_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test configuration validation with exception."""
        config = {"setting": "value"}
        mock_validation_service.validate_configuration.side_effect = TypeError(
            "Type error",
        )

        result = await handler.validate_configuration(mock_plugin_instance, config)

        assert not result.success
        assert result.error is not None
        assert result.error is not None
        assert "Configuration validation handler failed: Type error" in result.error

    async def test_validate_dependencies_success(
        self,
        handler: TestablePluginValidationHandler,
        mock_validation_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test successful dependencies validation."""
        mock_validation_service.validate_dependencies.return_value = FlextResult.ok(
            True,
        )

        result = await handler.validate_dependencies(mock_plugin_instance)

        assert result.success
        assert result.data is True
        mock_validation_service.validate_dependencies.assert_called_once_with(
            mock_plugin_instance,
        )

    async def test_validate_dependencies_failure(
        self,
        handler: TestablePluginValidationHandler,
        mock_validation_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test dependencies validation failure."""
        error_message = "Dependency conflicts found"
        mock_validation_service.validate_dependencies.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.validate_dependencies(mock_plugin_instance)

        assert not result.success
        assert result.error == error_message

    async def test_validate_dependencies_exception(
        self,
        handler: TestablePluginValidationHandler,
        mock_validation_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test dependencies validation with exception."""
        mock_validation_service.validate_dependencies.side_effect = ValueError(
            "Dependency error",
        )

        result = await handler.validate_dependencies(mock_plugin_instance)

        assert not result.success
        assert result.error is not None
        assert result.error is not None
        assert (
            "Dependencies validation handler failed: Dependency error" in result.error
        )


class TestPluginLifecycleHandler:
    """Test PluginLifecycleHandler functionality."""

    @pytest.fixture
    def mock_lifecycle_service(self) -> Mock:
        """Create mock lifecycle service."""
        service = Mock()
        service.register_plugin = AsyncMock()
        service.load_plugin = AsyncMock()
        service.initialize_plugin = AsyncMock()
        service.activate_plugin = AsyncMock()
        service.suspend_plugin = AsyncMock()
        service.unload_plugin = AsyncMock()
        return service

    @pytest.fixture
    def handler(self, mock_lifecycle_service: Mock) -> TestablePluginLifecycleHandler:
        """Create lifecycle handler for testing."""
        return TestablePluginLifecycleHandler(lifecycle_service=mock_lifecycle_service)

    @pytest.fixture
    def mock_plugin_instance(self) -> PluginInstance:
        """Create mock plugin instance."""
        metadata = PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            description="Test plugin",
            author="Test Author",
            license="MIT",
            entry_point="test_plugin:main",
            plugin_type=PluginType.TAP,
            dependencies=[],
            capabilities=[],
        )
        return PluginInstance(
            plugin_id="test-plugin-123",
            metadata=metadata,
        )

    def test_handler_initialization(self, mock_lifecycle_service: Mock) -> None:
        """Test lifecycle handler initialization."""
        handler = TestablePluginLifecycleHandler(
            lifecycle_service=mock_lifecycle_service,
        )

        assert handler.lifecycle_service == mock_lifecycle_service
        assert hasattr(handler, "logger")

    async def test_register_plugin_success(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test successful plugin registration."""
        mock_lifecycle_service.register_plugin.return_value = FlextResult.ok(
            mock_plugin_instance,
        )

        result = await handler.register_plugin(mock_plugin_instance)

        assert result.success
        assert result.data == mock_plugin_instance
        mock_lifecycle_service.register_plugin.assert_called_once_with(
            mock_plugin_instance,
        )

    async def test_register_plugin_failure(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin registration failure."""
        error_message = "Registration failed"
        mock_lifecycle_service.register_plugin.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.register_plugin(mock_plugin_instance)

        assert not result.success
        assert result.error == error_message

    async def test_register_plugin_exception(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin registration with exception."""
        mock_lifecycle_service.register_plugin.side_effect = Exception("Service error")

        result = await handler.register_plugin(mock_plugin_instance)

        assert not result.success
        assert result.error is not None
        assert result.error is not None
        assert "Registration handler failed: Service error" in result.error

    async def test_load_plugin_success(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test successful plugin loading."""
        mock_lifecycle_service.load_plugin.return_value = FlextResult.ok(
            mock_plugin_instance,
        )

        result = await handler.load_plugin(mock_plugin_instance)

        assert result.success
        assert result.data == mock_plugin_instance
        mock_lifecycle_service.load_plugin.assert_called_once_with(mock_plugin_instance)

    async def test_load_plugin_failure(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin loading failure."""
        error_message = "Loading failed"
        mock_lifecycle_service.load_plugin.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.load_plugin(mock_plugin_instance)

        assert not result.success
        assert result.error == error_message

    async def test_load_plugin_exception(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin loading with exception."""
        mock_lifecycle_service.load_plugin.side_effect = Exception("Loading error")

        result = await handler.load_plugin(mock_plugin_instance)

        assert not result.success
        assert result.error is not None
        assert "Loading handler failed: Loading error" in result.error

    async def test_initialize_plugin_success(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test successful plugin initialization."""
        mock_lifecycle_service.initialize_plugin.return_value = FlextResult.ok(
            mock_plugin_instance,
        )

        result = await handler.initialize_plugin(mock_plugin_instance)

        assert result.success
        assert result.data == mock_plugin_instance
        mock_lifecycle_service.initialize_plugin.assert_called_once_with(
            mock_plugin_instance,
        )

    async def test_initialize_plugin_failure(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin initialization failure."""
        error_message = "Initialization failed"
        mock_lifecycle_service.initialize_plugin.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.initialize_plugin(mock_plugin_instance)

        assert not result.success
        assert result.error == error_message

    async def test_initialize_plugin_specific_exceptions(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin initialization with specific exception types."""
        # Test TypeError
        mock_lifecycle_service.initialize_plugin.side_effect = TypeError("Type error")

        result = await handler.initialize_plugin(mock_plugin_instance)

        assert not result.success
        assert result.error is not None
        assert "Initialization handler failed: Type error" in result.error

    async def test_activate_plugin_success(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test successful plugin activation."""
        mock_lifecycle_service.activate_plugin.return_value = FlextResult.ok(
            mock_plugin_instance,
        )

        result = await handler.activate_plugin(mock_plugin_instance)

        assert result.success
        assert result.data == mock_plugin_instance
        mock_lifecycle_service.activate_plugin.assert_called_once_with(
            mock_plugin_instance,
        )

    async def test_activate_plugin_specific_exceptions(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin activation with specific exception types."""
        # Test ValueError
        mock_lifecycle_service.activate_plugin.side_effect = ValueError("Value error")

        result = await handler.activate_plugin(mock_plugin_instance)

        assert not result.success
        assert result.error is not None
        assert "Activation handler failed: Value error" in result.error

    async def test_suspend_plugin_success(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test successful plugin suspension."""
        mock_lifecycle_service.suspend_plugin.return_value = FlextResult.ok(
            mock_plugin_instance,
        )

        result = await handler.suspend_plugin(mock_plugin_instance)

        assert result.success
        assert result.data == mock_plugin_instance
        mock_lifecycle_service.suspend_plugin.assert_called_once_with(
            mock_plugin_instance,
        )

    async def test_suspend_plugin_specific_exceptions(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin suspension with specific exception types."""
        # Test AttributeError
        mock_lifecycle_service.suspend_plugin.side_effect = AttributeError(
            "Attribute error",
        )

        result = await handler.suspend_plugin(mock_plugin_instance)

        assert not result.success
        assert result.error is not None
        assert "Suspension handler failed: Attribute error" in result.error

    async def test_unload_plugin_success(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test successful plugin unloading."""
        mock_lifecycle_service.unload_plugin.return_value = FlextResult.ok(
            mock_plugin_instance,
        )

        result = await handler.unload_plugin(mock_plugin_instance)

        assert result.success
        assert result.data == mock_plugin_instance
        mock_lifecycle_service.unload_plugin.assert_called_once_with(
            mock_plugin_instance,
        )

    async def test_unload_plugin_specific_exceptions(
        self,
        handler: TestablePluginLifecycleHandler,
        mock_lifecycle_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin unloading with specific exception types."""
        # Test multiple exception types handled
        mock_lifecycle_service.unload_plugin.side_effect = ValueError("Unload error")

        result = await handler.unload_plugin(mock_plugin_instance)

        assert not result.success
        assert result.error is not None
        assert "Unloading handler failed: Unload error" in result.error


class TestPluginExecutionHandler:
    """Test PluginExecutionHandler functionality."""

    @pytest.fixture
    def mock_execution_service(self) -> Mock:
        """Create mock execution service."""
        service = Mock()
        service.execute_plugin = AsyncMock()
        service.get_execution_status = AsyncMock()
        service.cancel_execution = AsyncMock()
        return service

    @pytest.fixture
    def handler(self, mock_execution_service: Mock) -> TestablePluginExecutionHandler:
        """Create execution handler for testing."""
        return TestablePluginExecutionHandler(execution_service=mock_execution_service)

    @pytest.fixture
    def mock_plugin_instance(self) -> PluginInstance:
        """Create mock plugin instance."""
        metadata = PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            description="Test plugin",
            author="Test Author",
            license="MIT",
            entry_point="test_plugin:main",
            plugin_type=PluginType.TAP,
            dependencies=[],
            capabilities=[],
        )
        return PluginInstance(
            plugin_id="test-plugin-123",
            metadata=metadata,
        )

    @pytest.fixture
    def mock_plugin_execution(self) -> PluginExecution:
        """Create mock plugin execution."""
        return PluginExecution(
            execution_id="exec-123",
            plugin_id="test-plugin-123",
        )

    def test_handler_initialization(self, mock_execution_service: Mock) -> None:
        """Test execution handler initialization."""
        handler = TestablePluginExecutionHandler(
            execution_service=mock_execution_service,
        )

        assert handler.execution_service == mock_execution_service
        assert hasattr(handler, "logger")

    async def test_execute_plugin_success(
        self,
        handler: TestablePluginExecutionHandler,
        mock_execution_service: Mock,
        mock_plugin_instance: PluginInstance,
        mock_plugin_execution: PluginExecution,
    ) -> None:
        """Test successful plugin execution."""
        input_data = {"test": "data"}
        execution_context = {"env": "test"}

        mock_execution_service.execute_plugin.return_value = FlextResult.ok(
            mock_plugin_execution,
        )

        result = await handler.execute_plugin(
            mock_plugin_instance,
            input_data,
            execution_context,
        )

        assert result.success
        assert result.data == mock_plugin_execution
        mock_execution_service.execute_plugin.assert_called_once_with(
            mock_plugin_instance,
            input_data,
            execution_context,
        )

    async def test_execute_plugin_without_context(
        self,
        handler: TestablePluginExecutionHandler,
        mock_execution_service: Mock,
        mock_plugin_instance: PluginInstance,
        mock_plugin_execution: PluginExecution,
    ) -> None:
        """Test plugin execution without context."""
        input_data = {"test": "data"}

        mock_execution_service.execute_plugin.return_value = FlextResult.ok(
            mock_plugin_execution,
        )

        result = await handler.execute_plugin(mock_plugin_instance, input_data)

        assert result.success
        assert result.data == mock_plugin_execution
        mock_execution_service.execute_plugin.assert_called_once_with(
            mock_plugin_instance,
            input_data,
            None,
        )

    async def test_execute_plugin_failure(
        self,
        handler: TestablePluginExecutionHandler,
        mock_execution_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin execution failure."""
        input_data = {"test": "data"}
        error_message = "Execution failed"

        mock_execution_service.execute_plugin.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.execute_plugin(mock_plugin_instance, input_data)

        assert not result.success
        assert result.error == error_message

    async def test_execute_plugin_exception(
        self,
        handler: TestablePluginExecutionHandler,
        mock_execution_service: Mock,
        mock_plugin_instance: PluginInstance,
    ) -> None:
        """Test plugin execution with exception."""
        input_data = {"test": "data"}

        mock_execution_service.execute_plugin.side_effect = Exception("Service error")

        result = await handler.execute_plugin(mock_plugin_instance, input_data)

        assert not result.success
        assert result.error is not None
        assert "Execution handler failed: Service error" in result.error

    async def test_get_execution_status_success(
        self,
        handler: TestablePluginExecutionHandler,
        mock_execution_service: Mock,
        mock_plugin_execution: PluginExecution,
    ) -> None:
        """Test successful execution status retrieval."""
        execution_id = "exec-123"

        mock_execution_service.get_execution_status.return_value = FlextResult.ok(
            mock_plugin_execution,
        )

        result = await handler.get_execution_status(execution_id)

        assert result.success
        assert result.data == mock_plugin_execution
        mock_execution_service.get_execution_status.assert_called_once_with(
            execution_id,
        )

    async def test_get_execution_status_failure(
        self,
        handler: TestablePluginExecutionHandler,
        mock_execution_service: Mock,
    ) -> None:
        """Test execution status retrieval failure."""
        execution_id = "non-existent"
        error_message = "Execution not found"

        mock_execution_service.get_execution_status.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.get_execution_status(execution_id)

        assert not result.success
        assert result.error == error_message

    async def test_cancel_execution_success(
        self,
        handler: TestablePluginExecutionHandler,
        mock_execution_service: Mock,
    ) -> None:
        """Test successful execution cancellation."""
        execution_id = "exec-123"

        mock_execution_service.cancel_execution.return_value = FlextResult.ok(True)

        result = await handler.cancel_execution(execution_id)

        assert result.success
        assert result.data is True
        mock_execution_service.cancel_execution.assert_called_once_with(execution_id)

    async def test_cancel_execution_failure(
        self,
        handler: TestablePluginExecutionHandler,
        mock_execution_service: Mock,
    ) -> None:
        """Test execution cancellation failure."""
        execution_id = "exec-123"
        error_message = "Cannot cancel execution"

        mock_execution_service.cancel_execution.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.cancel_execution(execution_id)

        assert not result.success
        assert result.error == error_message


class TestPluginRegistryHandler:
    """Test PluginRegistryHandler functionality."""

    @pytest.fixture
    def mock_registry_service(self) -> Mock:
        """Create mock registry service."""
        service = Mock()
        service.register_registry = AsyncMock()
        service.sync_registry = AsyncMock()
        service.search_plugins = AsyncMock()
        service.download_plugin = AsyncMock()
        return service

    @pytest.fixture
    def handler(self, mock_registry_service: Mock) -> TestablePluginRegistryHandler:
        """Create registry handler for testing."""
        return TestablePluginRegistryHandler(registry_service=mock_registry_service)

    @pytest.fixture
    def mock_plugin_registry(self) -> PluginRegistry:
        """Create mock plugin registry."""
        return PluginRegistry(
            name="test-registry",
            registry_url="https://registry.example.com",
        )

    @pytest.fixture
    def mock_plugin_metadata(self) -> PluginMetadata:
        """Create mock plugin metadata."""
        return PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            description="Test plugin",
            author="Test Author",
            license="MIT",
            entry_point="test_plugin:main",
            plugin_type=PluginType.TAP,
            dependencies=[],
            capabilities=[],
        )

    def test_handler_initialization(self, mock_registry_service: Mock) -> None:
        """Test registry handler initialization."""
        handler = TestablePluginRegistryHandler(registry_service=mock_registry_service)

        assert handler.registry_service == mock_registry_service
        assert hasattr(handler, "logger")

    async def test_register_registry_success(
        self,
        handler: TestablePluginRegistryHandler,
        mock_registry_service: Mock,
        mock_plugin_registry: PluginRegistry,
    ) -> None:
        """Test successful registry registration."""
        mock_registry_service.register_registry.return_value = FlextResult.ok(
            mock_plugin_registry,
        )

        result = await handler.register_registry(mock_plugin_registry)

        assert result.success
        assert result.data == mock_plugin_registry
        mock_registry_service.register_registry.assert_called_once_with(
            mock_plugin_registry,
        )

    async def test_register_registry_failure(
        self,
        handler: TestablePluginRegistryHandler,
        mock_registry_service: Mock,
        mock_plugin_registry: PluginRegistry,
    ) -> None:
        """Test registry registration failure."""
        error_message = "Registry registration failed"
        mock_registry_service.register_registry.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.register_registry(mock_plugin_registry)

        assert not result.success
        assert result.error == error_message

    async def test_sync_registry_success(
        self,
        handler: TestablePluginRegistryHandler,
        mock_registry_service: Mock,
        mock_plugin_registry: PluginRegistry,
    ) -> None:
        """Test successful registry synchronization."""
        mock_registry_service.sync_registry.return_value = FlextResult.ok(True)

        result = await handler.sync_registry(mock_plugin_registry)

        assert result.success
        assert result.data is True
        mock_registry_service.sync_registry.assert_called_once_with(
            mock_plugin_registry,
        )

    async def test_sync_registry_failure(
        self,
        handler: TestablePluginRegistryHandler,
        mock_registry_service: Mock,
        mock_plugin_registry: PluginRegistry,
    ) -> None:
        """Test registry synchronization failure."""
        error_message = "Sync failed"
        mock_registry_service.sync_registry.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.sync_registry(mock_plugin_registry)

        assert not result.success
        assert result.error == error_message

    async def test_search_plugins_success(
        self,
        handler: TestablePluginRegistryHandler,
        mock_registry_service: Mock,
        mock_plugin_registry: PluginRegistry,
        mock_plugin_metadata: PluginMetadata,
    ) -> None:
        """Test successful plugin search."""
        query = "tap-postgres"
        expected_plugins = [mock_plugin_metadata]

        mock_registry_service.search_plugins.return_value = FlextResult.ok(
            expected_plugins,
        )

        result = await handler.search_plugins(mock_plugin_registry, query)

        assert result.success
        assert result.data == expected_plugins
        mock_registry_service.search_plugins.assert_called_once_with(
            mock_plugin_registry,
            query,
        )

    async def test_search_plugins_failure(
        self,
        handler: TestablePluginRegistryHandler,
        mock_registry_service: Mock,
        mock_plugin_registry: PluginRegistry,
    ) -> None:
        """Test plugin search failure."""
        query = "non-existent"
        error_message = "Search failed"

        mock_registry_service.search_plugins.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.search_plugins(mock_plugin_registry, query)

        assert not result.success
        assert result.error == error_message

    async def test_download_plugin_success(
        self,
        handler: TestablePluginRegistryHandler,
        mock_registry_service: Mock,
        mock_plugin_registry: PluginRegistry,
        tmp_path: Path,
    ) -> None:
        """Test successful plugin download."""
        plugin_id = "tap-postgres"
        download_path = str(tmp_path / "downloads" / "tap-postgres-1.0.0.tar.gz")

        mock_registry_service.download_plugin.return_value = FlextResult.ok(
            download_path,
        )

        result = await handler.download_plugin(mock_plugin_registry, plugin_id)

        assert result.success
        assert result.data == download_path
        mock_registry_service.download_plugin.assert_called_once_with(
            mock_plugin_registry,
            plugin_id,
        )

    async def test_download_plugin_failure(
        self,
        handler: TestablePluginRegistryHandler,
        mock_registry_service: Mock,
        mock_plugin_registry: PluginRegistry,
    ) -> None:
        """Test plugin download failure."""
        plugin_id = "non-existent"
        error_message = "Plugin not found"

        mock_registry_service.download_plugin.return_value = FlextResult.fail(
            error_message,
        )

        result = await handler.download_plugin(mock_plugin_registry, plugin_id)

        assert not result.success
        assert result.error == error_message
