"""Type aliases for flextplugin.

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

# Why: FlextPluginTypes is owned by flext_plugin, not flext_core (pyrefly).
from flext_plugin import FlextPluginTypes


class ExamplesFlextPluginTypes(FlextPluginTypes):
    """Type aliases for flextplugin."""


__all__: list[str] = ["ExamplesFlextPluginTypes"]
