# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

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

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextPluginConstantsApi": ".api",
        "FlextPluginConstantsBase": ".base",
        "FlextPluginConstantsConfig": ".config",
        "FlextPluginConstantsPlugin": ".plugin",
    },
    public_exports=__all__,
    deferred_members={
        "FlextPluginConstantsPlugin": (
            "DEFAULT_PLUGIN_VERSION",
            "REGISTRY_CATEGORY",
            "Type",
            "SINGER_PLUGIN_TYPES",
            "ARCHITECTURE_PLUGIN_TYPES",
            "INTEGRATION_PLUGIN_TYPES",
            "UTILITY_PLUGIN_TYPES",
            "ALL_PLUGIN_TYPES",
            "PluginValidation",
            "PluginStatus",
            "DiscoveryTypeLiteral",
            "DiscoveryMethodLiteral",
        ),
    },
)
