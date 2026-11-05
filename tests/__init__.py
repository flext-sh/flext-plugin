# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from examples import (
        ExamplesFlextPluginConstants,
        ExamplesFlextPluginModels,
        ExamplesFlextPluginProtocols,
        ExamplesFlextPluginTypes,
        ExamplesFlextPluginUtilities,
    )
    from flext_tests import api, d, e, h, r, td, tf, tk, tm, x

    from flext_plugin import (
        FlextPluginApi,
        FlextPluginCli,
        FlextPluginConfig,
        FlextPluginConstants,
        FlextPluginDiscovery,
        FlextPluginModels,
        FlextPluginModelsConfig,
        FlextPluginPlatform,
        FlextPluginProtocols,
        FlextPluginServiceBase,
        FlextPluginSettings,
        FlextPluginTypes,
        FlextPluginUtilities,
        FlextPluginVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        config,
        main,
        plugin,
        settings,
    )
    from tests.base import TestsFlextPluginServiceBase, s
    from tests.constants import TestsFlextPluginConstants, c
    from tests.models import TestsFlextPluginModels, m
    from tests.protocols import TestsFlextPluginProtocols, p
    from tests.settings import TestsFlextPluginSettings
    from tests.typings import TestsFlextPluginTypes, t
    from tests.utilities import TestsFlextPluginUtilities, u


__all__: tuple[str, ...] = (
    "ExamplesFlextPluginConstants",
    "ExamplesFlextPluginModels",
    "ExamplesFlextPluginProtocols",
    "ExamplesFlextPluginTypes",
    "ExamplesFlextPluginUtilities",
    "FlextPluginApi",
    "FlextPluginCli",
    "FlextPluginConfig",
    "FlextPluginConstants",
    "FlextPluginDiscovery",
    "FlextPluginModels",
    "FlextPluginModelsConfig",
    "FlextPluginPlatform",
    "FlextPluginProtocols",
    "FlextPluginServiceBase",
    "FlextPluginSettings",
    "FlextPluginTypes",
    "FlextPluginUtilities",
    "FlextPluginVersion",
    "TestsFlextPluginConstants",
    "TestsFlextPluginModels",
    "TestsFlextPluginProtocols",
    "TestsFlextPluginServiceBase",
    "TestsFlextPluginSettings",
    "TestsFlextPluginTypes",
    "TestsFlextPluginUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "api",
    "c",
    "config",
    "d",
    "e",
    "h",
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
    {
        "ExamplesFlextPluginConstants": "examples",
        "ExamplesFlextPluginModels": "examples",
        "ExamplesFlextPluginProtocols": "examples",
        "ExamplesFlextPluginTypes": "examples",
        "ExamplesFlextPluginUtilities": "examples",
        "FlextPluginApi": "flext_plugin",
        "FlextPluginCli": "flext_plugin",
        "FlextPluginConfig": "flext_plugin",
        "FlextPluginConstants": "flext_plugin",
        "FlextPluginDiscovery": "flext_plugin",
        "FlextPluginModels": "flext_plugin",
        "FlextPluginModelsConfig": "flext_plugin",
        "FlextPluginPlatform": "flext_plugin",
        "FlextPluginProtocols": "flext_plugin",
        "FlextPluginServiceBase": "flext_plugin",
        "FlextPluginSettings": "flext_plugin",
        "FlextPluginTypes": "flext_plugin",
        "FlextPluginUtilities": "flext_plugin",
        "FlextPluginVersion": "flext_plugin",
        "TestsFlextPluginConstants": ".constants",
        "TestsFlextPluginModels": ".models",
        "TestsFlextPluginProtocols": ".protocols",
        "TestsFlextPluginServiceBase": ".base",
        "TestsFlextPluginSettings": ".settings",
        "TestsFlextPluginTypes": ".typings",
        "TestsFlextPluginUtilities": ".utilities",
        "__author__": "flext_plugin",
        "__author_email__": "flext_plugin",
        "__description__": "flext_plugin",
        "__license__": "flext_plugin",
        "__title__": "flext_plugin",
        "__url__": "flext_plugin",
        "__version__": "flext_plugin",
        "__version_info__": "flext_plugin",
        "api": "flext_tests",
        "c": ".constants",
        "config": "flext_plugin",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "m": ".models",
        "main": "flext_plugin",
        "p": ".protocols",
        "plugin": "flext_plugin",
        "r": "flext_tests",
        "s": ".base",
        "settings": "flext_plugin",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    },
    public_exports=__all__,
)
