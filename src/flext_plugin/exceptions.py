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

    @classmethod
    def _extract_common_kwargs(
        cls, kwargs: dict[str, object]
    ) -> tuple[dict[str, object], str | None, str | None]:
        """Extract common kwargs for error initialization.

        Args:
            kwargs: Raw kwargs dictionary

        Returns:
            Tuple of (base_context, correlation_id, error_code)
        """
        # Extract known parameters
        context_raw = kwargs.get("context", {})
        correlation_id_raw = kwargs.get("correlation_id")
        error_code_raw = kwargs.get("error_code")

        # Ensure correlation_id and error_code are strings or None
        correlation_id = (
            str(correlation_id_raw) if correlation_id_raw is not None else None
        )
        error_code = str(error_code_raw) if error_code_raw is not None else None

        # Remove extracted parameters from kwargs to avoid duplication
        remaining_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in {"context", "correlation_id", "error_code"}
        }

        # Build context dict, ensuring it's always dict[str, object]
        if isinstance(context_raw, dict):
            context: dict[str, object] = dict(context_raw)
            if remaining_kwargs:
                context.update(remaining_kwargs)
        else:
            # If context is not a dict, start with empty dict and add remaining kwargs
            context = dict(remaining_kwargs)

        return context, correlation_id, error_code

    @classmethod
    def _build_context(
        cls, base_context: dict[str, object], **additional_fields: object
    ) -> dict[str, object]:
        """Build error context dictionary with additional fields.

        Args:
            base_context: Base context dictionary
            **additional_fields: Additional fields to include

        Returns:
            Complete context dictionary
        """
        context = dict(base_context)  # Create a copy
        context.update(additional_fields)
        return context

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
    class PluginBaseError(FlextExceptions.BaseError):
        """Base exception for all plugin domain errors extending FlextExceptions.BaseError."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize plugin error with context using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier that caused the error
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store plugin_id before extracting common kwargs
            self.plugin_id = plugin_id

            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                code=error_code or "PLUGIN_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class DiscoveryError(PluginBaseError):
        """Plugin discovery errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize discovery error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_DISCOVERY_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class LoadingError(PluginBaseError):
        """Plugin loading errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize loading error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_LOADING_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class ExecutionError(PluginBaseError):
        """Plugin execution errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize execution error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_EXECUTION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class PluginConfigurationError(PluginBaseError):
        """Plugin configuration errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize configuration error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_CONFIGURATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class PluginValidationError(PluginBaseError):
        """Plugin validation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize validation error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_VALIDATION_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class LifecycleError(PluginBaseError):
        """Plugin lifecycle management errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize lifecycle error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_LIFECYCLE_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class DependencyError(PluginBaseError):
        """Plugin dependency resolution errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize dependency error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_DEPENDENCY_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class RegistryError(PluginBaseError):
        """Plugin registry operation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize registry error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_REGISTRY_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class HotReloadError(PluginBaseError):
        """Plugin hot reload errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize hot reload error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_HOT_RELOAD_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class SecurityError(PluginBaseError):
        """Plugin security validation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize security error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_SECURITY_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class CompatibilityError(PluginBaseError):
        """Plugin compatibility errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize compatibility error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_COMPATIBILITY_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class MetadataError(PluginBaseError):
        """Plugin metadata validation errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize metadata error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_METADATA_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

    class PlatformError(PluginBaseError):
        """Plugin platform integration errors."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize platform error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_PLATFORM_ERROR",
                context=context,
                correlation_id=correlation_id,
            )

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

    class ProcessingError(FlextExceptions.BaseError):
        """Plugin processing operation errors extending FlextExceptions.BaseError."""

        @override
        def __init__(
            self,
            message: str,
            *,
            plugin_id: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize processing error using helpers.

            Args:
                message: Error message
                plugin_id: Plugin identifier
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = (
                FlextPluginExceptions._extract_common_kwargs(kwargs)
            )

            # Build context with plugin-specific fields
            context = FlextPluginExceptions._build_context(
                base_context,
                plugin_id=plugin_id,
            )

            # Call parent with specific error code
            super().__init__(
                message,
                plugin_id=plugin_id,
                code=error_code or "PLUGIN_PROCESSING_ERROR",
                context=context,
                correlation_id=correlation_id,
            )


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
