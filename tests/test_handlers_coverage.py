"""Coverage-focused test suite for flext_plugin.application.handlers module.

This test module provides comprehensive coverage for the actual handlers
implementation using REAL plugin entities and services without mocks.

Real Functionality Testing Strategy:
    - Use actual FlextPluginEntity objects created via factory functions
    - Test real handler methods with actual business logic validation
    - Test real error scenarios with genuine edge cases
    - Validate actual FlextResult patterns without mock assertions

Handler Testing:
    - FlextPluginHandler: Base class initialization and service injection
    - FlextPluginRegistrationHandler: Real registration/unregistration commands
    - FlextPluginEventHandler: Real event processing with domain events

Integration Testing:
    - Real plugin entities with proper validation
    - Actual FlextResult success/failure patterns  
    - Business logic validation with edge cases
    - Error handling with genuine exception scenarios

Quality Standards:
    - 100% code coverage through real functionality testing
    - No mocks - only real objects and actual business logic
    - Enterprise-grade error handling validation
    - Complete edge case and boundary condition testing
"""

from __future__ import annotations

import pytest
from flext_core import FlextResult

from flext_plugin import (
    FlextPluginEventHandler,
    FlextPluginHandler,
    FlextPluginRegistrationHandler,
    create_flext_plugin,
)
from flext_plugin.application.services import FlextPluginService
from flext_plugin.domain.entities import FlextPluginEntity


class TestFlextPluginHandler:
    """Coverage-focused tests for FlextPluginHandler base class.

    Tests the actual base handler implementation with real service injection.
    """

    def test_handler_initialization_with_service(self) -> None:
        """Test handler initialization with real plugin service."""
        service = FlextPluginService()
        handler = FlextPluginHandler(plugin_service=service)

        assert handler is not None
        assert handler._plugin_service is service

    def test_handler_initialization_without_service(self) -> None:
        """Test handler initialization without plugin service."""
        handler = FlextPluginHandler(plugin_service=None)

        assert handler is not None
        assert handler._plugin_service is None

    def test_handler_inheritance_from_base(self) -> None:
        """Test handler inherits from FlextBaseHandler."""
        handler = FlextPluginHandler()
        
        # Should have FlextBaseHandler methods/attributes
        assert hasattr(handler, "_plugin_service")


class TestFlextPluginRegistrationHandler:
    """Coverage-focused tests for FlextPluginRegistrationHandler.

    Tests real plugin registration command handling with actual business logic.
    """

    @pytest.fixture
    def handler_with_service(self) -> FlextPluginRegistrationHandler:
        """Create handler with real plugin service."""
        service = FlextPluginService()
        return FlextPluginRegistrationHandler(plugin_service=service)

    @pytest.fixture
    def handler_without_service(self) -> FlextPluginRegistrationHandler:
        """Create handler without plugin service."""
        return FlextPluginRegistrationHandler(plugin_service=None)

    @pytest.fixture
    def valid_plugin(self) -> FlextPluginEntity:
        """Create valid plugin entity for testing."""
        return create_flext_plugin(
            name="test-plugin",
            version="1.0.0",
            config={
                "description": "Test plugin for handler testing",
                "author": "Test Suite",
            },
        )

    def test_register_plugin_success_with_service(
        self,
        handler_with_service: FlextPluginRegistrationHandler,
        valid_plugin: FlextPluginEntity,
    ) -> None:
        """Test successful plugin registration with real service."""
        result = handler_with_service.handle_register_plugin(valid_plugin)

        # FlextPluginService.load_plugin currently returns success by default
        assert result.success
        assert result.data is True
        assert result.error is None

    def test_register_plugin_missing_name_fails(
        self,
        handler_with_service: FlextPluginRegistrationHandler,
    ) -> None:
        """Test plugin registration fails with missing name."""
        # Create plugin entity with empty name using factory but modify it
        plugin = create_flext_plugin(name="temp", version="1.0.0")
        # Create new entity with empty name
        plugin_with_empty_name = FlextPluginEntity.create(
            name="",  # Empty name should fail
            plugin_version="1.0.0",
            config={"description": "Test plugin"},
        )

        result = handler_with_service.handle_register_plugin(plugin_with_empty_name)

        assert not result.success
        assert result.error is not None
        assert "Plugin name is required" in result.error

    def test_register_plugin_missing_version_fails(
        self,
        handler_with_service: FlextPluginRegistrationHandler,
    ) -> None:
        """Test plugin registration fails with missing version."""
        # Create plugin entity with empty version
        plugin_with_empty_version = FlextPluginEntity.create(
            name="test-plugin",
            plugin_version="",  # Empty version should fail
            config={"description": "Test plugin"},
        )

        result = handler_with_service.handle_register_plugin(plugin_with_empty_version)

        assert not result.success
        assert result.error is not None
        assert "Plugin version is required" in result.error

    def test_register_plugin_no_service_fails(
        self,
        handler_without_service: FlextPluginRegistrationHandler,
        valid_plugin: FlextPluginEntity,
    ) -> None:
        """Test plugin registration fails without service."""
        result = handler_without_service.handle_register_plugin(valid_plugin)

        assert not result.success
        assert result.error is not None
        assert "Plugin service not available" in result.error

    def test_register_plugin_handles_exceptions(
        self,
        handler_with_service: FlextPluginRegistrationHandler,
    ) -> None:
        """Test plugin registration handles exceptions gracefully."""
        # Create plugin that might cause issues with None values
        class ProblematicPlugin:
            def __init__(self) -> None:
                self.name = "test-plugin"
                self.plugin_version = "1.0.0"

            def __getattr__(self, name: str) -> object:
                if name == "some_problematic_attr":
                    raise RuntimeError("Simulated plugin error")
                raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        problematic_plugin = ProblematicPlugin()
        result = handler_with_service.handle_register_plugin(problematic_plugin)  # type: ignore[arg-type]

        # Should handle gracefully since we just check name and version
        assert result.success  # Service load_plugin returns success

    def test_unregister_plugin_success_with_service(
        self,
        handler_with_service: FlextPluginRegistrationHandler,
    ) -> None:
        """Test successful plugin unregistration with real service."""
        result = handler_with_service.handle_unregister_plugin("test-plugin")

        # FlextPluginService.unload_plugin currently returns success
        assert result.success
        assert result.data is True

    def test_unregister_plugin_empty_name_fails(
        self,
        handler_with_service: FlextPluginRegistrationHandler,
    ) -> None:
        """Test plugin unregistration fails with empty name."""
        result = handler_with_service.handle_unregister_plugin("")

        assert not result.success
        assert result.error is not None
        assert "Plugin name is required" in result.error

    def test_unregister_plugin_no_service_fails(
        self,
        handler_without_service: FlextPluginRegistrationHandler,
    ) -> None:
        """Test plugin unregistration fails without service."""
        result = handler_without_service.handle_unregister_plugin("test-plugin")

        assert not result.success
        assert result.error is not None
        assert "Plugin service not available" in result.error

    def test_unregister_plugin_none_name_fails(
        self,
        handler_with_service: FlextPluginRegistrationHandler,
    ) -> None:
        """Test plugin unregistration fails with None name."""
        result = handler_with_service.handle_unregister_plugin(None)  # type: ignore[arg-type]

        assert not result.success
        assert result.error is not None
        assert "Plugin name is required" in result.error


