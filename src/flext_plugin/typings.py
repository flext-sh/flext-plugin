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

from typing import Literal, TypeVar

from flext_core import FlextResult, FlextTypes

# Plugin-specific TypeVars
TPluginResult = TypeVar("TPluginResult", bound=FlextResult)

# =============================================================================
# PLUGIN-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for plugin operations
# =============================================================================


# Plugin domain TypeVars
class FlextPluginTypes(FlextTypes):
    """Plugin system-specific type definitions extending FlextTypes.

    Domain-specific type system for plugin management operations.
    Contains ONLY complex plugin-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # PLUGIN MANAGEMENT TYPES - Complex plugin lifecycle types
    # =========================================================================

    class PluginManagement:
        """Plugin management complex types."""

        type PluginConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type PluginRegistration = dict[
            str, str | bool | dict[str, FlextTypes.JsonValue]
        ]
        type PluginLifecycle = dict[
            str, str | bool | FlextTypes.StringList | FlextTypes.Dict
        ]
        type PluginDependencies = list[dict[str, str | FlextTypes.Dict]]
        type PluginCapabilities = dict[
            str, bool | FlextTypes.StringList | dict[str, FlextTypes.JsonValue]
        ]
        type PluginValidation = dict[
            str, bool | str | FlextTypes.StringList | FlextTypes.Dict
        ]

    # =========================================================================
    # PLUGIN DISCOVERY TYPES - Complex plugin discovery types
    # =========================================================================

    class Discovery:
        """Plugin discovery complex types."""

        type DiscoveryConfiguration = dict[
            str, str | bool | FlextTypes.StringList | dict[str, FlextTypes.ConfigValue]
        ]
        type DiscoveryContext = dict[
            str, str | FlextTypes.StringList | dict[str, FlextTypes.JsonValue]
        ]
        type DiscoveryResult = dict[str, list[FlextTypes.Dict] | bool | str]
        type DiscoveryFilters = list[dict[str, str | bool | FlextTypes.StringList]]
        type DiscoveryMetrics = dict[str, int | float | dict[str, FlextTypes.JsonValue]]
        type DiscoveryCache = dict[str, str | dict[str, FlextTypes.JsonValue]]

    # =========================================================================
    # PLUGIN EXECUTION TYPES - Complex plugin execution types
    # =========================================================================

    class Execution:
        """Plugin execution complex types."""

        type ExecutionConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type ExecutionContext = dict[
            str, str | object | dict[str, FlextTypes.JsonValue]
        ]
        type ExecutionResult = dict[
            str, bool | str | object | dict[str, FlextTypes.JsonValue]
        ]
        type ExecutionMetrics = dict[str, int | float | dict[str, FlextTypes.JsonValue]]
        type ExecutionSecurity = dict[
            str, str | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type ExecutionSandbox = dict[
            str, str | bool | FlextTypes.StringList | FlextTypes.Dict
        ]

    # =========================================================================
    # PLUGIN REGISTRY TYPES - Complex plugin registry types
    # =========================================================================

    class Registry:
        """Plugin registry complex types."""

        type RegistryConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type RegistryEntry = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type RegistryIndex = dict[str, list[FlextTypes.Dict] | FlextTypes.Dict]
        type RegistryMetadata = dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        type RegistryValidation = dict[str, bool | str | FlextTypes.StringList]
        type RegistrySync = dict[str, str | bool | FlextTypes.Dict]

    # =========================================================================
    # PLUGIN SECURITY TYPES - Complex plugin security types
    # =========================================================================

    class Security:
        """Plugin security complex types."""

        type SecurityConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type SecurityPolicy = dict[
            str, str | bool | FlextTypes.StringList | FlextTypes.Dict
        ]
        type SecurityValidation = dict[
            str, bool | str | FlextTypes.StringList | FlextTypes.Dict
        ]
        type SecuritySandbox = dict[
            str, str | bool | FlextTypes.StringList | dict[str, FlextTypes.ConfigValue]
        ]
        type SecurityAudit = list[
            dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        ]
        type SecurityCredentials = dict[str, str | dict[str, FlextTypes.ConfigValue]]

    # =========================================================================
    # PLUGIN HOT RELOAD TYPES - Complex hot reload types
    # =========================================================================

    class HotReload:
        """Plugin hot reload complex types."""

        type HotReloadConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type HotReloadContext = dict[str, str | bool | dict[str, FlextTypes.JsonValue]]
        type HotReloadEvent = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type HotReloadState = dict[
            str, str | bool | FlextTypes.StringList | FlextTypes.Dict
        ]
        type HotReloadMetrics = dict[str, int | float | dict[str, FlextTypes.JsonValue]]
        type HotReloadValidation = dict[str, bool | str | FlextTypes.StringList]

    # =========================================================================
    # PLUGIN MONITORING TYPES - Complex plugin monitoring types
    # =========================================================================

    class Monitoring:
        """Plugin monitoring complex types."""

        type MonitoringConfiguration = dict[
            str, bool | str | int | dict[str, FlextTypes.ConfigValue]
        ]
        type MonitoringMetrics = dict[
            str, int | float | dict[str, FlextTypes.JsonValue]
        ]
        type MonitoringAlerts = list[dict[str, str | int | bool | FlextTypes.Dict]]
        type MonitoringDashboard = dict[
            str, str | list[dict[str, FlextTypes.JsonValue]]
        ]
        type MonitoringReports = dict[str, str | list[FlextTypes.Dict]]
        type MonitoringHealth = dict[str, bool | str | FlextTypes.Dict]

    # =========================================================================
    # CORE TYPES - Essential Plugin types extending FlextTypes
    # =========================================================================

    class Core(FlextTypes):
        """Core Plugin system types extending FlextTypes.

        Essential domain-specific types for plugin management operations.
        Replaces generic FlextTypes.Dict with semantic plugin types.
        """

        # Configuration and management types
        type ConfigDict = dict[str, FlextTypes.ConfigValue | object]
        type PluginDict = FlextTypes.Dict
        type MetadataDict = FlextTypes.Dict
        type SettingsDict = FlextTypes.Dict

        # Execution and processing types
        type InputDict = FlextTypes.Dict
        type OutputDict = FlextTypes.Dict
        type StateDict = FlextTypes.Dict
        type ContextDict = FlextTypes.Dict

        # Discovery and registry types
        type DiscoveryDict = dict[str, list[FlextTypes.Dict] | bool | str]
        type RegistryDict = dict[str, list[FlextTypes.Dict] | FlextTypes.Dict]
        type LoadedPluginsDict = FlextTypes.Dict
        type ManifestDict = FlextTypes.Dict

        # Lifecycle and operation types
        type LifecycleDict = dict[
            str, str | bool | FlextTypes.StringList | FlextTypes.Dict
        ]
        type SecurityDict = dict[
            str, str | bool | FlextTypes.StringList | FlextTypes.Dict
        ]
        type MonitoringDict = dict[str, bool | str | FlextTypes.Dict]
        type DetailsDict = FlextTypes.Dict

        # Collection types for plugin operations
        type PluginList = list[PluginDict]
        type MetadataList = list[MetadataDict]
        type StringList = FlextTypes.StringList

    # =========================================================================
    # PLUGIN PROJECT TYPES - Domain-specific project types extending FlextTypes
    # =========================================================================

    class Project(FlextTypes.Project):
        """Plugin-specific project types extending FlextTypes.Project.

        Adds plugin/extensibility-specific project types while inheriting
        generic types from FlextTypes. Follows domain separation principle:
        Plugin domain owns extensibility and plugin management-specific types.
        """

        # Plugin-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextTypes.Project
            "library",
            "application",
            "service",
            # Plugin-specific types
            "plugin",
            "extension",
            "addon",
            "plugin-manager",
            "plugin-system",
            "extensibility-platform",
            "plugin-registry",
            "plugin-discovery",
            "plugin-loader",
            "hot-reload-system",
            "plugin-api",
            "extension-framework",
            "plugin-validator",
            "plugin-security",
            "plugin-monitor",
            "plugin-platform",
        ]

        # Plugin-specific project configurations
        type PluginProjectConfig = dict[str, FlextTypes.ConfigValue | object]
        type ExtensibilityConfig = dict[str, str | int | bool | FlextTypes.StringList]
        type PluginRegistryConfig = dict[str, bool | str | FlextTypes.Dict]
        type HotReloadConfig = dict[str, FlextTypes.ConfigValue | object]


# =============================================================================
# PUBLIC API EXPORTS - Plugin TypeVars and types
# =============================================================================

__all__: FlextTypes.StringList = [
    "FlextPluginTypes",
    "TPluginResult",
]
