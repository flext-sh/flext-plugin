# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin._models.base import FlextPluginModelsBase
    from flext_plugin._models.config import FlextPluginConfigModels
    from flext_plugin._models.plugin import FlextPluginModelsPlugin


__all__: tuple[str, ...] = (
    "FlextPluginConfigModels",
    "FlextPluginModelsBase",
    "FlextPluginModelsPlugin",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextPluginConfigModels": ".config",
        "FlextPluginModelsBase": ".base",
        "FlextPluginModelsPlugin": ".plugin",
    }),
    public_exports=__all__,
)