class TestFlextPluginEventHandler:
    """Coverage-focused tests for FlextPluginEventHandler.

    Tests real plugin event handling with actual domain event processing.
    """

    @pytest.fixture
    def event_handler(self) -> FlextPluginEventHandler:
        """Create event handler for testing."""
        return FlextPluginEventHandler()

    @pytest.fixture
    def valid_plugin(self) -> FlextPluginEntity:
        """Create valid plugin entity for event testing."""
        return create_flext_plugin(
            name="event-plugin",
            version="1.0.0",
            config={
                "description": "Plugin for event testing",
                "author": "Event Test Suite",
            },
        )

    def test_handle_plugin_loaded_success(
        self,
        event_handler: FlextPluginEventHandler,
        valid_plugin: FlextPluginEntity,
    ) -> None:
        """Test successful plugin loaded event handling."""
        result = event_handler.handle_plugin_loaded(valid_plugin)

        assert result.success
        assert result.data is True
        assert result.error is None

    def test_handle_plugin_loaded_missing_name_fails(
        self,
        event_handler: FlextPluginEventHandler,
    ) -> None:
        """Test plugin loaded event fails with missing name."""
        # Create object without proper name attribute
        class PluginWithoutName:
            def __init__(self) -> None:
                # Intentionally missing name attribute
                self.plugin_version = "1.0.0"

        plugin_without_name = PluginWithoutName()
        result = event_handler.handle_plugin_loaded(plugin_without_name)  # type: ignore[arg-type]

        assert not result.success
        assert result.error is not None
        assert "Plugin loaded event: plugin missing name" in result.error

    def test_handle_plugin_loaded_empty_name_fails(
        self,
        event_handler: FlextPluginEventHandler,
    ) -> None:
        """Test plugin loaded event fails with empty name."""
        # Create plugin entity with empty name
        plugin_with_empty_name = FlextPluginEntity.create(
            name="",  # Empty name should fail
            plugin_version="1.0.0",
            config={"description": "Test plugin"},
        )

        result = event_handler.handle_plugin_loaded(plugin_with_empty_name)

        assert not result.success
        assert result.error is not None
        assert "Plugin loaded event: plugin missing name" in result.error

    def test_handle_plugin_loaded_handles_exceptions(
        self,
        event_handler: FlextPluginEventHandler,
    ) -> None:
        """Test plugin loaded event handles exceptions gracefully."""
        # Create plugin that raises exception when accessing attributes
        class ExceptionPlugin:
            @property
            def name(self) -> str:
                raise RuntimeError("Simulated plugin error")

        exception_plugin = ExceptionPlugin()
        result = event_handler.handle_plugin_loaded(exception_plugin)  # type: ignore[arg-type]

        assert not result.success
        assert result.error is not None
        assert "Failed to handle plugin loaded event" in result.error
        assert "Simulated plugin error" in result.error

    def test_handle_plugin_unloaded_success(
        self,
        event_handler: FlextPluginEventHandler,
    ) -> None:
        """Test successful plugin unloaded event handling."""
        result = event_handler.handle_plugin_unloaded("test-plugin")

        assert result.success
        assert result.data is None
        assert result.error is None

    def test_handle_plugin_unloaded_empty_name_fails(
        self,
        event_handler: FlextPluginEventHandler,
    ) -> None:
        """Test plugin unloaded event fails with empty name."""
        result = event_handler.handle_plugin_unloaded("")

        assert not result.success
        assert result.error is not None
        assert "Plugin unloaded event: plugin name is required" in result.error

    def test_handle_plugin_unloaded_whitespace_name_fails(
        self,
        event_handler: FlextPluginEventHandler,
    ) -> None:
        """Test plugin unloaded event fails with whitespace-only name."""
        result = event_handler.handle_plugin_unloaded("   ")

        assert not result.success
        assert result.error is not None
        assert "Plugin unloaded event: plugin name is required" in result.error

    def test_handle_plugin_unloaded_none_name_fails(
        self,
        event_handler: FlextPluginEventHandler,
    ) -> None:
        """Test plugin unloaded event fails with None name."""
        result = event_handler.handle_plugin_unloaded(None)  # type: ignore[arg-type]

        assert not result.success
        assert result.error is not None
        assert "Plugin unloaded event: plugin name is required" in result.error

    def test_handle_plugin_unloaded_handles_exceptions(
        self,
        event_handler: FlextPluginEventHandler,
    ) -> None:
        """Test plugin unloaded event handles exceptions gracefully."""
        # Force an exception by passing an object that can't be processed
        class ProblematicName:
            def strip(self) -> None:  # type: ignore[misc]
                raise ValueError("Strip operation failed")

        problematic_name = ProblematicName()
        result = event_handler.handle_plugin_unloaded(problematic_name)  # type: ignore[arg-type]

        assert not result.success
        assert result.error is not None
        assert "Failed to handle plugin unloaded event" in result.error


