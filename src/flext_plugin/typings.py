"""FLEXT Plugin Types - type system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping, Sequence

from flext_core import FlextTypes

from flext_plugin import FlextPluginConstants as c


class FlextPluginTypes(FlextTypes):
    """Plugin type system with Python 3.13+ patterns.

    Follows FLEXT ecosystem namespace conventions:
    - FlextTypes.Plugin.* for plugin-specific types
    - Canonical container contracts inherited from core `t.*`
    """

    class Plugin:
        """Core collection and plugin type aliases."""

        type StringList = FlextTypes.StrSequence
        type StringSet = set[str]
        type StringDict = FlextTypes.StrMapping
        type IntDict = Mapping[str, int]
        type FloatDict = Mapping[str, float]
        type PluginList = Sequence[FlextTypes.GeneralValueMapping]
        type PluginDict = FlextTypes.GeneralValueMapping
        type ConfigDict = FlextTypes.GeneralValueMapping
        type SettingsDict = FlextTypes.GeneralValueMapping
        type MetadataDict = FlextTypes.GeneralValueMapping
        type InputDict = FlextTypes.GeneralValueMapping
        type OutputDict = FlextTypes.GeneralValueMapping
        type PluginEntity = FlextTypes.GeneralValueMapping
        DiscoveryTypeLiteral = c.Plugin.DiscoveryTypeLiteral
        DiscoveryMethodLiteral = c.Plugin.DiscoveryMethodLiteral
        LoadTypeLiteral = c.Plugin.LoadTypeLiteral

        class Handlers:
            """Event handler type definitions."""

            type EventHandler = Callable[
                [FlextTypes.GeneralValueMapping],
                Awaitable[FlextTypes.GeneralValueMapping],
            ]

            class HandlerInfo:
                """Handler metadata container."""

                def __init__(
                    self,
                    handler: Callable[
                        [FlextTypes.GeneralValueMapping],
                        Awaitable[FlextTypes.GeneralValueMapping],
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
            type SecurityConfig = FlextTypes.GeneralValueMapping
            SecurityLevelLiteral = c.Plugin.SecurityLevelLiteral

        class Performance:
            """Performance metrics and monitoring type aliases."""

            type Metrics = FlextTypes.GeneralValueMapping
            type PerformanceData = FlextTypes.GeneralValueMapping
            type ResourceUsage = FlextTypes.GeneralValueMapping

        class Discovery:
            """Plugin discovery type aliases."""

            type DiscoveryPath = str
            type DiscoveryResult = FlextTypes.GeneralValueMapping
            type PluginLoader = FlextTypes.GeneralValueType
            type EntryPoint = str

        class Execution:
            """Plugin execution type aliases."""

            type ExecutionContext = FlextTypes.GeneralValueMapping
            type ExecutionResult = FlextTypes.GeneralValueMapping
            type ExecutionError = str
            type ResourceLimits = FlextTypes.GeneralValueMapping

        class Registry:
            """Plugin registry type aliases."""

            type RegistryConfig = FlextTypes.GeneralValueMapping
            type RegistryEntry = FlextTypes.GeneralValueMapping
            type RegistrySync = FlextTypes.GeneralValueMapping

        class HotReload:
            """Hot reload and file watching type aliases."""

            type WatchConfig = FlextTypes.GeneralValueMapping
            type ReloadEvent = FlextTypes.GeneralValueMapping
            type FileWatcher = FlextTypes.GeneralValueType


t = FlextPluginTypes
__all__ = ["FlextPluginTypes", "t"]
