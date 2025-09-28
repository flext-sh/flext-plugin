"""FLEXT Plugin Constants - Plugin system constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Final

from flext_core import FlextConstants


class FlextPluginConstants:
    """Plugin system-specific constants following FLEXT single-class pattern.

    Inherits from FlextConstants for universal constants, defines only
    plugin-specific constants using nested namespace classes.

    Usage:
        ```python
        from flext_plugin import FlextPluginConstants

        timeout = FlextPluginConstants.Discovery.DEFAULT_TIMEOUT_SECONDS
        plugin_type = FlextPluginConstants.Types.TAP
        ```
    """

    # Project metadata (Final attributes inherited from FlextConstants)
    # CONSTANTS_VERSION, PROJECT_PREFIX, PROJECT_NAME inherited from FlextConstants

    class Discovery:
        """Plugin discovery and loading configuration."""

        # Use FlextConstants for common timeouts where applicable
        DEFAULT_TIMEOUT_SECONDS: Final[int] = FlextConstants.Network.DEFAULT_TIMEOUT
        DISCOVERY_TIMEOUT_SECONDS: Final[int] = 10

        # Plugin-specific discovery paths
        DEFAULT_PLUGIN_PATHS: ClassVar[list[str]] = [
            "/opt/flext/plugins",
            "~/.flext/plugins",
            "./plugins",
        ]

        # Discovery validation
        MIN_PLUGIN_NAME_LENGTH: Final[int] = 3
        MAX_PLUGIN_NAME_LENGTH: Final[int] = 100
        VALID_PLUGIN_NAME_PATTERN: Final[str] = r"^[a-zA-Z][a-zA-Z0-9_-]*$"

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

        # Use FlextConstants for worker configuration
        MAX_PLUGIN_WORKERS: Final[int] = FlextConstants.Container.MAX_WORKERS
        MIN_PLUGIN_WORKERS: Final[int] = FlextConstants.Container.MIN_WORKERS
        DEFAULT_WORKERS: Final[int] = FlextConstants.Container.DEFAULT_WORKERS

    class HotReload:
        """Hot reload configuration constants."""

        DEFAULT_INTERVAL_SECONDS: Final[int] = 2
        DEBOUNCE_MS: Final[int] = 500
        MAX_RETRIES: Final[int] = FlextConstants.Reliability.MAX_RETRY_ATTEMPTS

    class Files:
        """Plugin file extension and directory constants."""

        # Plugin file extensions
        PYTHON_EXTENSION: Final[str] = FlextConstants.Platform.EXT_PYTHON
        YAML_CONFIG_EXTENSION: Final[str] = FlextConstants.Platform.EXT_YAML
        JSON_CONFIG_EXTENSION: Final[str] = FlextConstants.Platform.EXT_JSON
        TOML_CONFIG_EXTENSION: Final[str] = FlextConstants.Platform.EXT_TOML

        # Directory structure
        DEFAULT_PLUGIN_DIR: Final[str] = "plugins"
        DEFAULT_CACHE_DIR: Final[str] = ".plugin_cache"
        DEFAULT_CONFIG_DIR: Final[str] = FlextConstants.Platform.DIR_CONFIG

    class Messages:
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

    class Security:
        """Plugin security-related constants."""

        SECURITY_LEVELS: Final[list[str]] = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        DEFAULT_SECURITY_LEVEL: Final[str] = "MEDIUM"

        # Use FlextConstants for security-related timeouts
        SECURITY_SCAN_TIMEOUT: Final[int] = FlextConstants.Network.DEFAULT_TIMEOUT

    class Performance:
        """Plugin performance and resource limits."""

        # Concurrent loading thresholds
        MAX_CONCURRENT_LOADS_WARNING_THRESHOLD: Final[int] = 20

        # Memory limits
        MINIMUM_MEMORY_LIMIT_MB: Final[int] = 64

        # Execution timeouts
        MAXIMUM_EXECUTION_TIMEOUT_SECONDS: Final[int] = 3600  # 1 hour


__all__ = ["FlextPluginConstants"]
