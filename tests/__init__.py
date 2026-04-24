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
    from flext_tests import td, tf, tk, tm, tv

    from flext_plugin import d, e, h, r, s, x
    from tests.constants import TestsFlextPluginConstants, c
    from tests.models import TestsFlextPluginModels, m
    from tests.protocols import TestsFlextPluginProtocols, p
    from tests.typings import TestsFlextPluginTypes, t
    from tests.unit.test_application_handlers import TestsFlextPluginApplicationHandlers
    from tests.unit.test_application_services import TestsFlextPluginApplicationServices
    from tests.unit.test_config import TestsFlextPluginConfig
    from tests.unit.test_constants import TestsFlextPluginConstantsUnit
    from tests.unit.test_core_types import TestsFlextPluginCoreTypes
    from tests.unit.test_discovery import TestsFlextPluginDiscovery
    from tests.unit.test_domain_entities import TestsFlextPluginDomainEntities
    from tests.unit.test_domain_ports import TestsFlextPluginDomainPorts
    from tests.unit.test_handlers import TestsFlextPluginHandlers
    from tests.unit.test_hot_reload import TestsFlextPluginHotReload
    from tests.unit.test_hot_reload_package import TestsFlextPluginHotReloadPackage
    from tests.unit.test_loader import TestsFlextPluginLoader
    from tests.unit.test_manager import TestsFlextPluginManager
    from tests.unit.test_models import TestsFlextPluginModelsUnit
    from tests.unit.test_plugin import TestsFlextPluginPlugin
    from tests.unit.test_types import TestsFlextPluginTypes
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
            ".unit.test_application_handlers": ("TestsFlextPluginApplicationHandlers",),
            ".unit.test_application_services": ("TestsFlextPluginApplicationServices",),
            ".unit.test_config": ("TestsFlextPluginConfig",),
            ".unit.test_constants": ("TestsFlextPluginConstantsUnit",),
            ".unit.test_core_types": ("TestsFlextPluginCoreTypes",),
            ".unit.test_discovery": ("TestsFlextPluginDiscovery",),
            ".unit.test_domain_entities": ("TestsFlextPluginDomainEntities",),
            ".unit.test_domain_ports": ("TestsFlextPluginDomainPorts",),
            ".unit.test_handlers": ("TestsFlextPluginHandlers",),
            ".unit.test_hot_reload": ("TestsFlextPluginHotReload",),
            ".unit.test_hot_reload_package": ("TestsFlextPluginHotReloadPackage",),
            ".unit.test_loader": ("TestsFlextPluginLoader",),
            ".unit.test_manager": ("TestsFlextPluginManager",),
            ".unit.test_models": ("TestsFlextPluginModelsUnit",),
            ".unit.test_plugin": ("TestsFlextPluginPlugin",),
            ".unit.test_types": ("TestsFlextPluginTypes",),
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
    "TestsFlextPluginApplicationHandlers",
    "TestsFlextPluginApplicationServices",
    "TestsFlextPluginConfig",
    "TestsFlextPluginConstants",
    "TestsFlextPluginConstantsUnit",
    "TestsFlextPluginCoreTypes",
    "TestsFlextPluginDiscovery",
    "TestsFlextPluginDomainEntities",
    "TestsFlextPluginDomainPorts",
    "TestsFlextPluginHandlers",
    "TestsFlextPluginHotReload",
    "TestsFlextPluginHotReloadPackage",
    "TestsFlextPluginLoader",
    "TestsFlextPluginManager",
    "TestsFlextPluginModels",
    "TestsFlextPluginModelsUnit",
    "TestsFlextPluginPlugin",
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
