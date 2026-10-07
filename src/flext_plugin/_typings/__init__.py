# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin._typings.base import FlextPluginTypingsBase


__all__: tuple[str, ...] = ("FlextPluginTypingsBase",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"FlextPluginTypingsBase": ".base"}),
    public_exports=__all__,
)
