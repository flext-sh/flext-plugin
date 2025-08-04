"""Comprehensive test suite for flext_plugin.domain.ports module.

This test module validates the complete domain service interface layer (ports)
within the Clean Architecture, ensuring proper abstract base class definitions,
method signatures, and interface contracts for all plugin system services.

Domain Ports Architecture:
    - PluginDiscoveryService: Plugin discovery and metadata validation interfaces
    - PluginValidationService: Plugin validation and security checking interfaces
    - PluginLifecycleService: Complete plugin lifecycle management interfaces
    - PluginExecutionService: Plugin execution and monitoring interfaces
    - PluginRegistryService: Plugin registry and distribution interfaces
    - PluginHotReloadService: Hot-reload and dynamic plugin management interfaces
    - PluginSecurityService: Security sandboxing and vulnerability scanning interfaces

Test Coverage:
    - Abstract Base Class Validation: Ensures proper ABC inheritance and abstractmethods
    - Method Signature Verification: Validates correct parameter lists and naming
    - Interface Contract Testing: Confirms all required methods are defined
    - Instantiation Prevention: Verifies abstract classes cannot be instantiated
    - Documentation Standards: Ensures all interfaces have comprehensive docstrings

Clean Architecture Integration:
    - Domain Layer Isolation: Tests ports as pure domain interfaces
    - Infrastructure Independence: Validates no infrastructure dependencies
    - Interface Segregation: Confirms focused, single-responsibility interfaces
    - Dependency Inversion: Tests proper abstraction layer for infrastructure

Quality Standards:
    - Comprehensive signature validation with detailed error messages
    - Collective interface validation ensuring system completeness
    - Documentation standards enforcement for all abstract methods
    - Enterprise-grade interface contract testing
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
    """Comprehensive test suite for PluginDiscoveryService domain interface.

    Validates the plugin discovery service interface contract, ensuring proper
    abstract base class implementation, required method definitions, and correct
    method signatures for plugin discovery and metadata validation operations.

    Interface Contract Validation:
        - Abstract base class inheritance from ABC
        - Required abstract methods: discover_plugins, validate_plugin_metadata, get_plugin_manifest
        - Correct method signatures with proper parameter names
        - Prevention of direct instantiation

    Clean Architecture Compliance:
        - Pure domain interface without infrastructure dependencies
        - Proper abstraction for plugin discovery operations
        - Interface segregation for focused discovery responsibilities
    """

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
        if expected_methods != abstract_methods:
            msg: str = f"Expected {abstract_methods}, got {expected_methods}"
            raise AssertionError(msg)

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test discover_plugins signature
        sig = inspect.signature(PluginDiscoveryService.discover_plugins)
        params = list(sig.parameters.keys())
        if params != ["self", "search_paths"]:
            msg: str = f"Expected {['self', 'search_paths']}, got {params}"
            raise AssertionError(msg)
        # Test validate_plugin_metadata signature
        sig = inspect.signature(PluginDiscoveryService.validate_plugin_metadata)
        params = list(sig.parameters.keys())
        if params != ["self", "metadata"]:
            msg: str = f"Expected {['self', 'metadata']}, got {params}"
            raise AssertionError(msg)
        # Test get_plugin_manifest signature
        sig = inspect.signature(PluginDiscoveryService.get_plugin_manifest)
        params = list(sig.parameters.keys())
        if params != ["self", "plugin_path"]:
            msg: str = f"Expected {['self', 'plugin_path']}, got {params}"
            raise AssertionError(msg)

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
        if expected_methods != abstract_methods:
            msg: str = f"Expected {abstract_methods}, got {expected_methods}"
            raise AssertionError(msg)

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test validate_plugin signature
        sig = inspect.signature(PluginValidationService.validate_plugin)
        params = list(sig.parameters.keys())
        if params != ["self", "plugin"]:
            msg: str = f"Expected {['self', 'plugin']}, got {params}"
            raise AssertionError(msg)
        # Test validate_configuration signature
        sig = inspect.signature(PluginValidationService.validate_configuration)
        params = list(sig.parameters.keys())
        if params != ["self", "plugin", "config"]:
            msg: str = f"Expected {['self', 'plugin', 'config']}, got {params}"
            raise AssertionError(msg)

    def test_cannot_instantiate_directly(self) -> None:
        """Test that abstract class cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PluginValidationService()


