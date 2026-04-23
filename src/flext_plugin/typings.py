"""FLEXT Plugin Types - type system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Awaitable,
    Callable,
    Mapping,
)
from typing import ClassVar

from flext_cli import m, t as cli_t
from pydantic import TypeAdapter


class FlextPluginTypes(cli_t):
    """Plugin type system with Python 3.13+ patterns.

    Follows FLEXT ecosystem namespace conventions:
    - t.Plugin.* for plugin-specific types
    - Canonical container contracts inherited from core `t.*`
    """

    CONTAINER_MAPPING_ADAPTER: ClassVar[TypeAdapter[cli_t.JsonMapping]] = m.TypeAdapter(
        cli_t.JsonMapping
    )
    CONTAINER_VALUE_MAPPING_ADAPTER: ClassVar[TypeAdapter[cli_t.JsonMapping]] = (
        m.TypeAdapter(cli_t.JsonMapping)
    )

    class Plugin:
        """Core collection and plugin type aliases."""

        type StringList = cli_t.StrSequence
        type StringSet = set[str]
        type StringDict = cli_t.StrMapping
        type FloatDict = Mapping[str, float]
        type PluginList = cli_t.JsonList
        type PluginDict = cli_t.JsonMapping
        type ConfigDict = cli_t.JsonMapping
        type MetadataDict = cli_t.JsonMapping
        type InputDict = cli_t.JsonMapping
        type OutputDict = cli_t.JsonMapping
        type PluginEntity = cli_t.JsonMapping

        type EventHandler = Callable[
            [cli_t.JsonMapping],
            Awaitable[cli_t.JsonMapping],
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
