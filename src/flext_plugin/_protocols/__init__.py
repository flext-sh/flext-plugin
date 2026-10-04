# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin._protocols.base import FlextPluginProtocolsBase
    from flext_plugin._protocols.platform import FlextPluginProtocolsPlatformService
    from flext_plugin._protocols.plugin import FlextPluginProtocolsPlugin


__all__: tuple[str, ...] = (
    "FlextPluginProtocolsBase",
    "FlextPluginProtocolsPlatformService",
    "FlextPluginProtocolsPlugin",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("FlextPluginProtocolsBase",),
            ".platform": ("FlextPluginProtocolsPlatformService",),
            ".plugin": ("FlextPluginProtocolsPlugin",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
