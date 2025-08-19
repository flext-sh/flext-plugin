"""Plugin Exception Hierarchy - Modern Pydantic v2 Patterns.

This module provides plugin-specific exceptions using modern patterns from flext-core.
All exceptions follow the FlextErrorMixin pattern with keyword-only arguments and
modern Python 3.13 type aliases for comprehensive error handling in plugin operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum

from flext_core import FlextError
from flext_core.exceptions import FlextErrorMixin


class FlextPluginErrorCodes(Enum):
    """Error codes for plugin domain operations."""

    PLUGIN_ERROR = "PLUGIN_ERROR"
    PLUGIN_DISCOVERY_ERROR = "PLUGIN_DISCOVERY_ERROR"
    PLUGIN_LOADING_ERROR = "PLUGIN_LOADING_ERROR"
    PLUGIN_EXECUTION_ERROR = "PLUGIN_EXECUTION_ERROR"
    PLUGIN_CONFIGURATION_ERROR = "PLUGIN_CONFIGURATION_ERROR"
    PLUGIN_VALIDATION_ERROR = "PLUGIN_VALIDATION_ERROR"
    PLUGIN_LIFECYCLE_ERROR = "PLUGIN_LIFECYCLE_ERROR"
    PLUGIN_DEPENDENCY_ERROR = "PLUGIN_DEPENDENCY_ERROR"
    PLUGIN_REGISTRY_ERROR = "PLUGIN_REGISTRY_ERROR"
    PLUGIN_HOT_RELOAD_ERROR = "PLUGIN_HOT_RELOAD_ERROR"
    PLUGIN_SECURITY_ERROR = "PLUGIN_SECURITY_ERROR"
    PLUGIN_COMPATIBILITY_ERROR = "PLUGIN_COMPATIBILITY_ERROR"
    PLUGIN_METADATA_ERROR = "PLUGIN_METADATA_ERROR"
    PLUGIN_PLATFORM_ERROR = "PLUGIN_PLATFORM_ERROR"


# Base plugin exception hierarchy using FlextErrorMixin pattern
class FlextPluginError(FlextError, FlextErrorMixin):
    """Base exception for all plugin domain errors."""


# Legacy alias for backwards compatibility
PluginError = FlextPluginError


class FlextPluginDiscoveryError(FlextPluginError):
    """Plugin discovery errors."""


class FlextPluginLoadingError(FlextPluginError):
    """Plugin loading errors."""


class FlextPluginExecutionError(FlextPluginError):
    """Plugin execution errors."""


class FlextPluginConfigurationError(FlextPluginError):
    """Plugin configuration errors."""


class FlextPluginValidationError(FlextPluginError):
    """Plugin validation errors."""


class FlextPluginLifecycleError(FlextPluginError):
    """Plugin lifecycle management errors."""


class FlextPluginDependencyError(FlextPluginError):
    """Plugin dependency resolution errors."""


class FlextPluginRegistryError(FlextPluginError):
    """Plugin registry operation errors."""


class FlextPluginHotReloadError(FlextPluginError):
    """Plugin hot reload errors."""


class FlextPluginSecurityError(FlextPluginError):
    """Plugin security validation errors."""


class FlextPluginCompatibilityError(FlextPluginError):
    """Plugin compatibility errors."""


class FlextPluginMetadataError(FlextPluginError):
    """Plugin metadata validation errors."""


class FlextPluginPlatformError(FlextPluginError):
    """Plugin platform integration errors."""


# Domain-specific exceptions for plugin business logic
# Using modern FlextErrorMixin pattern with context support


class FlextPluginDiscoveryOperationError(FlextPluginDiscoveryError):
    """Plugin discovery operation errors with discovery context."""

    def __init__(
        self,
        message: str,
        *,
        discovery_path: str | None = None,
        plugin_pattern: str | None = None,
        discovered_count: int | None = None,
        code: FlextPluginErrorCodes
        | None = FlextPluginErrorCodes.PLUGIN_DISCOVERY_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with plugin discovery context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if discovery_path is not None:
            context_dict["discovery_path"] = discovery_path
        if plugin_pattern is not None:
            context_dict["plugin_pattern"] = plugin_pattern
        if discovered_count is not None:
            context_dict["discovered_count"] = discovered_count

        # Initialize base exception with message
        super().__init__(message)
        # Set additional attributes from FlextErrorMixin
        self.code = str(code) if code is not None else "PLUGIN_ERROR"
        self.context = context_dict


class FlextPluginLoadOperationError(FlextPluginLoadingError):
    """Plugin loading operation errors with loading context."""

    def __init__(
        self,
        message: str,
        *,
        plugin_name: str | None = None,
        plugin_path: str | None = None,
        load_stage: str | None = None,
        code: FlextPluginErrorCodes | None = FlextPluginErrorCodes.PLUGIN_LOADING_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with plugin loading context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if plugin_name is not None:
            context_dict["plugin_name"] = plugin_name
        if plugin_path is not None:
            context_dict["plugin_path"] = plugin_path
        if load_stage is not None:
            context_dict["load_stage"] = load_stage

        # Initialize base exception with message
        super().__init__(message)
        # Set additional attributes from FlextErrorMixin
        self.code = str(code) if code is not None else "PLUGIN_ERROR"
        self.context = context_dict


class FlextPluginExecutionOperationError(FlextPluginExecutionError):
    """Plugin execution operation errors with execution context."""

    def __init__(
        self,
        message: str,
        *,
        plugin_name: str | None = None,
        execution_id: str | None = None,
        execution_stage: str | None = None,
        timeout_seconds: int | None = None,
        code: FlextPluginErrorCodes
        | None = FlextPluginErrorCodes.PLUGIN_EXECUTION_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with plugin execution context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if plugin_name is not None:
            context_dict["plugin_name"] = plugin_name
        if execution_id is not None:
            context_dict["execution_id"] = execution_id
        if execution_stage is not None:
            context_dict["execution_stage"] = execution_stage
        if timeout_seconds is not None:
            context_dict["timeout_seconds"] = timeout_seconds

        # Initialize base exception with message
        super().__init__(message)
        # Set additional attributes from FlextErrorMixin
        self.code = str(code) if code is not None else "PLUGIN_ERROR"
        self.context = context_dict


class FlextPluginConfigurationOperationError(FlextPluginConfigurationError):
    """Plugin configuration operation errors with configuration context."""

    def __init__(
        self,
        message: str,
        *,
        plugin_name: str | None = None,
        config_key: str | None = None,
        config_value: object | None = None,
        validation_rule: str | None = None,
        code: FlextPluginErrorCodes
        | None = FlextPluginErrorCodes.PLUGIN_CONFIGURATION_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with plugin configuration context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if plugin_name is not None:
            context_dict["plugin_name"] = plugin_name
        if config_key is not None:
            context_dict["config_key"] = config_key
        if config_value is not None:
            context_dict["config_value"] = config_value
        if validation_rule is not None:
            context_dict["validation_rule"] = validation_rule

        # Initialize base exception with message
        super().__init__(message)
        # Set additional attributes from FlextErrorMixin
        self.code = str(code) if code is not None else "PLUGIN_ERROR"
        self.context = context_dict


class FlextPluginLifecycleOperationError(FlextPluginLifecycleError):
    """Plugin lifecycle operation errors with lifecycle context."""

    def __init__(
        self,
        message: str,
        *,
        plugin_name: str | None = None,
        current_status: str | None = None,
        target_status: str | None = None,
        lifecycle_operation: str | None = None,
        code: FlextPluginErrorCodes
        | None = FlextPluginErrorCodes.PLUGIN_LIFECYCLE_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with plugin lifecycle context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if plugin_name is not None:
            context_dict["plugin_name"] = plugin_name
        if current_status is not None:
            context_dict["current_status"] = current_status
        if target_status is not None:
            context_dict["target_status"] = target_status
        if lifecycle_operation is not None:
            context_dict["lifecycle_operation"] = lifecycle_operation

        # Initialize base exception with message
        super().__init__(message)
        # Set additional attributes from FlextErrorMixin
        self.code = str(code) if code is not None else "PLUGIN_ERROR"
        self.context = context_dict


class FlextPluginHotReloadOperationError(FlextPluginHotReloadError):
    """Plugin hot reload operation errors with reload context."""

    def __init__(
        self,
        message: str,
        *,
        plugin_name: str | None = None,
        file_path: str | None = None,
        reload_trigger: str | None = None,
        reload_stage: str | None = None,
        code: FlextPluginErrorCodes
        | None = FlextPluginErrorCodes.PLUGIN_HOT_RELOAD_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize with plugin hot reload context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if plugin_name is not None:
            context_dict["plugin_name"] = plugin_name
        if file_path is not None:
            context_dict["file_path"] = file_path
        if reload_trigger is not None:
            context_dict["reload_trigger"] = reload_trigger
        if reload_stage is not None:
            context_dict["reload_stage"] = reload_stage

        # Initialize base exception with message
        super().__init__(message)
        # Set additional attributes from FlextErrorMixin
        self.code = str(code) if code is not None else "PLUGIN_ERROR"
        self.context = context_dict


__all__: list[str] = [
    # Base exceptions (alphabetical)
    "FlextPluginCompatibilityError",
    "FlextPluginConfigurationError",
    # Domain-specific operation exceptions
    "FlextPluginConfigurationOperationError",
    "FlextPluginDependencyError",
    "FlextPluginDiscoveryError",
    "FlextPluginDiscoveryOperationError",
    "FlextPluginError",
    # Error codes enum
    "FlextPluginErrorCodes",
    "FlextPluginExecutionError",
    "FlextPluginExecutionOperationError",
    "FlextPluginHotReloadError",
    "FlextPluginHotReloadOperationError",
    "FlextPluginLifecycleError",
    "FlextPluginLifecycleOperationError",
    "FlextPluginLoadOperationError",
    "FlextPluginLoadingError",
    "FlextPluginMetadataError",
    "FlextPluginPlatformError",
    "FlextPluginRegistryError",
    "FlextPluginSecurityError",
    "FlextPluginValidationError",
]
