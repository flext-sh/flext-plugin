# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli
    from pydantic_core import from_json, to_json, to_jsonable_python

    from flext_core import (
        core,
        d,
        e,
        h,
        lazy,
        lazy_attribute,
        normalize_lazy_imports,
        r,
        x,
    )
    from flext_plugin import c, config, m, p, plugin, s, settings, t, u

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
    "c",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "from_json",
    "h",
    "lazy",
    "lazy_attribute",
    "m",
    "normalize_lazy_imports",
    "p",
    "plugin",
    "r",
    "s",
    "settings",
    "t",
    "to_json",
    "to_jsonable_python",
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
            "flext_cli": ("cli",),
            "flext_core": (
                "core",
                "d",
                "e",
                "h",
                "lazy",
                "lazy_attribute",
                "normalize_lazy_imports",
                "r",
                "x",
            ),
            "flext_plugin": (
                "c",
                "config",
                "m",
                "p",
                "plugin",
                "s",
                "settings",
                "t",
                "u",
            ),
            "pydantic_core": ("from_json", "to_json", "to_jsonable_python"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
