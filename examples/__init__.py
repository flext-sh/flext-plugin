# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_core import d, e, h, r, x
    from flext_plugin import FlextPluginConstants, s

    from .constants import (
        ExamplesFlextPluginConstants,
        ExamplesFlextPluginConstants as c,
    )
    from .models import ExamplesFlextPluginModels, ExamplesFlextPluginModels as m
    from .protocols import (
        ExamplesFlextPluginProtocols,
        ExamplesFlextPluginProtocols as p,
    )
    from .typings import ExamplesFlextPluginTypes, ExamplesFlextPluginTypes as t
    from .utilities import (
        ExamplesFlextPluginUtilities,
        ExamplesFlextPluginUtilities as u,
    )
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
            ".constants": ("ExamplesFlextPluginConstants", "c"),
            ".models": ("ExamplesFlextPluginModels", "m"),
            ".protocols": ("ExamplesFlextPluginProtocols", "p"),
            ".typings": ("ExamplesFlextPluginTypes", "t"),
            ".utilities": ("ExamplesFlextPluginUtilities", "u"),
            "flext_core": ("d", "e", "h", "r", "x"),
            "flext_plugin": ("FlextPluginConstants", "s"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
