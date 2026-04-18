"""FLEXT Plugin Types - type system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping, Sequence

from flext_cli import m, t

from flext_plugin import c


class FlextPluginTypes(t):
    """Plugin type system with Python 3.13+ patterns.

    Follows FLEXT ecosystem namespace conventions:
    - t.Plugin.* for plugin-specific types
    - Canonical container contracts inherited from core `t.*`
    """

    CONTAINER_MAPPING_ADAPTER: m.TypeAdapter[t.ContainerMapping] = m.TypeAdapter(
        t.ContainerMapping
    )
    CONTAINER_VALUE_MAPPING_ADAPTER: m.TypeAdapter[t.ContainerValueMapping] = (
        m.TypeAdapter(t.ContainerValueMapping)
    )

    class Plugin:
        """Core collection and plugin type aliases."""

        type StringList = t.StrSequence
        type StringSet = set[str]
        type StringDict = t.StrMapping
        type FloatDict = Mapping[str, float]
        type PluginList = Sequence[t.GeneralValueMapping]
        type PluginDict = t.GeneralValueMapping
        type ConfigDict = t.GeneralValueMapping
        type MetadataDict = t.GeneralValueMapping
        type InputDict = t.GeneralValueMapping
        type OutputDict = t.GeneralValueMapping
        type PluginEntity = t.GeneralValueMapping
        DiscoveryTypeLiteral = c.Plugin.DiscoveryTypeLiteral
        DiscoveryMethodLiteral = c.Plugin.DiscoveryMethodLiteral
        LoadTypeLiteral = c.Plugin.LoadTypeLiteral

        class Handlers:
            """Event handler type definitions."""

            type EventHandler = Callable[
                [t.ContainerMapping],
                Awaitable[t.ContainerMapping],
            ]

            class HandlerInfo:
                """Handler metadata container."""

                def __init__(
                    self,
                    handler: Callable[
                        [t.ContainerMapping],
                        Awaitable[t.ContainerMapping],
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
            type SecurityConfig = t.GeneralValueMapping
            SecurityLevelLiteral = c.Plugin.SecurityLevelLiteral

        class Performance:
            """Performance metrics and monitoring type aliases."""

            type Metrics = t.GeneralValueMapping
            type PerformanceData = t.GeneralValueMapping
            type ResourceUsage = t.GeneralValueMapping

        class Discovery:
            """Plugin discovery type aliases."""

            type DiscoveryPath = str
            type DiscoveryResult = t.GeneralValueMapping
            type PluginLoader = t.GeneralValueType
            type EntryPoint = str

        class Execution:
            """Plugin execution type aliases."""

            type ExecutionContext = t.GeneralValueMapping
            type ExecutionResult = t.GeneralValueMapping
            type ExecutionError = str
            type ResourceLimits = t.GeneralValueMapping

        class Registry:
            """Plugin registry type aliases."""

            type RegistryConfig = t.GeneralValueMapping
            type RegistryEntry = t.GeneralValueMapping
            type RegistrySync = t.GeneralValueMapping

        class HotReload:
            """Hot reload and file watching type aliases."""

            type WatchConfig = t.GeneralValueMapping
            type ReloadEvent = t.GeneralValueMapping
            type FileWatcher = t.GeneralValueType


t = FlextPluginTypes
__all__: list[str] = ["FlextPluginTypes", "t"]
