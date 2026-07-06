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
    from flext_plugin.api import FlextPluginApi, plugin
    from flext_plugin.constants import FlextPluginConstants, c
    from flext_plugin.models import FlextPluginModels, m
    from flext_plugin.protocols import FlextPluginProtocols, p
    from flext_plugin.settings import FlextPluginSettings
    from flext_plugin.typings import FlextPluginTypes, t
    from flext_plugin.utilities import FlextPluginUtilities, u
_LAZY_IMPORTS = build_lazy_import_map(
    {
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
        ".settings": ("FlextPluginSettings",),
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
    },
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
