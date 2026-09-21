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
    from flext_cli import c as cli_c, d, e, h, r, x

    from . import services
    from .__version__ import FlextPluginVersion
    from ._config import FlextPluginConfig, config
    from ._settings import FlextPluginSettings, settings
    from .api import FlextPluginApi, plugin
    from .base import FlextPluginServiceBase, FlextPluginServiceBase as s
    from .cli import FlextPluginCli
    from .constants import FlextPluginConstants, FlextPluginConstants as c
    from .models import FlextPluginModels, FlextPluginModels as m
    from .protocols import FlextPluginProtocols, FlextPluginProtocols as p
    from .typings import FlextPluginTypes, FlextPluginTypes as t
    from .utilities import (
        FlextPluginDiscovery,
        FlextPluginPlatform,
        FlextPluginUtilities,
        FlextPluginUtilities as u,
    )
__all__: tuple[str, ...] = (
    "FlextPluginApi", "FlextPluginCli", "FlextPluginConfig", "FlextPluginConstants",
    "FlextPluginDiscovery", "FlextPluginModels", "FlextPluginPlatform", "FlextPluginProtocols",
    "FlextPluginServiceBase", "FlextPluginSettings", "FlextPluginTypes", "FlextPluginUtilities",
    "FlextPluginVersion", "__author__", "__author_email__", "__description__",
    "__license__", "__title__", "__url__", "__version__",
    "__version_info__", "c", "cli_c", "config",
    "d", "e", "h", "m",
    "p", "plugin", "r", "s",
    "services", "settings", "t", "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".__version__": ("FlextPluginVersion",),
            "._config": ("FlextPluginConfig", "config"),
            "._settings": ("FlextPluginSettings", "settings"),
            ".api": ("FlextPluginApi", "plugin"),
            ".base": ("FlextPluginServiceBase", "s"),
            ".cli": ("FlextPluginCli",),
            ".constants": ("FlextPluginConstants", "c"),
            ".models": ("FlextPluginModels", "m"),
            ".protocols": ("FlextPluginProtocols", "p"),
            ".services": ("services",),
            ".typings": ("FlextPluginTypes", "t"),
            ".utilities": (
                "FlextPluginDiscovery", "FlextPluginPlatform", "FlextPluginUtilities",
                "u",
            ),
            "flext_cli": ("d", "e", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({"flext_cli": (("cli_c", "c"),)}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
