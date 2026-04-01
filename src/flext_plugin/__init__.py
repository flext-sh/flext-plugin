# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext plugin package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

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

if _TYPE_CHECKING:
    from flext_core import FlextTypes, d, e, h, r, s, x

    from flext_plugin import (
        _utilities,
        api,
        constants,
        models,
        protocols,
        settings,
        typings,
        utilities,
    )
    from flext_plugin._utilities import (
        FlextPluginAdapters,
        FlextPluginDiscovery,
        FlextPluginEntities,
        FlextPluginHandlers,
        FlextPluginHotReload,
        FlextPluginImplementations,
        FlextPluginLoader,
        FlextPluginPlatform,
        FlextPluginService,
        adapters,
        discovery,
        entities,
        handlers,
        hot_reload,
        implementations,
        loader,
        plugin_platform,
        services,
    )
    from flext_plugin.api import FlextPluginApi
    from flext_plugin.constants import FlextPluginConstants, FlextPluginConstants as c
    from flext_plugin.models import FlextPluginModels, FlextPluginModels as m
    from flext_plugin.protocols import FlextPluginProtocols, FlextPluginProtocols as p
    from flext_plugin.settings import FlextPluginSettings
    from flext_plugin.typings import FlextPluginTypes, FlextPluginTypes as t
    from flext_plugin.utilities import FlextPluginUtilities, FlextPluginUtilities as u

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    ("flext_plugin._utilities",),
    {
        "FlextPluginApi": "flext_plugin.api",
        "FlextPluginConstants": "flext_plugin.constants",
        "FlextPluginModels": "flext_plugin.models",
        "FlextPluginProtocols": "flext_plugin.protocols",
        "FlextPluginSettings": "flext_plugin.settings",
        "FlextPluginTypes": "flext_plugin.typings",
        "FlextPluginUtilities": "flext_plugin.utilities",
        "_utilities": "flext_plugin._utilities",
        "api": "flext_plugin.api",
        "c": ("flext_plugin.constants", "FlextPluginConstants"),
        "constants": "flext_plugin.constants",
        "d": "flext_core",
        "e": "flext_core",
        "h": "flext_core",
        "m": ("flext_plugin.models", "FlextPluginModels"),
        "models": "flext_plugin.models",
        "p": ("flext_plugin.protocols", "FlextPluginProtocols"),
        "protocols": "flext_plugin.protocols",
        "r": "flext_core",
        "s": "flext_core",
        "settings": "flext_plugin.settings",
        "t": ("flext_plugin.typings", "FlextPluginTypes"),
        "typings": "flext_plugin.typings",
        "u": ("flext_plugin.utilities", "FlextPluginUtilities"),
        "utilities": "flext_plugin.utilities",
        "x": "flext_core",
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)
