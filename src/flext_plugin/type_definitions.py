"""Centralized type definitions for the FLEXT Plugin system.

Type variables, protocols, and type aliases following flext-core patterns
for consistent typing across the plugin ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping, Sequence

from flext_core import (
    FlextProtocols,
    FlextResult,
    FlextTypes,
    # Plugin-specific TypeVars
    TPlugin,
    TPluginConfig,
    TPluginContext,
    TPluginData,
    TPluginDiscovery,
    TPluginHandler,
    TPluginLoader,
    TPluginManager,
    TPluginMetadata,
    TPluginPlatform,
    TPluginRegistry,
    TPluginService,
    TPluginSystem,
    TPluginValidator,
)

# All Plugin TypeVars now imported from flext-core centralized TypeVars


# Use flext-core plugin protocol instead of local definition
PluginProtocol = FlextProtocols.Extensions.Plugin


# Plugin execution uses Application Handler pattern
PluginExecutorProtocol = FlextProtocols.Application.Handler


# Plugin discovery uses Domain Service pattern
PluginDiscoveryProtocol = FlextProtocols.Domain.Service


# Plugin loading uses Service pattern
PluginLoaderProtocol = FlextProtocols.Domain.Service


# Plugin registry uses Repository pattern
PluginRegistryProtocol = FlextProtocols.Domain.Repository


# Plugin validation uses Validator pattern
PluginValidatorProtocol = FlextProtocols.Foundation.Validator


# Hot reload uses Infrastructure Service pattern
HotReloadProtocol = FlextProtocols.Domain.Service


# Basic type aliases
PluginName = str
PluginVersion = str
PluginId = str
ExecutionId = str

# Core data type definition using forward-compatible typing
# Use typing.Union for better Pydantic compatibility
PluginConfigData = (str | int | float) | (
    bool | FlextTypes.Core.Dict | FlextTypes.Core.List | None
)

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
PluginListResult = FlextResult[FlextTypes.Core.List]
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
DiscoveryPathList = FlextTypes.Core.StringList
DiscoveryPattern = str
DiscoveryFilters = dict[str, PluginConfigData]

# Platform type aliases
PlatformConfig = dict[str, PluginConfigData]
PlatformServices = FlextTypes.Core.Dict
PlatformHandlers = FlextTypes.Core.Dict


# Plugin data unions
# PluginConfigData is now defined earlier in TYPE ALIASES section
PluginData = PluginConfigData
PluginConfigValue = PluginConfigData

# Plugin identifier unions
PluginIdentifier = PluginName | PluginId

# Path unions
PluginPathOrUrl = PluginPath | PluginUrl

# Result unions
PluginOperationResult = (PluginResult | PluginBoolResult) | PluginStringResult


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
