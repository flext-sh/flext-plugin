"""🚨 ARCHITECTURAL COMPLIANCE: ELIMINATED DUPLICATE DI Container.

REFATORADO COMPLETO:
- REMOVIDA TODAS as duplicações de FlextContainer/DIContainer
- USA APENAS FlextContainer oficial do flext-core
- Mantém apenas utilitários flext_plugin-específicos
- SEM fallback, backward compatibility ou código duplicado

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# 🚨 ARCHITECTURAL COMPLIANCE: Use ONLY official flext-core FlextContainer
from flext_core import FlextContainer, get_logger

# Import actual plugin services and classes
from flext_plugin.application.services import (
    FlextPluginDiscoveryService,
    FlextPluginService,
)
from flext_plugin.discovery import PluginDiscovery
from flext_plugin.loader import PluginLoader

logger = get_logger(__name__)


# ==================== FLEXT_PLUGIN-SPECIFIC DI UTILITIES ====================

_flext_plugin_container_instance: FlextContainer | None = None


def get_flext_plugin_container() -> FlextContainer:
    """Get FLEXT_PLUGIN-specific DI container instance.

    Returns:
        FlextContainer: Official container from flext-core.

    """
    global _flext_plugin_container_instance
    if _flext_plugin_container_instance is None:
        _flext_plugin_container_instance = FlextContainer()
    return _flext_plugin_container_instance


def configure_flext_plugin_dependencies() -> None:
    """Configure FLEXT_PLUGIN dependencies using official FlextContainer."""
    get_flext_plugin_container()

    try:
        container = get_flext_plugin_container()

        # Register actual plugin services and components
        container.register("plugin_service", FlextPluginService(container))
        container.register(
            "plugin_discovery_service", FlextPluginDiscoveryService(container),
        )
        container.register("plugin_loader", PluginLoader())
        container.register("plugin_discovery", PluginDiscovery())

        logger.info("FLEXT_PLUGIN dependencies configured successfully")

    except ImportError:
        logger.exception("Failed to configure FLEXT_PLUGIN dependencies")


def get_flext_plugin_service(service_name: str) -> object:
    """Get flext_plugin service from container.

    Args:
        service_name: Name of service to retrieve.

    Returns:
        Service instance or None if not found.

    """
    container = get_flext_plugin_container()
    result = container.get(service_name)

    if result.success:
        return result.data

    logger.warning(f"FLEXT_PLUGIN service '{service_name}' not found: {result.error}")
    return None


# Initialize flext_plugin dependencies on module import
configure_flext_plugin_dependencies()
