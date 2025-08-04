"""FLEXT Plugin Domain Ports - Clean Architecture interfaces for external dependencies.

This module defines the domain ports (interfaces) that establish contracts
between the domain layer and external infrastructure concerns. Following
Clean Architecture principles, these ports ensure proper dependency inversion
and enable testability through interface segregation.

Domain ports serve as the boundaries through which the domain layer interacts
with external systems, infrastructure, and services. They define what the
domain needs without specifying how those needs are fulfilled, allowing
for flexible implementation strategies and comprehensive testing.

Key Ports:
    - FlextPluginDiscoveryPort: Plugin discovery and validation operations
    - FlextPluginLoaderPort: Plugin loading and memory management operations
    - FlextPluginManagerPort: Plugin installation and configuration operations

Architecture:
    These ports implement the Dependency Inversion Principle from Clean
    Architecture, allowing the domain layer to define its requirements
    while remaining independent of infrastructure implementation details.
    Infrastructure adapters implement these ports to provide concrete functionality.

Port Pattern:
    Each port defines a specific concern or capability, following the
    Interface Segregation Principle. This ensures that implementing
    classes only need to provide functionality relevant to their purpose.

Example:
    >>> from flext_plugin.domain.ports import FlextPluginDiscoveryPort
    >>> from flext_plugin.infrastructure.adapters import FileSystemDiscoveryAdapter
    >>>
    >>> # Infrastructure implements the domain port
    >>> discovery: FlextPluginDiscoveryPort = FileSystemDiscoveryAdapter()
    >>> result = discovery.discover_plugins("./plugins")
    >>> if result.success():
    ...     plugins = result.data

Integration:
    - Domain services depend on these ports for external operations
    - Infrastructure adapters implement these ports with concrete functionality
    - Application services coordinate domain operations through these interfaces
    - Testing is simplified through mock implementations of these ports

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_core import FlextResult

    from flext_plugin.domain.entities import FlextPlugin, FlextPluginConfig


class FlextPluginDiscoveryPort(ABC):
    """Domain port interface for plugin discovery and validation operations.

    Defines the contract for plugin discovery capabilities required by the
    domain layer. Implementations of this port provide concrete plugin
    discovery mechanisms such as file system scanning, registry queries,
    or network-based plugin repositories.

    This port abstracts the complexity of plugin discovery, allowing the
    domain layer to request plugin discovery without being coupled to
    specific discovery mechanisms or storage formats.

    Key Responsibilities:
        - Plugin discovery across various sources and formats
        - Plugin metadata extraction and validation
        - Plugin structure integrity verification
        - Discovery result filtering and organization
        - Integration with Singer/Meltano plugin discovery patterns

    Discovery Patterns:
        - Directory-based plugin scanning with configurable depth
        - Plugin manifest parsing and metadata extraction
        - Plugin type detection and classification
        - Dependency analysis and requirement validation
        - Performance optimization through caching strategies

    Implementation Considerations:
        - Should support multiple plugin formats and structures
        - Must provide comprehensive error handling and reporting
        - Should implement caching for performance optimization
        - Must validate plugin integrity and security requirements
        - Should support asynchronous discovery operations where beneficial

    Example Implementation:
        >>> class FileSystemDiscoveryAdapter(FlextPluginDiscoveryPort):
        ...     def discover_plugins(self, path: str) -> FlextResult[list[FlextPlugin]]:
        ...         # Scan file system for plugin directories
        ...         # Parse plugin manifests and metadata
        ...         # Return validated plugin list
        ...         pass
    """

    @abstractmethod
    def discover_plugins(self, path: str) -> FlextResult[list[FlextPlugin]]:
        """Discover plugins in the given path.

        Args:
            path: Path to search for plugins

        Returns:
            FlextResult containing list of discovered plugins

        """

    @abstractmethod
    def validate_plugin(self, plugin: FlextPlugin) -> FlextResult[bool]:
        """Validate a plugin.

        Args:
            plugin: Plugin to validate

        Returns:
            FlextResult indicating if plugin is valid

        """


class FlextPluginLoaderPort(ABC):
    """Domain port interface for plugin loading and memory management operations.

    Defines the contract for plugin loading capabilities required by the
    domain layer. Implementations of this port handle the complex aspects
    of plugin loading, memory management, and runtime lifecycle operations.

    This port abstracts plugin loading complexity, enabling the domain layer
    to request plugin loading without being coupled to specific loading
    mechanisms, memory management strategies, or runtime environments.

    Key Responsibilities:
        - Plugin loading into memory with proper isolation
        - Plugin unloading and cleanup operations
        - Plugin state tracking and status monitoring
        - Memory management and resource cleanup
        - Hot-reload and dynamic plugin management

    Loading Patterns:
        - Dynamic loading with proper class isolation
        - Dependency injection and service registration
        - Plugin sandboxing and security boundaries
        - Resource management and cleanup coordination
        - Performance monitoring and optimization

    Memory Management:
        - Plugin isolation to prevent conflicts
        - Resource cleanup on plugin unloading
        - Memory leak prevention and monitoring
        - Garbage collection coordination
        - Performance impact monitoring

    Implementation Considerations:
        - Must provide proper plugin isolation and sandboxing
        - Should implement comprehensive resource cleanup
        - Must handle plugin dependencies and conflicts
        - Should support hot-reload and dynamic loading
        - Must provide robust error handling and recovery

    Example Implementation:
        >>> class DynamicLoaderAdapter(FlextPluginLoaderPort):
        ...     def load_plugin(self, plugin: FlextPlugin) -> FlextResult[bool]:
        ...         # Load plugin into isolated environment
        ...         # Register plugin services and dependencies
        ...         # Track plugin state and resources
        ...         pass
    """

    @abstractmethod
    def load_plugin(self, plugin: FlextPlugin) -> FlextResult[bool]:
        """Load a plugin.

        Args:
            plugin: Plugin to load

        Returns:
            FlextResult indicating if loading was successful

        """

    @abstractmethod
    def unload_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Unload a plugin.

        Args:
            plugin_name: Name of plugin to unload

        Returns:
            FlextResult indicating if unloading was successful

        """

    @abstractmethod
    def is_plugin_loaded(self, plugin_name: str) -> FlextResult[bool]:
        """Check if a plugin is loaded.

        Args:
            plugin_name: Name of plugin to check

        Returns:
            FlextResult indicating if plugin is loaded

        """


