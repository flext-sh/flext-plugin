# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin.services package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin.services.discovery import FlextPluginDiscovery


__all__: tuple[str, ...] = ("FlextPluginDiscovery",)

install_lazy_exports(
    __name__,
    globals(),
    {"FlextPluginDiscovery": ".discovery"},
    public_exports=__all__,
)
