"""Tests for flext_plugin.domain.ports module.

Tests for domain service interfaces (ports) to ensure proper abstract class definitions.
"""

from __future__ import annotations

import inspect
from abc import ABC

import pytest

from flext_plugin.domain.ports import (
    PluginDiscoveryService,
    PluginExecutionService,
    PluginHotReloadService,
    PluginLifecycleService,
    PluginRegistryService,
    PluginSecurityService,
    PluginValidationService,
)


class TestPluginDiscoveryService:
    """Test PluginDiscoveryService interface."""

    def test_is_abstract_base_class(self) -> None:
        """Test that PluginDiscoveryService is an abstract base class."""
        assert issubclass(PluginDiscoveryService, ABC)
        assert PluginDiscoveryService.__abstractmethods__

    def test_has_required_abstract_methods(self) -> None:
        """Test that all required abstract methods are defined."""
        expected_methods = {
            "discover_plugins",
            "validate_plugin_metadata",
            "get_plugin_manifest",
        }
        abstract_methods = PluginDiscoveryService.__abstractmethods__
        assert expected_methods == abstract_methods

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test discover_plugins signature
        sig = inspect.signature(PluginDiscoveryService.discover_plugins)
        params = list(sig.parameters.keys())
        assert params == ["self", "search_paths"]
        # Test validate_plugin_metadata signature
        sig = inspect.signature(PluginDiscoveryService.validate_plugin_metadata)
        params = list(sig.parameters.keys())
        assert params == ["self", "metadata"]
        # Test get_plugin_manifest signature
        sig = inspect.signature(PluginDiscoveryService.get_plugin_manifest)
        params = list(sig.parameters.keys())
        assert params == ["self", "plugin_path"]

    def test_cannot_instantiate_directly(self) -> None:
        """Test that abstract class cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PluginDiscoveryService()


class TestPluginValidationService:
    """Test PluginValidationService interface."""

    def test_is_abstract_base_class(self) -> None:
        """Test that PluginValidationService is an abstract base class."""
        assert issubclass(PluginValidationService, ABC)
        assert PluginValidationService.__abstractmethods__

    def test_has_required_abstract_methods(self) -> None:
        """Test that all required abstract methods are defined."""
        expected_methods = {
            "validate_plugin",
            "validate_configuration",
            "validate_dependencies",
            "validate_permissions",
        }
        abstract_methods = PluginValidationService.__abstractmethods__
        assert expected_methods == abstract_methods

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test validate_plugin signature
        sig = inspect.signature(PluginValidationService.validate_plugin)
        params = list(sig.parameters.keys())
        assert params == ["self", "plugin"]
        # Test validate_configuration signature
        sig = inspect.signature(PluginValidationService.validate_configuration)
        params = list(sig.parameters.keys())
        assert params == ["self", "plugin", "config"]

    def test_cannot_instantiate_directly(self) -> None:
        """Test that abstract class cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PluginValidationService()


class TestPluginLifecycleService:
    """Test PluginLifecycleService interface."""

    def test_is_abstract_base_class(self) -> None:
        """Test that PluginLifecycleService is an abstract base class."""
        assert issubclass(PluginLifecycleService, ABC)
        assert PluginLifecycleService.__abstractmethods__

    def test_has_required_abstract_methods(self) -> None:
        """Test that all required abstract methods are defined."""
        expected_methods = {
            "register_plugin",
            "load_plugin",
            "initialize_plugin",
            "activate_plugin",
            "suspend_plugin",
            "unload_plugin",
            "unregister_plugin",
        }
        abstract_methods = PluginLifecycleService.__abstractmethods__
        assert expected_methods == abstract_methods

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test register_plugin signature
        sig = inspect.signature(PluginLifecycleService.register_plugin)
        params = list(sig.parameters.keys())
        assert params == ["self", "plugin"]
        # Test load_plugin signature
        sig = inspect.signature(PluginLifecycleService.load_plugin)
        params = list(sig.parameters.keys())
        assert params == ["self", "plugin"]

    def test_cannot_instantiate_directly(self) -> None:
        """Test that abstract class cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PluginLifecycleService()


class TestPluginExecutionService:
    """Test PluginExecutionService interface."""

    def test_is_abstract_base_class(self) -> None:
        """Test that PluginExecutionService is an abstract base class."""
        assert issubclass(PluginExecutionService, ABC)
        assert PluginExecutionService.__abstractmethods__

    def test_has_required_abstract_methods(self) -> None:
        """Test that all required abstract methods are defined."""
        expected_methods = {
            "execute_plugin",
            "get_execution_status",
            "cancel_execution",
            "get_execution_logs",
        }
        abstract_methods = PluginExecutionService.__abstractmethods__
        assert expected_methods == abstract_methods

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test execute_plugin signature
        sig = inspect.signature(PluginExecutionService.execute_plugin)
        params = list(sig.parameters.keys())
        assert params == ["self", "plugin", "input_data", "execution_context"]
        # Test get_execution_status signature
        sig = inspect.signature(PluginExecutionService.get_execution_status)
        params = list(sig.parameters.keys())
        assert params == ["self", "execution_id"]

    def test_cannot_instantiate_directly(self) -> None:
        """Test that abstract class cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PluginExecutionService()


