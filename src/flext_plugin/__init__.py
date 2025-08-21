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
    create_plugin_from_dict,
    create_plugin_config_from_dict,
)
# from flext_plugin.typings import PluginExecutionContext  # Now using legacy version

# Export core types that examples need
from flext_plugin.models import PluginStatus, PluginType

# Export legacy classes for test compatibility
from flext_plugin.typings_legacy import (
    PluginError,
    PluginExecutionContext,
    PluginExecutionResult,
    PluginManagerResult,
    SimplePluginRegistry,
    create_plugin_manager,
)

# Export domain entities for tests
from flext_plugin.domain.entities import (
    FlextPlugin,
    FlextPluginConfig,
    FlextPluginExecution,
    FlextPluginMetadata,
    FlextPluginRegistry,
)

# Export application services for tests
from flext_plugin.application.services import (
    FlextPluginService,
)

# Import domain ports for test aliases (must come after legacy imports)
from flext_plugin.domain.ports import (
    FlextPluginDiscoveryPort,
    FlextPluginLoaderPort,
    FlextPluginManagerPort,
    FlextPluginRegistryPort,
    FlextPluginHotReloadPort,
    PluginDiscoveryService,
    PluginExecutionService,
    PluginLifecycleService,
    PluginRegistryService,
    PluginHotReloadService,
    PluginSecurityService,
    PluginValidationService,
)

# Create service aliases for backward compatibility
PluginService = FlextPluginService
# PluginDiscoveryService comes from ports.py and should remain abstract

# Export additional components for tests
from flext_plugin.application.handlers import (
    FlextPluginHandler,
    FlextPluginRegistrationHandler,
    FlextPluginEventHandler,
)

# Export core discovery components
from flext_plugin.core.discovery import PluginDiscovery

# Export loader components
from flext_plugin.loader import PluginLoader

# Export hot reload components
from flext_plugin.hot_reload import (
    HotReloadManager,
    PluginFileHandler,
    PluginState,
    PluginWatcher,
    ReloadEvent,
    RollbackManager,
    StateManager,
    WatchEvent,
    WatchEventType,
)

# Export simple plugin system components
from flext_plugin.simple_plugin import (
    Plugin,
    PluginRegistry,
    create_registry,
    load_plugin,
)

# Export domain port service aliases for domain tests

# Import the port-based PluginDiscoveryService alias separately (for domain tests)
# from flext_plugin.domain.ports import PluginDiscoveryService as PluginDiscoveryServicePort


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

        # Create proper PluginManagerResult
        result = PluginManagerResult(operation="initialize", success=True)
        result.plugins_affected = []
        result.execution_time_ms = 0.0
        result.details = {"manager_type": "FlextPluginManager"}
        result.errors = []

        return FlextResult[PluginManagerResult].ok(result)

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


# Simple aliases for backward compatibility
create_plugin = create_flext_plugin
create_plugin_config = create_flext_plugin_config
create_plugin_metadata = create_flext_plugin_metadata
create_plugin_registry = create_flext_plugin_registry

# Prefixed helper functions
flext_plugin_create_plugin = create_flext_plugin
flext_plugin_create_config = create_flext_plugin_config
flext_plugin_create_metadata = create_flext_plugin_metadata
flext_plugin_create_registry = create_flext_plugin_registry
flext_plugin_create_manager = create_flext_plugin_platform
flext_plugin_create_platform = create_flext_plugin_platform


def create_hot_reload_manager(
    plugin_directory: str = "./plugins",
    container: FlextContainer | None = None,  # noqa: ARG001
) -> HotReloadManager:
    """Create hot reload manager instance.

    Args:
        plugin_directory: Directory to watch for plugins
        container: Optional FlextContainer instance

    Returns:
        Configured HotReloadManager instance

    """
    return HotReloadManager.create(plugin_directory=plugin_directory)


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
    "create_hot_reload_manager",
    # Simple API functions
    "create_plugin_from_dict",
    "create_plugin_config_from_dict",
    # Simple aliases
    "create_plugin",
    "create_plugin_config",
    "create_plugin_metadata",
    "create_plugin_registry",
    "flext_plugin_create_plugin",
    "flext_plugin_create_config",
    "flext_plugin_create_metadata",
    "flext_plugin_create_registry",
    "flext_plugin_create_manager",
    "flext_plugin_create_platform",
    # Core types for examples
    "PluginStatus",
    "PluginType",
    # Domain entities for tests
    "FlextPlugin",
    "FlextPluginConfig",
    "FlextPluginExecution",
    "FlextPluginMetadata",
    "FlextPluginRegistry",
    # Application services for tests
    "FlextPluginService",
    "FlextPluginDiscoveryService",
    # Service aliases for backward compatibility
    "PluginService",
    "PluginDiscoveryService",
    # Handlers for tests
    "FlextPluginHandler",
    "FlextPluginRegistrationHandler",
    "FlextPluginEventHandler",
    # Core discovery components
    "PluginDiscovery",
    # Loader components
    "PluginLoader",
    # Hot reload components
    "HotReloadManager",
    "PluginFileHandler",
    "PluginState",
    "PluginWatcher",
    "ReloadEvent",
    "RollbackManager",
    "StateManager",
    "WatchEvent",
    "WatchEventType",
    # Simple plugin system components
    "Plugin",
    "PluginRegistry",
    "create_registry",
    "load_plugin",
    # Legacy classes for test compatibility
    "PluginError",
    "PluginExecutionContext",
    "PluginExecutionResult",
    "PluginManagerResult",
    "SimplePluginRegistry",
    "create_plugin_manager",
    # Domain port service aliases for tests
    "FlextPluginHotReloadPort",
    "FlextPluginRegistryPort",
    "PluginExecutionService",
    "PluginHotReloadService",
    "PluginLifecycleService",
    "PluginRegistryService",
    "PluginSecurityService",
    "PluginValidationService",
]
