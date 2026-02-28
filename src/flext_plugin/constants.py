"""FLEXT Plugin Constants - constant definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum
from typing import ClassVar, Final

from flext_core import FlextConstants


class FlextPluginConstants(FlextConstants):
    """plugin constants with Python 3.13+ patterns.

    Usage:
    ```python
    from flext_plugin.constants import FlextPluginConstants

    timeout = FlextPluginConstants.Plugin.Discovery.DEFAULT_TIMEOUT_SECONDS
    plugin_type = FlextPluginConstants.Plugin.PluginType.TAP
    ```
    """

    class Plugin:
        """Plugin domain constants namespace.

        All plugin-specific constants are organized here for better namespace
        organization and to enable composition with other domain constants.
        """

        # Discovery constants
        class Discovery:
            """Discovery-related constants."""

            DEFAULT_TIMEOUT_SECONDS: Final[int] = FlextConstants.Network.DEFAULT_TIMEOUT
            DISCOVERY_TIMEOUT_SECONDS: Final[int] = 10
            DEFAULT_PLUGIN_PATHS: Final[list[str]] = [
                "/opt/flext/plugins",
                "~/.flext/plugins",
                "./plugins",
            ]
            MIN_PLUGIN_NAME_LENGTH: Final[int] = 3
            MAX_PLUGIN_NAME_LENGTH: Final[int] = 100
            VALID_PLUGIN_NAME_PATTERN: Final[str] = r"^[a-zA-Z][a-zA-Z0-9_-]*$"
            METHOD_FILE_SYSTEM: Final[str] = "file_system"
            METHOD_ENTRY_POINTS: Final[str] = "entry_points"
            METHOD_PACKAGE_SCAN: Final[str] = "package_scan"

        class PluginType(StrEnum):
            """Plugin type enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use PluginType.TAP.value
                or PluginType.TAP directly - no base strings needed.
            """

            # Singer platform types
            TAP = "tap"
            TARGET = "target"
            TRANSFORM = "transform"
            # Architecture types
            EXTENSION = "extension"
            SERVICE = "service"
            MIDDLEWARE = "middleware"
            TRANSFORMER = "transformer"
            # Integration types
            API = "api"
            DATABASE = "database"
            NOTIFICATION = "notification"
            AUTHENTICATION = "authentication"
            AUTHORIZATION = "authorization"
            # Utility types
            UTILITY = "utility"
            TOOL = "tool"
            HANDLER = "handler"
            PROCESSOR = "processor"
            # Other types
            CORE = "core"
            ADDON = "addon"
            THEME = "theme"
            LANGUAGE = "language"

        # ═══════════════════════════════════════════════════════════════════
        # LITERAL TYPES: PEP 695 strict type aliases (Python 3.13+)
        # ═══════════════════════════════════════════════════════════════════
        # All Literal types reference StrEnum members - NO string duplication!

        # PluginTypeLiteral moved to typings.py (t.Plugin.PluginTypeLiteral)
        # PluginStatusLiteral defined after PluginStatus class - see below

        # Plugin types with frozensets
        class Types:
            """Plugin type constants."""

            # Plugin type frozensets (backward compatibility)
            # Note: Values MUST match PluginType StrEnum values exactly.
            # For new code, use PluginType enum directly (e.g., PluginType.TAP).
            # Generated from PluginType StrEnum members (DRY principle) - will be set after enum definition
            SINGER_PLUGIN_TYPES: ClassVar[frozenset[str]]
            ARCHITECTURE_PLUGIN_TYPES: ClassVar[frozenset[str]]
            INTEGRATION_PLUGIN_TYPES: ClassVar[frozenset[str]]
            UTILITY_PLUGIN_TYPES: ClassVar[frozenset[str]]
            ALL_PLUGIN_TYPES: ClassVar[frozenset[str]]

            # PluginTypeLiteral moved to Plugin level - see below

            # Type values as constants (backward compatibility)
            # Note: These values MUST match PluginType StrEnum values exactly.
            # For new code, use PluginType enum directly (e.g., PluginType.TAP.value).
            TYPE_TAP: Final[str] = "tap"
            TYPE_TARGET: Final[str] = "target"
            TYPE_TRANSFORM: Final[str] = "transform"
            TYPE_EXTENSION: Final[str] = "extension"
            TYPE_SERVICE: Final[str] = "service"
            TYPE_MIDDLEWARE: Final[str] = "middleware"
            TYPE_TRANSFORMER: Final[str] = "transformer"
            TYPE_API: Final[str] = "api"
            TYPE_DATABASE: Final[str] = "database"
            TYPE_NOTIFICATION: Final[str] = "notification"
            TYPE_AUTHENTICATION: Final[str] = "authentication"
            TYPE_AUTHORIZATION: Final[str] = "authorization"
            TYPE_UTILITY: Final[str] = "utility"
            TYPE_TOOL: Final[str] = "tool"
            TYPE_HANDLER: Final[str] = "handler"
            TYPE_PROCESSOR: Final[str] = "processor"
            TYPE_CORE: Final[str] = "core"
            TYPE_ADDON: Final[str] = "addon"
            TYPE_THEME: Final[str] = "theme"
            TYPE_LANGUAGE: Final[str] = "language"

        # Lifecycle constants
        class Lifecycle:
            """Plugin lifecycle state constants."""

            # PluginStatusLiteral moved to Plugin level - see below

            MAX_PLUGIN_WORKERS: Final[int] = 10
            MIN_PLUGIN_WORKERS: Final[int] = 1
            DEFAULT_WORKERS: Final[int] = 4

            # Status values as constants (backward compatibility)
            # Note: These values MUST match PluginStatus StrEnum values exactly.
            # For new code, use PluginStatus enum directly (e.g., PluginStatus.UNKNOWN.value).
            STATUS_UNKNOWN: Final[str] = "unknown"
            STATUS_DISCOVERED: Final[str] = "discovered"
            STATUS_LOADED: Final[str] = "loaded"
            STATUS_ACTIVE: Final[str] = "active"
            STATUS_INACTIVE: Final[str] = "inactive"
            STATUS_LOADING: Final[str] = "loading"
            STATUS_ERROR: Final[str] = "error"
            STATUS_DISABLED: Final[str] = "disabled"
            STATUS_HEALTHY: Final[str] = "healthy"
            STATUS_UNHEALTHY: Final[str] = "unhealthy"
            # Additional status constants from platform.py
            STATUS_UNLOADED: Final[str] = "unloaded"
            PLUGIN_LIFECYCLE_STATES: Final[frozenset[str]] = frozenset({
                "unknown",
                "discovered",
                "loaded",
                "active",
                "inactive",
                "loading",
                "error",
                "disabled",
                "healthy",
                "unhealthy",
            })

        # Entity constants
        class Entities:
            """Entity-related constants."""

            SEMANTIC_VERSION_PARTS: Final[int] = 3
            # Field validation constants
            PLUGIN_NAME_MAX_LENGTH: Final[int] = 255
            PLUGIN_VERSION_MAX_LENGTH: Final[int] = 50
            PLUGIN_VERSION_MIN_LENGTH: Final[int] = 1

            # Generated from PluginStatus StrEnum (DRY principle)
            # Note: PluginStatus enum is defined later in the file, generated after definition
            PLUGIN_LIFECYCLE_STATES: ClassVar[frozenset[str]]

        # Security constants
        class PluginSecurity:
            """Plugin security level constants."""

            SECURITY_LEVELS: Final[list[str]] = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
            DEFAULT_SECURITY_LEVEL: Final[str] = "MEDIUM"
            # SecurityLevelLiteral moved to typings.py (t.Security.SecurityLevelLiteral)

            SECURITY_LOW: Final[str] = "low"
            SECURITY_MEDIUM: Final[str] = "medium"
            SECURITY_HIGH: Final[str] = "high"
            SECURITY_CRITICAL: Final[str] = "critical"

            PERMISSION_NETWORK: Final[str] = "network"
            PERMISSION_FILESYSTEM: Final[str] = "filesystem"
            PERMISSION_DATABASE: Final[str] = "database"
            PERMISSION_EXTERNAL_API: Final[str] = "external_api"

            SECURITY_SCAN_TIMEOUT: Final[int] = FlextConstants.Network.DEFAULT_TIMEOUT
            DEFAULT_ALLOWED_IMPORTS: Final[list[str]] = ["flext_core", "flext_plugin"]
            DEFAULT_BLOCKED_IMPORTS: Final[list[str]] = [
                "os",
                "sys",
                "subprocess",
                "importlib",
            ]

        # Performance constants
        class PluginPerformance:
            """Plugin performance metric constants."""

            PERCENTAGE_MAX: Final[int] = 100
            PERCENTAGE_MIN: Final[int] = 0
            EXCELLENT_SUCCESS_RATE: Final[float] = 95.0
            GOOD_SUCCESS_RATE: Final[float] = 90.0
            FAIR_SUCCESS_RATE: Final[float] = 80.0
            EXCELLENT_TIME_MS: Final[int] = 1000
            GOOD_TIME_MS: Final[int] = 2000
            FAIR_TIME_MS: Final[int] = 5000
            EXECUTION_TIME_SCALE_MS_TO_S: Final[int] = 1000
            READY_TIMEOUT_SECONDS: Final[int] = 300
            READY_MAX_MEMORY_MB: Final[int] = 1024
            MAX_CONCURRENT_LOADS_WARNING_THRESHOLD: Final[int] = 20
            MINIMUM_MEMORY_LIMIT_MB: Final[int] = 64
            MAXIMUM_EXECUTION_TIMEOUT_SECONDS: Final[int] = 3600
            DEFAULT_MAX_CPU_PERCENT: Final[int] = 50
            DEFAULT_MAX_CONCURRENT_PLUGINS: Final[int] = 10

        # Execution constants
        class Execution:
            """Execution state constants."""

            STATE_PENDING: Final[str] = "pending"
            STATE_RUNNING: Final[str] = "running"
            STATE_COMPLETED: Final[str] = "completed"
            STATE_FAILED: Final[str] = "failed"
            STATE_CANCELLED: Final[str] = "cancelled"

        # Registry constants
        class Registry:
            """Registry type constants."""

            TYPE_LOCAL: Final[str] = "local"
            TYPE_REMOTE: Final[str] = "remote"
            TYPE_HYBRID: Final[str] = "hybrid"
            DEFAULT_SYNC_INTERVAL: Final[int] = 3600

        # Hot reload constants
        class HotReload:
            """Hot reload configuration constants."""

            DEFAULT_INTERVAL_SECONDS: Final[int] = 2
            DEBOUNCE_MS: Final[int] = 500
            MAX_RETRIES: Final[int] = FlextConstants.Reliability.MAX_RETRY_ATTEMPTS
            EVENT_CREATED: Final[str] = "created"
            EVENT_MODIFIED: Final[str] = "modified"
            EVENT_DELETED: Final[str] = "deleted"
            EVENT_MOVED: Final[str] = "moved"

        # Monitoring constants
        class Monitoring:
            """Monitoring configuration constants."""

            LOG_LEVELS: Final[list[str]] = [
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ]
            DEFAULT_LOG_LEVEL: Final[str] = "INFO"
            # Log level literal - reuse from flext-core (no duplication)
            type LogLevelLiteral = FlextConstants.Literals.LogLevelLiteral
            """Log level literal - references flext-core."""
            DEFAULT_RETENTION_DAYS: Final[int] = 30
            MIN_RETENTION_DAYS: Final[int] = 1
            MAX_RETENTION_DAYS: Final[int] = 365
            DEFAULT_CPU_THRESHOLD: Final[float] = 80.0
            DEFAULT_MEMORY_THRESHOLD: Final[float] = 85.0
            DEFAULT_ERROR_RATE_THRESHOLD: Final[float] = 5.0
            DEFAULT_RESPONSE_TIME_THRESHOLD: Final[float] = 5000.0

        # Files constants
        class Files:
            """File extension constants."""

            PYTHON_EXTENSION: Final[str] = FlextConstants.Platform.EXT_PYTHON
            YAML_CONFIG_EXTENSION: Final[str] = FlextConstants.Platform.EXT_YAML
            JSON_CONFIG_EXTENSION: Final[str] = FlextConstants.Platform.EXT_JSON
            TOML_CONFIG_EXTENSION: Final[str] = FlextConstants.Platform.EXT_TOML
            DEFAULT_PLUGIN_DIR: Final[str] = "plugins"
            DEFAULT_CACHE_DIR: Final[str] = ".plugin_cache"
            DEFAULT_CONFIG_DIR: Final[str] = FlextConstants.Platform.DIR_CONFIG

        # Validation constants
        class PluginValidation:
            """Plugin validation pattern constants."""

            PLUGIN_NAME_PATTERN: Final[str] = r"^[a-zA-Z][a-zA-Z0-9_-]*$"
            VERSION_PATTERN: Final[str] = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$"
            SECURITY_LEVEL_PATTERN: Final[str] = r"^(low|medium|high|critical)$"
            LOG_LEVEL_PATTERN: Final[str] = r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
            MAX_DEPENDENCIES: Final[int] = 50
            MAX_PLUGIN_NAME_LENGTH: Final[int] = 100
            MIN_PLUGIN_NAME_LENGTH: Final[int] = 3
            MAX_DESCRIPTION_LENGTH: Final[int] = 1000
            MAX_AUTHOR_LENGTH: Final[int] = 200
            MIN_PRIORITY: Final[int] = 0
            MAX_PRIORITY: Final[int] = 100

        # Message constants
        class PluginMessages:
            """Plugin error message constants."""

            PLUGIN_NOT_FOUND: Final[str] = "Plugin '{plugin_name}' not found"
            PLUGIN_ALREADY_EXISTS: Final[str] = "Plugin '{plugin_name}' already exists"
            PLUGIN_LOAD_FAILED: Final[str] = (
                "Failed to load plugin '{plugin_name}': {error}"
            )
            PLUGIN_INVALID_NAME: Final[str] = "Invalid plugin name '{plugin_name}'"
            PLUGIN_LOADED_SUCCESS: Final[str] = (
                "Plugin '{plugin_name}' loaded successfully"
            )
            PLUGIN_ACTIVATED_SUCCESS: Final[str] = (
                "Plugin '{plugin_name}' activated successfully"
            )
            TOO_MANY_DEPENDENCIES: Final[str] = "Too many dependencies (max 50)"
            INVALID_DEPENDENCY_FORMAT: Final[str] = (
                "Invalid dependency name format: {dep}"
            )
            PLUGIN_CANNOT_BE_ACTIVE_WHEN_DISABLED: Final[str] = (
                "Plugin cannot be ACTIVE when disabled"
            )
            PLUGIN_CANNOT_DEPEND_ON_ITSELF: Final[str] = (
                "Plugin cannot depend on itself"
            )
            PRIORITY_MUST_BE_BETWEEN_0_AND_100: Final[str] = (
                "Priority must be between 0 and 100"
            )
            MEMORY_LIMIT_EXCEEDS_MAXIMUM: Final[str] = (
                "Memory limit exceeds production maximum: 1024MB"
            )
            MEMORY_LIMIT_TOO_LOW: Final[str] = "Memory limit too low (minimum 64MB)"
            INVALID_SECURITY_LEVEL: Final[str] = "Invalid security level: {level}"
            MISSING_REQUIRED_THRESHOLDS: Final[str] = (
                "Missing required thresholds: {missing}"
            )
            PERCENTAGE_THRESHOLD_MUST_BE_0_100: Final[str] = (
                "Percentage threshold {key} must be 0-100"
            )
            THRESHOLD_CANNOT_BE_NEGATIVE: Final[str] = (
                "Threshold {key} cannot be negative"
            )
            INVALID_LOG_LEVEL: Final[str] = "Invalid log level: {level}"
            RETENTION_DAYS_MUST_BE_BETWEEN_1_AND_365: Final[str] = (
                "Retention days must be between 1 and 365"
            )
            AT_LEAST_ONE_PLUGIN_PATH_MUST_BE_SPECIFIED: Final[str] = (
                "At least one plugin path must be specified"
            )
            TIMEOUT_MUST_BE_POSITIVE: Final[str] = "Timeout must be positive"
            WATCH_INTERVAL_MUST_BE_POSITIVE: Final[str] = (
                "Watch interval must be positive"
            )
            DEBOUNCE_TIME_CANNOT_BE_NEGATIVE: Final[str] = (
                "Debounce time cannot be negative"
            )
            CPU_PERCENTAGE_MUST_BE_BETWEEN_0_AND_100: Final[str] = (
                "CPU percentage must be between 0 and 100"
            )
            SYNC_INTERVAL_MUST_BE_POSITIVE: Final[str] = (
                "Sync interval must be positive"
            )

        class PluginStatus(StrEnum):
            """Plugin lifecycle and operational status enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use PluginStatus.UNKNOWN.value
                or PluginStatus.UNKNOWN directly - no base strings needed.
            """

            UNKNOWN = "unknown"
            DISCOVERED = "discovered"
            LOADED = "loaded"
            ACTIVE = "active"
            INACTIVE = "inactive"
            LOADING = "loading"
            ERROR = "error"
            DISABLED = "disabled"
            HEALTHY = "healthy"
            UNHEALTHY = "unhealthy"

            @classmethod
            def get_operational_statuses(
                cls,
            ) -> list[FlextPluginConstants.Plugin.PluginStatus]:
                """Get statuses representing operational states."""
                return [cls.ACTIVE, cls.HEALTHY, cls.LOADED]

            @classmethod
            def get_error_statuses(
                cls,
            ) -> list[FlextPluginConstants.Plugin.PluginStatus]:
                """Get statuses representing error states."""
                return [cls.ERROR, cls.UNHEALTHY, cls.DISABLED]

            def is_operational(self) -> bool:
                """Check if status represents operational state."""
                return self in self.get_operational_statuses()

            def is_error_state(self) -> bool:
                """Check if status represents error state."""
                return self in self.get_error_statuses()

        # ═══════════════════════════════════════════════════════════════════
        # LITERAL TYPES: PEP 695 strict type aliases (Python 3.13+)
        # ═══════════════════════════════════════════════════════════════════
        # PluginStatusLiteral moved to typings.py (t.Plugin.PluginStatusLiteral)

        # Generate plugin type frozensets from PluginType StrEnum (DRY principle)
        Types.SINGER_PLUGIN_TYPES = frozenset({
            PluginType.TAP.value,
            PluginType.TARGET.value,
            PluginType.TRANSFORM.value,
        })
        Types.ARCHITECTURE_PLUGIN_TYPES = frozenset({
            PluginType.EXTENSION.value,
            PluginType.SERVICE.value,
            PluginType.MIDDLEWARE.value,
            PluginType.TRANSFORMER.value,
        })
        Types.INTEGRATION_PLUGIN_TYPES = frozenset({
            PluginType.API.value,
            PluginType.DATABASE.value,
            PluginType.NOTIFICATION.value,
            PluginType.AUTHENTICATION.value,
        })
        Types.UTILITY_PLUGIN_TYPES = frozenset({
            PluginType.UTILITY.value,
            PluginType.TOOL.value,
            PluginType.HANDLER.value,
            PluginType.PROCESSOR.value,
        })
        Types.ALL_PLUGIN_TYPES = (
            Types.SINGER_PLUGIN_TYPES
            | Types.ARCHITECTURE_PLUGIN_TYPES
            | Types.INTEGRATION_PLUGIN_TYPES
            | Types.UTILITY_PLUGIN_TYPES
        )
        """All plugin types - union of all plugin type frozensets."""


c = FlextPluginConstants

__all__ = ["FlextPluginConstants", "c"]
