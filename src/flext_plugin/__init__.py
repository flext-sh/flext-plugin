# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports
from flext_plugin.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, x

    from flext_plugin import services
    from flext_plugin._config import FlextPluginConfig, config
    from flext_plugin._settings import FlextPluginSettings, settings
    from flext_plugin.api import FlextPluginApi, plugin
    from flext_plugin.base import FlextPluginServiceBase, s
    from flext_plugin.cli import FlextPluginCli, main
    from flext_plugin.constants import FlextPluginConstants, c
    from flext_plugin.models import FlextPluginModels, m
    from flext_plugin.protocols import FlextPluginProtocols, p
    from flext_plugin.typings import FlextPluginTypes, t
    from flext_plugin.utilities import (
        FlextPluginDiscovery,
        FlextPluginPlatform,
        FlextPluginUtilities,
        u,
    )


__all__: tuple[str, ...] = (
    "FlextPluginApi",
    "FlextPluginCli",
    "FlextPluginConfig",
    "FlextPluginConstants",
    "FlextPluginDiscovery",
    "FlextPluginModels",
    "FlextPluginPlatform",
    "FlextPluginProtocols",
    "FlextPluginServiceBase",
    "FlextPluginSettings",
    "FlextPluginTypes",
    "FlextPluginUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
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
    "services",
    "settings",
    "t",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextPluginConfig", "config"),
            "._settings": ("FlextPluginSettings", "settings"),
            ".api": ("FlextPluginApi", "plugin"),
            ".base": ("FlextPluginServiceBase", "s"),
            ".cli": ("FlextPluginCli", "main"),
            ".constants": ("FlextPluginConstants", "c"),
            ".models": ("FlextPluginModels", "m"),
            ".protocols": ("FlextPluginProtocols", "p"),
            ".services": ("services",),
            ".typings": ("FlextPluginTypes", "t"),
            ".utilities": (
                "FlextPluginDiscovery",
                "FlextPluginPlatform",
                "FlextPluginUtilities",
                "u",
            ),
            "flext_cli": ("d", "e", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
