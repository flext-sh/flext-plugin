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
    from flext_plugin import (
        conftest,
        constants,
        models,
        protocols,
        test_application_handlers,
        test_application_services,
        test_config,
        test_constants,
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
        test_models,
        test_plugin,
        test_types,
        typings,
        unit,
        utilities,
    )
    from flext_plugin.conftest import (
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
    from flext_plugin.constants import (
        FlextPluginTestConstants,
        FlextPluginTestConstants as c,
    )
    from flext_plugin.models import FlextPluginTestModels, FlextPluginTestModels as m
    from flext_plugin.protocols import (
        FlextPluginTestProtocols,
        FlextPluginTestProtocols as p,
    )
    from flext_plugin.test_application_services import (
        PluginInterface,
        real_discovery_service_with_adapters,
        real_plugin_discovery,
        real_plugin_loader,
        real_service_with_adapters,
        temp_plugin_dir,
    )
    from flext_plugin.test_core_types import TestFlextPluginConstantsPluginType
    from flext_plugin.test_domain_entities import TestFlextPlugin
    from flext_plugin.test_domain_ports import TestFlextPluginDiscovery
    from flext_plugin.test_examples import (
        test_basic_plugin_example_execution,
        test_docker_integration_example_with_connection_testing,
    )
    from flext_plugin.test_handlers import TestFlextPluginHandlers
    from flext_plugin.test_hot_reload import TestFlextPluginHotReload
    from flext_plugin.test_hot_reload_package import TestHotReloadPackage
    from flext_plugin.test_imports import modules_to_test
    from flext_plugin.test_loader import TestFlextPluginLoader
    from flext_plugin.test_manager import TestFlextPluginService
    from flext_plugin.test_plugin import TestPluginModel
    from flext_plugin.typings import FlextPluginTestTypes, FlextPluginTestTypes as t
    from flext_plugin.unit import (
        TestFlextPluginConstants,
        TestFlextPluginModels,
        TestFlextPluginSettings,
        TestFlextPluginTypes,
    )
    from flext_plugin.utilities import (
        FlextPluginTestUtilities,
        FlextPluginTestUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    ("flext_plugin.unit",),
    {
        "FlextPluginTestConstants": "flext_plugin.constants",
        "FlextPluginTestModels": "flext_plugin.models",
        "FlextPluginTestProtocols": "flext_plugin.protocols",
        "FlextPluginTestTypes": "flext_plugin.typings",
        "FlextPluginTestUtilities": "flext_plugin.utilities",
        "PluginInterface": "flext_plugin.test_application_services",
        "TestFlextPlugin": "flext_plugin.test_domain_entities",
        "TestFlextPluginConstantsPluginType": "flext_plugin.test_core_types",
        "TestFlextPluginDiscovery": "flext_plugin.test_domain_ports",
        "TestFlextPluginHandlers": "flext_plugin.test_handlers",
        "TestFlextPluginHotReload": "flext_plugin.test_hot_reload",
        "TestFlextPluginLoader": "flext_plugin.test_loader",
        "TestFlextPluginService": "flext_plugin.test_manager",
        "TestHotReloadPackage": "flext_plugin.test_hot_reload_package",
        "TestPluginModel": "flext_plugin.test_plugin",
        "c": ("flext_plugin.constants", "FlextPluginTestConstants"),
        "conftest": "flext_plugin.conftest",
        "constants": "flext_plugin.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_plugin.models", "FlextPluginTestModels"),
        "models": "flext_plugin.models",
        "modules_to_test": "flext_plugin.test_imports",
        "p": ("flext_plugin.protocols", "FlextPluginTestProtocols"),
        "performance_config": "flext_plugin.conftest",
        "protocols": "flext_plugin.protocols",
        "pytest_configure": "flext_plugin.conftest",
        "r": ("flext_core.result", "FlextResult"),
        "real_container_with_adapters": "flext_plugin.conftest",
        "real_discovery_adapter": "flext_plugin.conftest",
        "real_discovery_service_with_adapters": "flext_plugin.test_application_services",
        "real_loader_adapter": "flext_plugin.conftest",
        "real_manager_adapter": "flext_plugin.conftest",
        "real_plugin_config": "flext_plugin.conftest",
        "real_plugin_configs": "flext_plugin.conftest",
        "real_plugin_data": "flext_plugin.conftest",
        "real_plugin_dependencies": "flext_plugin.conftest",
        "real_plugin_directory": "flext_plugin.conftest",
        "real_plugin_discovery": "flext_plugin.test_application_services",
        "real_plugin_entity": "flext_plugin.conftest",
        "real_plugin_loader": "flext_plugin.test_application_services",
        "real_processor_plugin": "flext_plugin.conftest",
        "real_service_with_adapters": "flext_plugin.test_application_services",
        "real_tap_plugin": "flext_plugin.conftest",
        "real_target_plugin": "flext_plugin.conftest",
        "s": ("flext_core.service", "FlextService"),
        "set_test_environment": "flext_plugin.conftest",
        "simple_plugin_directory": "flext_plugin.conftest",
        "t": ("flext_plugin.typings", "FlextPluginTestTypes"),
        "temp_plugin_dir": "flext_plugin.test_application_services",
        "test_application_handlers": "flext_plugin.test_application_handlers",
        "test_application_services": "flext_plugin.test_application_services",
        "test_basic_plugin_example_execution": "flext_plugin.test_examples",
        "test_config": "flext_plugin.test_config",
        "test_constants": "flext_plugin.test_constants",
        "test_core_types": "flext_plugin.test_core_types",
        "test_discovery": "flext_plugin.test_discovery",
        "test_docker_integration_example_with_connection_testing": "flext_plugin.test_examples",
        "test_domain_entities": "flext_plugin.test_domain_entities",
        "test_domain_ports": "flext_plugin.test_domain_ports",
        "test_examples": "flext_plugin.test_examples",
        "test_handlers": "flext_plugin.test_handlers",
        "test_hot_reload": "flext_plugin.test_hot_reload",
        "test_hot_reload_package": "flext_plugin.test_hot_reload_package",
        "test_imports": "flext_plugin.test_imports",
        "test_loader": "flext_plugin.test_loader",
        "test_manager": "flext_plugin.test_manager",
        "test_models": "flext_plugin.test_models",
        "test_plugin": "flext_plugin.test_plugin",
        "test_types": "flext_plugin.test_types",
        "typings": "flext_plugin.typings",
        "u": ("flext_plugin.utilities", "FlextPluginTestUtilities"),
        "unit": "flext_plugin.unit",
        "utilities": "flext_plugin.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
