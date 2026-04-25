"""FLEXT Plugin Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Awaitable,
    Callable,
)
from typing import ClassVar

from flext_cli import m, t


class FlextPluginTypes(t):
    """Plugin type system extending flext_cli via MRO."""

    CONTAINER_MAPPING_ADAPTER: ClassVar[m.TypeAdapter[t.JsonMapping]] = m.TypeAdapter(
        t.JsonMapping,
    )
    CONTAINER_VALUE_MAPPING_ADAPTER: ClassVar[m.TypeAdapter[t.JsonMapping]] = (
        m.TypeAdapter(t.JsonMapping)
    )

    class Plugin:
        """Plugin domain namespace (flat members per AGENTS.md §149)."""

        type EventHandler = Callable[
            [t.JsonMapping],
            Awaitable[t.JsonMapping],
        ]

        class HandlerInfo:
            """Handler metadata container."""

            handler: FlextPluginTypes.Plugin.EventHandler
            priority: int

            def __init__(
                self,
                handler: FlextPluginTypes.Plugin.EventHandler,
                priority: int = 0,
            ) -> None:
                """Initialize handler info."""
                self.handler = handler
                self.priority = priority


t: type[FlextPluginTypes] = FlextPluginTypes

__all__: list[str] = ["FlextPluginTypes", "t"]
