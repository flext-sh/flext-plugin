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
    from flext_tests import td as td, tf as tf, tk as tk, tm as tm, tv as tv

    from flext_plugin import d as d, e as e, h as h, r as r, x as x
    from tests.base import (
        TestsFlextPluginServiceBase as TestsFlextPluginServiceBase,
        s as s,
    )
    from tests.constants import (
        TestsFlextPluginConstants as TestsFlextPluginConstants,
        c as c,
    )
    from tests.models import TestsFlextPluginModels as TestsFlextPluginModels, m as m
    from tests.protocols import (
        TestsFlextPluginProtocols as TestsFlextPluginProtocols,
        p as p,
    )
    from tests.settings import TestsFlextPluginSettings as TestsFlextPluginSettings
    from tests.typings import TestsFlextPluginTypes as TestsFlextPluginTypes, t as t
    from tests.unit.test_config import TestsFlextPluginConfig as TestsFlextPluginConfig
    from tests.unit.test_constants import (
        TestsFlextPluginConstantsUnit as TestsFlextPluginConstantsUnit,
    )
    from tests.unit.test_core_types import (
        TestsFlextPluginCoreTypes as TestsFlextPluginCoreTypes,
    )
    from tests.unit.test_discovery import (
        TestsFlextPluginDiscovery as TestsFlextPluginDiscovery,
    )
    from tests.unit.test_domain_entities import (
        TestsFlextPluginDomainEntities as TestsFlextPluginDomainEntities,
    )
    from tests.unit.test_domain_ports import (
        TestsFlextPluginDomainPorts as TestsFlextPluginDomainPorts,
    )
    from tests.unit.test_examples import (
        TestsFlextPluginExamples as TestsFlextPluginExamples,
    )
    from tests.unit.test_models import (
        TestsFlextPluginModelsUnit as TestsFlextPluginModelsUnit,
    )
    from tests.unit.test_plugin import TestsFlextPluginPlugin as TestsFlextPluginPlugin
    from tests.unit.test_types import (
        TestsFlextPluginTypesUnit as TestsFlextPluginTypesUnit,
    )
    from tests.utilities import (
        TestsFlextPluginUtilities as TestsFlextPluginUtilities,
        u as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map(
        {
            ".base": (
                "TestsFlextPluginServiceBase",
                "s",
            ),
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
            ".unit.test_config": ("TestsFlextPluginConfig",),
            ".unit.test_constants": ("TestsFlextPluginConstantsUnit",),
            ".unit.test_core_types": ("TestsFlextPluginCoreTypes",),
            ".unit.test_discovery": ("TestsFlextPluginDiscovery",),
            ".unit.test_domain_entities": ("TestsFlextPluginDomainEntities",),
            ".unit.test_domain_ports": ("TestsFlextPluginDomainPorts",),
            ".unit.test_examples": ("TestsFlextPluginExamples",),
            ".unit.test_models": ("TestsFlextPluginModelsUnit",),
            ".unit.test_plugin": ("TestsFlextPluginPlugin",),
            ".unit.test_types": ("TestsFlextPluginTypesUnit",),
            ".utilities": (
                "TestsFlextPluginUtilities",
                "u",
            ),
            "flext_plugin": (
                "d",
                "e",
                "h",
                "r",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "TestsFlextPluginConfig",
    "TestsFlextPluginConstants",
    "TestsFlextPluginConstantsUnit",
    "TestsFlextPluginCoreTypes",
    "TestsFlextPluginDiscovery",
    "TestsFlextPluginDomainEntities",
    "TestsFlextPluginDomainPorts",
    "TestsFlextPluginExamples",
    "TestsFlextPluginModels",
    "TestsFlextPluginModelsUnit",
    "TestsFlextPluginPlugin",
    "TestsFlextPluginProtocols",
    "TestsFlextPluginServiceBase",
    "TestsFlextPluginSettings",
    "TestsFlextPluginTypes",
    "TestsFlextPluginTypesUnit",
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
