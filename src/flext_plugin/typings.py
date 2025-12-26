"""FLEXT Plugin Types - type system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextTypes


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

        # Plugin types - Using JsonDict from FlextTypes for JSON-like data
        type PluginList = list[FlextTypes.Core.JsonDict]
        type PluginDict = FlextTypes.Core.JsonDict
        type ConfigDict = FlextTypes.Core.JsonDict
        type SettingsDict = FlextTypes.Core.JsonDict
        type MetadataDict = FlextTypes.Core.JsonDict
        type InputDict = FlextTypes.Core.JsonDict
        type OutputDict = FlextTypes.Core.JsonDict
        type PluginEntity = FlextTypes.Core.JsonDict

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
        type SecurityConfig = FlextTypes.Core.JsonDict

    class Performance:
        """Performance metrics and monitoring type aliases."""

        type Metrics = FlextTypes.Core.JsonDict
        type PerformanceData = FlextTypes.Core.JsonDict
        type ResourceUsage = FlextTypes.Core.JsonDict

    class Discovery:
        """Plugin discovery type aliases."""

        type DiscoveryPath = str
        type DiscoveryResult = FlextTypes.Core.JsonDict
        type PluginLoader = FlextTypes.Core.GeneralValueType
        type EntryPoint = str

    class Execution:
        """Plugin execution type aliases."""

        type ExecutionContext = FlextTypes.Core.JsonDict
        type ExecutionResult = FlextTypes.Core.JsonDict
        type ExecutionError = str
        type ResourceLimits = FlextTypes.Core.JsonDict

    class Registry:
        """Plugin registry type aliases."""

        type RegistryConfig = FlextTypes.Core.JsonDict
        type RegistryEntry = FlextTypes.Core.JsonDict
        type RegistrySync = FlextTypes.Core.JsonDict

    class HotReload:
        """Hot reload and file watching type aliases."""

        type WatchConfig = FlextTypes.Core.JsonDict
        type ReloadEvent = FlextTypes.Core.JsonDict
        type FileWatcher = FlextTypes.Core.GeneralValueType


# Standard FLEXT alias for namespace access
t = FlextPluginTypes

__all__ = ["FlextPluginTypes", "t"]
