"""Plugin event typings for flext-plugin.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from flext_cli import FlextCliTypes


class FlextPluginTypingsEvents:
    """Plugin event type aliases composed into ``t.Plugin``."""

    type EventHandler = Callable[
        [FlextCliTypes.JsonMapping],
        Awaitable[FlextCliTypes.JsonMapping],
    ]


__all__: list[str] = ["FlextPluginTypingsEvents"]
