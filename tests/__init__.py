# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests import d, e, h, r, td, tf, tk, tm, tv, x

    from tests.base import TestsFlextPluginServiceBase, s
    from tests.constants import TestsFlextPluginConstants, c
    from tests.models import TestsFlextPluginModels, m
    from tests.protocols import TestsFlextPluginProtocols, p
    from tests.settings import TestsFlextPluginSettings
    from tests.typings import TestsFlextPluginTypes, t
    from tests.unit.test_api_direct import TestsFlextPluginApi
    from tests.unit.test_config import TestsFlextPluginConfig
    from tests.unit.test_constants import TestsFlextPluginConstantsUnit
    from tests.unit.test_core_types import TestsFlextPluginCoreTypes
    from tests.unit.test_discovery import TestsFlextPluginDiscovery
    from tests.unit.test_domain_entities import TestsFlextPluginDomainEntities
    from tests.unit.test_domain_ports import TestsFlextPluginDomainPorts
    from tests.unit.test_examples import TestsFlextPluginExamples
    from tests.unit.test_imports import TestsFlextPluginImports
    from tests.unit.test_models import TestsFlextPluginModelsUnit
    from tests.unit.test_platform_service import (
        TestsFlextPluginPlatformExecution,
        TestsFlextPluginPlatformRegistry,
        TestsFlextPluginPlatformService,
    )
    from tests.unit.test_plugin import TestsFlextPluginPlugin
    from tests.unit.test_types import TestsFlextPluginTypesUnit
    from tests.utilities import TestsFlextPluginUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map(
        {
            ".base": (
                "TestsFlextPluginServiceBase",
                "s",
            ),
            ".conftest": ("conftest",),
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
            ".settings": ("TestsFlextPluginSettings",),
            ".typings": (
                "TestsFlextPluginTypes",
                "t",
            ),
            ".unit": ("unit",),
            ".unit.test_api_direct": ("TestsFlextPluginApi",),
            ".unit.test_config": ("TestsFlextPluginConfig",),
            ".unit.test_constants": ("TestsFlextPluginConstantsUnit",),
            ".unit.test_core_types": ("TestsFlextPluginCoreTypes",),
            ".unit.test_discovery": ("TestsFlextPluginDiscovery",),
            ".unit.test_domain_entities": ("TestsFlextPluginDomainEntities",),
            ".unit.test_domain_ports": ("TestsFlextPluginDomainPorts",),
            ".unit.test_examples": ("TestsFlextPluginExamples",),
            ".unit.test_imports": ("TestsFlextPluginImports",),
            ".unit.test_models": ("TestsFlextPluginModelsUnit",),
            ".unit.test_platform_service": (
                "TestsFlextPluginPlatformExecution",
                "TestsFlextPluginPlatformRegistry",
                "TestsFlextPluginPlatformService",
            ),
            ".unit.test_plugin": ("TestsFlextPluginPlugin",),
            ".unit.test_types": ("TestsFlextPluginTypesUnit",),
            ".utilities": (
                "TestsFlextPluginUtilities",
                "u",
            ),
            "flext_tests": (
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
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
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
