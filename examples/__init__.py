# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin import (
        FlextPluginConstants,
        FlextPluginConstants as c,
        d,
        e,
        h,
        m,
        p,
        r,
        s,
        t,
        u,
        x,
    )

    from .constants import ExamplesFlextPluginConstants
    from .models import ExamplesFlextPluginModels
    from .protocols import ExamplesFlextPluginProtocols
    from .typings import ExamplesFlextPluginTypes
    from .utilities import ExamplesFlextPluginUtilities
__all__: tuple[str, ...] = (
    "ExamplesFlextPluginConstants",
    "ExamplesFlextPluginModels",
    "ExamplesFlextPluginProtocols",
    "ExamplesFlextPluginTypes",
    "ExamplesFlextPluginUtilities",
    "FlextPluginConstants",
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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".constants": ("ExamplesFlextPluginConstants",),
            ".models": ("ExamplesFlextPluginModels",),
            ".protocols": ("ExamplesFlextPluginProtocols",),
            ".typings": ("ExamplesFlextPluginTypes",),
            ".utilities": ("ExamplesFlextPluginUtilities",),
            "flext_plugin": (
                "FlextPluginConstants",
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
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
