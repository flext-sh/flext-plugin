"""FLEXT Plugin Exceptions - Single CONSOLIDATED Class Following FLEXT Patterns.

This module implements the CONSOLIDATED exception pattern with a single FlextPluginExceptions
class containing ALL plugin exception definitions as nested classes. Maintains backward
compatibility through property re-exports and follows FLEXT architectural standards.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import Enum
from typing import override

from flext_core import FlextExceptions


class FlextPluginExceptions(FlextExceptions):
    """Single CONSOLIDATED class containing ALL plugin exceptions."""

    class PluginErrorCodes(Enum):
        """Error codes for plugin domain operations."""

        PLUGIN_ERROR = "PLUGIN_ERROR"
        PLUGIN_PROCESSING_ERROR = "PLUGIN_PROCESSING_ERROR"
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

    # Base plugin exception classes as nested classes
    class PluginBaseError(Exception):
        """Base exception for all plugin domain errors."""

        @override
        def __init__(
            self,
            message: str,
            plugin_id: str | None = None,
            **_kwargs: object,
        ) -> None:
            """Initialize the instance."""
            # Store error_code for later use if needed
            self.error_code = "PLUGIN_PROCESSING_ERROR"
            super().__init__(message)
            self.plugin_id = plugin_id

        @override
        def __str__(self) -> str:
            """Format exception with error code prefix."""
            message = super().__str__()
            return f"[{self.error_code}] {message}"

    class DiscoveryError(PluginBaseError):
        """Plugin discovery errors."""

    class LoadingError(PluginBaseError):
        """Plugin loading errors."""

    class ExecutionError(PluginBaseError):
        """Plugin execution errors."""

    class PluginConfigurationError(PluginBaseError):
        """Plugin configuration errors."""

    class PluginValidationError(PluginBaseError):
        """Plugin validation errors."""

    class LifecycleError(PluginBaseError):
        """Plugin lifecycle management errors."""

    class DependencyError(PluginBaseError):
        """Plugin dependency resolution errors."""

    class RegistryError(PluginBaseError):
        """Plugin registry operation errors."""

    class HotReloadError(PluginBaseError):
        """Plugin hot reload errors."""

    class SecurityError(PluginBaseError):
        """Plugin security validation errors."""

    class CompatibilityError(PluginBaseError):
        """Plugin compatibility errors."""

    class MetadataError(PluginBaseError):
        """Plugin metadata validation errors."""

    class PlatformError(PluginBaseError):
        """Plugin platform integration errors."""

    # Domain-specific operation exceptions
    class DiscoveryOperationError(DiscoveryError):
        """Plugin discovery operation specific errors."""

    class LoadOperationError(LoadingError):
        """Plugin load operation specific errors."""

    class ExecutionOperationError(ExecutionError):
        """Plugin execution operation specific errors."""

    class ConfigurationOperationError(PluginConfigurationError):
        """Plugin configuration operation specific errors."""

    class LifecycleOperationError(LifecycleError):
        """Plugin lifecycle operation specific errors."""

    class HotReloadOperationError(HotReloadError):
        """Plugin hot reload operation specific errors."""


# Backward compatibility aliases - property-based exports
FlextPluginError = FlextPluginExceptions.PluginBaseError
FlextPluginErrorCodes = FlextPluginExceptions.PluginErrorCodes
FlextPluginDiscoveryError = FlextPluginExceptions.DiscoveryError
FlextPluginDiscoveryOperationError = FlextPluginExceptions.DiscoveryOperationError
FlextPluginLoadingError = FlextPluginExceptions.LoadingError
FlextPluginLoadOperationError = FlextPluginExceptions.LoadOperationError
FlextPluginExecutionError = FlextPluginExceptions.ExecutionError
FlextPluginExecutionOperationError = FlextPluginExceptions.ExecutionOperationError
FlextPluginConfigurationError = FlextPluginExceptions.PluginConfigurationError
FlextPluginConfigurationOperationError = (
    FlextPluginExceptions.ConfigurationOperationError
)
FlextPluginValidationError = FlextPluginExceptions.PluginValidationError
FlextPluginLifecycleError = FlextPluginExceptions.LifecycleError
FlextPluginLifecycleOperationError = FlextPluginExceptions.LifecycleOperationError
FlextPluginDependencyError = FlextPluginExceptions.DependencyError
FlextPluginRegistryError = FlextPluginExceptions.RegistryError
FlextPluginHotReloadError = FlextPluginExceptions.HotReloadError
FlextPluginHotReloadOperationError = FlextPluginExceptions.HotReloadOperationError
FlextPluginSecurityError = FlextPluginExceptions.SecurityError
FlextPluginCompatibilityError = FlextPluginExceptions.CompatibilityError
FlextPluginMetadataError = FlextPluginExceptions.MetadataError
FlextPluginPlatformError = FlextPluginExceptions.PlatformError

__all__ = [
    "FlextPluginCompatibilityError",
    "FlextPluginConfigurationError",
    "FlextPluginConfigurationOperationError",
    "FlextPluginDependencyError",
    "FlextPluginDiscoveryError",
    "FlextPluginDiscoveryOperationError",
    "FlextPluginError",
    "FlextPluginErrorCodes",
    "FlextPluginExceptions",
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
