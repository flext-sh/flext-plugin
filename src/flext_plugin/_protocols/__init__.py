# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin._protocols.base import FlextPluginProtocolsBase
    from flext_plugin._protocols.platform import FlextPluginProtocolsPlatform
    from flext_plugin._protocols.plugin import FlextPluginProtocolsPlugin


__all__: tuple[str, ...] = (
    "FlextPluginProtocolsBase",
    "FlextPluginProtocolsPlatform",
    "FlextPluginProtocolsPlugin",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextPluginProtocolsBase": ".base",
        "FlextPluginProtocolsPlatform": ".platform",
        "FlextPluginProtocolsPlugin": ".plugin",
    }),
    public_exports=__all__,
)
