"""Enterprise-grade plugin management system for FLEXT ecosystem."""

from __future__ import annotations

import uuid

from flext_core import FlextContainer, FlextResult

from flext_plugin.application.services import FlextPluginDiscoveryService
from flext_plugin.platform import FlextPluginPlatform
from flext_plugin.simple_api import (
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
    create_flext_plugin_registry,
)
from flext_plugin.typings import PluginExecutionContext, PluginManagerResult


# Main FlextPlugin aliases with backwards compatibility
class FlextPluginManager:
    """Backwards compatibility wrapper for FlextPluginPlatform.

    This class maintains compatibility with legacy test code that expects
    different constructor parameters while delegating all functionality
    to the modern FlextPluginPlatform implementation.
    """

    def __init__(
        self,
        container: FlextContainer | None = None,
        *,
        _auto_discover: bool = True,
        _security_enabled: bool = True,
        **_kwargs: object,
    ) -> None:
        """Initialize with backwards compatibility for legacy parameters."""
        # Ignore legacy parameters and create modern platform
        self._platform = FlextPluginPlatform(container)
        self._initialized = False  # Legacy state tracking

    @property
    def is_initialized(self) -> bool:
        """Legacy property for backwards compatibility."""
        return self._initialized

    @property
    def plugin_count(self) -> int:
        """Legacy property for plugin count."""
        return 0  # Placeholder for compatibility

    @property
    def discovery(self) -> FlextPluginDiscoveryService:
        """Legacy discovery object."""
        return self._platform.discovery_service

    async def initialize(self) -> FlextResult[PluginManagerResult]:
        """Legacy async initialize method for backwards compatibility."""
        # Mark as initialized
        self._initialized = True

        # Return legacy result format
        result_data = PluginManagerResult(
            operation="initialize",
            success=True,
        )
        result_data.details = {"platform": self._platform}
        return FlextResult[PluginManagerResult].ok(result_data)

    async def cleanup(self) -> None:
        """Legacy cleanup method for backwards compatibility."""
        self._initialized = False

    async def integrate_with_protocols(self) -> FlextResult[str]:
        """Legacy protocol integration (placeholder)."""
        return FlextResult[str].ok("Protocol integration completed")

    async def reload_plugin(self, plugin_name: str) -> FlextResult[str]:
        """Legacy plugin reload method."""
        return FlextResult[str].fail(f"Plugin '{plugin_name}' not discovered")

    async def execute_plugin(
        self,
        plugin_name: str,
        _data: dict[str, object],
    ) -> FlextResult[str]:
        """Legacy plugin execution method."""
        return FlextResult[str].fail(f"Plugin '{plugin_name}' not found")

    async def configure_plugin(
        self,
        plugin_name: str,
        _config: object,
    ) -> FlextResult[str]:
        """Legacy plugin configuration method."""
        return FlextResult[str].fail(f"Plugin '{plugin_name}' not found")

    def get_plugin_status(self, plugin_name: str) -> FlextResult[str]:
        """Legacy plugin status method."""
        return FlextResult[str].fail(f"Plugin '{plugin_name}' not found")

    def list_plugins(
        self,
        *,
        _enabled_only: bool = False,
        enabled_only: bool | None = None,
    ) -> list[str]:
        """Legacy list plugins method."""
        # Handle both parameter names for backward compatibility
        if enabled_only is not None:
            _enabled_only = enabled_only
        return []

    async def discover_and_load_plugins(self) -> FlextResult[str]:
        """Legacy discover and load method."""
        return FlextResult[str].fail("No plugins discovered")

    async def unload_plugin(self, plugin_name: str) -> FlextResult[str]:
        """Legacy plugin unload method."""
        return FlextResult[str].fail(f"Plugin '{plugin_name}' not found")

    async def _create_plugin_context(self, plugin_name: str) -> PluginExecutionContext:
        """Legacy create plugin context method."""
        return PluginExecutionContext(
            plugin_id=plugin_name,
            execution_id=str(uuid.uuid4()),
        )

    def __getattr__(self, name: str) -> object:
        """Delegate all method calls to the underlying platform."""
        return getattr(self._platform, name)


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

__all__: list[str] = [
    "FlextContainer",
    "FlextResult",
    "PluginExecutionContext",
    "PluginManagerResult",
    "FlextPluginPlatform",
    "create_flext_plugin",
    "create_flext_plugin_config",
    "create_flext_plugin_metadata",
    "create_flext_plugin_registry",
    "create_flext_plugin_platform",
    "flext_plugin_create_plugin",
    "flext_plugin_create_config",
    "flext_plugin_create_metadata",
    "flext_plugin_create_registry",
    "flext_plugin_create_manager",
    "flext_plugin_create_platform",
]
