"""FLEXT Plugin Constants - Plugin system constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Final, Literal

from flext_core import FlextCore


class FlextPluginConstants(FlextCore.Constants):
    """Plugin system-specific constants extending FlextCore.Constants with domain functionality.

    Extends FlextCore.Constants to inherit universal constants while adding plugin-specific
    constants using nested namespace classes. Maintains full inheritance hierarchy.

    Usage:
        ```python
        from flext_plugin import FlextPluginConstants

        # Inherited from FlextCore.Constants
        timeout = FlextPluginConstants.Defaults.TIMEOUT

        # Plugin-specific constants
        plugin_timeout = FlextPluginConstants.Discovery.DEFAULT_TIMEOUT_SECONDS
        plugin_type = FlextPluginConstants.Types.TAP
        error_msg = FlextPluginConstants.PluginMessages.PLUGIN_NOT_FOUND
        security_level = FlextPluginConstants.PluginSecurity.DEFAULT_SECURITY_LEVEL
        success_rate = FlextPluginConstants.PluginPerformance.EXCELLENT_SUCCESS_RATE
        ```
    """

    class Discovery:
        """Plugin discovery and loading configuration."""

        # Use FlextCore.Constants for common timeouts where applicable
        DEFAULT_TIMEOUT_SECONDS: Final[int] = (
            FlextCore.Constants.Network.DEFAULT_TIMEOUT
        )
        DISCOVERY_TIMEOUT_SECONDS: Final[int] = 10

        # Plugin-specific discovery paths
        DEFAULT_PLUGIN_PATHS: ClassVar[FlextCore.Types.StringList] = [
            "/opt/flext/plugins",
            "~/.flext/plugins",
            "./plugins",
        ]

        # Discovery validation
        MIN_PLUGIN_NAME_LENGTH: Final[int] = 3
        MAX_PLUGIN_NAME_LENGTH: Final[int] = 100
        VALID_PLUGIN_NAME_PATTERN: Final[str] = r"^[a-zA-Z][a-zA-Z0-9_-]*$"

        # Discovery methods
        METHOD_FILE_SYSTEM: Final[str] = "file_system"
        METHOD_ENTRY_POINTS: Final[str] = "entry_points"
        METHOD_PACKAGE_SCAN: Final[str] = "package_scan"

    class Types:
        """Plugin type categorization constants."""

        SINGER_PLUGIN_TYPES: ClassVar[Final[set[str]]] = {"TAP", "TARGET", "TRANSFORM"}
        ARCHITECTURE_PLUGIN_TYPES: ClassVar[Final[set[str]]] = {
            "EXTENSION",
            "SERVICE",
            "MIDDLEWARE",
            "TRANSFORMER",
        }
        INTEGRATION_PLUGIN_TYPES: ClassVar[Final[set[str]]] = {
            "API",
            "DATABASE",
            "NOTIFICATION",
            "AUTHENTICATION",
        }
        UTILITY_PLUGIN_TYPES: ClassVar[Final[set[str]]] = {
            "UTILITY",
            "TOOL",
            "HANDLER",
            "PROCESSOR",
        }

        # All valid plugin types combined
        ALL_PLUGIN_TYPES: ClassVar[Final[set[str]]] = (
            SINGER_PLUGIN_TYPES
            | ARCHITECTURE_PLUGIN_TYPES
            | INTEGRATION_PLUGIN_TYPES
            | UTILITY_PLUGIN_TYPES
        )

        # Literal types for plugin types
        PluginTypeLiteral = Literal[
            "tap",
            "target",
            "transform",
            "extension",
            "service",
            "middleware",
            "transformer",
            "api",
            "database",
            "notification",
            "authentication",
            "authorization",
            "utility",
            "tool",
            "handler",
            "processor",
            "core",
            "addon",
            "theme",
            "language",
        ]

        # Type values
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

    class Lifecycle:
        """Plugin lifecycle states and management."""

        PLUGIN_LIFECYCLE_STATES: Final[set[str]] = {
            "UNKNOWN",
            "DISCOVERED",
            "LOADED",
            "ACTIVE",
            "INACTIVE",
            "LOADING",
            "ERROR",
            "DISABLED",
            "HEALTHY",
            "UNHEALTHY",
        }

        # Literal types for plugin status
        PluginStatusLiteral = Literal[
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
        ]

        # Use FlextCore.Constants for worker configuration
        MAX_PLUGIN_WORKERS: Final[int] = FlextCore.Constants.Container.MAX_WORKERS
        MIN_PLUGIN_WORKERS: Final[int] = FlextCore.Constants.Container.MIN_WORKERS
        DEFAULT_WORKERS: Final[int] = FlextCore.Constants.Container.DEFAULT_WORKERS

        # Status values
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

    class PluginSecurity:
        """Plugin security and validation constants."""

        SECURITY_LEVELS: Final[FlextCore.Types.StringList] = [
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
        ]
        DEFAULT_SECURITY_LEVEL: Final[str] = "MEDIUM"

        # Literal types for security levels
        SecurityLevelLiteral = Literal["low", "medium", "high", "critical"]

        # Security levels
        SECURITY_LOW: Final[str] = "low"
        SECURITY_MEDIUM: Final[str] = "medium"
        SECURITY_HIGH: Final[str] = "high"
        SECURITY_CRITICAL: Final[str] = "critical"

        # Permissions
        PERMISSION_NETWORK: Final[str] = "network"
        PERMISSION_FILESYSTEM: Final[str] = "filesystem"
        PERMISSION_DATABASE: Final[str] = "database"
        PERMISSION_EXTERNAL_API: Final[str] = "external_api"

        # Use FlextCore.Constants for security-related timeouts
        SECURITY_SCAN_TIMEOUT: Final[int] = FlextCore.Constants.Network.DEFAULT_TIMEOUT

        # Allowed and blocked imports
        DEFAULT_ALLOWED_IMPORTS: Final[FlextCore.Types.StringList] = [
            "flext_core",
            "flext_plugin",
        ]
        DEFAULT_BLOCKED_IMPORTS: Final[FlextCore.Types.StringList] = [
            "os",
            "sys",
            "subprocess",
            "importlib",
        ]

    class PluginPerformance:
        """Plugin performance and resource limits."""

        # Percentage constants
        PERCENTAGE_MAX: Final[int] = 100
        PERCENTAGE_MIN: Final[int] = 0

        # Success rate thresholds
        EXCELLENT_SUCCESS_RATE: Final[float] = 95.0
        GOOD_SUCCESS_RATE: Final[float] = 90.0
        FAIR_SUCCESS_RATE: Final[float] = 80.0

        # Time thresholds in milliseconds
        EXCELLENT_TIME_MS: Final[int] = 1000
        GOOD_TIME_MS: Final[int] = 2000
        FAIR_TIME_MS: Final[int] = 5000

        # Execution time conversion
        EXECUTION_TIME_SCALE_MS_TO_S: Final[int] = 1000

        # Production ready limits
        READY_TIMEOUT_SECONDS: Final[int] = 300
        READY_MAX_MEMORY_MB: Final[int] = 1024

        # Concurrent loading thresholds
        MAX_CONCURRENT_LOADS_WARNING_THRESHOLD: Final[int] = 20

        # Memory limits
        MINIMUM_MEMORY_LIMIT_MB: Final[int] = 64

        # Execution timeouts
        MAXIMUM_EXECUTION_TIMEOUT_SECONDS: Final[int] = 3600  # 1 hour

        # Default performance values
        DEFAULT_MAX_CPU_PERCENT: Final[int] = 50  # Alias for compatibility
        DEFAULT_MAX_CONCURRENT_PLUGINS: Final[int] = 10

    class Execution:
        """Plugin execution and runtime constants."""

        # Execution states
        STATE_PENDING: Final[str] = "pending"
        STATE_RUNNING: Final[str] = "running"
        STATE_COMPLETED: Final[str] = "completed"
        STATE_FAILED: Final[str] = "failed"
        STATE_CANCELLED: Final[str] = "cancelled"

    class Registry:
        """Plugin registry and management constants."""

        # Registry types
        TYPE_LOCAL: Final[str] = "local"
        TYPE_REMOTE: Final[str] = "remote"
        TYPE_HYBRID: Final[str] = "hybrid"

        # Default registry settings
        DEFAULT_SYNC_INTERVAL: Final[int] = 3600

    class HotReload:
        """Hot reload configuration constants."""

        DEFAULT_INTERVAL_SECONDS: Final[int] = 2
        DEBOUNCE_MS: Final[int] = 500
        MAX_RETRIES: Final[int] = FlextCore.Constants.Reliability.MAX_RETRY_ATTEMPTS

        # Watch events
        EVENT_CREATED: Final[str] = "created"
        EVENT_MODIFIED: Final[str] = "modified"
        EVENT_DELETED: Final[str] = "deleted"
        EVENT_MOVED: Final[str] = "moved"

    class Monitoring:
        """Plugin monitoring and observability constants."""

        # Log levels
        LOG_LEVELS: Final[FlextCore.Types.StringList] = [
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ]
        DEFAULT_LOG_LEVEL: Final[str] = "INFO"

        # Literal types for log levels
        LogLevelLiteral = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        # Default monitoring settings
        DEFAULT_RETENTION_DAYS: Final[int] = 30
        MIN_RETENTION_DAYS: Final[int] = 1
        MAX_RETENTION_DAYS: Final[int] = 365

        # Default alert thresholds
        DEFAULT_CPU_THRESHOLD: Final[float] = 80.0
        DEFAULT_MEMORY_THRESHOLD: Final[float] = 85.0
        DEFAULT_ERROR_RATE_THRESHOLD: Final[float] = 5.0
        DEFAULT_RESPONSE_TIME_THRESHOLD: Final[float] = 5000.0

    class Files:
        """Plugin file extension and directory constants."""

        # Plugin file extensions
        PYTHON_EXTENSION: Final[str] = FlextCore.Constants.Platform.EXT_PYTHON
        YAML_CONFIG_EXTENSION: Final[str] = FlextCore.Constants.Platform.EXT_YAML
        JSON_CONFIG_EXTENSION: Final[str] = FlextCore.Constants.Platform.EXT_JSON
        TOML_CONFIG_EXTENSION: Final[str] = FlextCore.Constants.Platform.EXT_TOML

        # Directory structure
        DEFAULT_PLUGIN_DIR: Final[str] = "plugins"
        DEFAULT_CACHE_DIR: Final[str] = ".plugin_cache"
        DEFAULT_CONFIG_DIR: Final[str] = FlextCore.Constants.Platform.DIR_CONFIG

    class PluginValidation:
        """Plugin validation patterns and rules."""

        # Regex patterns
        PLUGIN_NAME_PATTERN: Final[str] = r"^[a-zA-Z][a-zA-Z0-9_-]*$"
        VERSION_PATTERN: Final[str] = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$"
        SECURITY_LEVEL_PATTERN: Final[str] = r"^(low|medium|high|critical)$"
        LOG_LEVEL_PATTERN: Final[str] = r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"

        # Validation limits
        MAX_DEPENDENCIES: Final[int] = 50
        MAX_PLUGIN_NAME_LENGTH: Final[int] = 100
        MIN_PLUGIN_NAME_LENGTH: Final[int] = 3
        MAX_DESCRIPTION_LENGTH: Final[int] = 1000
        MAX_AUTHOR_LENGTH: Final[int] = 200

        # Priority limits
        MIN_PRIORITY: Final[int] = 0
        MAX_PRIORITY: Final[int] = 100

    class PluginMessages:
        """Plugin-specific error and status messages."""

        PLUGIN_NOT_FOUND: Final[str] = "Plugin '{plugin_name}' not found"
        PLUGIN_ALREADY_EXISTS: Final[str] = "Plugin '{plugin_name}' already exists"
        PLUGIN_LOAD_FAILED: Final[str] = (
            "Failed to load plugin '{plugin_name}': {error}"
        )
        PLUGIN_INVALID_NAME: Final[str] = "Invalid plugin name '{plugin_name}'"

        # Success messages
        PLUGIN_LOADED_SUCCESS: Final[str] = "Plugin '{plugin_name}' loaded successfully"
        PLUGIN_ACTIVATED_SUCCESS: Final[str] = (
            "Plugin '{plugin_name}' activated successfully"
        )

        # Validation messages
        TOO_MANY_DEPENDENCIES: Final[str] = "Too many dependencies (max 50)"
        INVALID_DEPENDENCY_FORMAT: Final[str] = "Invalid dependency name format: {dep}"
        PLUGIN_CANNOT_BE_ACTIVE_WHEN_DISABLED: Final[str] = (
            "Plugin cannot be ACTIVE when disabled"
        )
        PLUGIN_CANNOT_DEPEND_ON_ITSELF: Final[str] = "Plugin cannot depend on itself"
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
        THRESHOLD_CANNOT_BE_NEGATIVE: Final[str] = "Threshold {key} cannot be negative"
        INVALID_LOG_LEVEL: Final[str] = "Invalid log level: {level}"
        RETENTION_DAYS_MUST_BE_BETWEEN_1_AND_365: Final[str] = (
            "Retention days must be between 1 and 365"
        )
        AT_LEAST_ONE_PLUGIN_PATH_MUST_BE_SPECIFIED: Final[str] = (
            "At least one plugin path must be specified"
        )
        TIMEOUT_MUST_BE_POSITIVE: Final[str] = "Timeout must be positive"
        WATCH_INTERVAL_MUST_BE_POSITIVE: Final[str] = "Watch interval must be positive"
        DEBOUNCE_TIME_CANNOT_BE_NEGATIVE: Final[str] = (
            "Debounce time cannot be negative"
        )
        CPU_PERCENTAGE_MUST_BE_BETWEEN_0_AND_100: Final[str] = (
            "CPU percentage must be between 0 and 100"
        )
        SYNC_INTERVAL_MUST_BE_POSITIVE: Final[str] = "Sync interval must be positive"


__all__ = ["FlextPluginConstants"]
