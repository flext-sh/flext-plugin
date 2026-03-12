"""FLEXT Plugin Types - type system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from typing import Literal, TypeAlias, TypeVar

from flext_core import FlextTypes

from .constants import FlextPluginConstants as c_plugin

T = TypeVar("T")


class FlextPluginTypes(FlextTypes):
    """Plugin type system with Python 3.13+ patterns.

    Follows FLEXT ecosystem namespace conventions:
    - t.Plugin.* for plugin-specific types
    - t.Core.JsonDict, t.Core.object via Core alias
    """

    class Handlers:
        """Event handler type definitions."""

        EventHandler: TypeAlias = Callable[
            [Mapping[str, object]],
            Awaitable[object],
        ]

        class HandlerInfo:
            """Handler metadata container."""

            def __init__(
                self,
                handler: Callable[
                    [Mapping[str, object]],
                    Awaitable[object],
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

        type StringList = list[str]
        type StringSet = set[str]
        type StringDict = Mapping[str, str]
        type IntDict = Mapping[str, int]
        type FloatDict = Mapping[str, float]
        type PluginList = list[Mapping[str, object]]
        type PluginDict = Mapping[str, object]
        type ConfigDict = Mapping[str, object]
        type SettingsDict = Mapping[str, object]
        type MetadataDict = Mapping[str, object]
        type InputDict = Mapping[str, object]
        type OutputDict = Mapping[str, object]
        type PluginEntity = Mapping[str, object]
        type DiscoveryTypeLiteral = Literal["file", "directory", "entry_point"]
        type DiscoveryMethodLiteral = Literal["file_system", "entry_points"]
        type LoadTypeLiteral = Literal["file", "directory", "entry_point"]
        type PluginTypeLiteral = Literal[
            c_plugin.Plugin.PluginType.TAP,
            c_plugin.Plugin.PluginType.TARGET,
            c_plugin.Plugin.PluginType.TRANSFORM,
            c_plugin.Plugin.PluginType.EXTENSION,
            c_plugin.Plugin.PluginType.SERVICE,
            c_plugin.Plugin.PluginType.MIDDLEWARE,
            c_plugin.Plugin.PluginType.TRANSFORMER,
            c_plugin.Plugin.PluginType.API,
            c_plugin.Plugin.PluginType.DATABASE,
            c_plugin.Plugin.PluginType.NOTIFICATION,
            c_plugin.Plugin.PluginType.AUTHENTICATION,
            c_plugin.Plugin.PluginType.AUTHORIZATION,
            c_plugin.Plugin.PluginType.UTILITY,
            c_plugin.Plugin.PluginType.TOOL,
            c_plugin.Plugin.PluginType.HANDLER,
            c_plugin.Plugin.PluginType.PROCESSOR,
            c_plugin.Plugin.PluginType.CORE,
            c_plugin.Plugin.PluginType.ADDON,
            c_plugin.Plugin.PluginType.THEME,
            c_plugin.Plugin.PluginType.LANGUAGE,
        ]
        "Plugin type literal - references PluginType StrEnum members."
        type PluginStatusLiteral = Literal[
            c_plugin.Plugin.PluginStatus.UNKNOWN,
            c_plugin.Plugin.PluginStatus.DISCOVERED,
            c_plugin.Plugin.PluginStatus.LOADED,
            c_plugin.Plugin.PluginStatus.ACTIVE,
            c_plugin.Plugin.PluginStatus.INACTIVE,
            c_plugin.Plugin.PluginStatus.LOADING,
            c_plugin.Plugin.PluginStatus.ERROR,
            c_plugin.Plugin.PluginStatus.DISABLED,
            c_plugin.Plugin.PluginStatus.HEALTHY,
            c_plugin.Plugin.PluginStatus.UNHEALTHY,
        ]
        "Plugin status literal - references PluginStatus StrEnum members."

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
        type SecurityConfig = Mapping[str, object]
        type SecurityLevelLiteral = Literal["low", "medium", "high", "critical"]
        "Security level literal - no corresponding StrEnum."

    class Performance:
        """Performance metrics and monitoring type aliases."""

        type Metrics = Mapping[str, object]
        type PerformanceData = Mapping[str, object]
        type ResourceUsage = Mapping[str, object]

    class Discovery:
        """Plugin discovery type aliases."""

        type DiscoveryPath = str
        type DiscoveryResult = Mapping[str, object]
        type PluginLoader = object
        type EntryPoint = str

    class Execution:
        """Plugin execution type aliases."""

        type ExecutionContext = Mapping[str, object]
        type ExecutionResult = Mapping[str, object]
        type ExecutionError = str
        type ResourceLimits = Mapping[str, object]

    class Registry:
        """Plugin registry type aliases."""

        type RegistryConfig = Mapping[str, object]
        type RegistryEntry = Mapping[str, object]
        type RegistrySync = Mapping[str, object]
        type DiscoveryTypeLiteral = Literal["file", "directory", "entry_point"]
        type DiscoveryMethodLiteral = Literal["file_system", "entry_points"]
        type LoadTypeLiteral = Literal["file", "directory", "entry_point"]

    class HotReload:
        """Hot reload and file watching type aliases."""

        type WatchConfig = Mapping[str, object]
        type ReloadEvent = Mapping[str, object]
        type FileWatcher = object


t = FlextPluginTypes
__all__ = ["FlextPluginTypes", "t"]
