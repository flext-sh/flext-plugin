"""Centralized constants following flext-core patterns for consistency.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextConstants


class FlextPluginConstants(FlextConstants):
    """Plugin-specific constants extending FlextConstants."""

    # Plugin System Configuration
    DEFAULT_PLUGIN_TIMEOUT_SECONDS = 30
    DEFAULT_DISCOVERY_TIMEOUT_SECONDS = 10
    DEFAULT_HOT_RELOAD_INTERVAL_SECONDS = 2
    MAX_PLUGIN_WORKERS = 10
    MIN_PLUGIN_WORKERS = 1

    # Plugin File Extensions
    PYTHON_PLUGIN_EXTENSION = ".py"
    YAML_CONFIG_EXTENSION = ".yml"
    JSON_CONFIG_EXTENSION = ".json"
    TOML_CONFIG_EXTENSION = ".toml"

    # Plugin Directory Names
    DEFAULT_PLUGIN_DIR = "plugins"
    DEFAULT_CACHE_DIR = ".plugin_cache"
    DEFAULT_CONFIG_DIR = "config"

    # Plugin Validation
    MIN_PLUGIN_NAME_LENGTH = 3
    MAX_PLUGIN_NAME_LENGTH = 100
    VALID_PLUGIN_NAME_PATTERN = r"^[a-zA-Z][a-zA-Z0-9_-]*$"

    # Hot Reload Configuration
    HOT_RELOAD_DEBOUNCE_MS = 500
    HOT_RELOAD_MAX_RETRIES = 3

    # Plugin Lifecycle States
    PLUGIN_LIFECYCLE_STATES: ClassVar[set[str]] = {
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

    # Plugin Types
    SINGER_PLUGIN_TYPES: ClassVar[set[str]] = {"TAP", "TARGET", "TRANSFORM"}
    ARCHITECTURE_PLUGIN_TYPES: ClassVar[set[str]] = {
        "EXTENSION",
        "SERVICE",
        "MIDDLEWARE",
        "TRANSFORMER",
    }
    INTEGRATION_PLUGIN_TYPES: ClassVar[set[str]] = {
        "API",
        "DATABASE",
        "NOTIFICATION",
        "AUTHENTICATION",
    }
    UTILITY_PLUGIN_TYPES: ClassVar[set[str]] = {
        "UTILITY",
        "TOOL",
        "HANDLER",
        "PROCESSOR",
    }

    # Error Messages
    PLUGIN_NOT_FOUND_MSG = "Plugin '{plugin_name}' not found"
    PLUGIN_ALREADY_EXISTS_MSG = "Plugin '{plugin_name}' already exists"
    PLUGIN_LOAD_FAILED_MSG = "Failed to load plugin '{plugin_name}': {error}"
    PLUGIN_INVALID_NAME_MSG = "Invalid plugin name '{plugin_name}'"


# Export constants as module-level variables for backward compatibility
DEFAULT_PLUGIN_TIMEOUT_SECONDS = FlextPluginConstants.DEFAULT_PLUGIN_TIMEOUT_SECONDS
DEFAULT_DISCOVERY_TIMEOUT_SECONDS = (
    FlextPluginConstants.DEFAULT_DISCOVERY_TIMEOUT_SECONDS
)
DEFAULT_HOT_RELOAD_INTERVAL_SECONDS = (
    FlextPluginConstants.DEFAULT_HOT_RELOAD_INTERVAL_SECONDS
)
MAX_PLUGIN_WORKERS = FlextPluginConstants.MAX_PLUGIN_WORKERS
ARCHITECTURE_PLUGIN_TYPES = FlextPluginConstants.ARCHITECTURE_PLUGIN_TYPES
INTEGRATION_PLUGIN_TYPES = FlextPluginConstants.INTEGRATION_PLUGIN_TYPES
JSON_CONFIG_EXTENSION = FlextPluginConstants.JSON_CONFIG_EXTENSION
MIN_PLUGIN_NAME_LENGTH = FlextPluginConstants.MIN_PLUGIN_NAME_LENGTH
MAX_PLUGIN_NAME_LENGTH = FlextPluginConstants.MAX_PLUGIN_NAME_LENGTH
VALID_PLUGIN_NAME_PATTERN = FlextPluginConstants.VALID_PLUGIN_NAME_PATTERN
DEFAULT_CACHE_DIR = FlextPluginConstants.DEFAULT_CACHE_DIR
DEFAULT_CONFIG_DIR = FlextPluginConstants.DEFAULT_CONFIG_DIR
DEFAULT_PLUGIN_DIR = FlextPluginConstants.DEFAULT_PLUGIN_DIR
HOT_RELOAD_DEBOUNCE_MS = FlextPluginConstants.HOT_RELOAD_DEBOUNCE_MS
HOT_RELOAD_MAX_RETRIES = FlextPluginConstants.HOT_RELOAD_MAX_RETRIES
MIN_PLUGIN_WORKERS = FlextPluginConstants.MIN_PLUGIN_WORKERS
PLUGIN_ALREADY_EXISTS_MSG = FlextPluginConstants.PLUGIN_ALREADY_EXISTS_MSG
PLUGIN_INVALID_NAME_MSG = FlextPluginConstants.PLUGIN_INVALID_NAME_MSG
PLUGIN_LIFECYCLE_STATES = FlextPluginConstants.PLUGIN_LIFECYCLE_STATES
PLUGIN_LOAD_FAILED_MSG = FlextPluginConstants.PLUGIN_LOAD_FAILED_MSG
PLUGIN_NOT_FOUND_MSG = FlextPluginConstants.PLUGIN_NOT_FOUND_MSG
PYTHON_PLUGIN_EXTENSION = FlextPluginConstants.PYTHON_PLUGIN_EXTENSION
SINGER_PLUGIN_TYPES = FlextPluginConstants.SINGER_PLUGIN_TYPES
TOML_CONFIG_EXTENSION = FlextPluginConstants.TOML_CONFIG_EXTENSION
UTILITY_PLUGIN_TYPES = FlextPluginConstants.UTILITY_PLUGIN_TYPES
YAML_CONFIG_EXTENSION = FlextPluginConstants.YAML_CONFIG_EXTENSION


__all__ = [
    "FlextPluginConstants",
]
