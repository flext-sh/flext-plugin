"""FLEXT Plugin Types - Domain-specific plugin system type definitions.

This module provides plugin system-specific type definitions extending FlextCore.Types.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextCore.Types properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TypeVar

from flext_core import FlextCore

# Plugin-specific TypeVars
TPluginResult = TypeVar("TPluginResult", bound=FlextCore.Result)

# =============================================================================
# PLUGIN-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for plugin operations
# =============================================================================


class FlextPluginTypes(FlextCore.Types):
    """Plugin system-specific type definitions extending FlextCore.Types.

    Domain-specific type system for plugin management operations.
    Contains ONLY complex plugin-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # CORE TYPES - Essential Plugin types extending FlextCore.Types
    # =========================================================================

    class Core(FlextCore.Types.Core):
        """Core Plugin system types for plugin management operations.

        Essential domain-specific types for plugin management operations.
        Replaces generic FlextCore.Types.Dict with semantic plugin types.
        """

        # String collections
        type StringList = FlextCore.Types.StringList
        type StringSet = set[str]
        type StringDict = dict[str, str]

        # Numeric collections
        type IntList = FlextCore.Types.IntList
        type FloatList = FlextCore.Types.FloatList
        type IntDict = dict[str, int]
        type FloatDict = dict[str, float]

        # Mixed collections
        type AnyList = FlextCore.Types.List
        type AnyDict = FlextCore.Types.Dict

        # Plugin-specific collections
        type PluginList = list[FlextCore.Types.Dict]
        type PluginDict = FlextCore.Types.Dict
        type ConfigDict = FlextCore.Types.Dict
        type SettingsDict = FlextCore.Types.Dict
        type MetadataDict = FlextCore.Types.Dict
        type InputDict = FlextCore.Types.Dict
        type OutputDict = FlextCore.Types.Dict

        # Plugin entity types
        type PluginEntity = FlextCore.Types.Dict
        type PluginConfig = FlextCore.Types.Dict
        type PluginMetadata = FlextCore.Types.Dict
        type PluginRegistry = FlextCore.Types.Dict
        type PluginExecution = FlextCore.Types.Dict

    class Lifecycle:
        """Plugin lifecycle and status types."""

        type PluginStatus = str
        type PluginType = str
        type LifecycleState = str
        type ExecutionStatus = str

    class Security:
        """Plugin security and validation types."""

        type SecurityLevel = str
        type Permission = str
        type SecurityConfig = FlextCore.Types.Dict

    class Performance:
        """Plugin performance and monitoring types."""

        type Metrics = FlextCore.Types.Dict
        type PerformanceData = FlextCore.Types.Dict
        type ResourceUsage = FlextCore.Types.Dict

    class Discovery:
        """Plugin discovery and loading types."""

        type DiscoveryPath = str
        type DiscoveryResult = FlextCore.Types.Dict
        type PluginLoader = object
        type EntryPoint = str

    class Execution:
        """Plugin execution and runtime types."""

        type ExecutionContext = FlextCore.Types.Dict
        type ExecutionResult = FlextCore.Types.Dict
        type ExecutionError = str
        type ResourceLimits = FlextCore.Types.Dict

    class Registry:
        """Plugin registry and management types."""

        type RegistryConfig = FlextCore.Types.Dict
        type RegistryEntry = FlextCore.Types.Dict
        type RegistrySync = FlextCore.Types.Dict

    class HotReload:
        """Plugin hot reload and monitoring types."""

        type WatchConfig = FlextCore.Types.Dict
        type ReloadEvent = FlextCore.Types.Dict
        type FileWatcher = object


# =============================================================================
# PUBLIC API EXPORTS - Plugin TypeVars and types
# =============================================================================

__all__ = [
    "FlextPluginTypes",
    "TPluginResult",
]
