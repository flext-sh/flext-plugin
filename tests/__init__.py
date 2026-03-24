# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests import unit
    from tests.conftest import (
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
    from tests.constants import FlextPluginTestConstants, FlextPluginTestConstants as c
    from tests.models import FlextPluginTestModels, FlextPluginTestModels as m
    from tests.protocols import FlextPluginTestProtocols, FlextPluginTestProtocols as p
    from tests.test_application_services import (
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
    from tests.test_core_types import (
        TestFlextPluginConstantsLifecycle,
        TestFlextPluginConstantsPluginType,
        TestPluginError,
    )
    from tests.test_domain_entities import (
        TestFlextPlugin,
        TestFlextPluginExecution,
        TestFlextPluginMetadata,
        TestFlextPluginRegistryEntity,
    )
    from tests.test_domain_ports import TestFlextPluginDiscovery
    from tests.test_examples import (
        test_basic_plugin_example_execution,
        test_docker_integration_example_execution,
        test_docker_integration_example_with_connection_testing,
        test_plugin_configuration_example_execution,
    )
    from tests.test_handlers import TestFlextPluginHandlers
    from tests.test_hot_reload import TestFlextPluginHotReload
    from tests.test_hot_reload_package import TestHotReloadPackage
    from tests.test_imports import modules_to_test
    from tests.test_loader import TestDynamicLoaderAdapter, TestFlextPluginLoader
    from tests.test_manager import (
        TestFlextPluginService,
        TestFlextPluginServiceStubBridges,
    )
    from tests.test_plugin import (
        TestPluginModel,
        TestPluginPlatform,
        TestPluginRegistry,
    )
    from tests.typings import FlextPluginTestTypes, FlextPluginTestTypes as t
    from tests.unit.test_config import TestFlextPluginSettings
    from tests.unit.test_constants import TestFlextPluginConstants
    from tests.unit.test_models import TestFlextPluginModels
    from tests.unit.test_types import TestFlextPluginTypes
    from tests.utilities import FlextPluginTestUtilities, FlextPluginTestUtilities as u

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
    "FlextPluginTestConstants": ("tests.constants", "FlextPluginTestConstants"),
    "FlextPluginTestModels": ("tests.models", "FlextPluginTestModels"),
    "FlextPluginTestProtocols": ("tests.protocols", "FlextPluginTestProtocols"),
    "FlextPluginTestTypes": ("tests.typings", "FlextPluginTestTypes"),
    "FlextPluginTestUtilities": ("tests.utilities", "FlextPluginTestUtilities"),
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
    "c": ("tests.constants", "FlextPluginTestConstants"),
    "d": ("flext_tests", "d"),
    "e": ("flext_tests", "e"),
    "h": ("flext_tests", "h"),
    "m": ("tests.models", "FlextPluginTestModels"),
    "modules_to_test": ("tests.test_imports", "modules_to_test"),
    "p": ("tests.protocols", "FlextPluginTestProtocols"),
    "performance_config": ("tests.conftest", "performance_config"),
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "r": ("flext_tests", "r"),
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
    "s": ("flext_tests", "s"),
    "set_test_environment": ("tests.conftest", "set_test_environment"),
    "simple_plugin_directory": ("tests.conftest", "simple_plugin_directory"),
    "t": ("tests.typings", "FlextPluginTestTypes"),
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
    "u": ("tests.utilities", "FlextPluginTestUtilities"),
    "unit": ("tests.unit", ""),
    "x": ("flext_tests", "x"),
}

__all__ = [
    "FlextPluginTestConstants",
    "FlextPluginTestModels",
    "FlextPluginTestProtocols",
    "FlextPluginTestTypes",
    "FlextPluginTestUtilities",
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
    "c",
    "d",
    "e",
    "h",
    "m",
    "modules_to_test",
    "p",
    "performance_config",
    "pytest_configure",
    "r",
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
    "s",
    "set_test_environment",
    "simple_plugin_directory",
    "t",
    "temp_plugin_dir",
    "test_basic_plugin_example_execution",
    "test_docker_integration_example_execution",
    "test_docker_integration_example_with_connection_testing",
    "test_plugin_configuration_example_execution",
    "u",
    "unit",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


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


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
