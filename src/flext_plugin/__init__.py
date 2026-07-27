# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_plugin.__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, s, x

    from ._config import FlextPluginConfig, config
    from ._settings import FlextPluginSettings, settings
    from ._utilities.discovery import FlextPluginDiscovery
    from ._utilities.plugin_platform import FlextPluginPlatform
    from .api import FlextPluginApi, plugin
    from .constants import FlextPluginConstants, FlextPluginConstants as c
    from .models import FlextPluginModels, FlextPluginModels as m
    from .protocols import FlextPluginProtocols, FlextPluginProtocols as p
    from .typings import FlextPluginTypes, FlextPluginTypes as t
    from .utilities import FlextPluginUtilities, FlextPluginUtilities as u

    _ = (
        c,
        FlextPluginConstants,
        t,
        FlextPluginTypes,
        p,
        FlextPluginProtocols,
        m,
        FlextPluginModels,
        u,
        FlextPluginUtilities,
        d,
        e,
        h,
        r,
        s,
        x,
        FlextPluginConfig,
        config,
        FlextPluginSettings,
        settings,
        FlextPluginDiscovery,
        FlextPluginPlatform,
        FlextPluginApi,
        plugin,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextPluginConfig", "config"),
    "._settings": ("FlextPluginSettings", "settings"),
    "._utilities.discovery": ("FlextPluginDiscovery",),
    "._utilities.plugin_platform": ("FlextPluginPlatform",),
    ".api": ("FlextPluginApi", "plugin"),
    ".constants": ("FlextPluginConstants", "c"),
    ".models": ("FlextPluginModels", "m"),
    ".protocols": ("FlextPluginProtocols", "p"),
    ".typings": ("FlextPluginTypes", "t"),
    ".utilities": ("FlextPluginUtilities", "u"),
    "flext_cli": ("d", "e", "h", "r", "s", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_DIRECT_IMPORTS: tuple[str, ...] = (
    "FlextPluginApi",
    "FlextPluginConfig",
    "FlextPluginConstants",
    "FlextPluginDiscovery",
    "FlextPluginModels",
    "FlextPluginPlatform",
    "FlextPluginProtocols",
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
    "build_lazy_import_map",
    "c",
    "config",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "m",
    "p",
    "plugin",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)

__all__: tuple[str, ...] = (
    "FlextPluginApi",
    "FlextPluginConstants",
    "FlextPluginModels",
    "FlextPluginProtocols",
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
    "d",
    "e",
    "h",
    "m",
    "p",
    "plugin",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
