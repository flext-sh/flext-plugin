# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests import (
        conftest as conftest,
        constants as constants,
        models as models,
        protocols as protocols,
        test_application_handlers as test_application_handlers,
        test_application_services as test_application_services,
        test_core_types as test_core_types,
        test_discovery as test_discovery,
        test_domain_entities as test_domain_entities,
        test_domain_ports as test_domain_ports,
        test_examples as test_examples,
        test_handlers as test_handlers,
        test_hot_reload as test_hot_reload,
        test_hot_reload_package as test_hot_reload_package,
        test_imports as test_imports,
        test_loader as test_loader,
        test_manager as test_manager,
        test_plugin as test_plugin,
        typings as typings,
        unit as unit,
        utilities as utilities,
    )
    from tests.conftest import (
        performance_config as performance_config,
        pytest_configure as pytest_configure,
        real_container_with_adapters as real_container_with_adapters,
        real_discovery_adapter as real_discovery_adapter,
        real_loader_adapter as real_loader_adapter,
        real_manager_adapter as real_manager_adapter,
        real_plugin_config as real_plugin_config,
        real_plugin_configs as real_plugin_configs,
        real_plugin_data as real_plugin_data,
        real_plugin_dependencies as real_plugin_dependencies,
        real_plugin_directory as real_plugin_directory,
        real_plugin_entity as real_plugin_entity,
        real_processor_plugin as real_processor_plugin,
        real_tap_plugin as real_tap_plugin,
        real_target_plugin as real_target_plugin,
        set_test_environment as set_test_environment,
        simple_plugin_directory as simple_plugin_directory,
    )
    from tests.constants import (
        FlextPluginTestConstants as FlextPluginTestConstants,
        FlextPluginTestConstants as c,
    )
    from tests.models import (
        FlextPluginTestModels as FlextPluginTestModels,
        FlextPluginTestModels as m,
    )
    from tests.protocols import (
        FlextPluginTestProtocols as FlextPluginTestProtocols,
        FlextPluginTestProtocols as p,
    )
    from tests.test_application_services import (
        PluginInterface as PluginInterface,
        TestBackwardsCompatibilityAliasesReal as TestBackwardsCompatibilityAliasesReal,
        TestFlextPluginDiscoveryReal as TestFlextPluginDiscoveryReal,
        TestFlextPluginServiceReal as TestFlextPluginServiceReal,
        TestFlextPluginServiceWithRealAdapters as TestFlextPluginServiceWithRealAdapters,
        TestRealPluginDiscoveryAndExecution as TestRealPluginDiscoveryAndExecution,
        TestRealPluginErrorScenarios as TestRealPluginErrorScenarios,
        TestRealPluginIntegrationWorkflow as TestRealPluginIntegrationWorkflow,
        TestServiceErrorHandling as TestServiceErrorHandling,
        TestServicesIntegrationReal as TestServicesIntegrationReal,
        real_discovery_service_with_adapters as real_discovery_service_with_adapters,
        real_plugin_discovery as real_plugin_discovery,
        real_plugin_loader as real_plugin_loader,
        real_service_with_adapters as real_service_with_adapters,
        temp_plugin_dir as temp_plugin_dir,
    )
    from tests.test_core_types import (
        TestFlextPluginConstantsLifecycle as TestFlextPluginConstantsLifecycle,
        TestFlextPluginConstantsPluginType as TestFlextPluginConstantsPluginType,
        TestPluginError as TestPluginError,
    )
    from tests.test_domain_entities import (
        TestFlextPlugin as TestFlextPlugin,
        TestFlextPluginExecution as TestFlextPluginExecution,
        TestFlextPluginMetadata as TestFlextPluginMetadata,
        TestFlextPluginRegistryEntity as TestFlextPluginRegistryEntity,
    )
    from tests.test_domain_ports import (
        TestFlextPluginDiscovery as TestFlextPluginDiscovery,
    )
    from tests.test_examples import (
        test_basic_plugin_example_execution as test_basic_plugin_example_execution,
        test_docker_integration_example_execution as test_docker_integration_example_execution,
        test_docker_integration_example_with_connection_testing as test_docker_integration_example_with_connection_testing,
        test_plugin_configuration_example_execution as test_plugin_configuration_example_execution,
    )
    from tests.test_handlers import TestFlextPluginHandlers as TestFlextPluginHandlers
    from tests.test_hot_reload import (
        TestFlextPluginHotReload as TestFlextPluginHotReload,
    )
    from tests.test_hot_reload_package import (
        TestHotReloadPackage as TestHotReloadPackage,
    )
    from tests.test_imports import modules_to_test as modules_to_test
    from tests.test_loader import (
        TestDynamicLoaderAdapter as TestDynamicLoaderAdapter,
        TestFlextPluginLoader as TestFlextPluginLoader,
    )
    from tests.test_manager import (
        TestFlextPluginService as TestFlextPluginService,
        TestFlextPluginServiceStubBridges as TestFlextPluginServiceStubBridges,
    )
    from tests.test_plugin import (
        TestPluginModel as TestPluginModel,
        TestPluginPlatform as TestPluginPlatform,
        TestPluginRegistry as TestPluginRegistry,
    )
    from tests.typings import (
        FlextPluginTestTypes as FlextPluginTestTypes,
        FlextPluginTestTypes as t,
    )
    from tests.unit import (
        test_config as test_config,
        test_constants as test_constants,
        test_models as test_models,
        test_types as test_types,
    )
    from tests.unit.test_config import (
        TestFlextPluginSettings as TestFlextPluginSettings,
    )
    from tests.unit.test_constants import (
        TestFlextPluginConstants as TestFlextPluginConstants,
    )
    from tests.unit.test_models import TestFlextPluginModels as TestFlextPluginModels
    from tests.unit.test_types import TestFlextPluginTypes as TestFlextPluginTypes
    from tests.utilities import (
        FlextPluginTestUtilities as FlextPluginTestUtilities,
        FlextPluginTestUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextPluginTestConstants": ["tests.constants", "FlextPluginTestConstants"],
    "FlextPluginTestModels": ["tests.models", "FlextPluginTestModels"],
    "FlextPluginTestProtocols": ["tests.protocols", "FlextPluginTestProtocols"],
    "FlextPluginTestTypes": ["tests.typings", "FlextPluginTestTypes"],
    "FlextPluginTestUtilities": ["tests.utilities", "FlextPluginTestUtilities"],
    "PluginInterface": ["tests.test_application_services", "PluginInterface"],
    "TestBackwardsCompatibilityAliasesReal": [
        "tests.test_application_services",
        "TestBackwardsCompatibilityAliasesReal",
    ],
    "TestDynamicLoaderAdapter": ["tests.test_loader", "TestDynamicLoaderAdapter"],
    "TestFlextPlugin": ["tests.test_domain_entities", "TestFlextPlugin"],
    "TestFlextPluginConstants": [
        "tests.unit.test_constants",
        "TestFlextPluginConstants",
    ],
    "TestFlextPluginConstantsLifecycle": [
        "tests.test_core_types",
        "TestFlextPluginConstantsLifecycle",
    ],
    "TestFlextPluginConstantsPluginType": [
        "tests.test_core_types",
        "TestFlextPluginConstantsPluginType",
    ],
    "TestFlextPluginDiscovery": ["tests.test_domain_ports", "TestFlextPluginDiscovery"],
    "TestFlextPluginDiscoveryReal": [
        "tests.test_application_services",
        "TestFlextPluginDiscoveryReal",
    ],
    "TestFlextPluginExecution": [
        "tests.test_domain_entities",
        "TestFlextPluginExecution",
    ],
    "TestFlextPluginHandlers": ["tests.test_handlers", "TestFlextPluginHandlers"],
    "TestFlextPluginHotReload": ["tests.test_hot_reload", "TestFlextPluginHotReload"],
    "TestFlextPluginLoader": ["tests.test_loader", "TestFlextPluginLoader"],
    "TestFlextPluginMetadata": [
        "tests.test_domain_entities",
        "TestFlextPluginMetadata",
    ],
    "TestFlextPluginModels": ["tests.unit.test_models", "TestFlextPluginModels"],
    "TestFlextPluginRegistryEntity": [
        "tests.test_domain_entities",
        "TestFlextPluginRegistryEntity",
    ],
    "TestFlextPluginService": ["tests.test_manager", "TestFlextPluginService"],
    "TestFlextPluginServiceReal": [
        "tests.test_application_services",
        "TestFlextPluginServiceReal",
    ],
    "TestFlextPluginServiceStubBridges": [
        "tests.test_manager",
        "TestFlextPluginServiceStubBridges",
    ],
    "TestFlextPluginServiceWithRealAdapters": [
        "tests.test_application_services",
        "TestFlextPluginServiceWithRealAdapters",
    ],
    "TestFlextPluginSettings": ["tests.unit.test_config", "TestFlextPluginSettings"],
    "TestFlextPluginTypes": ["tests.unit.test_types", "TestFlextPluginTypes"],
    "TestHotReloadPackage": ["tests.test_hot_reload_package", "TestHotReloadPackage"],
    "TestPluginError": ["tests.test_core_types", "TestPluginError"],
    "TestPluginModel": ["tests.test_plugin", "TestPluginModel"],
    "TestPluginPlatform": ["tests.test_plugin", "TestPluginPlatform"],
    "TestPluginRegistry": ["tests.test_plugin", "TestPluginRegistry"],
    "TestRealPluginDiscoveryAndExecution": [
        "tests.test_application_services",
        "TestRealPluginDiscoveryAndExecution",
    ],
    "TestRealPluginErrorScenarios": [
        "tests.test_application_services",
        "TestRealPluginErrorScenarios",
    ],
    "TestRealPluginIntegrationWorkflow": [
        "tests.test_application_services",
        "TestRealPluginIntegrationWorkflow",
    ],
    "TestServiceErrorHandling": [
        "tests.test_application_services",
        "TestServiceErrorHandling",
    ],
    "TestServicesIntegrationReal": [
        "tests.test_application_services",
        "TestServicesIntegrationReal",
    ],
    "c": ["tests.constants", "FlextPluginTestConstants"],
    "conftest": ["tests.conftest", ""],
    "constants": ["tests.constants", ""],
    "d": ["flext_tests", "d"],
    "e": ["flext_tests", "e"],
    "h": ["flext_tests", "h"],
    "m": ["tests.models", "FlextPluginTestModels"],
    "models": ["tests.models", ""],
    "modules_to_test": ["tests.test_imports", "modules_to_test"],
    "p": ["tests.protocols", "FlextPluginTestProtocols"],
    "performance_config": ["tests.conftest", "performance_config"],
    "protocols": ["tests.protocols", ""],
    "pytest_configure": ["tests.conftest", "pytest_configure"],
    "r": ["flext_tests", "r"],
    "real_container_with_adapters": ["tests.conftest", "real_container_with_adapters"],
    "real_discovery_adapter": ["tests.conftest", "real_discovery_adapter"],
    "real_discovery_service_with_adapters": [
        "tests.test_application_services",
        "real_discovery_service_with_adapters",
    ],
    "real_loader_adapter": ["tests.conftest", "real_loader_adapter"],
    "real_manager_adapter": ["tests.conftest", "real_manager_adapter"],
    "real_plugin_config": ["tests.conftest", "real_plugin_config"],
    "real_plugin_configs": ["tests.conftest", "real_plugin_configs"],
    "real_plugin_data": ["tests.conftest", "real_plugin_data"],
    "real_plugin_dependencies": ["tests.conftest", "real_plugin_dependencies"],
    "real_plugin_directory": ["tests.conftest", "real_plugin_directory"],
    "real_plugin_discovery": [
        "tests.test_application_services",
        "real_plugin_discovery",
    ],
    "real_plugin_entity": ["tests.conftest", "real_plugin_entity"],
    "real_plugin_loader": ["tests.test_application_services", "real_plugin_loader"],
    "real_processor_plugin": ["tests.conftest", "real_processor_plugin"],
    "real_service_with_adapters": [
        "tests.test_application_services",
        "real_service_with_adapters",
    ],
    "real_tap_plugin": ["tests.conftest", "real_tap_plugin"],
    "real_target_plugin": ["tests.conftest", "real_target_plugin"],
    "s": ["flext_tests", "s"],
    "set_test_environment": ["tests.conftest", "set_test_environment"],
    "simple_plugin_directory": ["tests.conftest", "simple_plugin_directory"],
    "t": ["tests.typings", "FlextPluginTestTypes"],
    "temp_plugin_dir": ["tests.test_application_services", "temp_plugin_dir"],
    "test_application_handlers": ["tests.test_application_handlers", ""],
    "test_application_services": ["tests.test_application_services", ""],
    "test_basic_plugin_example_execution": [
        "tests.test_examples",
        "test_basic_plugin_example_execution",
    ],
    "test_config": ["tests.unit.test_config", ""],
    "test_constants": ["tests.unit.test_constants", ""],
    "test_core_types": ["tests.test_core_types", ""],
    "test_discovery": ["tests.test_discovery", ""],
    "test_docker_integration_example_execution": [
        "tests.test_examples",
        "test_docker_integration_example_execution",
    ],
    "test_docker_integration_example_with_connection_testing": [
        "tests.test_examples",
        "test_docker_integration_example_with_connection_testing",
    ],
    "test_domain_entities": ["tests.test_domain_entities", ""],
    "test_domain_ports": ["tests.test_domain_ports", ""],
    "test_examples": ["tests.test_examples", ""],
    "test_handlers": ["tests.test_handlers", ""],
    "test_hot_reload": ["tests.test_hot_reload", ""],
    "test_hot_reload_package": ["tests.test_hot_reload_package", ""],
    "test_imports": ["tests.test_imports", ""],
    "test_loader": ["tests.test_loader", ""],
    "test_manager": ["tests.test_manager", ""],
    "test_models": ["tests.unit.test_models", ""],
    "test_plugin": ["tests.test_plugin", ""],
    "test_plugin_configuration_example_execution": [
        "tests.test_examples",
        "test_plugin_configuration_example_execution",
    ],
    "test_types": ["tests.unit.test_types", ""],
    "typings": ["tests.typings", ""],
    "u": ["tests.utilities", "FlextPluginTestUtilities"],
    "unit": ["tests.unit", ""],
    "utilities": ["tests.utilities", ""],
    "x": ["flext_tests", "x"],
}

_EXPORTS: Sequence[str] = [
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
    "conftest",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "models",
    "modules_to_test",
    "p",
    "performance_config",
    "protocols",
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
    "test_application_handlers",
    "test_application_services",
    "test_basic_plugin_example_execution",
    "test_config",
    "test_constants",
    "test_core_types",
    "test_discovery",
    "test_docker_integration_example_execution",
    "test_docker_integration_example_with_connection_testing",
    "test_domain_entities",
    "test_domain_ports",
    "test_examples",
    "test_handlers",
    "test_hot_reload",
    "test_hot_reload_package",
    "test_imports",
    "test_loader",
    "test_manager",
    "test_models",
    "test_plugin",
    "test_plugin_configuration_example_execution",
    "test_types",
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