class FlextPluginManagerPort(ABC):
    """Domain port interface for comprehensive plugin management and configuration.

    Defines the contract for high-level plugin management capabilities required
    by the domain layer. Implementations of this port handle complex plugin
    management workflows including installation, configuration, and lifecycle
    coordination across the entire plugin ecosystem.

    This port abstracts the complexity of plugin management, enabling the domain
    layer to request sophisticated plugin operations without being coupled to
    specific management strategies, storage mechanisms, or configuration formats.

    Key Responsibilities:
        - Plugin installation and removal operations
        - Plugin configuration management and persistence
        - Plugin enable/disable lifecycle coordination
        - Plugin dependency resolution and validation
        - Integration with plugin registries and repositories

    Management Operations:
        - Installation with dependency resolution
        - Configuration validation and persistence
        - Lifecycle state management and coordination
        - Security validation and permission management
        - Performance monitoring and optimization

    Configuration Management:
        - Schema validation and type checking
        - Configuration versioning and migration
        - Environment-specific configuration handling
        - Configuration backup and recovery
        - Real-time configuration updates and hot-reload

    Security Considerations:
        - Plugin authentication and authorization
        - Permission validation and enforcement
        - Security scanning and vulnerability detection
        - Secure configuration storage and access
        - Audit logging and compliance tracking

    Implementation Considerations:
        - Must provide comprehensive dependency resolution
        - Should implement robust configuration validation
        - Must handle complex plugin installation workflows
        - Should support rollback and recovery operations
        - Must provide secure configuration management

    Example Implementation:
        >>> class ComprehensiveManagerAdapter(FlextPluginManagerPort):
        ...     def install_plugin(self, plugin_path: str) -> FlextResult[FlextPlugin]:
        ...         # Validate plugin package and dependencies
        ...         # Install plugin with proper security checks
        ...         # Configure plugin and register services
        ...         # Return installed plugin entity
        ...         pass
    """

    @abstractmethod
    def install_plugin(self, plugin_path: str) -> FlextResult[FlextPlugin]:
        """Install a plugin from the given path.

        Args:
            plugin_path: Path to plugin to install

        Returns:
            FlextResult containing installed plugin

        """

    @abstractmethod
    def uninstall_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Uninstall a plugin.

        Args:
            plugin_name: Name of plugin to uninstall

        Returns:
            FlextResult indicating if uninstallation was successful

        """

    @abstractmethod
    def enable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Enable a plugin.

        Args:
            plugin_name: Name of plugin to enable

        Returns:
            FlextResult indicating if enabling was successful

        """

    @abstractmethod
    def disable_plugin(self, plugin_name: str) -> FlextResult[bool]:
        """Disable a plugin.

        Args:
            plugin_name: Name of plugin to disable

        Returns:
            FlextResult indicating if disabling was successful

        """

    @abstractmethod
    def get_plugin_config(self, plugin_name: str) -> FlextResult[FlextPluginConfig]:
        """Get configuration for a plugin.

        Args:
            plugin_name: Name of plugin to get config for

        Returns:
            FlextResult containing plugin configuration

        """

    @abstractmethod
    def update_plugin_config(
        self,
        plugin_name: str,
        config: FlextPluginConfig,
    ) -> FlextResult[bool]:
        """Update configuration for a plugin.

        Args:
            plugin_name: Name of plugin to update config for
            config: New plugin configuration

        Returns:
            FlextResult indicating if update was successful

        """


# Backwards compatibility aliases
PluginDiscoveryPort = FlextPluginDiscoveryPort
PluginLoaderPort = FlextPluginLoaderPort
PluginManagerPort = FlextPluginManagerPort

# Service aliases for tests (mapped to appropriate ports)
PluginDiscoveryService = FlextPluginDiscoveryPort
PluginExecutionService = FlextPluginLoaderPort  # Execution is handled by loader
PluginHotReloadService = FlextPluginLoaderPort  # Hot reload is a loader concern
PluginLifecycleService = FlextPluginManagerPort  # Lifecycle is managed by manager
PluginRegistryService = FlextPluginManagerPort  # Registry is managed by manager
PluginSecurityService = FlextPluginManagerPort  # Security is a manager concern
PluginValidationService = FlextPluginDiscoveryPort  # Validation is part of discovery
