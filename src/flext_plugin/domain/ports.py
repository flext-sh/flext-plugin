"""Domain ports (service interfaces) for FLEXT-PLUGIN.

Using clean architecture patterns - NO duplication with flext-core.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from flext_core.domain.types import ServiceResult

if TYPE_CHECKING:
    from flext_plugin.domain.entities import (
        PluginExecution,
        PluginInstance,
        PluginMetadata,
        PluginRegistry,
    )


class PluginDiscoveryService(ABC):
    """Abstract plugin discovery service port."""

    @abstractmethod
    async def discover_plugins(self, search_paths: list[str]) -> ServiceResult[list[PluginMetadata]]:
        """Discover plugins in specified paths."""

    @abstractmethod
    async def validate_plugin_metadata(self, metadata: PluginMetadata) -> ServiceResult[bool]:
        """Validate plugin metadata."""

    @abstractmethod
    async def get_plugin_manifest(self, plugin_path: str) -> ServiceResult[dict[str, Any]]:
        """Get plugin manifest from path."""


class PluginValidationService(ABC):
    """Abstract plugin validation service port."""

    @abstractmethod
    async def validate_plugin(self, plugin: PluginInstance) -> ServiceResult[bool]:
        """Validate plugin instance."""

    @abstractmethod
    async def validate_configuration(self, plugin: PluginInstance, config: dict[str, Any]) -> ServiceResult[bool]:
        """Validate plugin configuration."""

    @abstractmethod
    async def validate_dependencies(self, plugin: PluginInstance) -> ServiceResult[bool]:
        """Validate plugin dependencies."""

    @abstractmethod
    async def validate_permissions(self, plugin: PluginInstance) -> ServiceResult[bool]:
        """Validate plugin permissions."""


class PluginLifecycleService(ABC):
    """Abstract plugin lifecycle service port."""

    @abstractmethod
    async def register_plugin(self, plugin: PluginInstance) -> ServiceResult[PluginInstance]:
        """Register plugin in system."""

    @abstractmethod
    async def load_plugin(self, plugin: PluginInstance) -> ServiceResult[PluginInstance]:
        """Load plugin into memory."""

    @abstractmethod
    async def initialize_plugin(self, plugin: PluginInstance) -> ServiceResult[PluginInstance]:
        """Initialize plugin."""

    @abstractmethod
    async def activate_plugin(self, plugin: PluginInstance) -> ServiceResult[PluginInstance]:
        """Activate plugin."""

    @abstractmethod
    async def suspend_plugin(self, plugin: PluginInstance) -> ServiceResult[PluginInstance]:
        """Suspend plugin."""

    @abstractmethod
    async def unload_plugin(self, plugin: PluginInstance) -> ServiceResult[PluginInstance]:
        """Unload plugin from memory."""

    @abstractmethod
    async def unregister_plugin(self, plugin: PluginInstance) -> ServiceResult[bool]:
        """Unregister plugin from system."""


class PluginExecutionService(ABC):
    """Abstract plugin execution service port."""

    @abstractmethod
    async def execute_plugin(
        self,
        plugin: PluginInstance,
        input_data: dict[str, Any],
        execution_context: dict[str, Any] | None = None,
    ) -> ServiceResult[PluginExecution]:
        """Execute plugin with input data."""

    @abstractmethod
    async def get_execution_status(self, execution_id: str) -> ServiceResult[PluginExecution]:
        """Get execution status."""

    @abstractmethod
    async def cancel_execution(self, execution_id: str) -> ServiceResult[bool]:
        """Cancel running execution."""

    @abstractmethod
    async def get_execution_logs(self, execution_id: str) -> ServiceResult[list[dict[str, Any]]]:
        """Get execution logs."""


class PluginRegistryService(ABC):
    """Abstract plugin registry service port."""

    @abstractmethod
    async def register_registry(self, registry: PluginRegistry) -> ServiceResult[PluginRegistry]:
        """Register a plugin registry."""

    @abstractmethod
    async def sync_registry(self, registry: PluginRegistry) -> ServiceResult[bool]:
        """Sync registry with remote."""

    @abstractmethod
    async def search_plugins(self, registry: PluginRegistry, query: str) -> ServiceResult[list[PluginMetadata]]:
        """Search plugins in registry."""

    @abstractmethod
    async def download_plugin(self, registry: PluginRegistry, plugin_id: str) -> ServiceResult[str]:
        """Download plugin from registry."""

    @abstractmethod
    async def verify_plugin_signature(self, registry: PluginRegistry, plugin_path: str) -> ServiceResult[bool]:
        """Verify plugin digital signature."""


class PluginHotReloadService(ABC):
    """Abstract plugin hot reload service port."""

    @abstractmethod
    async def start_watching(self, watch_paths: list[str]) -> ServiceResult[bool]:
        """Start watching for plugin changes."""

    @abstractmethod
    async def stop_watching(self) -> ServiceResult[bool]:
        """Stop watching for changes."""

    @abstractmethod
    async def reload_plugin(self, plugin: PluginInstance) -> ServiceResult[PluginInstance]:
        """Reload plugin."""

    @abstractmethod
    async def backup_plugin_state(self, plugin: PluginInstance) -> ServiceResult[dict[str, Any]]:
        """Backup plugin state."""

    @abstractmethod
    async def restore_plugin_state(self, plugin: PluginInstance, state: dict[str, Any]) -> ServiceResult[bool]:
        """Restore plugin state."""


class PluginSecurityService(ABC):
    """Abstract plugin security service port."""

    @abstractmethod
    async def create_sandbox(self, plugin: PluginInstance) -> ServiceResult[dict[str, Any]]:
        """Create security sandbox for plugin."""

    @abstractmethod
    async def enforce_resource_limits(self, plugin: PluginInstance) -> ServiceResult[bool]:
        """Enforce resource limits."""

    @abstractmethod
    async def validate_imports(self, plugin: PluginInstance) -> ServiceResult[bool]:
        """Validate plugin imports."""

    @abstractmethod
    async def scan_for_vulnerabilities(self, plugin: PluginInstance) -> ServiceResult[list[dict[str, Any]]]:
        """Scan plugin for vulnerabilities."""
