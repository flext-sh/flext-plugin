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

from typing import TypeVar

from flext_core import FlextResult, FlextTypes

# Plugin-specific TypeVars
TPluginResult = TypeVar("TPluginResult", bound=FlextResult)

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
        type StringList = list[str]
        type StringSet = set[str]
        type StringDict = dict[str, str]

        # Numeric collections
        type IntList = list[int]
        type FloatList = list[float]
        type IntDict = dict[str, int]
        type FloatDict = dict[str, float]

        # Mixed collections
        type AnyList = list[object]
        type AnyDict = dict[str, object]

        # Plugin-specific collections
        type PluginList = list[dict[str, object]]
        type PluginDict = dict[str, object]
        type ConfigDict = dict[str, object]
        type SettingsDict = dict[str, object]
        type MetadataDict = dict[str, object]
        type InputDict = dict[str, object]
        type OutputDict = dict[str, object]

        # Plugin entity types
        type PluginEntity = dict[str, object]
        type PluginConfig = dict[str, object]
        type PluginMetadata = dict[str, object]
        type PluginRegistry = dict[str, object]
        type PluginExecution = dict[str, object]

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
        type SecurityConfig = dict[str, object]

    class Performance:
        """Plugin performance and monitoring types."""

        type Metrics = dict[str, object]
        type PerformanceData = dict[str, object]
        type ResourceUsage = dict[str, object]

    class Discovery:
        """Plugin discovery and loading types."""

        type DiscoveryPath = str
        type DiscoveryResult = dict[str, object]
        type PluginLoader = object
        type EntryPoint = str

    class Execution:
        """Plugin execution and runtime types."""

        type ExecutionContext = dict[str, object]
        type ExecutionResult = dict[str, object]
        type ExecutionError = str
        type ResourceLimits = dict[str, object]

    class Registry:
        """Plugin registry and management types."""

        type RegistryConfig = dict[str, object]
        type RegistryEntry = dict[str, object]
        type RegistrySync = dict[str, object]

    class HotReload:
        """Plugin hot reload and monitoring types."""

        type WatchConfig = dict[str, object]
        type ReloadEvent = dict[str, object]
        type FileWatcher = object


# =============================================================================
# PUBLIC API EXPORTS - Plugin TypeVars and types
# =============================================================================

__all__ = [
    "FlextPluginTypes",
    "TPluginResult",
]
