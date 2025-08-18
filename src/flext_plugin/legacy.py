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
    FlextPluginConfig,
    FlextPluginEntity,
    FlextPluginMetadata,
    FlextPluginRegistry,
)
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
def plugin_service() -> FlextPluginService:
    """Legacy alias for FlextPluginService."""
    _deprecation_warning("PluginService", "FlextPluginService")
    return FlextPluginService()


def plugin_manager() -> FlextPluginPlatform:
    """Legacy alias for FlextPluginPlatform."""
    _deprecation_warning("PluginManager", "FlextPluginPlatform")
    return FlextPluginPlatform()


def plugin_discovery() -> FlextPluginDiscoveryService:
    """Legacy alias for FlextPluginDiscoveryService."""
    _deprecation_warning("PluginDiscovery", "FlextPluginDiscoveryService")
    return FlextPluginDiscoveryService()


def plugin_registry() -> FlextPluginRegistry:
    """Legacy alias for FlextPluginRegistry."""
    _deprecation_warning("PluginRegistry", "FlextPluginRegistry")
    return FlextPluginRegistry.create(name="legacy_registry")


def plugin_config() -> FlextPluginConfig:
    """Legacy alias for FlextPluginConfig."""
    _deprecation_warning("PluginConfig", "FlextPluginConfig")
    return FlextPluginConfig.create(plugin_name="legacy_config")


def plugin() -> FlextPluginEntity:
    """Legacy alias for FlextPluginEntity."""
    _deprecation_warning("Plugin", "FlextPluginEntity")
    return FlextPluginEntity.create(name="legacy_plugin", plugin_version="1.0.0")


# Legacy aliases for factory functions
def create_plugin(name: str, version: str) -> FlextPluginEntity:
    """Legacy alias for create_flext_plugin."""
    _deprecation_warning("create_plugin", "create_flext_plugin")
    return create_flext_plugin(name=name, version=version)


def create_plugin_config(
    plugin_name: str, config_data: dict[str, object] | None = None
) -> FlextPluginConfig:
    """Legacy alias for create_flext_plugin_config."""
    _deprecation_warning("create_plugin_config", "create_flext_plugin_config")
    return create_flext_plugin_config(plugin_name=plugin_name, config_data=config_data)


def create_plugin_registry(
    name: str, plugins: dict[str, FlextPluginEntity] | None = None
) -> FlextPluginRegistry:
    """Legacy alias for create_flext_plugin_registry."""
    _deprecation_warning("create_plugin_registry", "create_flext_plugin_registry")
    return create_flext_plugin_registry(name=name, plugins=plugins)


def create_plugin_metadata(
    plugin_name: str, metadata: dict[str, object] | None = None
) -> FlextPluginMetadata:
    """Legacy alias for create_flext_plugin_metadata."""
    _deprecation_warning("create_plugin_metadata", "create_flext_plugin_metadata")
    return create_flext_plugin_metadata(plugin_name=plugin_name, metadata=metadata)


# Legacy aliases for exception classes
def plugin_error(message: str) -> FlextPluginError:
    """Legacy alias for FlextPluginError."""
    _deprecation_warning("plugin_error", "FlextPluginError")
    return FlextPluginError(message)


def plugin_discovery_error(message: str) -> FlextPluginDiscoveryError:
    """Legacy alias for FlextPluginDiscoveryError."""
    _deprecation_warning("plugin_discovery_error", "FlextPluginDiscoveryError")
    return FlextPluginDiscoveryError(message)


def plugin_loading_error(message: str) -> FlextPluginLoadingError:
    """Legacy alias for FlextPluginLoadingError."""
    _deprecation_warning("plugin_loading_error", "FlextPluginLoadingError")
    return FlextPluginLoadingError(message)


def plugin_execution_error(message: str) -> FlextPluginExecutionError:
    """Legacy alias for FlextPluginExecutionError."""
    _deprecation_warning("plugin_execution_error", "FlextPluginExecutionError")
    return FlextPluginExecutionError(message)


def plugin_configuration_error(message: str) -> FlextPluginConfigurationError:
    """Legacy alias for FlextPluginConfigurationError."""
    _deprecation_warning("plugin_configuration_error", "FlextPluginConfigurationError")
    return FlextPluginConfigurationError(message)


