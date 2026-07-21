"""FLEXT Plugin Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from flext_cli import t


class FlextPluginTypes(t):
    """Plugin type system extending flext_cli via MRO."""

    class Plugin:
        """Plugin domain namespace (flat members per AGENTS.md §149)."""

        type EventHandler = Callable[
            [t.JsonMapping],
            Awaitable[t.JsonMapping],
        ]


t = FlextPluginTypes

__all__: list[str] = ["FlextPluginTypes", "t"]
