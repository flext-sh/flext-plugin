# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Plugin Types - public facade re-exporting from _typings.

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

from flext_cli import t as flext_cli_t

from flext_plugin._typings import FlextPluginTypingsBase, FlextPluginTypingsEvents


class FlextPluginTypes(flext_cli_t, FlextPluginTypingsBase):
    """Plugin type system extending flext_cli via MRO with internal typings."""

    class Plugin(FlextPluginTypingsBase, FlextPluginTypingsEvents):
        """Plugin domain namespace (flat members per AGENTS.md)."""


t = FlextPluginTypes
__all__: list[str] = ["FlextPluginTypes", "t"]
