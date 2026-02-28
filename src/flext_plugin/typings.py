"""FLEXT Plugin Types - type system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from typing import Literal, TypeVar

from flext_core import FlextTypes
from pydantic import BaseModel, ConfigDict

from .constants import FlextPluginConstants as c_plugin

T = TypeVar("T")


class FlextPluginTypes(FlextTypes):
    """Plugin type system with Python 3.13+ patterns.

    Follows FLEXT ecosystem namespace conventions:
    - t.Plugin.* for plugin-specific types
    - t.Core.JsonDict, t.Core.GeneralValueType via Core alias
    """

    class Handlers:
        """Event handler type definitions."""

        type EventHandler = Callable[
            [Mapping[str, FlextTypes.JsonValue]],
            Awaitable[FlextTypes.JsonValue],
        ]

        class HandlerInfo(BaseModel):
            """Handler registration info."""

            model_config = ConfigDict(frozen=False, extra="forbid")

            handler: FlextPluginTypes.Handlers.EventHandler
            priority: int

    class Plugin:
        """Core collection and plugin type aliases."""

        # Collections
        type StringList = list[str]
        type StringSet = set[str]
        type StringDict = Mapping[str, str]
        type IntDict = Mapping[str, int]
        type FloatDict = Mapping[str, float]

        # Plugin types - Using JsonDict from FlextTypes for JSON-like data
        type PluginList = list[Mapping[str, FlextTypes.JsonValue]]
        type PluginDict = Mapping[str, FlextTypes.JsonValue]
        type ConfigDict = Mapping[str, FlextTypes.JsonValue]
        type SettingsDict = Mapping[str, FlextTypes.JsonValue]
        type MetadataDict = Mapping[str, FlextTypes.JsonValue]
        type InputDict = Mapping[str, FlextTypes.JsonValue]
        type OutputDict = Mapping[str, FlextTypes.JsonValue]
        type PluginEntity = Mapping[str, FlextTypes.JsonValue]

        # Literal types for plugin operations
        type DiscoveryTypeLiteral = Literal["file", "directory", "entry_point"]
        type DiscoveryMethodLiteral = Literal["file_system", "entry_points"]
        type LoadTypeLiteral = Literal["file", "directory", "entry_point"]

        # Literal types referencing StrEnum members (DRY principle)
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
        """Plugin type literal - references PluginType StrEnum members."""

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
        """Plugin status literal - references PluginStatus StrEnum members."""

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
        type SecurityConfig = Mapping[str, FlextTypes.JsonValue]

        # Literal type for security levels
        type SecurityLevelLiteral = Literal["low", "medium", "high", "critical"]
        """Security level literal - no corresponding StrEnum."""

    class Performance:
        """Performance metrics and monitoring type aliases."""

        type Metrics = Mapping[str, FlextTypes.JsonValue]
        type PerformanceData = Mapping[str, FlextTypes.JsonValue]
        type ResourceUsage = Mapping[str, FlextTypes.JsonValue]

    class Discovery:
        """Plugin discovery type aliases."""

        type DiscoveryPath = str
        type DiscoveryResult = Mapping[str, FlextTypes.JsonValue]
        type PluginLoader = FlextTypes.JsonValue
        type EntryPoint = str

    class Execution:
        """Plugin execution type aliases."""

        type ExecutionContext = Mapping[str, FlextTypes.JsonValue]
        type ExecutionResult = Mapping[str, FlextTypes.JsonValue]
        type ExecutionError = str
        type ResourceLimits = Mapping[str, FlextTypes.JsonValue]

    class Registry:
        """Plugin registry type aliases."""

        type RegistryConfig = Mapping[str, FlextTypes.JsonValue]
        type RegistryEntry = Mapping[str, FlextTypes.JsonValue]
        type RegistrySync = Mapping[str, FlextTypes.JsonValue]

        # Literal types for plugin operations
        type DiscoveryTypeLiteral = Literal["file", "directory", "entry_point"]
        type DiscoveryMethodLiteral = Literal["file_system", "entry_points"]
        type LoadTypeLiteral = Literal["file", "directory", "entry_point"]

    class HotReload:
        """Hot reload and file watching type aliases."""

        type WatchConfig = Mapping[str, FlextTypes.JsonValue]
        type ReloadEvent = Mapping[str, FlextTypes.JsonValue]
        type FileWatcher = FlextTypes.JsonValue


# Shorthand alias for convenient use throughout ecosystem
t = FlextPluginTypes

__all__ = ["FlextPluginTypes", "t"]
