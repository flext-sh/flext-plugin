# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin._protocols.base import FlextPluginProtocolsBase
    from flext_plugin._protocols.platform import FlextPluginProtocolsPlatformService
    from flext_plugin._protocols.plugin import FlextPluginProtocolsPlugin


__all__: tuple[str, ...] = (
    "FlextPluginProtocolsBase",
    "FlextPluginProtocolsPlatformService",
    "FlextPluginProtocolsPlugin",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextPluginProtocolsBase": ".base",
        "FlextPluginProtocolsPlatformService": ".platform",
        "FlextPluginProtocolsPlugin": ".plugin",
    }),
    public_exports=__all__,
)
