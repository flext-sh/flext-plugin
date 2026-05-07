"""FLEXT Plugin Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Awaitable,
    Callable,
)

from flext_cli import t as cli_t


class FlextPluginTypes(cli_t):
    """Plugin type system extending flext_cli via MRO."""

    class Plugin:
        """Plugin domain namespace (flat members per AGENTS.md §149)."""

        type EventHandler = Callable[
            [cli_t.JsonMapping],
            Awaitable[cli_t.JsonMapping],
        ]


t = FlextPluginTypes

__all__: list[str] = ["FlextPluginTypes", "t"]
