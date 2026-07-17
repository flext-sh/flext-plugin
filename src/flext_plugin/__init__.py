# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
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
    from flext_cli import d, e, h, r, s, x

    from ._config import FlextPluginConfig, config
    from ._settings import FlextPluginSettings, settings
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
        FlextPluginSettings,
        settings,
        FlextPluginApi,
        plugin,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": (
        "FlextPluginConfig",
        "config",
    ),
    "._settings": (
        "FlextPluginSettings",
        "settings",
    ),
    ".api": (
        "FlextPluginApi",
        "plugin",
    ),
    ".constants": (
        "FlextPluginConstants",
        "c",
    ),
    ".models": (
        "FlextPluginModels",
        "m",
    ),
    ".protocols": (
        "FlextPluginProtocols",
        "p",
    ),
    ".typings": (
        "FlextPluginTypes",
        "t",
    ),
    ".utilities": (
        "FlextPluginUtilities",
        "u",
    ),
    "flext_cli": (
        "d",
        "e",
        "h",
        "r",
        "s",
        "x",
    ),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES,
    alias_groups=_LAZY_ALIAS_GROUPS,
    sort_keys=False,
)

_DIRECT_IMPORTS: tuple[str, ...] = (
    "FlextPluginApi",
    "FlextPluginConfig",
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
    "build_lazy_import_map",
    "c",
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
    "FlextPluginConfig",
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
    "config",
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
