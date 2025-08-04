"""Coverage-focused test suite for flext_plugin.application.handlers module.

This test module focuses on maximizing code coverage for the actual handlers
implementation by testing the real classes that exist in the codebase.

Strategy: Test the 3 real handler classes with comprehensive scenarios:
- FlextPluginHandler (base class)
- FlextPluginRegistrationHandler (registration commands)
- FlextPluginEventHandler (event processing)
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest
from flext_core import FlextResult

from flext_plugin.application.handlers import (
    FlextPluginEventHandler,
    FlextPluginHandler,
    FlextPluginRegistrationHandler,
)
from flext_plugin.application.services import FlextPluginService
from flext_plugin.domain.entities import FlextPlugin


class TestFlextPluginHandler:
    """Coverage-focused tests for FlextPluginHandler base class.

    Tests the actual base handler implementation with service injection.
    """

    def test_handler_initialization_with_service(self) -> None:
        """Test handler initialization with plugin service."""
        mock_service = Mock(spec=FlextPluginService)
        handler = FlextPluginHandler(plugin_service=mock_service)

        assert handler is not None
        assert handler._plugin_service is mock_service

    def test_handler_initialization_without_service(self) -> None:
        """Test handler initialization without plugin service."""
        handler = FlextPluginHandler(plugin_service=None)

        assert handler is not None
        assert handler._plugin_service is None

    def test_handler_initialization_default_parameter(self) -> None:
        """Test handler initialization with default parameter."""
        handler = FlextPluginHandler()

        assert handler is not None
        assert handler._plugin_service is None

    def test_handler_service_access(self) -> None:
        """Test handler service access patterns."""
        mock_service = Mock(spec=FlextPluginService)
        handler = FlextPluginHandler(plugin_service=mock_service)

        # Verify service is accessible via private attribute
        service = handler._plugin_service
        assert service is mock_service

    def test_handler_service_none_handling(self) -> None:
        """Test handler handles None service gracefully."""
        handler = FlextPluginHandler(plugin_service=None)

        # Should not raise exception when accessing None service
        service = handler._plugin_service
        assert service is None


class TestFlextPluginRegistrationHandler:
    """Coverage-focused tests for FlextPluginRegistrationHandler.

    Tests the actual registration handler implementation with real scenarios.
    """

    @pytest.fixture
    def mock_plugin_service(self) -> Mock:
        """Create mock plugin service."""
        service = Mock(spec=FlextPluginService)
        service.load_plugin = Mock()
        service.unload_plugin = Mock()
        return service

    @pytest.fixture
    def handler(self, mock_plugin_service: Mock) -> FlextPluginRegistrationHandler:
        """Create registration handler for testing."""
        return FlextPluginRegistrationHandler(plugin_service=mock_plugin_service)

    @pytest.fixture
    def mock_plugin(self) -> FlextPlugin:
        """Create mock plugin for testing."""
        return FlextPlugin(
            name="test-plugin",
            version="1.0.0",
            config={
                "description": "Test plugin",
                "author": "Test Author",
            },
        )

    def test_handler_initialization(self, mock_plugin_service: Mock) -> None:
        """Test registration handler initialization."""
        handler = FlextPluginRegistrationHandler(plugin_service=mock_plugin_service)

        assert handler is not None
        assert handler._plugin_service is mock_plugin_service

    def test_handler_initialization_without_service(self) -> None:
        """Test registration handler initialization without service."""
        handler = FlextPluginRegistrationHandler(plugin_service=None)

        assert handler is not None
        assert handler._plugin_service is None

    def test_handle_register_plugin_success(
        self,
        handler: FlextPluginRegistrationHandler,
        mock_plugin_service: Mock,
        mock_plugin: FlextPlugin,
    ) -> None:
        """Test successful plugin registration."""
        mock_plugin_service.load_plugin.return_value = FlextResult.ok(True)

        result = handler.handle_register_plugin(mock_plugin)

        assert result.success
        assert result.data is True
        mock_plugin_service.load_plugin.assert_called_once_with(mock_plugin)

    def test_handle_register_plugin_empty_name_fails(
        self, handler: FlextPluginRegistrationHandler, mock_plugin_service: Mock
    ) -> None:
        """Test plugin registration with empty name fails."""
        # Create mock plugin with empty name (bypass Pydantic validation)
        plugin_with_empty_name = Mock()
        plugin_with_empty_name.name = ""
        plugin_with_empty_name.version = "1.0.0"

        result = handler.handle_register_plugin(plugin_with_empty_name)

        assert not result.success
        assert "Plugin name is required" in result.error
        mock_plugin_service.load_plugin.assert_not_called()

    def test_handle_register_plugin_none_name_fails(
        self, handler: FlextPluginRegistrationHandler, mock_plugin_service: Mock
    ) -> None:
        """Test plugin registration with None name fails."""
        # Create mock plugin with None name
        plugin_with_none_name = Mock()
        plugin_with_none_name.name = None
        plugin_with_none_name.version = "1.0.0"

        result = handler.handle_register_plugin(plugin_with_none_name)

        assert not result.success
        assert "Plugin name is required" in result.error
        mock_plugin_service.load_plugin.assert_not_called()

    def test_handle_register_plugin_empty_version_fails(
        self, handler: FlextPluginRegistrationHandler, mock_plugin_service: Mock
    ) -> None:
        """Test plugin registration with empty version fails."""
        # Create mock plugin with empty version
        plugin_with_empty_version = Mock()
        plugin_with_empty_version.name = "test-plugin"
        plugin_with_empty_version.version = ""

        result = handler.handle_register_plugin(plugin_with_empty_version)

        assert not result.success
        assert "Plugin version is required" in result.error
        mock_plugin_service.load_plugin.assert_not_called()

    def test_handle_register_plugin_none_version_fails(
        self, handler: FlextPluginRegistrationHandler, mock_plugin_service: Mock
    ) -> None:
        """Test plugin registration with None version fails."""
        # Create mock plugin with None version
        plugin_with_none_version = Mock()
        plugin_with_none_version.name = "test-plugin"
        plugin_with_none_version.version = None

        result = handler.handle_register_plugin(plugin_with_none_version)

        assert not result.success
        assert "Plugin version is required" in result.error
        mock_plugin_service.load_plugin.assert_not_called()

    def test_handle_register_plugin_no_service_fails(
        self, mock_plugin: FlextPlugin
    ) -> None:
        """Test plugin registration without service fails."""
        handler = FlextPluginRegistrationHandler(plugin_service=None)

        result = handler.handle_register_plugin(mock_plugin)

        assert not result.success
        assert "Plugin service not available" in result.error

    def test_handle_register_plugin_service_failure(
        self,
        handler: FlextPluginRegistrationHandler,
        mock_plugin_service: Mock,
        mock_plugin: FlextPlugin,
    ) -> None:
        """Test plugin registration with service failure."""
        mock_plugin_service.load_plugin.return_value = FlextResult.fail("Service error")

        result = handler.handle_register_plugin(mock_plugin)

        assert not result.success
        assert result.error == "Service error"

    def test_handle_register_plugin_runtime_exception(
        self,
        handler: FlextPluginRegistrationHandler,
        mock_plugin_service: Mock,
        mock_plugin: FlextPlugin,
    ) -> None:
        """Test plugin registration with RuntimeError exception."""
        mock_plugin_service.load_plugin.side_effect = RuntimeError("Runtime error")

        result = handler.handle_register_plugin(mock_plugin)

        assert not result.success
        assert "Failed to register plugin: Runtime error" in result.error

    def test_handle_register_plugin_value_exception(
        self,
        handler: FlextPluginRegistrationHandler,
        mock_plugin_service: Mock,
        mock_plugin: FlextPlugin,
    ) -> None:
        """Test plugin registration with ValueError exception."""
        mock_plugin_service.load_plugin.side_effect = ValueError("Value error")

        result = handler.handle_register_plugin(mock_plugin)

        assert not result.success
        assert "Failed to register plugin: Value error" in result.error

    def test_handle_register_plugin_type_exception(
        self,
        handler: FlextPluginRegistrationHandler,
        mock_plugin_service: Mock,
        mock_plugin: FlextPlugin,
    ) -> None:
        """Test plugin registration with TypeError exception."""
        mock_plugin_service.load_plugin.side_effect = TypeError("Type error")

        result = handler.handle_register_plugin(mock_plugin)

        assert not result.success
        assert "Failed to register plugin: Type error" in result.error

    def test_handle_unregister_plugin_success(
        self, handler: FlextPluginRegistrationHandler, mock_plugin_service: Mock
    ) -> None:
        """Test successful plugin unregistration."""
        plugin_name = "test-plugin"
        mock_plugin_service.unload_plugin.return_value = FlextResult.ok(True)

        result = handler.handle_unregister_plugin(plugin_name)

        assert result.success
        assert result.data is True
        mock_plugin_service.unload_plugin.assert_called_once_with(plugin_name)

    def test_handle_unregister_plugin_empty_name_fails(
        self, handler: FlextPluginRegistrationHandler, mock_plugin_service: Mock
    ) -> None:
        """Test plugin unregistration with empty name fails."""
        result = handler.handle_unregister_plugin("")

        assert not result.success
        assert "Plugin name is required" in result.error
        mock_plugin_service.unload_plugin.assert_not_called()

    def test_handle_unregister_plugin_none_name_fails(
        self, handler: FlextPluginRegistrationHandler, mock_plugin_service: Mock
    ) -> None:
        """Test plugin unregistration with None name fails."""
        result = handler.handle_unregister_plugin(None)  # type: ignore

        assert not result.success
        assert "Plugin name is required" in result.error
        mock_plugin_service.unload_plugin.assert_not_called()

    def test_handle_unregister_plugin_no_service_fails(self) -> None:
        """Test plugin unregistration without service fails."""
        handler = FlextPluginRegistrationHandler(plugin_service=None)

        result = handler.handle_unregister_plugin("test-plugin")

        assert not result.success
        assert "Plugin service not available" in result.error

    def test_handle_unregister_plugin_service_failure(
        self, handler: FlextPluginRegistrationHandler, mock_plugin_service: Mock
    ) -> None:
        """Test plugin unregistration with service failure."""
        plugin_name = "test-plugin"
        mock_plugin_service.unload_plugin.return_value = FlextResult.fail(
            "Unload error"
        )

        result = handler.handle_unregister_plugin(plugin_name)

        assert not result.success
        assert result.error == "Unload error"

    def test_handle_unregister_plugin_runtime_exception(
        self, handler: FlextPluginRegistrationHandler, mock_plugin_service: Mock
    ) -> None:
        """Test plugin unregistration with RuntimeError exception."""
        plugin_name = "test-plugin"
        mock_plugin_service.unload_plugin.side_effect = RuntimeError("Runtime error")

        result = handler.handle_unregister_plugin(plugin_name)

        assert not result.success
        assert "Failed to unregister plugin: Runtime error" in result.error

    def test_handle_unregister_plugin_value_exception(
        self, handler: FlextPluginRegistrationHandler, mock_plugin_service: Mock
    ) -> None:
        """Test plugin unregistration with ValueError exception."""
        plugin_name = "test-plugin"
        mock_plugin_service.unload_plugin.side_effect = ValueError("Value error")

        result = handler.handle_unregister_plugin(plugin_name)

        assert not result.success
        assert "Failed to unregister plugin: Value error" in result.error

    def test_handle_unregister_plugin_type_exception(
        self, handler: FlextPluginRegistrationHandler, mock_plugin_service: Mock
    ) -> None:
        """Test plugin unregistration with TypeError exception."""
        plugin_name = "test-plugin"
        mock_plugin_service.unload_plugin.side_effect = TypeError("Type error")

        result = handler.handle_unregister_plugin(plugin_name)

        assert not result.success
        assert "Failed to unregister plugin: Type error" in result.error


class TestFlextPluginEventHandler:
    """Coverage-focused tests for FlextPluginEventHandler.

    Tests the actual event handler implementation with real scenarios.
    """

    @pytest.fixture
    def handler(self) -> FlextPluginEventHandler:
        """Create event handler for testing."""
        return FlextPluginEventHandler()

    @pytest.fixture
    def mock_plugin(self) -> FlextPlugin:
        """Create mock plugin for testing."""
        return FlextPlugin(
            name="test-plugin",
            version="1.0.0",
            config={
                "description": "Test plugin",
                "author": "Test Author",
            },
        )

    def test_handler_initialization(self) -> None:
        """Test event handler initialization."""
        handler = FlextPluginEventHandler()

        assert handler is not None

    def test_handle_plugin_loaded_success(
        self, handler: FlextPluginEventHandler, mock_plugin: FlextPlugin
    ) -> None:
        """Test successful plugin loaded event handling."""
        result = handler.handle_plugin_loaded(mock_plugin)

        assert result.success
        assert result.data is True

    def test_handle_plugin_loaded_missing_name_fails(
        self, handler: FlextPluginEventHandler
    ) -> None:
        """Test plugin loaded event with missing name fails."""
        # Create mock plugin with empty name
        plugin_without_name = Mock()
        plugin_without_name.name = ""

        result = handler.handle_plugin_loaded(plugin_without_name)

        assert not result.success
        assert "Plugin loaded event: plugin missing name" in result.error

    def test_handle_plugin_loaded_none_name_fails(
        self, handler: FlextPluginEventHandler
    ) -> None:
        """Test plugin loaded event with None name fails."""
        # Create mock plugin with None name
        plugin_with_none_name = Mock()
        plugin_with_none_name.name = None

        result = handler.handle_plugin_loaded(plugin_with_none_name)

        assert not result.success
        assert "Plugin loaded event: plugin missing name" in result.error

    def test_handle_plugin_loaded_plugin_without_name_attribute(
        self, handler: FlextPluginEventHandler
    ) -> None:
        """Test plugin loaded event with plugin missing name attribute."""
        # Create object without name attribute
        plugin_without_name_attr = object()

        result = handler.handle_plugin_loaded(plugin_without_name_attr)  # type: ignore

        assert not result.success
        assert "Plugin loaded event: plugin missing name" in result.error

    def test_handle_plugin_loaded_runtime_exception(
        self, handler: FlextPluginEventHandler, mock_plugin: FlextPlugin
    ) -> None:
        """Test plugin loaded event with RuntimeError exception."""
        # Mock getattr to raise exception
        original_getattr = getattr

        def mock_getattr(obj, name, default=None):
            if name == "name":
                msg = "Attribute access error"
                raise RuntimeError(msg)
            return original_getattr(obj, name, default)

        import builtins

        builtins.getattr = mock_getattr  # type: ignore

        try:
            result = handler.handle_plugin_loaded(mock_plugin)

            assert not result.success
            assert (
                "Failed to handle plugin loaded event: Attribute access error"
                in result.error
            )
        finally:
            builtins.getattr = original_getattr  # type: ignore

    def test_handle_plugin_loaded_value_exception(
        self, handler: FlextPluginEventHandler, mock_plugin: FlextPlugin
    ) -> None:
        """Test plugin loaded event with ValueError exception."""
        # Mock getattr to raise exception
        original_getattr = getattr

        def mock_getattr(obj, name, default=None):
            if name == "name":
                msg = "Value error"
                raise ValueError(msg)
            return original_getattr(obj, name, default)

        import builtins

        builtins.getattr = mock_getattr  # type: ignore

        try:
            result = handler.handle_plugin_loaded(mock_plugin)

            assert not result.success
            assert "Failed to handle plugin loaded event: Value error" in result.error
        finally:
            builtins.getattr = original_getattr  # type: ignore

    def test_handle_plugin_loaded_type_exception(
        self, handler: FlextPluginEventHandler, mock_plugin: FlextPlugin
    ) -> None:
        """Test plugin loaded event with TypeError exception."""
        # Mock getattr to raise exception
        original_getattr = getattr

        def mock_getattr(obj, name, default=None):
            if name == "name":
                msg = "Type error"
                raise TypeError(msg)
            return original_getattr(obj, name, default)

        import builtins

        builtins.getattr = mock_getattr  # type: ignore

        try:
            result = handler.handle_plugin_loaded(mock_plugin)

            assert not result.success
            assert "Failed to handle plugin loaded event: Type error" in result.error
        finally:
            builtins.getattr = original_getattr  # type: ignore

    def test_handle_plugin_unloaded_success(
        self, handler: FlextPluginEventHandler
    ) -> None:
        """Test successful plugin unloaded event handling."""
        plugin_name = "test-plugin"

        result = handler.handle_plugin_unloaded(plugin_name)

        assert result.success
        assert result.data is True

    def test_handle_plugin_unloaded_empty_name_fails(
        self, handler: FlextPluginEventHandler
    ) -> None:
        """Test plugin unloaded event with empty name fails."""
        result = handler.handle_plugin_unloaded("")

        assert not result.success
        assert "Plugin unloaded event: plugin name is required" in result.error

    def test_handle_plugin_unloaded_whitespace_name_fails(
        self, handler: FlextPluginEventHandler
    ) -> None:
        """Test plugin unloaded event with whitespace-only name fails."""
        result = handler.handle_plugin_unloaded("   ")

        assert not result.success
        assert "Plugin unloaded event: plugin name is required" in result.error

    def test_handle_plugin_unloaded_none_name_fails(
        self, handler: FlextPluginEventHandler
    ) -> None:
        """Test plugin unloaded event with None name fails."""
        result = handler.handle_plugin_unloaded(None)  # type: ignore

        assert not result.success
        assert "Plugin unloaded event: plugin name is required" in result.error

    def test_handle_plugin_unloaded_runtime_exception(
        self, handler: FlextPluginEventHandler
    ) -> None:
        """Test plugin unloaded event with RuntimeError exception."""
        # Create a mock string that raises exception on strip()
        mock_plugin_name = Mock()
        mock_plugin_name.strip.side_effect = RuntimeError("Strip error")

        result = handler.handle_plugin_unloaded(mock_plugin_name)

        assert not result.success
        assert "Failed to handle plugin unloaded event: Strip error" in result.error

    def test_handle_plugin_unloaded_value_exception(
        self, handler: FlextPluginEventHandler
    ) -> None:
        """Test plugin unloaded event with ValueError exception."""
        # Create a mock string that raises exception on strip()
        mock_plugin_name = Mock()
        mock_plugin_name.strip.side_effect = ValueError("Value error")

        result = handler.handle_plugin_unloaded(mock_plugin_name)

        assert not result.success
        assert "Failed to handle plugin unloaded event: Value error" in result.error

    def test_handle_plugin_unloaded_type_exception(
        self, handler: FlextPluginEventHandler
    ) -> None:
        """Test plugin unloaded event with TypeError exception."""
        # Create a mock string that raises exception on strip()
        mock_plugin_name = Mock()
        mock_plugin_name.strip.side_effect = TypeError("Type error")

        result = handler.handle_plugin_unloaded(mock_plugin_name)

        assert not result.success
        assert "Failed to handle plugin unloaded event: Type error" in result.error


class TestHandlerIntegration:
    """Integration tests for handler interactions."""

    def test_registration_and_event_handler_integration(self) -> None:
        """Test integration between registration and event handlers."""
        mock_service = Mock(spec=FlextPluginService)
        mock_service.load_plugin.return_value = FlextResult.ok(True)

        registration_handler = FlextPluginRegistrationHandler(
            plugin_service=mock_service
        )
        event_handler = FlextPluginEventHandler()

        # Create plugin
        plugin = FlextPlugin(
            name="integration-test-plugin",
            version="1.0.0",
            config={
                "description": "Integration test plugin",
                "author": "Test Author",
            },
        )

        # Register plugin
        register_result = registration_handler.handle_register_plugin(plugin)
        assert register_result.success

        # Handle plugin loaded event
        loaded_result = event_handler.handle_plugin_loaded(plugin)
        assert loaded_result.success

        # Unregister plugin
        unregister_result = registration_handler.handle_unregister_plugin(
            "integration-test-plugin"
        )
        assert unregister_result.success

        # Handle plugin unloaded event
        unloaded_result = event_handler.handle_plugin_unloaded(
            "integration-test-plugin"
        )
        assert unloaded_result.success

    def test_handler_error_consistency(self) -> None:
        """Test error handling consistency across handlers."""
        registration_handler = FlextPluginRegistrationHandler(plugin_service=None)
        event_handler = FlextPluginEventHandler()

        # Both handlers should handle None/empty values consistently
        reg_result = registration_handler.handle_unregister_plugin("")
        event_result = event_handler.handle_plugin_unloaded("")

        assert not reg_result.success
        assert not event_result.success
        assert "required" in reg_result.error.lower()
        assert "required" in event_result.error.lower()

    def test_all_handlers_instantiation(self) -> None:
        """Test all handler classes can be instantiated."""
        mock_service = Mock(spec=FlextPluginService)

        # Test all handler instantiation
        base_handler = FlextPluginHandler(plugin_service=mock_service)
        registration_handler = FlextPluginRegistrationHandler(
            plugin_service=mock_service
        )
        event_handler = FlextPluginEventHandler()

        assert base_handler is not None
        assert registration_handler is not None
        assert event_handler is not None

        # Verify inheritance
        assert isinstance(registration_handler, FlextPluginHandler)
        # Note: FlextPluginEventHandler doesn't inherit from FlextPluginHandler in current implementation
