"""FLEXT Plugin Types - Domain-specific plugin system type definitions.

This module provides plugin system-specific type definitions extending FlextTypes.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextTypes properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextTypes

#
# =============================================================================
# PLUGIN-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for plugin operations
# =============================================================================


class FlextPluginTypes(FlextTypes):
    """Plugin system-specific type definitions extending FlextTypes.

    Domain-specific type system for plugin management operations.
    Contains ONLY complex plugin-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # CORE TYPES - Essential Plugin types extending FlextTypes
    # =========================================================================

    class Core(FlextTypes.Core):
        """Core Plugin system types for plugin management operations.

        Essential domain-specific types for plugin management operations.
        Replaces generic FlextTypes.Dict with semantic plugin types.
        """

        # String collections
        type StringList = FlextTypes.StringList
        type StringSet = set[str]
        type StringDict = dict[str, str]

        # Numeric collections
        type IntList = FlextTypes.IntList
        type FloatList = FlextTypes.FloatList
        type IntDict = dict[str, int]
        type FloatDict = dict[str, float]

        # Mixed collections
        type AnyList = FlextTypes.List
        type AnyDict = FlextTypes.Dict

        # Plugin-specific collections
        type PluginList = list[FlextTypes.Dict]
        type PluginDict = FlextTypes.Dict
        type ConfigDict = FlextTypes.Dict
        type SettingsDict = FlextTypes.Dict
        type MetadataDict = FlextTypes.Dict
        type InputDict = FlextTypes.Dict
        type OutputDict = FlextTypes.Dict

        # Plugin entity types
        type PluginEntity = FlextTypes.Dict
        type PluginConfig = FlextTypes.Dict
        type PluginMetadata = FlextTypes.Dict
        type PluginRegistry = FlextTypes.Dict
        type PluginExecution = FlextTypes.Dict

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
        type SecurityConfig = FlextTypes.Dict

    class Performance:
        """Plugin performance and monitoring types."""

        type Metrics = FlextTypes.Dict
        type PerformanceData = FlextTypes.Dict
        type ResourceUsage = FlextTypes.Dict

    class Discovery:
        """Plugin discovery and loading types."""

        type DiscoveryPath = str
        type DiscoveryResult = FlextTypes.Dict
        type PluginLoader = object
        type EntryPoint = str

    class Execution:
        """Plugin execution and runtime types."""

        type ExecutionContext = FlextTypes.Dict
        type ExecutionResult = FlextTypes.Dict
        type ExecutionError = str
        type ResourceLimits = FlextTypes.Dict

    class Registry:
        """Plugin registry and management types."""

        type RegistryConfig = FlextTypes.Dict
        type RegistryEntry = FlextTypes.Dict
        type RegistrySync = FlextTypes.Dict

    class HotReload:
        """Plugin hot reload and monitoring types."""

        type WatchConfig = FlextTypes.Dict
        type ReloadEvent = FlextTypes.Dict
        type FileWatcher = object


# =============================================================================
# PUBLIC API EXPORTS - Plugin TypeVars and types
# =============================================================================

__all__ = [
    "FlextPluginTypes",
]
