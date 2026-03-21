# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes


if TYPE_CHECKING:
    from . import unit as unit
    from .conftest import (
        performance_config,
        pytest_configure,
        real_container_with_adapters,
        real_discovery_adapter,
        real_loader_adapter,
        real_manager_adapter,
        real_plugin_config,
        real_plugin_configs,
        real_plugin_data,
        real_plugin_dependencies,
        real_plugin_directory,
        real_plugin_entity,
        real_processor_plugin,
        real_tap_plugin,
        real_target_plugin,
        set_test_environment,
        simple_plugin_directory,
    )
    from .constants import TestsFlextPluginConstants, TestsFlextPluginConstants as c
    from .models import TestsFlextPluginModels, TestsFlextPluginModels as m, tm
    from .protocols import TestsFlextPluginProtocols, TestsFlextPluginProtocols as p
    from .test_application_services import (
        PluginInterface,
        TestBackwardsCompatibilityAliasesReal,
        TestFlextPluginDiscoveryReal,
        TestFlextPluginServiceReal,
        TestFlextPluginServiceWithRealAdapters,
        TestRealPluginDiscoveryAndExecution,
        TestRealPluginErrorScenarios,
        TestRealPluginIntegrationWorkflow,
        TestServiceErrorHandling,
        TestServicesIntegrationReal,
        real_discovery_service_with_adapters,
        real_plugin_discovery,
        real_plugin_loader,
        real_service_with_adapters,
        temp_plugin_dir,
    )
    from .test_core_types import (
        TestFlextPluginConstantsLifecycle,
        TestFlextPluginConstantsPluginType,
        TestPluginError,
    )
    from .test_domain_entities import (
        TestFlextPlugin,
        TestFlextPluginExecution,
        TestFlextPluginMetadata,
        TestFlextPluginRegistryEntity,
    )
    from .test_domain_ports import TestFlextPluginDiscovery
    from .test_examples import (
        test_basic_plugin_example_execution,
        test_docker_integration_example_execution,
        test_docker_integration_example_with_connection_testing,
        test_plugin_configuration_example_execution,
    )
    from .test_handlers import TestFlextPluginHandlers
    from .test_hot_reload import TestFlextPluginHotReload
    from .test_hot_reload_package import TestHotReloadPackage
    from .test_imports import modules_to_test
    from .test_loader import TestDynamicLoaderAdapter, TestFlextPluginLoader
    from .test_manager import TestFlextPluginService, TestFlextPluginServiceStubBridges
    from .test_plugin import TestPluginModel, TestPluginPlatform, TestPluginRegistry
    from .typings import TestsFlextPluginTypes, TestsFlextPluginTypes as t
    from .unit.test_config import TestFlextPluginSettings
    from .unit.test_constants import TestFlextPluginConstants
    from .unit.test_models import TestFlextPluginModels
    from .unit.test_types import TestFlextPluginTypes
    from .utilities import TestsFlextPluginUtilities, TestsFlextPluginUtilities as u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "PluginInterface": ("tests.test_application_services", "PluginInterface"),
    "TestBackwardsCompatibilityAliasesReal": (
        "tests.test_application_services",
        "TestBackwardsCompatibilityAliasesReal",
    ),
    "TestDynamicLoaderAdapter": ("tests.test_loader", "TestDynamicLoaderAdapter"),
    "TestFlextPlugin": ("tests.test_domain_entities", "TestFlextPlugin"),
    "TestFlextPluginConstants": (
        "tests.unit.test_constants",
        "TestFlextPluginConstants",
    ),
    "TestFlextPluginConstantsLifecycle": (
        "tests.test_core_types",
        "TestFlextPluginConstantsLifecycle",
    ),
    "TestFlextPluginConstantsPluginType": (
        "tests.test_core_types",
        "TestFlextPluginConstantsPluginType",
    ),
    "TestFlextPluginDiscovery": ("tests.test_domain_ports", "TestFlextPluginDiscovery"),
    "TestFlextPluginDiscoveryReal": (
        "tests.test_application_services",
        "TestFlextPluginDiscoveryReal",
    ),
    "TestFlextPluginExecution": (
        "tests.test_domain_entities",
        "TestFlextPluginExecution",
    ),
    "TestFlextPluginHandlers": ("tests.test_handlers", "TestFlextPluginHandlers"),
    "TestFlextPluginHotReload": ("tests.test_hot_reload", "TestFlextPluginHotReload"),
    "TestFlextPluginLoader": ("tests.test_loader", "TestFlextPluginLoader"),
    "TestFlextPluginMetadata": (
        "tests.test_domain_entities",
        "TestFlextPluginMetadata",
    ),
    "TestFlextPluginModels": ("tests.unit.test_models", "TestFlextPluginModels"),
    "TestFlextPluginRegistryEntity": (
        "tests.test_domain_entities",
        "TestFlextPluginRegistryEntity",
    ),
    "TestFlextPluginService": ("tests.test_manager", "TestFlextPluginService"),
    "TestFlextPluginServiceReal": (
        "tests.test_application_services",
        "TestFlextPluginServiceReal",
    ),
    "TestFlextPluginServiceStubBridges": (
        "tests.test_manager",
        "TestFlextPluginServiceStubBridges",
    ),
    "TestFlextPluginServiceWithRealAdapters": (
        "tests.test_application_services",
        "TestFlextPluginServiceWithRealAdapters",
    ),
    "TestFlextPluginSettings": ("tests.unit.test_config", "TestFlextPluginSettings"),
    "TestFlextPluginTypes": ("tests.unit.test_types", "TestFlextPluginTypes"),
    "TestHotReloadPackage": ("tests.test_hot_reload_package", "TestHotReloadPackage"),
    "TestPluginError": ("tests.test_core_types", "TestPluginError"),
    "TestPluginModel": ("tests.test_plugin", "TestPluginModel"),
    "TestPluginPlatform": ("tests.test_plugin", "TestPluginPlatform"),
    "TestPluginRegistry": ("tests.test_plugin", "TestPluginRegistry"),
    "TestRealPluginDiscoveryAndExecution": (
        "tests.test_application_services",
        "TestRealPluginDiscoveryAndExecution",
    ),
    "TestRealPluginErrorScenarios": (
        "tests.test_application_services",
        "TestRealPluginErrorScenarios",
    ),
    "TestRealPluginIntegrationWorkflow": (
        "tests.test_application_services",
        "TestRealPluginIntegrationWorkflow",
    ),
    "TestServiceErrorHandling": (
        "tests.test_application_services",
        "TestServiceErrorHandling",
    ),
    "TestServicesIntegrationReal": (
        "tests.test_application_services",
        "TestServicesIntegrationReal",
    ),
    "TestsFlextPluginConstants": ("tests.constants", "TestsFlextPluginConstants"),
    "TestsFlextPluginModels": ("tests.models", "TestsFlextPluginModels"),
    "TestsFlextPluginProtocols": ("tests.protocols", "TestsFlextPluginProtocols"),
    "TestsFlextPluginTypes": ("tests.typings", "TestsFlextPluginTypes"),
    "TestsFlextPluginUtilities": ("tests.utilities", "TestsFlextPluginUtilities"),
    "c": ("tests.constants", "TestsFlextPluginConstants"),
    "m": ("tests.models", "TestsFlextPluginModels"),
    "modules_to_test": ("tests.test_imports", "modules_to_test"),
    "p": ("tests.protocols", "TestsFlextPluginProtocols"),
    "performance_config": ("tests.conftest", "performance_config"),
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "real_container_with_adapters": ("tests.conftest", "real_container_with_adapters"),
    "real_discovery_adapter": ("tests.conftest", "real_discovery_adapter"),
    "real_discovery_service_with_adapters": (
        "tests.test_application_services",
        "real_discovery_service_with_adapters",
    ),
    "real_loader_adapter": ("tests.conftest", "real_loader_adapter"),
    "real_manager_adapter": ("tests.conftest", "real_manager_adapter"),
    "real_plugin_config": ("tests.conftest", "real_plugin_config"),
    "real_plugin_configs": ("tests.conftest", "real_plugin_configs"),
    "real_plugin_data": ("tests.conftest", "real_plugin_data"),
    "real_plugin_dependencies": ("tests.conftest", "real_plugin_dependencies"),
    "real_plugin_directory": ("tests.conftest", "real_plugin_directory"),
    "real_plugin_discovery": (
        "tests.test_application_services",
        "real_plugin_discovery",
    ),
    "real_plugin_entity": ("tests.conftest", "real_plugin_entity"),
    "real_plugin_loader": ("tests.test_application_services", "real_plugin_loader"),
    "real_processor_plugin": ("tests.conftest", "real_processor_plugin"),
    "real_service_with_adapters": (
        "tests.test_application_services",
        "real_service_with_adapters",
    ),
    "real_tap_plugin": ("tests.conftest", "real_tap_plugin"),
    "real_target_plugin": ("tests.conftest", "real_target_plugin"),
    "set_test_environment": ("tests.conftest", "set_test_environment"),
    "simple_plugin_directory": ("tests.conftest", "simple_plugin_directory"),
    "t": ("tests.typings", "TestsFlextPluginTypes"),
    "temp_plugin_dir": ("tests.test_application_services", "temp_plugin_dir"),
    "test_basic_plugin_example_execution": (
        "tests.test_examples",
        "test_basic_plugin_example_execution",
    ),
    "test_docker_integration_example_execution": (
        "tests.test_examples",
        "test_docker_integration_example_execution",
    ),
    "test_docker_integration_example_with_connection_testing": (
        "tests.test_examples",
        "test_docker_integration_example_with_connection_testing",
    ),
    "test_plugin_configuration_example_execution": (
        "tests.test_examples",
        "test_plugin_configuration_example_execution",
    ),
    "tm": ("tests.models", "tm"),
    "u": ("tests.utilities", "TestsFlextPluginUtilities"),
    "unit": ("tests.unit", ""),
}

