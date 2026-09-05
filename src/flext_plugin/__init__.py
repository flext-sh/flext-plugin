# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
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
    from enum import StrEnum, unique
    from typing import TYPE_CHECKING, ClassVar, Final

    from flext_cli import d, e, h, r, s, x

    from ._config import FlextPluginConfig, config
    from ._settings import FlextPluginSettings, settings
    from .api import FlextPluginApi, plugin
    from .constants import FlextPluginConstants, FlextPluginConstants as c
    from .models import FlextPluginModels, FlextPluginModels as m
    from .protocols import FlextPluginProtocols, FlextPluginProtocols as p
    from .typings import FlextPluginTypes, FlextPluginTypes as t
    from .utilities import (
        FlextPluginDiscovery,
        FlextPluginUtilities,
        FlextPluginUtilities as u,
    )
__all__: tuple[str, ...] = (
    "TYPE_CHECKING",
    "ClassVar",
    "Final",
    "FlextPluginApi",
    "FlextPluginConfig",
    "FlextPluginConstants",
    "FlextPluginDiscovery",
    "FlextPluginModels",
    "FlextPluginProtocols",
    "FlextPluginSettings",
    "FlextPluginTypes",
    "FlextPluginUtilities",
    "StrEnum",
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
    "unique",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextPluginConfig", "config"),
            "._settings": ("FlextPluginSettings", "settings"),
            ".api": ("FlextPluginApi", "plugin"),
            ".constants": ("FlextPluginConstants", "c"),
            ".models": ("FlextPluginModels", "m"),
            ".protocols": ("FlextPluginProtocols", "p"),
            ".typings": ("FlextPluginTypes", "t"),
            ".utilities": ("FlextPluginDiscovery", "FlextPluginUtilities", "u"),
            "enum": ("StrEnum", "unique"),
            "flext_cli": ("d", "e", "h", "r", "s", "x"),
            "typing": ("ClassVar", "Final", "TYPE_CHECKING"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