class TestPluginRegistryService:
    """Test PluginRegistryService interface."""

    def test_is_abstract_base_class(self) -> None:
        """Test that PluginRegistryService is an abstract base class."""
        assert issubclass(PluginRegistryService, ABC)
        assert PluginRegistryService.__abstractmethods__

    def test_has_required_abstract_methods(self) -> None:
        """Test that all required abstract methods are defined."""
        expected_methods = {
            "register_registry",
            "sync_registry",
            "search_plugins",
            "download_plugin",
            "verify_plugin_signature",
        }
        abstract_methods = PluginRegistryService.__abstractmethods__
        assert expected_methods == abstract_methods

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test register_registry signature
        sig = inspect.signature(PluginRegistryService.register_registry)
        params = list(sig.parameters.keys())
        assert params == ["self", "registry"]
        # Test search_plugins signature
        sig = inspect.signature(PluginRegistryService.search_plugins)
        params = list(sig.parameters.keys())
        assert params == ["self", "registry", "query"]

    def test_cannot_instantiate_directly(self) -> None:
        """Test that abstract class cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PluginRegistryService()


class TestPluginHotReloadService:
    """Test PluginHotReloadService interface."""

    def test_is_abstract_base_class(self) -> None:
        """Test that PluginHotReloadService is an abstract base class."""
        assert issubclass(PluginHotReloadService, ABC)
        assert PluginHotReloadService.__abstractmethods__

    def test_has_required_abstract_methods(self) -> None:
        """Test that all required abstract methods are defined."""
        expected_methods = {
            "start_watching",
            "stop_watching",
            "reload_plugin",
            "backup_plugin_state",
            "restore_plugin_state",
        }
        abstract_methods = PluginHotReloadService.__abstractmethods__
        assert expected_methods == abstract_methods

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test start_watching signature
        sig = inspect.signature(PluginHotReloadService.start_watching)
        params = list(sig.parameters.keys())
        assert params == ["self", "watch_paths"]
        # Test reload_plugin signature
        sig = inspect.signature(PluginHotReloadService.reload_plugin)
        params = list(sig.parameters.keys())
        assert params == ["self", "plugin"]

    def test_cannot_instantiate_directly(self) -> None:
        """Test that abstract class cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PluginHotReloadService()


class TestPluginSecurityService:
    """Test PluginSecurityService interface."""

    def test_is_abstract_base_class(self) -> None:
        """Test that PluginSecurityService is an abstract base class."""
        assert issubclass(PluginSecurityService, ABC)
        assert PluginSecurityService.__abstractmethods__

    def test_has_required_abstract_methods(self) -> None:
        """Test that all required abstract methods are defined."""
        expected_methods = {
            "create_sandbox",
            "enforce_resource_limits",
            "validate_imports",
            "scan_for_vulnerabilities",
        }
        abstract_methods = PluginSecurityService.__abstractmethods__
        assert expected_methods == abstract_methods

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test create_sandbox signature
        sig = inspect.signature(PluginSecurityService.create_sandbox)
        params = list(sig.parameters.keys())
        assert params == ["self", "plugin"]
        # Test scan_for_vulnerabilities signature
        sig = inspect.signature(PluginSecurityService.scan_for_vulnerabilities)
        params = list(sig.parameters.keys())
        assert params == ["self", "plugin"]

    def test_cannot_instantiate_directly(self) -> None:
        """Test that abstract class cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PluginSecurityService()


class TestAllPorts:
    """Test all port interfaces collectively."""

    def test_all_ports_are_abstract(self) -> None:
        """Test that all port classes are abstract."""
        port_classes = [
            PluginDiscoveryService,
            PluginValidationService,
            PluginLifecycleService,
            PluginExecutionService,
            PluginRegistryService,
            PluginHotReloadService,
            PluginSecurityService,
        ]
        for port_class in port_classes:
            assert issubclass(port_class, ABC)
            assert port_class.__abstractmethods__

    def test_all_ports_have_docstrings(self) -> None:
        """Test that all port classes have docstrings."""
        port_classes = [
            PluginDiscoveryService,
            PluginValidationService,
            PluginLifecycleService,
            PluginExecutionService,
            PluginRegistryService,
            PluginHotReloadService,
            PluginSecurityService,
        ]
        for port_class in port_classes:
            assert port_class.__doc__ is not None
            assert port_class.__doc__.strip()

    def test_all_abstract_methods_have_docstrings(self) -> None:
        """Test that all abstract methods have docstrings."""
        port_classes = [
            PluginDiscoveryService,
            PluginValidationService,
            PluginLifecycleService,
            PluginExecutionService,
            PluginRegistryService,
            PluginHotReloadService,
            PluginSecurityService,
        ]
        for port_class in port_classes:
            for method_name in port_class.__abstractmethods__:
                method = getattr(port_class, method_name)
                assert method.__doc__ is not None
                assert method.__doc__.strip()
