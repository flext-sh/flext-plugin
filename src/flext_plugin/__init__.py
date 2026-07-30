# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from flext_cli import d as d
    from flext_cli import e as e
    from flext_cli import h as h
    from flext_cli import r as r
    from flext_cli import s as s
    from flext_cli import x as x

    from ._config import FlextPluginConfig, FlextPluginConfig as config
    from ._settings import FlextPluginSettings, FlextPluginSettings as settings
    from ._utilities.discovery import FlextPluginDiscovery
    from ._utilities.plugin_platform import FlextPluginPlatform
    from .api import FlextPluginApi, FlextPluginApi as plugin
    from .constants import FlextPluginConstants, FlextPluginConstants as c
    from .models import FlextPluginModels, FlextPluginModels as m
    from .protocols import FlextPluginProtocols, FlextPluginProtocols as p
    from .typings import FlextPluginTypes, FlextPluginTypes as t
    from .utilities import FlextPluginUtilities, FlextPluginUtilities as u

    _ = (
        c,
        FlextPluginConstants,
        config,
        FlextPluginConfig,
        settings,
        FlextPluginSettings,
        FlextPluginApi,
        plugin,
        m,
        FlextPluginModels,
        p,
        FlextPluginProtocols,
        t,
        FlextPluginTypes,
        u,
        FlextPluginUtilities,
        FlextPluginDiscovery,
        FlextPluginPlatform,
        d,
        e,
        h,
        r,
        s,
        x,
    )

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextPluginConfig", "config"),
    "._settings": ("FlextPluginSettings", "settings"),
    ".api": ("FlextPluginApi", "plugin"),
    ".constants": ("FlextPluginConstants", "c"),
    ".models": ("FlextPluginModels", "m"),
    ".protocols": ("FlextPluginProtocols", "p"),
    ".typings": ("FlextPluginTypes", "t"),
    "._utilities.discovery": ("FlextPluginDiscovery",),
    "._utilities.plugin_platform": ("FlextPluginPlatform",),
    ".utilities": ("FlextPluginUtilities", "u"),
    "flext_cli": ("d", "e", "h", "r", "s", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
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

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
