# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_plugin import d, e, h, r, s, x
    from flext_tests import td, tf, tk, tm, tv
    from tests.constants import TestsFlextPluginConstants, c
    from tests.models import TestsFlextPluginModels, m
    from tests.protocols import TestsFlextPluginProtocols, p
    from tests.typings import TestsFlextPluginTypes, t
    from tests.unit.test_application_handlers import TestFlextPluginHandlers
    from tests.unit.test_application_services import (
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
    )
    from tests.unit.test_config import TestFlextPluginSettings
    from tests.unit.test_constants import TestFlextPluginConstants
    from tests.unit.test_core_types import (
        TestFlextPluginConstantsLifecycle,
        TestFlextPluginConstantsPluginType,
        TestPluginError,
    )
    from tests.unit.test_discovery import TestFlextPluginDiscovery
    from tests.unit.test_domain_entities import (
        TestFlextPlugin,
        TestFlextPluginExecution,
        TestFlextPluginMetadata,
        TestFlextPluginRegistryEntity,
        TestFlextPluginSettingsEntities,
    )
    from tests.unit.test_domain_ports import TestFlextPluginDiscoveryPorts
    from tests.unit.test_handlers import TestFlextPluginHandlersHandlers
    from tests.unit.test_hot_reload import TestFlextPluginHotReload
    from tests.unit.test_hot_reload_package import TestHotReloadPackage
    from tests.unit.test_loader import TestDynamicLoaderAdapter, TestFlextPluginLoader
    from tests.unit.test_manager import (
        TestFlextPluginService,
        TestFlextPluginServiceStubBridges,
    )
    from tests.unit.test_models import TestFlextPluginModels
    from tests.unit.test_plugin import (
        TestPluginModel,
        TestPluginPlatform,
        TestPluginRegistry,
    )
    from tests.unit.test_types import TestFlextPluginTypes
    from tests.utilities import TestsFlextPluginUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map(
        {
            ".constants": (
                "TestsFlextPluginConstants",
                "c",
            ),
            ".models": (
                "TestsFlextPluginModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextPluginProtocols",
                "p",
            ),
            ".typings": (
                "TestsFlextPluginTypes",
                "t",
            ),
            ".unit.test_application_handlers": ("TestFlextPluginHandlers",),
            ".unit.test_application_services": (
                "PluginInterface",
                "TestBackwardsCompatibilityAliasesReal",
                "TestFlextPluginDiscoveryReal",
                "TestFlextPluginServiceReal",
                "TestFlextPluginServiceWithRealAdapters",
                "TestRealPluginDiscoveryAndExecution",
                "TestRealPluginErrorScenarios",
                "TestRealPluginIntegrationWorkflow",
                "TestServiceErrorHandling",
                "TestServicesIntegrationReal",
            ),
            ".unit.test_config": ("TestFlextPluginSettings",),
            ".unit.test_constants": ("TestFlextPluginConstants",),
            ".unit.test_core_types": (
                "TestFlextPluginConstantsLifecycle",
                "TestFlextPluginConstantsPluginType",
                "TestPluginError",
            ),
            ".unit.test_discovery": ("TestFlextPluginDiscovery",),
            ".unit.test_domain_entities": (
                "TestFlextPlugin",
                "TestFlextPluginExecution",
                "TestFlextPluginMetadata",
                "TestFlextPluginRegistryEntity",
                "TestFlextPluginSettingsEntities",
            ),
            ".unit.test_domain_ports": ("TestFlextPluginDiscoveryPorts",),
            ".unit.test_handlers": ("TestFlextPluginHandlersHandlers",),
            ".unit.test_hot_reload": ("TestFlextPluginHotReload",),
            ".unit.test_hot_reload_package": ("TestHotReloadPackage",),
            ".unit.test_loader": (
                "TestDynamicLoaderAdapter",
                "TestFlextPluginLoader",
            ),
            ".unit.test_manager": (
                "TestFlextPluginService",
                "TestFlextPluginServiceStubBridges",
            ),
            ".unit.test_models": ("TestFlextPluginModels",),
            ".unit.test_plugin": (
                "TestPluginModel",
                "TestPluginPlatform",
                "TestPluginRegistry",
            ),
            ".unit.test_types": ("TestFlextPluginTypes",),
            ".utilities": (
                "TestsFlextPluginUtilities",
                "u",
            ),
            "flext_plugin": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
            "flext_tests": (
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "PluginInterface",
    "TestBackwardsCompatibilityAliasesReal",
    "TestDynamicLoaderAdapter",
    "TestFlextPlugin",
    "TestFlextPluginConstants",
    "TestFlextPluginConstantsLifecycle",
    "TestFlextPluginConstantsPluginType",
    "TestFlextPluginDiscovery",
    "TestFlextPluginDiscoveryPorts",
    "TestFlextPluginDiscoveryReal",
    "TestFlextPluginExecution",
    "TestFlextPluginHandlers",
    "TestFlextPluginHandlersHandlers",
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
    "TestFlextPluginSettingsEntities",
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
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]
