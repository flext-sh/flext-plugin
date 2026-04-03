# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests import (
        conftest,
        constants,
        models,
        protocols,
        test_application_handlers,
        test_application_services,
        test_core_types,
        test_discovery,
        test_domain_entities,
        test_domain_ports,
        test_examples,
        test_handlers,
        test_hot_reload,
        test_hot_reload_package,
        test_imports,
        test_loader,
        test_manager,
        test_plugin,
        typings,
        unit,
        utilities,
    )
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
    from tests.utilities import FlextPluginTestUtilities, FlextPluginTestUtilities as u

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    ("tests.unit",),
    {
        "FlextPluginTestConstants": "tests.constants",
        "FlextPluginTestModels": "tests.models",
        "FlextPluginTestProtocols": "tests.protocols",
        "FlextPluginTestTypes": "tests.typings",
        "FlextPluginTestUtilities": "tests.utilities",
        "PluginInterface": "tests.test_application_services",
        "TestBackwardsCompatibilityAliasesReal": "tests.test_application_services",
        "TestDynamicLoaderAdapter": "tests.test_loader",
        "TestFlextPlugin": "tests.test_domain_entities",
        "TestFlextPluginConstantsLifecycle": "tests.test_core_types",
        "TestFlextPluginConstantsPluginType": "tests.test_core_types",
        "TestFlextPluginDiscovery": "tests.test_domain_ports",
        "TestFlextPluginDiscoveryReal": "tests.test_application_services",
        "TestFlextPluginExecution": "tests.test_domain_entities",
        "TestFlextPluginHandlers": "tests.test_handlers",
        "TestFlextPluginHotReload": "tests.test_hot_reload",
        "TestFlextPluginLoader": "tests.test_loader",
        "TestFlextPluginMetadata": "tests.test_domain_entities",
        "TestFlextPluginRegistryEntity": "tests.test_domain_entities",
        "TestFlextPluginService": "tests.test_manager",
        "TestFlextPluginServiceReal": "tests.test_application_services",
        "TestFlextPluginServiceStubBridges": "tests.test_manager",
        "TestFlextPluginServiceWithRealAdapters": "tests.test_application_services",
        "TestHotReloadPackage": "tests.test_hot_reload_package",
        "TestPluginError": "tests.test_core_types",
        "TestPluginModel": "tests.test_plugin",
        "TestPluginPlatform": "tests.test_plugin",
        "TestPluginRegistry": "tests.test_plugin",
        "TestRealPluginDiscoveryAndExecution": "tests.test_application_services",
        "TestRealPluginErrorScenarios": "tests.test_application_services",
        "TestRealPluginIntegrationWorkflow": "tests.test_application_services",
        "TestServiceErrorHandling": "tests.test_application_services",
        "TestServicesIntegrationReal": "tests.test_application_services",
        "c": ("tests.constants", "FlextPluginTestConstants"),
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("tests.models", "FlextPluginTestModels"),
        "models": "tests.models",
        "modules_to_test": "tests.test_imports",
        "p": ("tests.protocols", "FlextPluginTestProtocols"),
        "performance_config": "tests.conftest",
        "protocols": "tests.protocols",
        "pytest_configure": "tests.conftest",
        "r": ("flext_core.result", "FlextResult"),
        "real_container_with_adapters": "tests.conftest",
        "real_discovery_adapter": "tests.conftest",
        "real_discovery_service_with_adapters": "tests.test_application_services",
        "real_loader_adapter": "tests.conftest",
        "real_manager_adapter": "tests.conftest",
        "real_plugin_config": "tests.conftest",
        "real_plugin_configs": "tests.conftest",
        "real_plugin_data": "tests.conftest",
        "real_plugin_dependencies": "tests.conftest",
        "real_plugin_directory": "tests.conftest",
        "real_plugin_discovery": "tests.test_application_services",
        "real_plugin_entity": "tests.conftest",
        "real_plugin_loader": "tests.test_application_services",
        "real_processor_plugin": "tests.conftest",
        "real_service_with_adapters": "tests.test_application_services",
        "real_tap_plugin": "tests.conftest",
        "real_target_plugin": "tests.conftest",
        "s": ("flext_core.service", "FlextService"),
        "set_test_environment": "tests.conftest",
        "simple_plugin_directory": "tests.conftest",
        "t": ("tests.typings", "FlextPluginTestTypes"),
        "temp_plugin_dir": "tests.test_application_services",
        "test_application_handlers": "tests.test_application_handlers",
        "test_application_services": "tests.test_application_services",
        "test_basic_plugin_example_execution": "tests.test_examples",
        "test_core_types": "tests.test_core_types",
        "test_discovery": "tests.test_discovery",
        "test_docker_integration_example_execution": "tests.test_examples",
        "test_docker_integration_example_with_connection_testing": "tests.test_examples",
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
        "test_plugin_configuration_example_execution": "tests.test_examples",
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextPluginTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
