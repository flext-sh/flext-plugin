"""FLEXT Plugin Types - type system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Awaitable,
    Callable,
    Mapping,
    Sequence,
)

from flext_cli import m, t

from flext_plugin import c


class FlextPluginTypes(t):
    """Plugin type system with Python 3.13+ patterns.

    Follows FLEXT ecosystem namespace conventions:
    - t.Plugin.* for plugin-specific types
    - Canonical container contracts inherited from core `t.*`
    """

    CONTAINER_MAPPING_ADAPTER: m.TypeAdapter[Mapping[str, t.Container]] = m.TypeAdapter(
        Mapping[str, t.Container]
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
        type PluginList = Sequence[t.Container]
        type PluginDict = t.Container
        type ConfigDict = t.Container
        type MetadataDict = t.Container
        type InputDict = t.Container
        type OutputDict = t.Container
        type PluginEntity = t.Container
        DiscoveryTypeLiteral = c.Plugin.DiscoveryTypeLiteral
        DiscoveryMethodLiteral = c.Plugin.DiscoveryMethodLiteral
        LoadTypeLiteral = c.Plugin.LoadTypeLiteral

        class Handlers:
            """Event handler type definitions."""

            type EventHandler = Callable[
                [Mapping[str, t.Container]],
                Awaitable[Mapping[str, t.Container]],
            ]

            class HandlerInfo:
                """Handler metadata container."""

                def __init__(
                    self,
                    handler: Callable[
                        [Mapping[str, t.Container]],
                        Awaitable[Mapping[str, t.Container]],
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
            type SecurityConfig = t.Container
            SecurityLevelLiteral = c.Plugin.SecurityLevelLiteral

        class Performance:
            """Performance metrics and monitoring type aliases."""

            type Metrics = t.Container
            type PerformanceData = t.Container
            type ResourceUsage = t.Container

        class Discovery:
            """Plugin discovery type aliases."""

            type DiscoveryPath = str
            type DiscoveryResult = t.Container
            type PluginLoader = t.GeneralValueType
            type EntryPoint = str

        class Execution:
            """Plugin execution type aliases."""

            type ExecutionContext = t.Container
            type ExecutionResult = t.Container
            type ExecutionError = str
            type ResourceLimits = t.Container

        class Registry:
            """Plugin registry type aliases."""

            type RegistryConfig = t.Container
            type RegistryEntry = t.Container
            type RegistrySync = t.Container

        class HotReload:
            """Hot reload and file watching type aliases."""

            type WatchConfig = t.Container
            type ReloadEvent = t.Container
            type FileWatcher = t.GeneralValueType


t = FlextPluginTypes
__all__: list[str] = ["FlextPluginTypes", "t"]
