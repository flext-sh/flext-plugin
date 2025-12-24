"""FLEXT Plugin Types - type system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext import FlextTypes


class FlextPluginTypes(FlextTypes):
    """Plugin type system with Python 3.13+ patterns.

    Follows FLEXT ecosystem namespace conventions:
    - t.Plugin.* for plugin-specific types
    - Inherits t.Core.* from FlextTypes
    """

    class Plugin:
        """Core collection and plugin type aliases."""

        # Collections
        type StringList = list[str]
        type StringSet = set[str]
        type StringDict = dict[str, str]
        type IntDict = dict[str, int]
        type FloatDict = dict[str, float]
        type AnyList = list[object]
        type AnyDict = dict[str, object]

        # Plugin types
        type PluginList = list[dict[str, object]]
        type PluginDict = dict[str, object]
        type ConfigDict = dict[str, object]
        type SettingsDict = dict[str, object]
        type MetadataDict = dict[str, object]
        type InputDict = dict[str, object]
        type OutputDict = dict[str, object]
        type PluginEntity = dict[str, object]

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
        type SecurityConfig = dict[str, object]

    class Performance:
        """Performance metrics and monitoring type aliases."""

        type Metrics = dict[str, object]
        type PerformanceData = dict[str, object]
        type ResourceUsage = dict[str, object]

    class Discovery:
        """Plugin discovery type aliases."""

        type DiscoveryPath = str
        type DiscoveryResult = dict[str, object]
        type PluginLoader = object
        type EntryPoint = str

    class Execution:
        """Plugin execution type aliases."""

        type ExecutionContext = dict[str, object]
        type ExecutionResult = dict[str, object]
        type ExecutionError = str
        type ResourceLimits = dict[str, object]

    class Registry:
        """Plugin registry type aliases."""

        type RegistryConfig = dict[str, object]
        type RegistryEntry = dict[str, object]
        type RegistrySync = dict[str, object]

    class HotReload:
        """Hot reload and file watching type aliases."""

        type WatchConfig = dict[str, object]
        type ReloadEvent = dict[str, object]
        type FileWatcher = object


# Standard FLEXT alias for namespace access
t = FlextPluginTypes

__all__ = ["FlextPluginTypes", "t"]
