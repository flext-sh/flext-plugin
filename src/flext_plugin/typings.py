"""FLEXT Plugin Types - type system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping, Sequence

from flext_core import FlextTypes

from flext_plugin.constants import FlextPluginConstants as c


class FlextPluginTypes(FlextTypes):
    """Plugin type system with Python 3.13+ patterns.

    Follows FLEXT ecosystem namespace conventions:
    - FlextTypes.Plugin.* for plugin-specific types
    - FlextTypes.Core.JsonDict, FlextTypes.Core.FlextTypes.NormalizedValue via Core alias
    """

    class Handlers:
        """Event handler type definitions."""

        type EventHandler = Callable[
            [Mapping[str, FlextTypes.NormalizedValue]],
            Awaitable[Mapping[str, FlextTypes.NormalizedValue]],
        ]

        class HandlerInfo:
            """Handler metadata container."""

            def __init__(
                self,
                handler: Callable[
                    [Mapping[str, FlextTypes.NormalizedValue]],
                    Awaitable[Mapping[str, FlextTypes.NormalizedValue]],
                ],
                priority: int = 0,
            ) -> None:
                """Initialize handler info.

                Args:
                    handler: Event handler function
                    priority: Handler execution priority (higher = first)

                """
                self.handler = handler
                self.priority = priority

    class Plugin:
        """Core collection and plugin type aliases."""

        type StringList = FlextTypes.StrSequence
        type StringSet = set[str]
        type StringDict = FlextTypes.StrMapping
        type IntDict = Mapping[str, int]
        type FloatDict = Mapping[str, float]
        type PluginList = Sequence[Mapping[str, FlextTypes.NormalizedValue]]
        type PluginDict = Mapping[str, FlextTypes.NormalizedValue]
        type ConfigDict = Mapping[str, FlextTypes.NormalizedValue]
        type SettingsDict = Mapping[str, FlextTypes.NormalizedValue]
        type MetadataDict = Mapping[str, FlextTypes.NormalizedValue]
        type InputDict = Mapping[str, FlextTypes.NormalizedValue]
        type OutputDict = Mapping[str, FlextTypes.NormalizedValue]
        type PluginEntity = Mapping[str, FlextTypes.NormalizedValue]
        DiscoveryTypeLiteral = c.DiscoveryTypeLiteral
        DiscoveryMethodLiteral = c.DiscoveryMethodLiteral
        LoadTypeLiteral = c.LoadTypeLiteral

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
        type SecurityConfig = Mapping[str, FlextTypes.NormalizedValue]
        SecurityLevelLiteral = c.SecurityLevelLiteral

    class Performance:
        """Performance metrics and monitoring type aliases."""

        type Metrics = Mapping[str, FlextTypes.NormalizedValue]
        type PerformanceData = Mapping[str, FlextTypes.NormalizedValue]
        type ResourceUsage = Mapping[str, FlextTypes.NormalizedValue]

    class Discovery:
        """Plugin discovery type aliases."""

        type DiscoveryPath = str
        type DiscoveryResult = Mapping[str, FlextTypes.NormalizedValue]
        type PluginLoader = FlextTypes.NormalizedValue
        type EntryPoint = str

    class Execution:
        """Plugin execution type aliases."""

        type ExecutionContext = Mapping[str, FlextTypes.NormalizedValue]
        type ExecutionResult = Mapping[str, FlextTypes.NormalizedValue]
        type ExecutionError = str
        type ResourceLimits = Mapping[str, FlextTypes.NormalizedValue]

    class Registry:
        """Plugin registry type aliases."""

        type RegistryConfig = Mapping[str, FlextTypes.NormalizedValue]
        type RegistryEntry = Mapping[str, FlextTypes.NormalizedValue]
        type RegistrySync = Mapping[str, FlextTypes.NormalizedValue]

    class HotReload:
        """Hot reload and file watching type aliases."""

        type WatchConfig = Mapping[str, FlextTypes.NormalizedValue]
        type ReloadEvent = Mapping[str, FlextTypes.NormalizedValue]
        type FileWatcher = FlextTypes.NormalizedValue


t = FlextPluginTypes
__all__ = ["FlextPluginTypes", "t"]