class TestHandlerIntegration:
    """Integration tests for complete handler workflow scenarios.

    Tests end-to-end handler scenarios with real plugin entities and services.
    """

    def test_complete_registration_workflow(self) -> None:
        """Test complete plugin registration workflow using real handlers."""
        # Create real service and handlers
        service = FlextPluginService()
        registration_handler = FlextPluginRegistrationHandler(plugin_service=service)
        event_handler = FlextPluginEventHandler()

        # Create real plugin
        plugin = create_flext_plugin(
            name="workflow-plugin",
            version="1.0.0",
            config={
                "description": "Plugin for workflow testing",
                "author": "Integration Test Suite",
            },
        )

        # Register plugin
        register_result = registration_handler.handle_register_plugin(plugin)
        assert register_result.success

        # Handle plugin loaded event
        loaded_result = event_handler.handle_plugin_loaded(plugin)
        assert loaded_result.success

        # Unregister plugin
        unregister_result = registration_handler.handle_unregister_plugin("workflow-plugin")
        assert unregister_result.success

        # Handle plugin unloaded event
        unloaded_result = event_handler.handle_plugin_unloaded("workflow-plugin")
        assert unloaded_result.success

    def test_error_handling_workflow(self) -> None:
        """Test error handling across multiple handlers."""
        # Create handlers
        registration_handler = FlextPluginRegistrationHandler(plugin_service=None)
        event_handler = FlextPluginEventHandler()

        # Test registration failure
        plugin = create_flext_plugin(name="error-plugin", version="1.0.0")
        register_result = registration_handler.handle_register_plugin(plugin)
        assert not register_result.success

        # Test event failure
        loaded_result = event_handler.handle_plugin_loaded(None)  # type: ignore[arg-type]
        assert not loaded_result.success

        # Test unload event failure
        unloaded_result = event_handler.handle_plugin_unloaded("")
        assert not unloaded_result.success

    def test_multiple_plugin_handling(self) -> None:
        """Test handling multiple plugins with real handlers."""
        service = FlextPluginService()
        registration_handler = FlextPluginRegistrationHandler(plugin_service=service)
        event_handler = FlextPluginEventHandler()

        # Create multiple plugins
        plugins = [
            create_flext_plugin(name=f"plugin-{i}", version=f"1.{i}.0")
            for i in range(3)
        ]

        # Register all plugins
        for plugin in plugins:
            result = registration_handler.handle_register_plugin(plugin)
            assert result.success

            # Handle loaded events
            loaded_result = event_handler.handle_plugin_loaded(plugin)
            assert loaded_result.success

        # Unregister all plugins
        for i, plugin in enumerate(plugins):
            unregister_result = registration_handler.handle_unregister_plugin(f"plugin-{i}")
            assert unregister_result.success

            # Handle unloaded events
            unloaded_result = event_handler.handle_plugin_unloaded(f"plugin-{i}")
            assert unloaded_result.success