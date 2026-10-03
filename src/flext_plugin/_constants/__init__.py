# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin._constants.api import FlextPluginConstantsApi
    from flext_plugin._constants.base import FlextPluginConstantsBase
    from flext_plugin._constants.config import FlextPluginConstantsConfig
    from flext_plugin._constants.plugin import FlextPluginConstantsPlugin


__all__: tuple[str, ...] = (
    "FlextPluginConstantsApi",
    "FlextPluginConstantsBase",
    "FlextPluginConstantsConfig",
    "FlextPluginConstantsPlugin",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".api": ("FlextPluginConstantsApi",),
            ".base": ("FlextPluginConstantsBase",),
            ".config": ("FlextPluginConstantsConfig",),
            ".plugin": ("FlextPluginConstantsPlugin",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
