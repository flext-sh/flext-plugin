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

from flext_cli import m, t

from flext_plugin import c


class FlextPluginTypes(t):
    """Plugin type system with Python 3.13+ patterns.

    Follows FLEXT ecosystem namespace conventions:
    - t.Plugin.* for plugin-specific types
    - Canonical container contracts inherited from core `t.*`
    """

    CONTAINER_MAPPING_ADAPTER: m.TypeAdapter[t.JsonMapping] = m.TypeAdapter(
        t.JsonMapping
    )
    CONTAINER_VALUE_MAPPING_ADAPTER: m.TypeAdapter[t.JsonMapping] = m.TypeAdapter(
        t.JsonMapping
    )

    class Plugin:
        """Core collection and plugin type aliases."""

        type StringList = t.StrSequence
        type StringSet = set[str]
        type StringDict = t.StrMapping
        type FloatDict = Mapping[str, float]
        type PluginList = t.JsonList
        type PluginDict = t.JsonValue
        type ConfigDict = t.JsonValue
        type MetadataDict = t.JsonValue
        type InputDict = t.JsonValue
        type OutputDict = t.JsonValue
        type PluginEntity = t.JsonValue
        DiscoveryTypeLiteral = c.Plugin.DiscoveryTypeLiteral
        DiscoveryMethodLiteral = c.Plugin.DiscoveryMethodLiteral
        LoadTypeLiteral = c.Plugin.LoadTypeLiteral

        class Handlers:
            """Event handler type definitions."""

            type EventHandler = Callable[
                [t.JsonMapping],
                Awaitable[t.JsonMapping],
            ]

            class HandlerInfo:
                """Handler metadata container."""

                def __init__(
                    self,
                    handler: Callable[
                        [t.JsonMapping],
                        Awaitable[t.JsonMapping],
                    ],
                    priority: int = 0,
                ) -> None:
                    """Initialize handler info."""
                    self.handler = handler
                    self.priority = priority

        class Lifecycle:
            """Plugin lifecycle and status type aliases."""

            type PluginStatus = str
            type PluginType = str
            type LifecycleState = str
            type ExecutionStatus = str

        class Security:
            """Security-related type aliases."""

            type SecurityLevel = str
            type Permission = str
            type SecurityConfig = t.JsonValue
            SecurityLevelLiteral = c.Plugin.SecurityLevelLiteral

        class Performance:
            """Performance metrics and monitoring type aliases."""

            type Metrics = t.JsonValue
            type PerformanceData = t.JsonValue
            type ResourceUsage = t.JsonValue

        class Discovery:
            """Plugin discovery type aliases."""

            type DiscoveryPath = str
            type DiscoveryResult = t.JsonValue
            type PluginLoader = t.GeneralValueType
            type EntryPoint = str

        class Execution:
            """Plugin execution type aliases."""

            type ExecutionContext = t.JsonValue
            type ExecutionResult = t.JsonValue
            type ExecutionError = str
            type ResourceLimits = t.JsonValue

        class Registry:
            """Plugin registry type aliases."""

            type RegistryConfig = t.JsonValue
            type RegistryEntry = t.JsonValue
            type RegistrySync = t.JsonValue

        class HotReload:
            """Hot reload and file watching type aliases."""

            type WatchConfig = t.JsonValue
            type ReloadEvent = t.JsonValue
            type FileWatcher = t.GeneralValueType


t = FlextPluginTypes
__all__: list[str] = ["FlextPluginTypes", "t"]
