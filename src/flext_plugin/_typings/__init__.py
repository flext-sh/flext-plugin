# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Typings package.

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
    from flext_plugin._typings.base import FlextPluginTypingsBase
    from flext_plugin._typings.events import FlextPluginTypingsEvents


__all__: tuple[str, ...] = ("FlextPluginTypingsBase", "FlextPluginTypingsEvents")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextPluginTypingsBase": ".base",
        "FlextPluginTypingsEvents": ".events",
    }),
    public_exports=__all__,
)
