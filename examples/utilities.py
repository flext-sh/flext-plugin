"""Example utilities for flext-plugin.

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

from flext_plugin import FlextPluginUtilities


class ExamplesFlextPluginUtilities(FlextPluginUtilities):
    """Examples utilities facade extending flext-plugin utilities."""


u = ExamplesFlextPluginUtilities

__all__: list[str] = ["ExamplesFlextPluginUtilities", "u"]
