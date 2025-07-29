"""FLEXT Plugin Core Types - Core plugin type definitions.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Core type definitions for the plugin system.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from flext_core import FlextProcessingError


class PluginStatus(Enum):
    """Plugin status enumeration."""

    INACTIVE = "inactive"
    ACTIVE = "active"
    LOADING = "loading"
    ERROR = "error"
    DISABLED = "disabled"


class PluginType(Enum):
    """Plugin type enumeration."""

    # Plugin architecture types
    EXTENSION = "extension"
    SERVICE = "service"
    MIDDLEWARE = "middleware"
    TRANSFORMER = "transformer"

    # Plugin integration types
    API = "api"
    DATABASE = "database"
    NOTIFICATION = "notification"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"

    # Plugin utility types
    UTILITY = "utility"
    TOOL = "tool"
    HANDLER = "handler"
    PROCESSOR = "processor"

    # Plugin system types
    CORE = "core"
    ADDON = "addon"
    THEME = "theme"
    LANGUAGE = "language"


class PluginError(FlextProcessingError):
    """Base exception for plugin-related errors."""

    def __init__(self, message: str, plugin_name: str = "", **kwargs: object) -> None:
        """Initialize plugin error.

        Args:
            message: Error message
            plugin_name: Name of the plugin that caused the error
            **kwargs: Additional error context

        """
        super().__init__(message, **kwargs)
        self.plugin_name = plugin_name


class PluginExecutionResult:
    """Result of plugin execution with status and data."""

    def __init__(
        self,
        success: bool = False,
        data: Any = None,
        error: str = "",
        plugin_name: str = "",
        execution_time: float = 0.0,
    ) -> None:
        """Initialize plugin execution result.

        Args:
            success: Whether the execution was successful
            data: Execution result data
            error: Error message if execution failed
            plugin_name: Name of the executed plugin
            execution_time: Time taken for execution in seconds

        """
        self.success = success
        self.data = data
        self.error = error
        self.plugin_name = plugin_name
        self.execution_time = execution_time

    def is_success(self) -> bool:
        """Check if execution was successful."""
        return self.success

    def is_failure(self) -> bool:
        """Check if execution failed."""
        return not self.success


__all__ = [
    "PluginError",
    "PluginExecutionResult",
    "PluginStatus",
    "PluginType",
]
