# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants
    from tests.conftest import (
        performance_config,
        plugin_settings,
        pytest_configure,
        pytest_plugins,
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

    constants = _tests_constants
    import tests.models as _tests_models
    from tests.constants import FlextPluginTestConstants, FlextPluginTestConstants as c

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import FlextPluginTestModels, FlextPluginTestModels as m

    protocols = _tests_protocols
    import tests.test_application_handlers as _tests_test_application_handlers
    from tests.protocols import FlextPluginTestProtocols, FlextPluginTestProtocols as p

    test_application_handlers = _tests_test_application_handlers
    import tests.test_application_services as _tests_test_application_services

    test_application_services = _tests_test_application_services
    import tests.test_core_types as _tests_test_core_types
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

    test_core_types = _tests_test_core_types
    import tests.test_discovery as _tests_test_discovery
    from tests.test_core_types import (
        TestFlextPluginConstantsLifecycle,
        TestFlextPluginConstantsPluginType,
        TestPluginError,
    )

    test_discovery = _tests_test_discovery
    import tests.test_domain_entities as _tests_test_domain_entities

    test_domain_entities = _tests_test_domain_entities
    import tests.test_domain_ports as _tests_test_domain_ports
    from tests.test_domain_entities import (
        TestFlextPlugin,
        TestFlextPluginExecution,
        TestFlextPluginMetadata,
        TestFlextPluginRegistryEntity,
    )

    test_domain_ports = _tests_test_domain_ports
    import tests.test_examples as _tests_test_examples
    from tests.test_domain_ports import TestFlextPluginDiscovery

    test_examples = _tests_test_examples
    import tests.test_handlers as _tests_test_handlers
    from tests.test_examples import (
        test_basic_plugin_example_execution,
        test_docker_integration_example_execution,
        test_docker_integration_example_with_connection_testing,
        test_plugin_configuration_example_execution,
    )

    test_handlers = _tests_test_handlers
    import tests.test_hot_reload as _tests_test_hot_reload
    from tests.test_handlers import TestFlextPluginHandlers

    test_hot_reload = _tests_test_hot_reload
    import tests.test_hot_reload_package as _tests_test_hot_reload_package
    from tests.test_hot_reload import TestFlextPluginHotReload

    test_hot_reload_package = _tests_test_hot_reload_package
    import tests.test_imports as _tests_test_imports
    from tests.test_hot_reload_package import TestHotReloadPackage

    test_imports = _tests_test_imports
    import tests.test_loader as _tests_test_loader
    from tests.test_imports import modules_to_test

    test_loader = _tests_test_loader
    import tests.test_manager as _tests_test_manager
    from tests.test_loader import TestDynamicLoaderAdapter, TestFlextPluginLoader

    test_manager = _tests_test_manager
    import tests.test_plugin as _tests_test_plugin
    from tests.test_manager import (
        TestFlextPluginService,
        TestFlextPluginServiceStubBridges,
    )

    test_plugin = _tests_test_plugin
    import tests.typings as _tests_typings
    from tests.test_plugin import (
        TestPluginModel,
        TestPluginPlatform,
        TestPluginRegistry,
    )

    typings = _tests_typings
    import tests.unit as _tests_unit
    from tests.typings import FlextPluginTestTypes, FlextPluginTestTypes as t

    unit = _tests_unit
    import tests.utilities as _tests_utilities
    from tests.unit import (
        TestFlextPluginConstants,
        TestFlextPluginModels,
        TestFlextPluginSettings,
        TestFlextPluginTypes,
        test_config,
        test_constants,
        test_models,
        test_types,
    )

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.utilities import FlextPluginTestUtilities, FlextPluginTestUtilities as u
_LAZY_IMPORTS = merge_lazy_imports(
    ("tests.unit",),
    {
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
        "TestFlextPluginConstantsLifecycle": (
            "tests.test_core_types",
            "TestFlextPluginConstantsLifecycle",
        ),
        "TestFlextPluginConstantsPluginType": (
            "tests.test_core_types",
            "TestFlextPluginConstantsPluginType",
        ),
        "TestFlextPluginDiscovery": (
            "tests.test_domain_ports",
            "TestFlextPluginDiscovery",
        ),
        "TestFlextPluginDiscoveryReal": (
            "tests.test_application_services",
            "TestFlextPluginDiscoveryReal",
        ),
        "TestFlextPluginExecution": (
            "tests.test_domain_entities",
            "TestFlextPluginExecution",
        ),
        "TestFlextPluginHandlers": ("tests.test_handlers", "TestFlextPluginHandlers"),
        "TestFlextPluginHotReload": (
            "tests.test_hot_reload",
            "TestFlextPluginHotReload",
        ),
        "TestFlextPluginLoader": ("tests.test_loader", "TestFlextPluginLoader"),
        "TestFlextPluginMetadata": (
            "tests.test_domain_entities",
            "TestFlextPluginMetadata",
        ),
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
        "TestHotReloadPackage": (
            "tests.test_hot_reload_package",
            "TestHotReloadPackage",
        ),
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
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("tests.models", "FlextPluginTestModels"),
        "models": "tests.models",
        "modules_to_test": ("tests.test_imports", "modules_to_test"),
        "p": ("tests.protocols", "FlextPluginTestProtocols"),
        "performance_config": ("tests.conftest", "performance_config"),
        "plugin_settings": ("tests.conftest", "plugin_settings"),
        "protocols": "tests.protocols",
        "pytest_configure": ("tests.conftest", "pytest_configure"),
        "pytest_plugins": ("tests.conftest", "pytest_plugins"),
        "r": ("flext_core.result", "FlextResult"),
        "real_container_with_adapters": (
            "tests.conftest",
            "real_container_with_adapters",
        ),
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
        "s": ("flext_core.service", "FlextService"),
        "set_test_environment": ("tests.conftest", "set_test_environment"),
        "simple_plugin_directory": ("tests.conftest", "simple_plugin_directory"),
        "t": ("tests.typings", "FlextPluginTestTypes"),
        "temp_plugin_dir": ("tests.test_application_services", "temp_plugin_dir"),
        "test_application_handlers": "tests.test_application_handlers",
        "test_application_services": "tests.test_application_services",
        "test_basic_plugin_example_execution": (
            "tests.test_examples",
            "test_basic_plugin_example_execution",
        ),
        "test_core_types": "tests.test_core_types",
        "test_discovery": "tests.test_discovery",
        "test_docker_integration_example_execution": (
            "tests.test_examples",
            "test_docker_integration_example_execution",
        ),
        "test_docker_integration_example_with_connection_testing": (
            "tests.test_examples",
            "test_docker_integration_example_with_connection_testing",
        ),
        "test_domain_entities": "tests.test_domain_entities",
        "test_domain_ports": "tests.test_domain_ports",
        "test_examples": "tests.test_examples",
        "test_handlers": "tests.test_handlers",
        "test_hot_reload": "tests.test_hot_reload",
        "test_hot_reload_package": "tests.test_hot_reload_package",
        "test_imports": "tests.test_imports",
        "test_loader": "tests.test_loader",
        "test_manager": "tests.test_manager",
        "test_plugin": "tests.test_plugin",
        "test_plugin_configuration_example_execution": (
            "tests.test_examples",
            "test_plugin_configuration_example_execution",
        ),
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextPluginTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

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
    "plugin_settings",
    "protocols",
    "pytest_configure",
    "pytest_plugins",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
