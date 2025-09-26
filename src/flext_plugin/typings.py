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

from typing import Literal

from flext_core import FlextTypes

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
            str, str | int | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type PluginRegistration = dict[
            str, str | bool | dict[str, FlextTypes.Core.JsonValue]
        ]
        type PluginLifecycle = dict[str, str | bool | list[str] | dict[str, object]]
        type PluginDependencies = list[dict[str, str | dict[str, object]]]
        type PluginCapabilities = dict[
            str, bool | list[str] | dict[str, FlextTypes.Core.JsonValue]
        ]
        type PluginValidation = dict[str, bool | str | list[str] | dict[str, object]]

    # =========================================================================
    # PLUGIN DISCOVERY TYPES - Complex plugin discovery types
    # =========================================================================

    class Discovery:
        """Plugin discovery complex types."""

        type DiscoveryConfiguration = dict[
            str, str | bool | list[str] | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type DiscoveryContext = dict[
            str, str | list[str] | dict[str, FlextTypes.Core.JsonValue]
        ]
        type DiscoveryResult = dict[str, list[dict[str, object]] | bool | str]
        type DiscoveryFilters = list[dict[str, str | bool | list[str]]]
        type DiscoveryMetrics = dict[
            str, int | float | dict[str, FlextTypes.Core.JsonValue]
        ]
        type DiscoveryCache = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]

    # =========================================================================
    # PLUGIN EXECUTION TYPES - Complex plugin execution types
    # =========================================================================

    class Execution:
        """Plugin execution complex types."""

        type ExecutionConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type ExecutionContext = dict[
            str, str | object | dict[str, FlextTypes.Core.JsonValue]
        ]
        type ExecutionResult = dict[
            str, bool | str | object | dict[str, FlextTypes.Core.JsonValue]
        ]
        type ExecutionMetrics = dict[
            str, int | float | dict[str, FlextTypes.Core.JsonValue]
        ]
        type ExecutionSecurity = dict[
            str, str | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type ExecutionSandbox = dict[str, str | bool | list[str] | dict[str, object]]

    # =========================================================================
    # PLUGIN REGISTRY TYPES - Complex plugin registry types
    # =========================================================================

    class Registry:
        """Plugin registry complex types."""

        type RegistryConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type RegistryEntry = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type RegistryIndex = dict[str, list[dict[str, object]] | dict[str, object]]
        type RegistryMetadata = dict[
            str, str | int | dict[str, FlextTypes.Core.JsonValue]
        ]
        type RegistryValidation = dict[str, bool | str | list[str]]
        type RegistrySync = dict[str, str | bool | dict[str, object]]

    # =========================================================================
    # PLUGIN SECURITY TYPES - Complex plugin security types
    # =========================================================================

    class Security:
        """Plugin security complex types."""

        type SecurityConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type SecurityPolicy = dict[str, str | bool | list[str] | dict[str, object]]
        type SecurityValidation = dict[str, bool | str | list[str] | dict[str, object]]
        type SecuritySandbox = dict[
            str, str | bool | list[str] | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type SecurityAudit = list[
            dict[str, str | int | dict[str, FlextTypes.Core.JsonValue]]
        ]
        type SecurityCredentials = dict[
            str, str | dict[str, FlextTypes.Core.ConfigValue]
        ]

    # =========================================================================
    # PLUGIN HOT RELOAD TYPES - Complex hot reload types
    # =========================================================================

    class HotReload:
        """Plugin hot reload complex types."""

        type HotReloadConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type HotReloadContext = dict[
            str, str | bool | dict[str, FlextTypes.Core.JsonValue]
        ]
        type HotReloadEvent = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type HotReloadState = dict[str, str | bool | list[str] | dict[str, object]]
        type HotReloadMetrics = dict[
            str, int | float | dict[str, FlextTypes.Core.JsonValue]
        ]
        type HotReloadValidation = dict[str, bool | str | list[str]]

    # =========================================================================
    # PLUGIN MONITORING TYPES - Complex plugin monitoring types
    # =========================================================================

    class Monitoring:
        """Plugin monitoring complex types."""

        type MonitoringConfiguration = dict[
            str, bool | str | int | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type MonitoringMetrics = dict[
            str, int | float | dict[str, FlextTypes.Core.JsonValue]
        ]
        type MonitoringAlerts = list[dict[str, str | int | bool | dict[str, object]]]
        type MonitoringDashboard = dict[
            str, str | list[dict[str, FlextTypes.Core.JsonValue]]
        ]
        type MonitoringReports = dict[str, str | list[dict[str, object]]]
        type MonitoringHealth = dict[str, bool | str | dict[str, object]]

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
        type PluginProjectConfig = dict[str, FlextTypes.Core.ConfigValue | object]
        type ExtensibilityConfig = dict[str, str | int | bool | list[str]]
        type PluginRegistryConfig = dict[str, bool | str | dict[str, object]]
        type HotReloadConfig = dict[str, FlextTypes.Core.ConfigValue | object]


# =============================================================================
# PUBLIC API EXPORTS - Plugin TypeVars and types
# =============================================================================

__all__: list[str] = [
    "FlextPluginTypes",
]
