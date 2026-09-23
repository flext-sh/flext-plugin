# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli
    from flext_tests import (
        api,
        config,
        core,
        d,
        e,
        h,
        install_local_packages,
        lazy_attribute,
        load_infra_report,
        r,
        services,
        settings,
        td,
        tf,
        tk,
        tm,
        tv,
        x,
    )

    from flext_plugin import main, plugin

    from . import unit
    from .base import TestsFlextPluginServiceBase, TestsFlextPluginServiceBase as s
    from .constants import TestsFlextPluginConstants, TestsFlextPluginConstants as c
    from .models import TestsFlextPluginModels, TestsFlextPluginModels as m
    from .protocols import TestsFlextPluginProtocols, TestsFlextPluginProtocols as p
    from .settings import TestsFlextPluginSettings
    from .typings import TestsFlextPluginTypes, TestsFlextPluginTypes as t
    from .utilities import TestsFlextPluginUtilities, TestsFlextPluginUtilities as u


__all__: tuple[str, ...] = (
    "TestsFlextPluginConstants",
    "TestsFlextPluginModels",
    "TestsFlextPluginProtocols",
    "TestsFlextPluginServiceBase",
    "TestsFlextPluginSettings",
    "TestsFlextPluginTypes",
    "TestsFlextPluginUtilities",
    "api",
    "c",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "h",
    "install_local_packages",
    "lazy_attribute",
    "load_infra_report",
    "m",
    "main",
    "p",
    "plugin",
    "r",
    "s",
    "services",
    "settings",
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
            "flext_cli": ("cli",),
            "flext_plugin": ("main", "plugin"),
            "flext_tests": (
                "api",
                "config",
                "core",
                "d",
                "e",
                "h",
                "install_local_packages",
                "lazy_attribute",
                "load_infra_report",
                "r",
                "services",
                "settings",
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
