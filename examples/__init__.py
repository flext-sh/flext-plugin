# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_core.service import s
    from flext_plugin.constants import c
    from flext_plugin.models import m
    from flext_plugin.protocols import p
    from flext_plugin.typings import t
    from flext_plugin.utilities import u
_LAZY_IMPORTS = build_lazy_import_map(
    {
        "flext_core.decorators": ("d",),
        "flext_core.exceptions": ("e",),
        "flext_core.handlers": ("h",),
        "flext_core.mixins": ("x",),
        "flext_core.result": ("r",),
        "flext_core.service": ("s",),
        "flext_plugin.constants": ("c",),
        "flext_plugin.models": ("m",),
        "flext_plugin.protocols": ("p",),
        "flext_plugin.typings": ("t",),
        "flext_plugin.utilities": ("u",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
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
]
