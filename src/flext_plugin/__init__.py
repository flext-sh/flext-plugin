# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

from flext_plugin.__version__ import *

if _t.TYPE_CHECKING:
    from flext_cli import d, e, h, r, s, x

    from flext_plugin._utilities.adapters import FlextPluginAdapters
    from flext_plugin._utilities.discovery import FlextPluginDiscovery
    from flext_plugin._utilities.entities import FlextPluginEntities
    from flext_plugin._utilities.handlers import FlextPluginHandlers
    from flext_plugin._utilities.hot_reload import FlextPluginHotReload
    from flext_plugin._utilities.implementations import FlextPluginImplementations
    from flext_plugin._utilities.loader import FlextPluginLoader
    from flext_plugin._utilities.plugin_platform import FlextPluginPlatform
    from flext_plugin._utilities.services import FlextPluginService
    from flext_plugin.api import FlextPluginApi, plugin
    from flext_plugin.constants import FlextPluginConstants, c
    from flext_plugin.models import FlextPluginModels, m
    from flext_plugin.protocols import FlextPluginProtocols, p
    from flext_plugin.settings import FlextPluginSettings
    from flext_plugin.typings import FlextPluginTypes, t
    from flext_plugin.utilities import FlextPluginUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    ("._utilities",),
    build_lazy_import_map(
        {
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
            "._utilities.adapters": ("FlextPluginAdapters",),
            "._utilities.discovery": ("FlextPluginDiscovery",),
            "._utilities.entities": ("FlextPluginEntities",),
            "._utilities.handlers": ("FlextPluginHandlers",),
            "._utilities.hot_reload": ("FlextPluginHotReload",),
            "._utilities.implementations": ("FlextPluginImplementations",),
            "._utilities.loader": ("FlextPluginLoader",),
            "._utilities.plugin_platform": ("FlextPluginPlatform",),
            "._utilities.services": ("FlextPluginService",),
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
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "FlextPluginAdapters",
    "FlextPluginApi",
    "FlextPluginConstants",
    "FlextPluginDiscovery",
    "FlextPluginEntities",
    "FlextPluginHandlers",
    "FlextPluginHotReload",
    "FlextPluginImplementations",
    "FlextPluginLoader",
    "FlextPluginModels",
    "FlextPluginPlatform",
    "FlextPluginProtocols",
    "FlextPluginService",
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
]
