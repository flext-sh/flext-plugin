# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext plugin package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

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
    from flext_core import *

    from flext_plugin import (
        api,
        constants,
        models,
        protocols,
        settings,
        typings,
        utilities,
    )
    from flext_plugin._utilities import *
    from flext_plugin.api import *
    from flext_plugin.constants import *
    from flext_plugin.models import *
    from flext_plugin.protocols import *
    from flext_plugin.settings import *
    from flext_plugin.typings import *
    from flext_plugin.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextPluginAdapters": "flext_plugin._utilities.adapters",
    "FlextPluginApi": "flext_plugin.api",
    "FlextPluginConstants": "flext_plugin.constants",
    "FlextPluginDiscovery": "flext_plugin._utilities.discovery",
    "FlextPluginEntities": "flext_plugin._utilities.entities",
    "FlextPluginHandlers": "flext_plugin._utilities.handlers",
    "FlextPluginHotReload": "flext_plugin._utilities.hot_reload",
    "FlextPluginImplementations": "flext_plugin._utilities.implementations",
    "FlextPluginLoader": "flext_plugin._utilities.loader",
    "FlextPluginModels": "flext_plugin.models",
    "FlextPluginPlatform": "flext_plugin._utilities.plugin_platform",
    "FlextPluginProtocols": "flext_plugin.protocols",
    "FlextPluginService": "flext_plugin._utilities.services",
    "FlextPluginSettings": "flext_plugin.settings",
    "FlextPluginTypes": "flext_plugin.typings",
    "FlextPluginUtilities": "flext_plugin.utilities",
    "_utilities": "flext_plugin._utilities",
    "adapters": "flext_plugin._utilities.adapters",
    "api": "flext_plugin.api",
    "c": ["flext_plugin.constants", "FlextPluginConstants"],
    "constants": "flext_plugin.constants",
    "d": "flext_core",
    "discovery": "flext_plugin._utilities.discovery",
    "e": "flext_core",
    "entities": "flext_plugin._utilities.entities",
    "h": "flext_core",
    "handlers": "flext_plugin._utilities.handlers",
    "hot_reload": "flext_plugin._utilities.hot_reload",
    "implementations": "flext_plugin._utilities.implementations",
    "loader": "flext_plugin._utilities.loader",
    "m": ["flext_plugin.models", "FlextPluginModels"],
    "models": "flext_plugin.models",
    "p": ["flext_plugin.protocols", "FlextPluginProtocols"],
    "plugin_platform": "flext_plugin._utilities.plugin_platform",
    "protocols": "flext_plugin.protocols",
    "r": "flext_core",
    "s": "flext_core",
    "services": "flext_plugin._utilities.services",
    "settings": "flext_plugin.settings",
    "t": ["flext_plugin.typings", "FlextPluginTypes"],
    "typings": "flext_plugin.typings",
    "u": ["flext_plugin.utilities", "FlextPluginUtilities"],
    "utilities": "flext_plugin.utilities",
    "x": "flext_core",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
