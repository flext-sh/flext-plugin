"""FLEXT Plugin Constants - constant definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import ClassVar, Final

from flext_cli import c


class FlextPluginConstants(c):
    """plugin constants with Python 3.13+ patterns.

    Usage:
    ```python
    from flext_plugin import FlextPluginConstants, t

    timeout = FlextPluginConstants.DEFAULT_TIMEOUT_SECONDS
    plugin_type = FlextPluginConstants.Plugin.Type.TAP
    ```
    """

    class Plugin:
        """Plugin domain constants namespace.

        All plugin-specific constants are organized here for better namespace
        organization and to enable composition with other domain constants.
        """

        DEFAULT_PLUGIN_VERSION: Final[str] = "1.0.0"

        @unique
        class Type(StrEnum):
            """Plugin type enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use Type.TAP.value
                or Type.TAP directly - no base strings needed.
            """

            TAP = "tap"
            TARGET = "target"
            TRANSFORM = "transform"
            EXTENSION = "extension"
            SERVICE = "service"
            MIDDLEWARE = "middleware"
            TRANSFORMER = "transformer"
            API = "api"
            DATABASE = "database"
            NOTIFICATION = "notification"
            AUTHENTICATION = "authentication"
            AUTHORIZATION = "authorization"
            UTILITY = "utility"
            TOOL = "tool"
            HANDLER = "handler"
            PROCESSOR = "processor"
            CORE = "core"
            ADDON = "addon"
            THEME = "theme"
            LANGUAGE = "language"

        SINGER_PLUGIN_TYPES: ClassVar[frozenset[str]] = frozenset({
            Type.TAP,
            Type.TARGET,
            Type.TRANSFORM,
        })
        ARCHITECTURE_PLUGIN_TYPES: ClassVar[frozenset[str]] = frozenset({
            Type.CORE,
            Type.ADDON,
            Type.THEME,
            Type.LANGUAGE,
        })
        INTEGRATION_PLUGIN_TYPES: ClassVar[frozenset[str]] = frozenset({
            Type.SERVICE,
            Type.MIDDLEWARE,
            Type.API,
            Type.DATABASE,
            Type.NOTIFICATION,
            Type.AUTHENTICATION,
            Type.AUTHORIZATION,
        })
        UTILITY_PLUGIN_TYPES: ClassVar[frozenset[str]] = frozenset({
            Type.EXTENSION,
            Type.TRANSFORMER,
            Type.UTILITY,
            Type.TOOL,
            Type.HANDLER,
            Type.PROCESSOR,
        })
        ALL_PLUGIN_TYPES: ClassVar[frozenset[str]] = frozenset({
            *SINGER_PLUGIN_TYPES,
            *ARCHITECTURE_PLUGIN_TYPES,
            *INTEGRATION_PLUGIN_TYPES,
            *UTILITY_PLUGIN_TYPES,
        })

        SECURITY_MEDIUM: Final[str] = "medium"

        class Execution:
            """Execution state constants."""

            STATE_PENDING: Final[str] = "pending"
            STATE_RUNNING: Final[str] = "running"
            STATE_COMPLETED: Final[str] = "completed"
            STATE_FAILED: Final[str] = "failed"
            STATE_CANCELLED: Final[str] = "cancelled"
            RESULT_EXECUTED: Final[str] = "executed"
            LOAD_TYPE_FILE: Final = "file"
            LOAD_TYPE_DIRECTORY: Final = "directory"
            LOAD_TYPE_ENTRY_POINT: Final = "entry_point"

        class Registry:
            """Registry type constants."""

            TYPE_LOCAL: Final[str] = "local"
            TYPE_REMOTE: Final[str] = "remote"
            TYPE_HYBRID: Final[str] = "hybrid"
            DEFAULT_SYNC_INTERVAL: Final[int] = 3600

        class Files:
            """File extension constants."""

            PYTHON_EXTENSION: Final[str] = ".py"
            YAML_CONFIG_EXTENSION: Final[str] = ".yaml"
            JSON_CONFIG_EXTENSION: Final[str] = ".json"
            TOML_CONFIG_EXTENSION: Final[str] = ".toml"
            DEFAULT_PLUGIN_DIR: Final[str] = "plugins"
            DEFAULT_CACHE_DIR: Final[str] = ".plugin_cache"
            DEFAULT_CONFIG_DIR: Final[str] = c.Directory.CONFIG.value
            DEFAULT_CONFIG_FILE: Final[str] = "plugin.yaml"
            CONFIG_SCHEMA_VERSION: Final[str] = "1.0"

        class PluginValidation:
            """Plugin validation pattern constants."""

            PLUGIN_NAME_PATTERN: Final[str] = "^[a-zA-Z][a-zA-Z0-9_-]*$"
            VERSION_PATTERN: Final[str] = "^\\d+\\.\\d+\\.\\d+(-[a-zA-Z0-9]+)?$"
            SECURITY_LEVEL_PATTERN: Final[str] = "^(low|medium|high|critical)$"
            LOG_LEVEL_PATTERN: Final[str] = "^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
            MAX_DEPENDENCIES: Final[int] = 50
            MAX_PLUGIN_NAME_LENGTH: Final[int] = 100
            MIN_PLUGIN_NAME_LENGTH: Final[int] = 3
            MAX_DESCRIPTION_LENGTH: Final[int] = 1000
            MAX_AUTHOR_LENGTH: Final[int] = 200
            MIN_PRIORITY: Final[int] = 0
            MAX_PRIORITY: Final[int] = 100

        @unique
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
            def get_error_statuses(cls) -> frozenset[str]:
                """Get error status values."""
                return frozenset({cls.ERROR, cls.UNHEALTHY, cls.DISABLED})

            @classmethod
            def get_operational_statuses(cls) -> frozenset[str]:
                """Get operational status values."""
                return frozenset({cls.ACTIVE, cls.HEALTHY, cls.LOADED})

            def is_error_state(self) -> bool:
                """Check if status is an error state."""
                return self in self.get_error_statuses()

            def is_operational(self) -> bool:
                """Check if status is operational."""
                return self in self.get_operational_statuses()

        "All plugin types - union of all plugin type frozensets."
        OPERATIONAL_STATUSES: ClassVar[frozenset[str]] = frozenset({
            PluginStatus.ACTIVE,
            PluginStatus.HEALTHY,
            PluginStatus.LOADED,
        })
        ERROR_STATUSES: ClassVar[frozenset[str]] = frozenset({
            PluginStatus.ERROR,
            PluginStatus.UNHEALTHY,
            PluginStatus.DISABLED,
        })

        @unique
        class DiscoveryTypeLiteral(StrEnum):
            """Discovery type literal enumeration."""

            FILE = "file"
            DIRECTORY = "directory"
            ENTRY_POINT = "entry_point"

        @unique
        class DiscoveryMethodLiteral(StrEnum):
            """Discovery method literal enumeration."""

            FILE_SYSTEM = "file_system"
            ENTRY_POINTS = "entry_points"


c = FlextPluginConstants
__all__: tuple[str, ...] = ("FlextPluginConstants", "c")
