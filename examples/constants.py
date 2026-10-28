"""Constants for flextplugin.

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

# Why: FlextPluginConstants is owned by flext_plugin, not flext_core (pyrefly).
from flext_plugin import FlextPluginConstants


class ExamplesFlextPluginConstants(FlextPluginConstants):
    """Constants for flextplugin."""


__all__: list[str] = ["ExamplesFlextPluginConstants"]
