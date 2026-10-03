"""FLEXT Plugin Types - public facade re-exporting from _typings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from flext_cli import FlextCliTypes

from flext_plugin._typings import FlextPluginTypingsBase


class FlextPluginTypes(FlextCliTypes, FlextPluginTypingsBase):
    """Plugin type system extending flext_cli via MRO with internal typings."""

    class Plugin:
        """Plugin domain namespace (flat members per AGENTS.md)."""

        type EventHandler = Callable[
            [FlextCliTypes.JsonMapping],
            Awaitable[FlextCliTypes.JsonMapping],
        ]


t = FlextPluginTypes

__all__: list[str] = ["FlextPluginTypes", "t"]
