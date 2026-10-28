# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Utilities package.

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
    from flext_plugin._utilities.base import FlextPluginUtilitiesBase
    from flext_plugin._utilities.discovery import FlextPluginDiscovery
    from flext_plugin._utilities.implementations import FlextPluginImplementations
    from flext_plugin._utilities.metadata import FlextPluginUtilitiesMetadata
    from flext_plugin._utilities.plugin_platform import FlextPluginPlatform


__all__: tuple[str, ...] = (
    "FlextPluginDiscovery",
    "FlextPluginImplementations",
    "FlextPluginPlatform",
    "FlextPluginUtilitiesBase",
    "FlextPluginUtilitiesMetadata",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextPluginDiscovery": ".discovery",
        "FlextPluginImplementations": ".implementations",
        "FlextPluginPlatform": ".plugin_platform",
        "FlextPluginUtilitiesBase": ".base",
        "FlextPluginUtilitiesMetadata": ".metadata",
    }),
    public_exports=__all__,
)
