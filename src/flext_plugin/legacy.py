"""Legacy compatibility facade for flext-plugin.

This module provides backward compatibility for APIs that may have been refactored
or renamed during the Pydantic modernization process. It follows the same pattern
as flext-core's legacy.py to ensure consistent facade patterns across the ecosystem.

All imports here should be considered deprecated and may issue warnings.
Modern code should import directly from the appropriate modules.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

from flext_plugin.application.services import (
    FlextPluginDiscoveryService,
    FlextPluginService,
)
from flext_plugin.domain.entities import (
    FlextPlugin,
    FlextPluginConfig,
    FlextPluginRegistry,
)

# Import modern implementations to re-export under legacy names
from flext_plugin.exceptions import (
    FlextPluginCompatibilityError,
    FlextPluginConfigurationError,
    FlextPluginDiscoveryError,
    FlextPluginError,
    FlextPluginExecutionError,
    FlextPluginHotReloadError,
    FlextPluginLifecycleError,
    FlextPluginLoadingError,
    FlextPluginMetadataError,
    FlextPluginPlatformError,
    FlextPluginRegistryError,
    FlextPluginSecurityError,
    FlextPluginValidationError,
)
from flext_plugin.platform import FlextPluginPlatform
from flext_plugin.simple_api import (
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
    create_flext_plugin_registry,
)


def _deprecation_warning(old_name: str, new_name: str) -> None:
    """Issue a deprecation warning for legacy imports."""
    warnings.warn(
        f"{old_name} is deprecated, use {new_name} instead",
        DeprecationWarning,
        stacklevel=3,
    )


# Legacy aliases for common plugin services - likely used names
def plugin_service(*args: object, **kwargs: object) -> object:
    """Legacy alias for FlextPluginService."""
    _deprecation_warning("PluginService", "FlextPluginService")
    if FlextPluginService is None:
        msg = "FlextPluginService not available"
        raise ImportError(msg)
    return FlextPluginService(*args, **kwargs)


def plugin_manager(*args: object, **kwargs: object) -> object:
    """Legacy alias for FlextPluginPlatform."""
    _deprecation_warning("PluginManager", "FlextPluginPlatform")
    if FlextPluginPlatform is None:
        msg = "FlextPluginPlatform not available"
        raise ImportError(msg)
    return FlextPluginPlatform(*args, **kwargs)


def plugin_discovery(*args: object, **kwargs: object) -> object:
    """Legacy alias for FlextPluginDiscoveryService."""
    _deprecation_warning("PluginDiscovery", "FlextPluginDiscoveryService")
    if FlextPluginDiscoveryService is None:
        msg = "FlextPluginDiscoveryService not available"
        raise ImportError(msg)
    return FlextPluginDiscoveryService(*args, **kwargs)


def plugin_registry(*args: object, **kwargs: object) -> object:
    """Legacy alias for FlextPluginRegistry."""
    _deprecation_warning("PluginRegistry", "FlextPluginRegistry")
    if FlextPluginRegistry is None:
        msg = "FlextPluginRegistry not available"
        raise ImportError(msg)
    return FlextPluginRegistry(*args, **kwargs)


def plugin_config(*args: object, **kwargs: object) -> object:
    """Legacy alias for FlextPluginConfig."""
    _deprecation_warning("PluginConfig", "FlextPluginConfig")
    if FlextPluginConfig is None:
        msg = "FlextPluginConfig not available"
        raise ImportError(msg)
    return FlextPluginConfig(*args, **kwargs)


def plugin(*args: object, **kwargs: object) -> object:
    """Legacy alias for FlextPlugin."""
    _deprecation_warning("Plugin", "FlextPlugin")
    if FlextPlugin is None:
        msg = "FlextPlugin not available"
        raise ImportError(msg)
    return FlextPlugin(*args, **kwargs)


# Legacy factory function aliases
def create_plugin(*args: object, **kwargs: object) -> object:
    """Legacy alias for create_flext_plugin."""
    _deprecation_warning("create_plugin", "create_flext_plugin")
    if create_flext_plugin is None:
        msg = "create_flext_plugin not available"
        raise ImportError(msg)
    return create_flext_plugin(*args, **kwargs)


def create_plugin_config(*args: object, **kwargs: object) -> object:
    """Legacy alias for create_flext_plugin_config."""
    _deprecation_warning("create_plugin_config", "create_flext_plugin_config")
    if create_flext_plugin_config is None:
        msg = "create_flext_plugin_config not available"
        raise ImportError(msg)
    return create_flext_plugin_config(*args, **kwargs)


def create_plugin_registry(*args: object, **kwargs: object) -> object:
    """Legacy alias for create_flext_plugin_registry."""
    _deprecation_warning("create_plugin_registry", "create_flext_plugin_registry")
    if create_flext_plugin_registry is None:
        msg = "create_flext_plugin_registry not available"
        raise ImportError(msg)
    return create_flext_plugin_registry(*args, **kwargs)


def create_plugin_metadata(*args: object, **kwargs: object) -> object:
    """Legacy alias for create_flext_plugin_metadata."""
    _deprecation_warning("create_plugin_metadata", "create_flext_plugin_metadata")
    if create_flext_plugin_metadata is None:
        msg = "create_flext_plugin_metadata not available"
        raise ImportError(msg)
    return create_flext_plugin_metadata(*args, **kwargs)


# Legacy exception aliases (more concise names that were probably used)
def plugin_error(*args: object, **kwargs: object) -> FlextPluginError:
    """Legacy alias for FlextPluginError."""
    _deprecation_warning("PluginError", "FlextPluginError")
    return FlextPluginError(*args, **kwargs)


def plugin_discovery_error(
    *args: object,
    **kwargs: object,
) -> FlextPluginDiscoveryError:
    """Legacy alias for FlextPluginDiscoveryError."""
    _deprecation_warning("PluginDiscoveryError", "FlextPluginDiscoveryError")
    return FlextPluginDiscoveryError(*args, **kwargs)


def plugin_loading_error(*args: object, **kwargs: object) -> FlextPluginLoadingError:
    """Legacy alias for FlextPluginLoadingError."""
    _deprecation_warning("PluginLoadingError", "FlextPluginLoadingError")
    return FlextPluginLoadingError(*args, **kwargs)


def plugin_execution_error(
    *args: object,
    **kwargs: object,
) -> FlextPluginExecutionError:
    """Legacy alias for FlextPluginExecutionError."""
    _deprecation_warning("PluginExecutionError", "FlextPluginExecutionError")
    return FlextPluginExecutionError(*args, **kwargs)


def plugin_configuration_error(
    *args: object,
    **kwargs: object,
) -> FlextPluginConfigurationError:
    """Legacy alias for FlextPluginConfigurationError."""
    _deprecation_warning("PluginConfigurationError", "FlextPluginConfigurationError")
    return FlextPluginConfigurationError(*args, **kwargs)


def plugin_validation_error(
    *args: object,
    **kwargs: object,
) -> FlextPluginValidationError:
    """Legacy alias for FlextPluginValidationError."""
    _deprecation_warning("PluginValidationError", "FlextPluginValidationError")
    return FlextPluginValidationError(*args, **kwargs)


def plugin_lifecycle_error(
    *args: object,
    **kwargs: object,
) -> FlextPluginLifecycleError:
    """Legacy alias for FlextPluginLifecycleError."""
    _deprecation_warning("PluginLifecycleError", "FlextPluginLifecycleError")
    return FlextPluginLifecycleError(*args, **kwargs)


def plugin_registry_error(*args: object, **kwargs: object) -> FlextPluginRegistryError:
    """Legacy alias for FlextPluginRegistryError."""
    _deprecation_warning("PluginRegistryError", "FlextPluginRegistryError")
    return FlextPluginRegistryError(*args, **kwargs)


def plugin_hot_reload_error(
    *args: object,
    **kwargs: object,
) -> FlextPluginHotReloadError:
    """Legacy alias for FlextPluginHotReloadError."""
    _deprecation_warning("PluginHotReloadError", "FlextPluginHotReloadError")
    return FlextPluginHotReloadError(*args, **kwargs)


def plugin_security_error(*args: object, **kwargs: object) -> FlextPluginSecurityError:
    """Legacy alias for FlextPluginSecurityError."""
    _deprecation_warning("PluginSecurityError", "FlextPluginSecurityError")
    return FlextPluginSecurityError(*args, **kwargs)


def plugin_compatibility_error(
    *args: object,
    **kwargs: object,
) -> FlextPluginCompatibilityError:
    """Legacy alias for FlextPluginCompatibilityError."""
    _deprecation_warning("PluginCompatibilityError", "FlextPluginCompatibilityError")
    return FlextPluginCompatibilityError(*args, **kwargs)


def plugin_metadata_error(*args: object, **kwargs: object) -> FlextPluginMetadataError:
    """Legacy alias for FlextPluginMetadataError."""
    _deprecation_warning("PluginMetadataError", "FlextPluginMetadataError")
    return FlextPluginMetadataError(*args, **kwargs)


def plugin_platform_error(*args: object, **kwargs: object) -> FlextPluginPlatformError:
    """Legacy alias for FlextPluginPlatformError."""
    _deprecation_warning("PluginPlatformError", "FlextPluginPlatformError")
    return FlextPluginPlatformError(*args, **kwargs)


# Alternative naming patterns that might have been used
def flext_plugin_manager(*args: object, **kwargs: object) -> object:
    """Legacy alias for FlextPluginPlatform (alternate naming)."""
    _deprecation_warning("FlextPluginManager", "FlextPluginPlatform")
    if FlextPluginPlatform is None:
        msg = "FlextPluginPlatform not available"
        raise ImportError(msg)
    return FlextPluginPlatform(*args, **kwargs)


def simple_plugin_manager(*args: object, **kwargs: object) -> object:
    """Legacy alias for FlextPluginPlatform (simple variant)."""
    _deprecation_warning("SimplePluginManager", "FlextPluginPlatform")
    if FlextPluginPlatform is None:
        msg = "FlextPluginPlatform not available"
        raise ImportError(msg)
    return FlextPluginPlatform(*args, **kwargs)


# Legacy setup function aliases
def init_plugin_system(*args: object, **kwargs: object) -> object:
    """Legacy alias for creating plugin platform."""
    _deprecation_warning("init_plugin_system", "create_flext_plugin_platform")
    if create_flext_plugin_registry is None:
        msg = "create_flext_plugin_registry not available"
        raise ImportError(msg)
    return create_flext_plugin_registry(*args, **kwargs)


def setup_plugins(*args: object, **kwargs: object) -> object:
    """Legacy alias for creating plugin platform."""
    _deprecation_warning("setup_plugins", "create_flext_plugin_platform")
    if create_flext_plugin_registry is None:
        msg = "create_flext_plugin_registry not available"
        raise ImportError(msg)
    return create_flext_plugin_registry(*args, **kwargs)


# Export legacy aliases for backward compatibility
__all__ = [
    "create_plugin",
    "create_plugin_config",
    "create_plugin_metadata",
    "create_plugin_registry",
    "flext_plugin_manager",
    "init_plugin_system",
    "plugin",
    "plugin_compatibility_error",
    "plugin_config",
    "plugin_configuration_error",
    "plugin_discovery",
    "plugin_discovery_error",
    "plugin_error",
    "plugin_execution_error",
    "plugin_hot_reload_error",
    "plugin_lifecycle_error",
    "plugin_loading_error",
    "plugin_manager",
    "plugin_metadata_error",
    "plugin_platform_error",
    "plugin_registry",
    "plugin_registry_error",
    "plugin_security_error",
    "plugin_service",
    "plugin_validation_error",
    "setup_plugins",
    "simple_plugin_manager",
]