def plugin_validation_error(message: str) -> FlextPluginValidationError:
    """Legacy alias for FlextPluginValidationError."""
    _deprecation_warning("plugin_validation_error", "FlextPluginValidationError")
    return FlextPluginValidationError(message)


def plugin_lifecycle_error(message: str) -> FlextPluginLifecycleError:
    """Legacy alias for FlextPluginLifecycleError."""
    _deprecation_warning("plugin_lifecycle_error", "FlextPluginLifecycleError")
    return FlextPluginLifecycleError(message)


def plugin_registry_error(message: str) -> FlextPluginRegistryError:
    """Legacy alias for FlextPluginRegistryError."""
    _deprecation_warning("plugin_registry_error", "FlextPluginRegistryError")
    return FlextPluginRegistryError(message)


def plugin_hot_reload_error(message: str) -> FlextPluginHotReloadError:
    """Legacy alias for FlextPluginHotReloadError."""
    _deprecation_warning("plugin_hot_reload_error", "FlextPluginHotReloadError")
    return FlextPluginHotReloadError(message)


def plugin_security_error(message: str) -> FlextPluginSecurityError:
    """Legacy alias for FlextPluginSecurityError."""
    _deprecation_warning("plugin_security_error", "FlextPluginSecurityError")
    return FlextPluginSecurityError(message)


def plugin_compatibility_error(message: str) -> FlextPluginCompatibilityError:
    """Legacy alias for FlextPluginCompatibilityError."""
    _deprecation_warning("plugin_compatibility_error", "FlextPluginCompatibilityError")
    return FlextPluginCompatibilityError(message)


def plugin_metadata_error(message: str) -> FlextPluginMetadataError:
    """Legacy alias for FlextPluginMetadataError."""
    _deprecation_warning("plugin_metadata_error", "FlextPluginMetadataError")
    return FlextPluginMetadataError(message)


def plugin_platform_error(message: str) -> FlextPluginPlatformError:
    """Legacy alias for FlextPluginPlatformError."""
    _deprecation_warning("plugin_platform_error", "FlextPluginPlatformError")
    return FlextPluginPlatformError(message)


# Legacy aliases for platform management
def flext_plugin_manager() -> FlextPluginPlatform:
    """Legacy alias for FlextPluginPlatform."""
    _deprecation_warning("flext_plugin_manager", "FlextPluginPlatform")
    return FlextPluginPlatform()


def simple_plugin_manager() -> FlextPluginPlatform:
    """Legacy alias for FlextPluginPlatform."""
    _deprecation_warning("simple_plugin_manager", "FlextPluginPlatform")
    return FlextPluginPlatform()


# Legacy aliases for system initialization
def init_plugin_system(
    name: str, plugins: dict[str, FlextPluginEntity] | None = None
) -> FlextPluginRegistry:
    """Legacy alias for create_flext_plugin_registry."""
    _deprecation_warning("init_plugin_system", "create_flext_plugin_registry")
    return create_flext_plugin_registry(name=name, plugins=plugins)


def setup_plugins(
    name: str, plugins: dict[str, FlextPluginEntity] | None = None
) -> FlextPluginRegistry:
    """Legacy alias for create_flext_plugin_registry."""
    _deprecation_warning("setup_plugins", "create_flext_plugin_registry")
    return create_flext_plugin_registry(name=name, plugins=plugins)


__all__: list[str] = [  # noqa: RUF022
    # Legacy exception aliases
    "plugin_compatibility_error",
    "plugin_configuration_error",
    "plugin_discovery_error",
    "plugin_error",
    "plugin_execution_error",
    "plugin_hot_reload_error",
    "plugin_lifecycle_error",
    "plugin_loading_error",
    "plugin_metadata_error",
    "plugin_platform_error",
    "plugin_registry_error",
    "plugin_security_error",
    "plugin_validation_error",
    # Legacy factory aliases
    "create_plugin",
    "create_plugin_config",
    "create_plugin_metadata",
    "create_plugin_registry",
    # Legacy platform aliases
    "flext_plugin_manager",
    "simple_plugin_manager",
    # Legacy service aliases
    "plugin",
    "plugin_config",
    "plugin_discovery",
    "plugin_manager",
    "plugin_registry",
    "plugin_service",
    # Legacy system aliases
    "init_plugin_system",
    "setup_plugins",
]
