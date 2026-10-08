# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin._utilities.base import FlextPluginUtilitiesBase
    from flext_plugin._utilities.discovery import FlextPluginDiscovery
    from flext_plugin._utilities.implementations import FlextPluginImplementations
    from flext_plugin._utilities.plugin_platform import (
        FlextPluginUtilitiesPluginPlatform,
    )


__all__: tuple[str, ...] = (
    "FlextPluginDiscovery",
    "FlextPluginImplementations",
    "FlextPluginUtilitiesBase",
    "FlextPluginUtilitiesPluginPlatform",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextPluginDiscovery": ".discovery",
        "FlextPluginImplementations": ".implementations",
        "FlextPluginUtilitiesBase": ".base",
        "FlextPluginUtilitiesPluginPlatform": ".plugin_platform",
    }),
    public_exports=__all__,
)
