"""FLEXT Plugin - Enterprise-grade plugin management system with Clean Architecture patterns.

This package provides a comprehensive plugin management system built on Clean Architecture,
Domain-Driven Design, and CQRS patterns. It enables dynamic plugin loading, hot-reload
capabilities, and enterprise-grade plugin lifecycle management for the FLEXT ecosystem.

Key Features:
    - Clean Architecture with strict layer separation
    - Domain-Driven Design with rich business entities
    - CQRS command and query responsibility segregation
    - Dynamic plugin loading with security validation
    - Hot-reload capabilities for development workflows
    - Enterprise-grade error handling and validation

Architecture Layers:
    - Platform: FlextPluginPlatform (unified facade)
    - Application: Services and CQRS handlers
    - Domain: Entities, ports, and business logic
    - Infrastructure: Plugin loading and discovery

Usage:
    >>> from flext_plugin import FlextPluginPlatform
    >>> platform = FlextPluginPlatform()
    >>> result = platform.discover_plugins("./plugins")

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.metadata

# Import from flext-core for foundational patterns
from flext_core import FlextContainer, FlextResult

try:
    __version__ = importlib.metadata.version("flext-plugin")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.9.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# Application handlers
from flext_plugin.application.handlers import (
    FlextPluginHandler,
    FlextPluginRegistrationHandler,
)

# Application services
from flext_plugin.application.services import (
    FlextPluginDiscoveryService,
    FlextPluginService,
)

# Domain entities
from flext_plugin.domain.entities import (
    FlextPlugin,
    FlextPluginConfig,
    FlextPluginMetadata,
    FlextPluginRegistry,
)

# Domain ports
from flext_plugin.domain.ports import (
    FlextPluginDiscoveryPort,
    FlextPluginLoaderPort,
    FlextPluginManagerPort,
)

# Platform
from flext_plugin.platform import FlextPluginPlatform

# Simple API
from flext_plugin.simple_api import (
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
    create_flext_plugin_registry,
)

# Main FlextPlugin aliases
FlextPluginManager = FlextPluginPlatform
FlextPluginResult = FlextResult


def create_flext_plugin_platform(
    config: dict[str, object] | None = None,
) -> FlextPluginPlatform:
    """Create unified FLEXT Plugin platform instance.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured FlextPluginPlatform instance

    """
    container = FlextContainer()
    # Configure container with config dict if provided
    if config:
        for key, value in config.items():
            container.register(key, value)
    return FlextPluginPlatform(container)


# Prefixed helper functions
flext_plugin_create_plugin = create_flext_plugin
flext_plugin_create_config = create_flext_plugin_config
flext_plugin_create_metadata = create_flext_plugin_metadata
flext_plugin_create_registry = create_flext_plugin_registry
flext_plugin_create_manager = create_flext_plugin_platform
flext_plugin_create_platform = create_flext_plugin_platform

__all__ = [
    "FlextContainer",
    "FlextPlugin",
    "FlextPluginConfig",
    "FlextPluginDiscoveryPort",
    "FlextPluginDiscoveryService",
    "FlextPluginHandler",
    "FlextPluginLoaderPort",
    "FlextPluginManager",
    "FlextPluginManagerPort",
    "FlextPluginMetadata",
    "FlextPluginPlatform",
    "FlextPluginRegistrationHandler",
    "FlextPluginRegistry",
    "FlextPluginResult",
    "FlextPluginService",
    "FlextResult",
    "__version__",
    "__version_info__",
    "create_flext_plugin",
    "create_flext_plugin_config",
    "create_flext_plugin_metadata",
    "create_flext_plugin_platform",
    "create_flext_plugin_registry",
    "flext_plugin_create_config",
    "flext_plugin_create_manager",
    "flext_plugin_create_metadata",
    "flext_plugin_create_platform",
    "flext_plugin_create_plugin",
    "flext_plugin_create_registry",
]

# Module metadata
__architecture__ = "Clean Architecture + DDD"
