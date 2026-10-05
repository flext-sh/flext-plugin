# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from examples.constants import ExamplesFlextPluginConstants
    from examples.models import ExamplesFlextPluginModels
    from examples.protocols import ExamplesFlextPluginProtocols
    from examples.typings import ExamplesFlextPluginTypes
    from examples.utilities import ExamplesFlextPluginUtilities
    from flext_plugin import c, d, e, h, m, p, r, s, t, u, x


__all__: tuple[str, ...] = (
    "ExamplesFlextPluginConstants",
    "ExamplesFlextPluginModels",
    "ExamplesFlextPluginProtocols",
    "ExamplesFlextPluginTypes",
    "ExamplesFlextPluginUtilities",
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

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "ExamplesFlextPluginConstants": ".constants",
        "ExamplesFlextPluginModels": ".models",
        "ExamplesFlextPluginProtocols": ".protocols",
        "ExamplesFlextPluginTypes": ".typings",
        "ExamplesFlextPluginUtilities": ".utilities",
        "c": "flext_plugin",
        "d": "flext_plugin",
        "e": "flext_plugin",
        "h": "flext_plugin",
        "m": "flext_plugin",
        "p": "flext_plugin",
        "r": "flext_plugin",
        "s": "flext_plugin",
        "t": "flext_plugin",
        "u": "flext_plugin",
        "x": "flext_plugin",
    }),
    public_exports=__all__,
)
