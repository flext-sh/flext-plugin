# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import unit as unit
    from flext_plugin import FlextPluginConstants
    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x

    from .base import TestsFlextPluginServiceBase, TestsFlextPluginServiceBase as s
    from .constants import TestsFlextPluginConstants, TestsFlextPluginConstants as c
    from .models import TestsFlextPluginModels, TestsFlextPluginModels as m
    from .protocols import TestsFlextPluginProtocols, TestsFlextPluginProtocols as p
    from .settings import TestsFlextPluginSettings
    from .typings import TestsFlextPluginTypes, TestsFlextPluginTypes as t
    from .utilities import TestsFlextPluginUtilities, TestsFlextPluginUtilities as u
__all__: tuple[str, ...] = (
    "FlextPluginConstants",
    "FlextTestsConstants",
    "TestsFlextPluginConstants",
    "TestsFlextPluginModels",
    "TestsFlextPluginProtocols",
    "TestsFlextPluginServiceBase",
    "TestsFlextPluginSettings",
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
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextPluginServiceBase", "s"),
            ".constants": ("TestsFlextPluginConstants", "c"),
            ".models": ("TestsFlextPluginModels", "m"),
            ".protocols": ("TestsFlextPluginProtocols", "p"),
            ".settings": ("TestsFlextPluginSettings",),
            ".typings": ("TestsFlextPluginTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextPluginUtilities", "u"),
            "flext_plugin": ("FlextPluginConstants",),
            "flext_tests": (
                "FlextTestsConstants",
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