__all__ = [
    "PluginInterface",
    "TestBackwardsCompatibilityAliasesReal",
    "TestDynamicLoaderAdapter",
    "TestFlextPlugin",
    "TestFlextPluginConstants",
    "TestFlextPluginConstantsLifecycle",
    "TestFlextPluginConstantsPluginType",
    "TestFlextPluginDiscovery",
    "TestFlextPluginDiscoveryReal",
    "TestFlextPluginExecution",
    "TestFlextPluginHandlers",
    "TestFlextPluginHotReload",
    "TestFlextPluginLoader",
    "TestFlextPluginMetadata",
    "TestFlextPluginModels",
    "TestFlextPluginRegistryEntity",
    "TestFlextPluginService",
    "TestFlextPluginServiceReal",
    "TestFlextPluginServiceStubBridges",
    "TestFlextPluginServiceWithRealAdapters",
    "TestFlextPluginSettings",
    "TestFlextPluginTypes",
    "TestHotReloadPackage",
    "TestPluginError",
    "TestPluginModel",
    "TestPluginPlatform",
    "TestPluginRegistry",
    "TestRealPluginDiscoveryAndExecution",
    "TestRealPluginErrorScenarios",
    "TestRealPluginIntegrationWorkflow",
    "TestServiceErrorHandling",
    "TestServicesIntegrationReal",
    "TestsFlextPluginConstants",
    "TestsFlextPluginModels",
    "TestsFlextPluginProtocols",
    "TestsFlextPluginTypes",
    "TestsFlextPluginUtilities",
    "c",
    "m",
    "modules_to_test",
    "p",
    "performance_config",
    "pytest_configure",
    "real_container_with_adapters",
    "real_discovery_adapter",
    "real_discovery_service_with_adapters",
    "real_loader_adapter",
    "real_manager_adapter",
    "real_plugin_config",
    "real_plugin_configs",
    "real_plugin_data",
    "real_plugin_dependencies",
    "real_plugin_directory",
    "real_plugin_discovery",
    "real_plugin_entity",
    "real_plugin_loader",
    "real_processor_plugin",
    "real_service_with_adapters",
    "real_tap_plugin",
    "real_target_plugin",
    "set_test_environment",
    "simple_plugin_directory",
    "t",
    "temp_plugin_dir",
    "test_basic_plugin_example_execution",
    "test_docker_integration_example_execution",
    "test_docker_integration_example_with_connection_testing",
    "test_plugin_configuration_example_execution",
    "tm",
    "u",
    "unit",
]


_LAZY_CACHE: dict[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
