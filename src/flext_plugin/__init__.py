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
    from flext_plugin._utilities.adapters import *
    from flext_plugin._utilities.discovery import *
    from flext_plugin._utilities.entities import *
    from flext_plugin._utilities.handlers import *
    from flext_plugin._utilities.hot_reload import *
    from flext_plugin._utilities.implementations import *
    from flext_plugin._utilities.loader import *
    from flext_plugin._utilities.plugin_platform import *
    from flext_plugin._utilities.services import *
    from flext_plugin.api import *
    from flext_plugin.constants import *
    from flext_plugin.models import *
    from flext_plugin.protocols import *
    from flext_plugin.settings import *
    from flext_plugin.typings import *
    from flext_plugin.utilities import *

from flext_plugin._utilities import _LAZY_IMPORTS as __UTILITIES_LAZY

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **__UTILITIES_LAZY,
    "FlextPluginApi": "flext_plugin.api",
    "FlextPluginConstants": "flext_plugin.constants",
    "FlextPluginModels": "flext_plugin.models",
    "FlextPluginProtocols": "flext_plugin.protocols",
    "FlextPluginSettings": "flext_plugin.settings",
    "FlextPluginTypes": "flext_plugin.typings",
    "FlextPluginUtilities": "flext_plugin.utilities",
    "_utilities": "flext_plugin._utilities",
    "api": "flext_plugin.api",
    "c": ["flext_plugin.constants", "FlextPluginConstants"],
    "constants": "flext_plugin.constants",
    "d": "flext_core",
    "e": "flext_core",
    "h": "flext_core",
    "m": ["flext_plugin.models", "FlextPluginModels"],
    "models": "flext_plugin.models",
    "p": ["flext_plugin.protocols", "FlextPluginProtocols"],
    "protocols": "flext_plugin.protocols",
    "r": "flext_core",
    "s": "flext_core",
    "settings": "flext_plugin.settings",
    "t": ["flext_plugin.typings", "FlextPluginTypes"],
    "typings": "flext_plugin.typings",
    "u": ["flext_plugin.utilities", "FlextPluginUtilities"],
    "utilities": "flext_plugin.utilities",
    "x": "flext_core",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
