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
    from flext_tests import (
        d as d,
        e as e,
        h as h,
        r as r,
        td as td,
        tf as tf,
        tk as tk,
        tm as tm,
        tv as tv,
        x as x,
    )

    from flext_plugin.tests.base import (
        TestsFlextPluginServiceBase as TestsFlextPluginServiceBase,
        s as s,
    )
    from flext_plugin.tests.constants import (
        TestsFlextPluginConstants as TestsFlextPluginConstants,
        c as c,
    )
    from flext_plugin.tests.models import (
        TestsFlextPluginModels as TestsFlextPluginModels,
        m as m,
    )
    from flext_plugin.tests.protocols import (
        TestsFlextPluginProtocols as TestsFlextPluginProtocols,
        p as p,
    )
    from flext_plugin.tests.settings import (
        TestsFlextPluginSettings as TestsFlextPluginSettings,
    )
    from flext_plugin.tests.typings import (
        TestsFlextPluginTypes as TestsFlextPluginTypes,
        t as t,
    )
    from flext_plugin.tests.unit.test_config import (
        TestsFlextPluginConfig as TestsFlextPluginConfig,
    )
    from flext_plugin.tests.unit.test_constants import (
        TestsFlextPluginConstantsUnit as TestsFlextPluginConstantsUnit,
    )
    from flext_plugin.tests.unit.test_core_types import (
        TestsFlextPluginCoreTypes as TestsFlextPluginCoreTypes,
    )
    from flext_plugin.tests.unit.test_discovery import (
        TestsFlextPluginDiscovery as TestsFlextPluginDiscovery,
    )
    from flext_plugin.tests.unit.test_domain_entities import (
        TestsFlextPluginDomainEntities as TestsFlextPluginDomainEntities,
    )
    from flext_plugin.tests.unit.test_domain_ports import (
        TestsFlextPluginDomainPorts as TestsFlextPluginDomainPorts,
    )
    from flext_plugin.tests.unit.test_examples import (
        TestsFlextPluginExamples as TestsFlextPluginExamples,
    )
    from flext_plugin.tests.unit.test_models import (
        TestsFlextPluginModelsUnit as TestsFlextPluginModelsUnit,
    )
    from flext_plugin.tests.unit.test_plugin import (
        TestsFlextPluginPlugin as TestsFlextPluginPlugin,
    )
    from flext_plugin.tests.unit.test_types import (
        TestsFlextPluginTypesUnit as TestsFlextPluginTypesUnit,
    )
    from flext_plugin.tests.utilities import (
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
