"""Dependency injection container for FLEXT-PLUGIN.

Using flext-core DI container - NO duplication, consistent patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.config import get_container
from flext_plugin.infrastructure.config import PluginConfig
from flext_plugin.infrastructure.persistence.repositories import (
    PluginExecutionRepository,
    PluginInstanceRepository,
    PluginRegistryRepository,
)
from flext_plugin.infrastructure.ports import (
    FileSystemPluginDiscoveryPort,
    LocalPluginExecutionPort,
    LocalPluginLifecyclePort,
    LocalPluginRegistryPort,
    PydanticPluginValidationPort,
)

if TYPE_CHECKING:
            from flext_plugin.domain.ports import (
        PluginDiscoveryService,
        PluginExecutionService,
        PluginLifecycleService,
        PluginRegistryService,
        PluginValidationService,
    )


def configure_plugin_dependencies() -> None:
    """Configure all plugin dependencies in DI container."""
    container = get_container()

    # Configuration
    container.register_singleton(PluginConfig, PluginConfig)

    # Repository Layer
    container.register_singleton(PluginInstanceRepository, PluginInstanceRepository)
    container.register_singleton(PluginExecutionRepository, PluginExecutionRepository)
    container.register_singleton(PluginRegistryRepository, PluginRegistryRepository)

    # Service Layer (Ports)
    container.register_singleton(
        FileSystemPluginDiscoveryPort,
        FileSystemPluginDiscoveryPort,
    )
    container.register_singleton(
        PydanticPluginValidationPort,
        PydanticPluginValidationPort,
    )
    container.register_singleton(LocalPluginLifecyclePort, LocalPluginLifecyclePort)
    container.register_singleton(LocalPluginExecutionPort, LocalPluginExecutionPort)
    container.register_singleton(LocalPluginRegistryPort, LocalPluginRegistryPort)


def get_plugin_config() -> PluginConfig:
    """Get plugin configuration from container."""
    container = get_container()
    return container.resolve(PluginConfig)


def get_plugin_discovery_service() -> PluginDiscoveryService:
    """Get plugin discovery service from container."""
    container = get_container()
    return container.resolve(FileSystemPluginDiscoveryPort)


def get_plugin_validation_service() -> PluginValidationService:
    """Get plugin validation service from container."""
    container = get_container()
    return container.resolve(PydanticPluginValidationPort)


def get_plugin_lifecycle_service() -> PluginLifecycleService:
    """Get plugin lifecycle service from container."""
    container = get_container()
    return container.resolve(LocalPluginLifecyclePort)


def get_plugin_execution_service() -> PluginExecutionService:
    """Get plugin execution service from container."""
    container = get_container()
    return container.resolve(LocalPluginExecutionPort)


def get_plugin_registry_service() -> PluginRegistryService:
    """Get plugin registry service from container."""
    container = get_container()
    return container.resolve(LocalPluginRegistryPort)
