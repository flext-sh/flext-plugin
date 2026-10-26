# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import (
        api,
        config,
        d,
        e,
        h,
        install_local_packages,
        r,
        settings,
        td,
        tf,
        tk,
        tm,
        x,
    )

    from flext_plugin import cli, main, plugin
    from tests.base import TestsFlextPluginServiceBase, s
    from tests.constants import TestsFlextPluginConstants, c
    from tests.models import TestsFlextPluginModels, m
    from tests.protocols import TestsFlextPluginProtocols, p
    from tests.settings import TestsFlextPluginSettings
    from tests.typings import TestsFlextPluginTypes, t
    from tests.utilities import TestsFlextPluginUtilities, u


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
    "d",
    "e",
    "h",
    "install_local_packages",
    "m",
    "main",
    "p",
    "plugin",
    "r",
    "s",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextPluginConstants": ".constants",
        "TestsFlextPluginModels": ".models",
        "TestsFlextPluginProtocols": ".protocols",
        "TestsFlextPluginServiceBase": ".base",
        "TestsFlextPluginSettings": ".settings",
        "TestsFlextPluginTypes": ".typings",
        "TestsFlextPluginUtilities": ".utilities",
        "api": "flext_tests",
        "c": ".constants",
        "cli": "flext_plugin",
        "config": "flext_tests",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "install_local_packages": "flext_tests",
        "m": ".models",
        "main": "flext_plugin",
        "p": ".protocols",
        "plugin": "flext_plugin",
        "r": "flext_tests",
        "s": ".base",
        "settings": "flext_tests",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    }),
    public_exports=__all__,
)