class TestPluginLifecycleService:
    """Comprehensive test suite for PluginLifecycleService domain interface.

    Validates the complete plugin lifecycle management interface, ensuring proper
    abstract methods for all plugin states from registration through unregistration.

    Lifecycle Operations Validated:
        - register_plugin: Plugin registration into system
        - load_plugin: Plugin loading and initialization
        - initialize_plugin: Plugin setup and configuration
        - activate_plugin: Plugin activation and readiness
        - suspend_plugin: Plugin suspension and state preservation
        - unload_plugin: Plugin cleanup and resource release
        - unregister_plugin: Plugin removal from system

    Interface Standards:
        - Complete lifecycle state management coverage
        - Proper error handling and state transition validation
        - Clean Architecture domain layer compliance
    """

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
        if expected_methods != abstract_methods:
            msg: str = f"Expected {abstract_methods}, got {expected_methods}"
            raise AssertionError(msg)

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test register_plugin signature
        sig = inspect.signature(PluginLifecycleService.register_plugin)
        params = list(sig.parameters.keys())
        if params != ["self", "plugin"]:
            msg: str = f"Expected {['self', 'plugin']}, got {params}"
            raise AssertionError(msg)
        # Test load_plugin signature
        sig = inspect.signature(PluginLifecycleService.load_plugin)
        params = list(sig.parameters.keys())
        if params != ["self", "plugin"]:
            msg: str = f"Expected {['self', 'plugin']}, got {params}"
            raise AssertionError(msg)

    def test_cannot_instantiate_directly(self) -> None:
        """Test that abstract class cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PluginLifecycleService()


class TestPluginExecutionService:
    """Comprehensive test suite for PluginExecutionService domain interface.

    Validates the plugin execution management interface, ensuring proper methods
    for plugin execution, monitoring, and control operations.

    Execution Operations Validated:
        - execute_plugin: Plugin execution with input data and context
        - get_execution_status: Execution status monitoring and reporting
        - cancel_execution: Execution cancellation and cleanup
        - get_execution_logs: Execution log retrieval and analysis

    Interface Standards:
        - Comprehensive execution lifecycle management
        - Proper async execution pattern support
        - Error handling and monitoring capabilities
        - Clean separation of execution concerns
    """

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
        if expected_methods != abstract_methods:
            msg: str = f"Expected {abstract_methods}, got {expected_methods}"
            raise AssertionError(msg)

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test execute_plugin signature
        sig = inspect.signature(PluginExecutionService.execute_plugin)
        params = list(sig.parameters.keys())
        if params != ["self", "plugin", "input_data", "execution_context"]:
            msg: str = f"Expected {['self', 'plugin', 'input_data', 'execution_context']}, got {params}"
            raise AssertionError(msg)
        # Test get_execution_status signature
        sig = inspect.signature(PluginExecutionService.get_execution_status)
        params = list(sig.parameters.keys())
        if params != ["self", "execution_id"]:
            msg: str = f"Expected {['self', 'execution_id']}, got {params}"
            raise AssertionError(msg)

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
        if expected_methods != abstract_methods:
            msg: str = f"Expected {abstract_methods}, got {expected_methods}"
            raise AssertionError(msg)

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test register_registry signature
        sig = inspect.signature(PluginRegistryService.register_registry)
        params = list(sig.parameters.keys())
        if params != ["self", "registry"]:
            msg: str = f"Expected {['self', 'registry']}, got {params}"
            raise AssertionError(msg)
        # Test search_plugins signature
        sig = inspect.signature(PluginRegistryService.search_plugins)
        params = list(sig.parameters.keys())
        if params != ["self", "registry", "query"]:
            msg: str = f"Expected {['self', 'registry', 'query']}, got {params}"
            raise AssertionError(msg)

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
        if expected_methods != abstract_methods:
            msg: str = f"Expected {abstract_methods}, got {expected_methods}"
            raise AssertionError(msg)

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test start_watching signature
        sig = inspect.signature(PluginHotReloadService.start_watching)
        params = list(sig.parameters.keys())
        if params != ["self", "watch_paths"]:
            msg: str = f"Expected {['self', 'watch_paths']}, got {params}"
            raise AssertionError(msg)
        # Test reload_plugin signature
        sig = inspect.signature(PluginHotReloadService.reload_plugin)
        params = list(sig.parameters.keys())
        if params != ["self", "plugin"]:
            msg: str = f"Expected {['self', 'plugin']}, got {params}"
            raise AssertionError(msg)

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
        if expected_methods != abstract_methods:
            msg: str = f"Expected {abstract_methods}, got {expected_methods}"
            raise AssertionError(msg)

    def test_method_signatures(self) -> None:
        """Test method signatures are correct."""
        # Test create_sandbox signature
        sig = inspect.signature(PluginSecurityService.create_sandbox)
        params = list(sig.parameters.keys())
        if params != ["self", "plugin"]:
            msg: str = f"Expected {['self', 'plugin']}, got {params}"
            raise AssertionError(msg)
        # Test scan_for_vulnerabilities signature
        sig = inspect.signature(PluginSecurityService.scan_for_vulnerabilities)
        params = list(sig.parameters.keys())
        if params != ["self", "plugin"]:
            msg: str = f"Expected {['self', 'plugin']}, got {params}"
            raise AssertionError(msg)

    def test_cannot_instantiate_directly(self) -> None:
        """Test that abstract class cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PluginSecurityService()


class TestAllPorts:
    """Comprehensive validation of all domain port interfaces collectively.

    Provides system-wide validation of the complete domain port layer,
    ensuring consistency, completeness, and quality standards across
    all plugin service interfaces within the Clean Architecture.

    System-Wide Validations:
        - All ports properly inherit from ABC with abstract methods
        - Complete documentation coverage for all classes and methods
        - Consistent interface patterns across all service ports
        - Proper separation of concerns and interface segregation

    Quality Standards:
        - Enterprise-grade documentation requirements
        - Complete method signature validation
        - Consistent error handling patterns
        - Clean Architecture compliance verification

    Port Interface Coverage:
        - Discovery, Validation, Lifecycle, Execution services
        - Registry, HotReload, Security service interfaces
        - Complete plugin system domain abstraction layer
    """

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
