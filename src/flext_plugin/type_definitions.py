"""Centralized type definitions for the FLEXT Plugin system.

Type variables, protocols, and type aliases following flext-core patterns
for consistent typing across the plugin ecosystem.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping, Sequence
from typing import Protocol, TypeVar

from flext_core import FlextResult

# =============================================================================
# PLUGIN SYSTEM TYPE VARIABLES
# =============================================================================

# Plugin-specific type variables
TPlugin = TypeVar("TPlugin")  # Generic plugin type
TPluginConfig = TypeVar("TPluginConfig")  # Plugin configuration type
TPluginMetadata = TypeVar("TPluginMetadata")  # Plugin metadata type
TPluginResult = TypeVar("TPluginResult")  # Plugin operation result type
TPluginData = TypeVar("TPluginData")  # Plugin data type
TPluginContext = TypeVar("TPluginContext")  # Plugin execution context type

# Service and handler type variables
TPluginService = TypeVar("TPluginService")  # Plugin service type
TPluginHandler = TypeVar("TPluginHandler")  # Plugin handler type
TPluginManager = TypeVar("TPluginManager")  # Plugin manager type
TPluginRegistry = TypeVar("TPluginRegistry")  # Plugin registry type

# Discovery and loading type variables
TPluginDiscovery = TypeVar("TPluginDiscovery")  # Plugin discovery type
TPluginLoader = TypeVar("TPluginLoader")  # Plugin loader type
TPluginValidator = TypeVar("TPluginValidator")  # Plugin validator type

# Platform and system type variables
TPluginPlatform = TypeVar("TPluginPlatform")  # Plugin platform type
TPluginSystem = TypeVar("TPluginSystem")  # Plugin system type

# =============================================================================
# PLUGIN PROTOCOLS
# =============================================================================


class PluginProtocol(Protocol):
    """Protocol for plugin instances."""

    @property
    def name(self) -> str:
        """Plugin name."""
        ...

    @property
    def version(self) -> str:
        """Plugin version."""
        ...

    async def initialize(self) -> FlextResult[bool]:
        """Initialize the plugin."""
        ...

    async def cleanup(self) -> FlextResult[bool]:
        """Cleanup plugin resources."""
        ...


class PluginExecutorProtocol(Protocol):
    """Protocol for plugin execution."""

    async def execute(
        self,
        plugin_name: str,
        data: dict[str, PluginConfigData],
        context: dict[str, PluginConfigData] | None = None,
    ) -> FlextResult[PluginConfigData]:
        """Execute a plugin with data."""
        ...


class PluginDiscoveryProtocol(Protocol):
    """Protocol for plugin discovery."""

    async def discover_plugins(
        self,
        path: str,
        *,
        recursive: bool = True,
    ) -> FlextResult[list[str]]:
        """Discover plugins in a path."""
        ...


class PluginLoaderProtocol(Protocol):
    """Protocol for plugin loading."""

    async def load_plugin(
        self,
        plugin_path: str,
    ) -> FlextResult[object]:
        """Load a plugin from path."""
        ...

    async def unload_plugin(
        self,
        plugin_name: str,
    ) -> FlextResult[bool]:
        """Unload a plugin by name."""
        ...


class PluginRegistryProtocol(Protocol):
    """Protocol for plugin registry."""

    async def register_plugin(
        self,
        plugin: object,
    ) -> FlextResult[bool]:
        """Register a plugin."""
        ...

    async def unregister_plugin(
        self,
        plugin_name: str,
    ) -> FlextResult[bool]:
        """Unregister a plugin."""
        ...

    def get_plugin(
        self,
        plugin_name: str,
    ) -> object | None:
        """Get a plugin by name."""
        ...

    def list_plugins(self) -> list[object]:
        """List all registered plugins."""
        ...


class PluginValidatorProtocol(Protocol):
    """Protocol for plugin validation."""

    async def validate_plugin(
        self,
        plugin: object,
    ) -> FlextResult[bool]:
        """Validate a plugin."""
        ...


class HotReloadProtocol(Protocol):
    """Protocol for hot reload functionality."""

    async def start_watching(
        self,
        path: str,
        callback: Callable[[str], Awaitable[None]],
    ) -> FlextResult[bool]:
        """Start watching for changes."""
        ...

    async def stop_watching(self) -> FlextResult[bool]:
        """Stop watching for changes."""
        ...


# =============================================================================
# TYPE ALIASES
# =============================================================================

# Basic type aliases
PluginName = str
PluginVersion = str
PluginId = str
ExecutionId = str

# Core data type definition using forward-compatible typing
# Use typing.Union for better Pydantic compatibility
PluginConfigData = str | int | float | bool | dict[str, object] | list[object] | None

# Configuration type aliases
PluginConfigDict = dict[str, PluginConfigData]
PluginMetadataDict = dict[str, PluginConfigData]
PluginRuntimeDict = dict[str, PluginConfigData]

# Collection type aliases
PluginList = list[TPlugin]
PluginNameList = list[PluginName]
PluginDict = dict[PluginName, TPlugin]

# Path and URL type aliases
PluginPath = str
PluginUrl = str
DirectoryPath = str

# Function type aliases
PluginFactory = Callable[[], object]
PluginCallback = Callable[[TPlugin], Awaitable[None]]
PluginErrorCallback = Callable[[Exception], Awaitable[None]]
FileChangeCallback = Callable[[str], Awaitable[None]]

# Result type aliases
PluginResult = FlextResult[object]
PluginListResult = FlextResult[list[object]]
PluginBoolResult = FlextResult[bool]
PluginDataResult = FlextResult[PluginConfigData]
PluginStringResult = FlextResult[str]

# Service type aliases
PluginServiceDict = dict[str, TPluginService]
PluginHandlerDict = dict[str, TPluginHandler]

# Execution type aliases
ExecutionContextDict = dict[str, PluginConfigData]
ExecutionInputDict = dict[str, PluginConfigData]
ExecutionOutputDict = dict[str, PluginConfigData]

# Discovery type aliases
DiscoveryPathList = list[str]
DiscoveryPattern = str
DiscoveryFilters = dict[str, PluginConfigData]

# Platform type aliases
PlatformConfig = dict[str, PluginConfigData]
PlatformServices = dict[str, object]
PlatformHandlers = dict[str, object]

# =============================================================================
# UNION TYPES
# =============================================================================

# Plugin data unions
# PluginConfigData is now defined earlier in TYPE ALIASES section
PluginData = PluginConfigData
PluginConfigValue = PluginConfigData

# Plugin identifier unions
PluginIdentifier = PluginName | PluginId

# Path unions
PluginPathOrUrl = PluginPath | PluginUrl

# Result unions
PluginOperationResult = PluginResult | PluginBoolResult | PluginStringResult

# =============================================================================
# GENERIC ALIASES
# =============================================================================

# Generic plugin container
PluginContainer = dict[str, TPlugin]

# Generic plugin mapping
PluginMapping = Mapping[str, TPlugin]

# Generic plugin sequence
PluginSequence = Sequence[TPlugin]

# Generic configuration mapping
ConfigMapping = Mapping[str, PluginConfigData]

# Generic metadata mapping
MetadataMapping = Mapping[str, PluginConfigData]

__all__ = [
    "ConfigMapping",
    "DirectoryPath",
    "DiscoveryFilters",
    # Discovery Aliases
    "DiscoveryPathList",
    "DiscoveryPattern",
    # Execution Aliases
    "ExecutionContextDict",
    "ExecutionId",
    "ExecutionInputDict",
    "ExecutionOutputDict",
    "FileChangeCallback",
    "HotReloadProtocol",
    "MetadataMapping",
    # Platform Aliases
    "PlatformConfig",
    "PlatformHandlers",
    "PlatformServices",
    "PluginBoolResult",
    "PluginCallback",
    # Configuration Aliases
    "PluginConfigDict",
    "PluginConfigValue",
    # Generic Aliases
    "PluginContainer",
    # Union Types
    "PluginData",
    "PluginDataResult",
    "PluginDict",
    "PluginDiscoveryProtocol",
    "PluginErrorCallback",
    "PluginExecutorProtocol",
    # Function Aliases
    "PluginFactory",
    "PluginHandlerDict",
    "PluginId",
    "PluginIdentifier",
    # Collection Aliases
    "PluginList",
    "PluginListResult",
    "PluginLoaderProtocol",
    "PluginMapping",
    "PluginMetadataDict",
    # Basic Aliases
    "PluginName",
    "PluginNameList",
    "PluginOperationResult",
    # Path Aliases
    "PluginPath",
    "PluginPathOrUrl",
    # Protocols
    "PluginProtocol",
    "PluginRegistryProtocol",
    # Result Aliases
    "PluginResult",
    "PluginRuntimeDict",
    "PluginSequence",
    # Service Aliases
    "PluginServiceDict",
    "PluginStringResult",
    "PluginUrl",
    "PluginValidatorProtocol",
    "PluginVersion",
    # Type Variables
    "TPlugin",
    "TPluginConfig",
    "TPluginContext",
    "TPluginData",
    "TPluginDiscovery",
    "TPluginHandler",
    "TPluginLoader",
    "TPluginManager",
    "TPluginMetadata",
    "TPluginPlatform",
    "TPluginRegistry",
    "TPluginResult",
    "TPluginService",
    "TPluginSystem",
    "TPluginValidator",
]
