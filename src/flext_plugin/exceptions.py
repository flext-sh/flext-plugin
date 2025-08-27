"""FLEXT Plugin Exceptions - Single CONSOLIDATED Class Following FLEXT Patterns.

This module implements the CONSOLIDATED exception pattern with a single FlextPluginExceptions
class containing ALL plugin exception definitions as nested classes. Maintains backward
compatibility through property re-exports and follows FLEXT architectural standards.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import Enum

from flext_core import FlextExceptions


class FlextPluginExceptions(FlextExceptions.Error):  # noqa: N818 # CONSOLIDATED class pattern
    """Single CONSOLIDATED class containing ALL plugin exceptions.

    Consolidates ALL exception definitions into one class following FLEXT patterns.
    Individual exceptions available as nested classes for organization while maintaining
    backward compatibility through property access.

    This approach follows FLEXT architectural standards for single consolidated classes
    per module while preserving existing API surface for seamless migration.
    """

    class ErrorCodes(Enum):
        """Error codes for plugin domain operations."""

        PLUGIN_ERROR = "PLUGIN_ERROR"
        FLEXT_PROCESSING_ERROR = "FLEXT_PROCESSING_ERROR"  # Legacy compatibility
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
    class BaseError(FlextExceptions.Error):
        """Base exception for all plugin domain errors."""

        def __init__(
            self, message: str, plugin_id: str | None = None, **kwargs: object
        ) -> None:
            # Remove error_code from kwargs if present and always use FLEXT_PROCESSING_ERROR
            kwargs.pop("error_code", None)
            super().__init__(message, error_code="FLEXT_PROCESSING_ERROR", **kwargs)
            self.plugin_id = plugin_id

    class DiscoveryError(FlextExceptions.Error):
        """Plugin discovery errors."""

    class LoadingError(FlextExceptions.Error):
        """Plugin loading errors."""

    class ExecutionError(FlextExceptions.Error):
        """Plugin execution errors."""

    class ConfigurationError(FlextExceptions.Error):
        """Plugin configuration errors."""

    class ValidationError(FlextExceptions.Error):
        """Plugin validation errors."""

    class LifecycleError(FlextExceptions.Error):
        """Plugin lifecycle management errors."""

    class DependencyError(FlextExceptions.Error):
        """Plugin dependency resolution errors."""

    class RegistryError(FlextExceptions.Error):
        """Plugin registry operation errors."""

    class HotReloadError(FlextExceptions.Error):
        """Plugin hot reload errors."""

    class SecurityError(FlextExceptions.Error):
        """Plugin security validation errors."""

    class CompatibilityError(FlextExceptions.Error):
        """Plugin compatibility errors."""

    class MetadataError(FlextExceptions.Error):
        """Plugin metadata validation errors."""

    class PlatformError(FlextExceptions.Error):
        """Plugin platform integration errors."""

    # Domain-specific operation exceptions
    class DiscoveryOperationError(DiscoveryError):
        """Plugin discovery operation specific errors."""

    class LoadOperationError(LoadingError):
        """Plugin load operation specific errors."""

    class ExecutionOperationError(ExecutionError):
        """Plugin execution operation specific errors."""

    class ConfigurationOperationError(ConfigurationError):
        """Plugin configuration operation specific errors."""

    class LifecycleOperationError(LifecycleError):
        """Plugin lifecycle operation specific errors."""

    class HotReloadOperationError(HotReloadError):
        """Plugin hot reload operation specific errors."""


# Export consolidated class and individual exceptions for backward compatibility
FlextPluginErrorCodes = FlextPluginExceptions.ErrorCodes
FlextPluginError = FlextPluginExceptions.BaseError
FlextPluginDiscoveryError = FlextPluginExceptions.DiscoveryError
FlextPluginLoadingError = FlextPluginExceptions.LoadingError
FlextPluginExecutionError = FlextPluginExceptions.ExecutionError
FlextPluginConfigurationError = FlextPluginExceptions.ConfigurationError
FlextPluginValidationError = FlextPluginExceptions.ValidationError
FlextPluginLifecycleError = FlextPluginExceptions.LifecycleError
FlextPluginDependencyError = FlextPluginExceptions.DependencyError
FlextPluginRegistryError = FlextPluginExceptions.RegistryError
FlextPluginHotReloadError = FlextPluginExceptions.HotReloadError
FlextPluginSecurityError = FlextPluginExceptions.SecurityError
FlextPluginCompatibilityError = FlextPluginExceptions.CompatibilityError
FlextPluginMetadataError = FlextPluginExceptions.MetadataError
FlextPluginPlatformError = FlextPluginExceptions.PlatformError
FlextPluginDiscoveryOperationError = FlextPluginExceptions.DiscoveryOperationError
FlextPluginLoadOperationError = FlextPluginExceptions.LoadOperationError
FlextPluginExecutionOperationError = FlextPluginExceptions.ExecutionOperationError
FlextPluginConfigurationOperationError = (
    FlextPluginExceptions.ConfigurationOperationError
)
FlextPluginLifecycleOperationError = FlextPluginExceptions.LifecycleOperationError
FlextPluginHotReloadOperationError = FlextPluginExceptions.HotReloadOperationError

# Legacy alias
PluginError = FlextPluginError

__all__ = [
    # Legacy backward compatibility exports
    "FlextPluginCompatibilityError",
    "FlextPluginConfigurationError",
    "FlextPluginConfigurationOperationError",
    "FlextPluginDependencyError",
    "FlextPluginDiscoveryError",
    "FlextPluginDiscoveryOperationError",
    "FlextPluginError",
    "FlextPluginErrorCodes",
    # CONSOLIDATED class (FLEXT pattern)
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
    # Legacy compatibility
    "PluginError",
]
