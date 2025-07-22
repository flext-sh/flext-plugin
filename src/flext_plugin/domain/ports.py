"""Domain ports (service interfaces) for FLEXT-PLUGIN.

Using clean architecture patterns - NO duplication with flext-core.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from flext_core.domain.shared_types import ServiceResult

    from flext_plugin.domain.entities import (
        PluginInstance,
        PluginMetadata,
        PluginRegistry,
    )


class PluginDiscoveryService(ABC):
    """Abstract plugin discovery service port."""

    @abstractmethod
    async def discover_plugins(
        self,
        search_paths: list[str],
    ) -> ServiceResult[Any]:
        """Discover plugins in specified paths."""

    @abstractmethod
    async def validate_plugin_metadata(
        self,
        metadata: PluginMetadata,
    ) -> ServiceResult[Any]:
        """Validate plugin metadata."""

    @abstractmethod
    async def get_plugin_manifest(
        self,
        plugin_path: str,
    ) -> ServiceResult[Any]:
        """Get plugin manifest from path."""


class PluginValidationService(ABC):
    """Abstract plugin validation service port."""

    @abstractmethod
    async def validate_plugin(self, plugin: PluginInstance) -> ServiceResult[Any]:
        """Validate plugin instance."""

    @abstractmethod
    async def validate_configuration(
        self,
        plugin: PluginInstance,
        config: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Validate plugin configuration."""

    @abstractmethod
    async def validate_dependencies(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Validate plugin dependencies."""

    @abstractmethod
    async def validate_permissions(self, plugin: PluginInstance) -> ServiceResult[Any]:
        """Validate plugin permissions."""


class PluginLifecycleService(ABC):
    """Abstract plugin lifecycle service port."""

    @abstractmethod
    async def register_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Register plugin in system."""

    @abstractmethod
    async def load_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Load plugin into memory."""

    @abstractmethod
    async def initialize_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Initialize plugin."""

    @abstractmethod
    async def activate_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Activate plugin."""

    @abstractmethod
    async def suspend_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Suspend plugin."""

    @abstractmethod
    async def unload_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Unload plugin from memory."""

    @abstractmethod
    async def unregister_plugin(self, plugin: PluginInstance) -> ServiceResult[Any]:
        """Unregister plugin from system."""


class PluginExecutionService(ABC):
    """Abstract plugin execution service port."""

    @abstractmethod
    async def execute_plugin(
        self,
        plugin: PluginInstance,
        input_data: dict[str, Any],
        execution_context: dict[str, Any] | None = None,
    ) -> ServiceResult[Any]:
        """Execute plugin with input data."""

    @abstractmethod
    async def get_execution_status(
        self,
        execution_id: str,
    ) -> ServiceResult[Any]:
        """Get execution status."""

    @abstractmethod
    async def cancel_execution(self, execution_id: str) -> ServiceResult[Any]:
        """Cancel running execution."""

    @abstractmethod
    async def get_execution_logs(
        self,
        execution_id: str,
    ) -> ServiceResult[Any]:
        """Get execution logs."""


class PluginRegistryService(ABC):
    """Abstract plugin registry service port."""

    @abstractmethod
    async def register_registry(
        self,
        registry: PluginRegistry,
    ) -> ServiceResult[Any]:
        """Register a plugin registry."""

    @abstractmethod
    async def sync_registry(self, registry: PluginRegistry) -> ServiceResult[Any]:
        """Sync registry with remote."""

    @abstractmethod
    async def search_plugins(
        self,
        registry: PluginRegistry,
        query: str,
    ) -> ServiceResult[Any]:
        """Search plugins in registry."""

    @abstractmethod
    async def download_plugin(
        self,
        registry: PluginRegistry,
        plugin_id: str,
    ) -> ServiceResult[Any]:
        """Download plugin from registry."""

    @abstractmethod
    async def verify_plugin_signature(
        self,
        registry: PluginRegistry,
        plugin_path: str,
    ) -> ServiceResult[Any]:
        """Verify plugin digital signature."""


class PluginHotReloadService(ABC):
    """Abstract plugin hot reload service port."""

    @abstractmethod
    async def start_watching(self, watch_paths: list[str]) -> ServiceResult[Any]:
        """Start watching for plugin changes."""

    @abstractmethod
    async def stop_watching(self) -> ServiceResult[Any]:
        """Stop watching for changes."""

    @abstractmethod
    async def reload_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Reload plugin."""

    @abstractmethod
    async def backup_plugin_state(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Backup plugin state."""

    @abstractmethod
    async def restore_plugin_state(
        self,
        plugin: PluginInstance,
        state: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Restore plugin state."""


class PluginSecurityService(ABC):
    """Abstract plugin security service port."""

    @abstractmethod
    async def create_sandbox(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Create security sandbox for plugin."""

    @abstractmethod
    async def enforce_resource_limits(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Enforce resource limits."""

    @abstractmethod
    async def validate_imports(self, plugin: PluginInstance) -> ServiceResult[Any]:
        """Validate plugin imports."""

    @abstractmethod
    async def scan_for_vulnerabilities(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[Any]:
        """Scan plugin for vulnerabilities."""
