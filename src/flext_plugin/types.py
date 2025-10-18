"""FLEXT Plugin Types - Advanced type system.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextTypes


class FlextPluginTypes(FlextTypes):
    """Advanced plugin type system with Python 3.13+ patterns."""

    class Core:
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
        type PluginStatus = str
        type PluginType = str
        type LifecycleState = str
        type ExecutionStatus = str

    class Security:
        type SecurityLevel = str
        type Permission = str
        type SecurityConfig = dict[str, object]

    class Performance:
        type Metrics = dict[str, object]
        type PerformanceData = dict[str, object]
        type ResourceUsage = dict[str, object]

    class Discovery:
        type DiscoveryPath = str
        type DiscoveryResult = dict[str, object]
        type PluginLoader = object
        type EntryPoint = str

    class Execution:
        type ExecutionContext = dict[str, object]
        type ExecutionResult = dict[str, object]
        type ExecutionError = str
        type ResourceLimits = dict[str, object]

    class Registry:
        type RegistryConfig = dict[str, object]
        type RegistryEntry = dict[str, object]
        type RegistrySync = dict[str, object]

    class HotReload:
        type WatchConfig = dict[str, object]
        type ReloadEvent = dict[str, object]
        type FileWatcher = object


__all__ = ["FlextPluginTypes"]
