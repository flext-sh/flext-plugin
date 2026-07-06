# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin package."""

from __future__ import annotations

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
from flext_plugin._exports import FLEXT_PLUGIN_LAZY_IMPORTS

if TYPE_CHECKING:
    from flext_core._root_typing_parts.facades import (
        d as d,
        e as e,
        h as h,
        r as r,
        s as s,
        x as x,
    )
    from flext_plugin.api import FlextPluginApi as FlextPluginApi, plugin as plugin
    from flext_plugin.constants import (
        FlextPluginConstants as FlextPluginConstants,
        c as c,
    )
    from flext_plugin.models import FlextPluginModels as FlextPluginModels, m as m
    from flext_plugin.protocols import (
        FlextPluginProtocols as FlextPluginProtocols,
        p as p,
    )
    from flext_plugin.settings import FlextPluginSettings as FlextPluginSettings
    from flext_plugin.typings import FlextPluginTypes as FlextPluginTypes, t as t
    from flext_plugin.utilities import (
        FlextPluginUtilities as FlextPluginUtilities,
        u as u,
    )


_LAZY_IMPORTS = FLEXT_PLUGIN_LAZY_IMPORTS


_EAGER_EXPORTS = (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)


_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextPluginApi",
    "FlextPluginConstants",
    "FlextPluginModels",
    "FlextPluginProtocols",
    "FlextPluginSettings",
    "FlextPluginTypes",
    "FlextPluginUtilities",
    "plugin",
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
    "r",
    "s",
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
    "t",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=_PUBLIC_EXPORTS,
)
