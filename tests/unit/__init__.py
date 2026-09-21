# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .test_api_direct import TestsFlextPluginApi
    from .test_config import TestsFlextPluginConfig
    from .test_constants import TestsFlextPluginConstantsUnit
    from .test_discovery import TestsFlextPluginDiscovery
    from .test_domain_entities import TestsFlextPluginDomainEntities
    from .test_domain_ports import TestsFlextPluginDomainPorts
    from .test_examples import TestsFlextPluginExamples
    from .test_imports import TestsFlextPluginImports
    from .test_models import TestsFlextPluginModelsUnit
    from .test_platform_service import (
        TestsFlextPluginPlatformExecution,
        TestsFlextPluginPlatformRegistry,
        TestsFlextPluginPlatformService,
    )
    from .test_plugin import TestsFlextPluginPlugin
    from .test_types import TestsFlextPluginTypesUnit
    from .test_utilities_direct import TestsFlextPluginUtilities
__all__: tuple[str, ...] = (
    "TestsFlextPluginApi",
    "TestsFlextPluginConfig",
    "TestsFlextPluginConstantsUnit",
    "TestsFlextPluginDiscovery",
    "TestsFlextPluginDomainEntities",
    "TestsFlextPluginDomainPorts",
    "TestsFlextPluginExamples",
    "TestsFlextPluginImports",
    "TestsFlextPluginModelsUnit",
    "TestsFlextPluginPlatformExecution",
    "TestsFlextPluginPlatformRegistry",
    "TestsFlextPluginPlatformService",
    "TestsFlextPluginPlugin",
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
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".test_api_direct": ("TestsFlextPluginApi",),
            ".test_config": ("TestsFlextPluginConfig",),
            ".test_constants": ("TestsFlextPluginConstantsUnit",),
            ".test_discovery": ("TestsFlextPluginDiscovery",),
            ".test_domain_entities": ("TestsFlextPluginDomainEntities",),
            ".test_domain_ports": ("TestsFlextPluginDomainPorts",),
            ".test_examples": ("TestsFlextPluginExamples",),
            ".test_imports": ("TestsFlextPluginImports",),
            ".test_models": ("TestsFlextPluginModelsUnit",),
            ".test_platform_service": (
                "TestsFlextPluginPlatformExecution",
                "TestsFlextPluginPlatformRegistry",
                "TestsFlextPluginPlatformService",
            ),
            ".test_plugin": ("TestsFlextPluginPlugin",),
            ".test_types": ("TestsFlextPluginTypesUnit",),
            ".test_utilities_direct": ("TestsFlextPluginUtilities",),
            "flext_tests": (
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
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
