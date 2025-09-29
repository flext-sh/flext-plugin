"""FLEXT Plugin System - Enterprise-grade plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes
from flext_plugin.__version__ import __version__, __version_info__

# Configuration - explicit imports (ACTUAL application configuration)
from flext_plugin.config import FlextPluginConfig

# Constants - explicit imports
from flext_plugin.constants import FlextPluginConstants

# CLI functionality - explicit imports
# Temporarily disabled due to flext-cli dependency issues
# from flext_plugin.cli import (
#     FlextPluginCliService,
#     PluginCLI,
#     install_plugin_legacy,
#     main,
# )
# Discovery - explicit imports
from flext_plugin.discovery import (
    PluginDiscovery,
)

# Core entities - explicit imports
from flext_plugin.entities import (
    FlextPlugin,
    FlextPluginConfigParams,
    FlextPluginEntity,
    FlextPluginExecution,
    FlextPluginMetadata,
    FlextPluginMetadataParams,
    FlextPluginRegistry,
    FlextPluginRegistryParams,
    Plugin,
    PluginExecution,
    PluginMetadata,
    PluginRegistry,
)

# Exceptions - explicit imports
from flext_plugin.exceptions import (
    FlextPluginCompatibilityError,
    FlextPluginConfigurationError,
    FlextPluginConfigurationOperationError,
    FlextPluginDependencyError,
    FlextPluginDiscoveryError,
    FlextPluginDiscoveryOperationError,
    FlextPluginError,
    FlextPluginErrorCodes,
    FlextPluginExceptions,
    FlextPluginExecutionError,
    FlextPluginExecutionOperationError,
    FlextPluginHotReloadError,
    FlextPluginHotReloadOperationError,
    FlextPluginLifecycleError,
    FlextPluginLifecycleOperationError,
    FlextPluginLoadingError,
    FlextPluginLoadOperationError,
    FlextPluginMetadataError,
    FlextPluginPlatformError,
    FlextPluginRegistryError,
    FlextPluginSecurityError,
    FlextPluginValidationError,
)

# Handlers - explicit imports
from flext_plugin.flext_plugin_handlers import (
    FlextPluginEventHandler,
    FlextPluginHandler,
    FlextPluginRegistrationHandler,
)

# Models - explicit imports
from flext_plugin.models import (
    FlextPluginConfigModel,
    FlextPluginMetadataModel,
    FlextPluginModel,
    FlextPluginModels,
    PluginExecutionContextModel,
    PluginExecutionResultModel,
    PluginManagerResultModel,
    PluginStatus,
    PluginType,
)

# Platform - explicit imports
from flext_plugin.flext_plugin_platform import (
    FlextPluginPlatform,
)

# Services - explicit imports
from flext_plugin.flext_plugin_services import (
    FlextPluginDiscoveryService,
    FlextPluginService,
    FlextPluginServices,
    PluginDiscoveryService,
    PluginService,
    create_plugin_manager,
)

# Hot reload - explicit imports
from flext_plugin.hot_reload import (
    HotReloadManager,
    PluginFileHandler,
    PluginState,
    PluginWatcher,
    ReloadEvent,
    RollbackManager,
    StatefulPlugin,
    StateManager,
    WatchEvent,
    WatchEventType,
    create_hot_reload_manager,
)

# Implementations - explicit imports
from flext_plugin.implementations import (
    ConcreteDataPlugin,
    ConcreteExecutablePlugin,
    ConcretePlugin,
    ConcretePluginContext,
    ConcretePluginLoader,
    ConcretePluginRegistry,
    ConcreteTransformPlugin,
)

# Loader - explicit imports
from flext_plugin.loader import (
    CleanupablePlugin,
    PluginLoader,
)

# Ports - explicit imports
from flext_plugin.ports import (
    FlextPluginDiscoveryPort,
    FlextPluginHotReloadPort,
    FlextPluginLoaderPort,
    FlextPluginManagerPort,
    FlextPluginRegistryPort,
)

# Protocols - explicit imports
from flext_plugin.protocols import FlextPluginProtocols

# Real adapters - explicit imports
from flext_plugin.real_adapters import (
    RealPluginDiscoveryAdapter,
    RealPluginLoaderAdapter,
    RealPluginManagerAdapter,
)

# Simple API - explicit imports
from flext_plugin.simple_api import (
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
    create_flext_plugin_registry,
    create_plugin_config_from_dict,
    create_plugin_from_dict,
)

# Simple plugin - explicit imports
from flext_plugin.simple_plugin import (
    Plugin as SimplePlugin,
    PluginRegistry as SimplePluginRegistry,
    create_registry,
    load_plugin,
)

# Utilities - explicit imports
from flext_plugin.utilities import FlextPluginUtilities

# Aliases for backward compatibility and convenience
PluginConfig = FlextPluginConfig
PluginConfiguration = FlextPluginConfig  # For backward compatibility
PluginInstance = FlextPluginEntity

__all__: FlextTypes.Core.StringList = [
    "CleanupablePlugin",
    "ConcreteDataPlugin",
    "ConcreteExecutablePlugin",
    "ConcretePlugin",
    "ConcretePluginContext",
    "ConcretePluginLoader",
    "ConcretePluginRegistry",
    "ConcreteTransformPlugin",
    "FlextPlugin",
    "FlextPluginCompatibilityError",
    "FlextPluginConfig",
    "FlextPluginConfigModel",
    "FlextPluginConfigParams",
    "FlextPluginConfigurationError",
    "FlextPluginConfigurationOperationError",
    "FlextPluginConstants",
    "FlextPluginDependencyError",
    "FlextPluginDiscoveryError",
    "FlextPluginDiscoveryOperationError",
    "FlextPluginDiscoveryPort",
    "FlextPluginDiscoveryService",
    "FlextPluginEntity",
    "FlextPluginError",
    "FlextPluginErrorCodes",
    "FlextPluginEventHandler",
    "FlextPluginExceptions",
    "FlextPluginExecution",
    "FlextPluginExecutionError",
    "FlextPluginExecutionOperationError",
    "FlextPluginHandler",
    "FlextPluginHotReloadError",
    "FlextPluginHotReloadOperationError",
    "FlextPluginHotReloadPort",
    "FlextPluginLifecycleError",
    "FlextPluginLifecycleOperationError",
    "FlextPluginLoadOperationError",
    "FlextPluginLoaderPort",
    "FlextPluginLoadingError",
    "FlextPluginManagerPort",
    "FlextPluginMetadata",
    "FlextPluginMetadataError",
    "FlextPluginMetadataModel",
    "FlextPluginMetadataParams",
    "FlextPluginModel",
    "FlextPluginModels",
    "FlextPluginPlatform",
    "FlextPluginPlatformError",
    "FlextPluginProtocols",
    "FlextPluginRegistrationHandler",
    "FlextPluginRegistry",
    "FlextPluginRegistryError",
    "FlextPluginRegistryParams",
    "FlextPluginRegistryPort",
    "FlextPluginSecurityError",
    "FlextPluginService",
    "FlextPluginServices",
    "FlextPluginUtilities",
    "FlextPluginValidationError",
    "HotReloadManager",
    "Plugin",
    "PluginConfig",
    "PluginConfiguration",
    "PluginDiscovery",
    "PluginDiscoveryService",
    "PluginExecution",
    "PluginExecutionContextModel",
    "PluginExecutionResultModel",
    "PluginFileHandler",
    "PluginInstance",
    "PluginLoader",
    "PluginManagerResultModel",
    "PluginMetadata",
    "PluginRegistry",
    "PluginService",
    "PluginState",
    "PluginStatus",
    "PluginType",
    "PluginWatcher",
    "RealPluginDiscoveryAdapter",
    "RealPluginLoaderAdapter",
    "RealPluginManagerAdapter",
    "ReloadEvent",
    "RollbackManager",
    "SimplePlugin",
    "SimplePluginRegistry",
    "StateManager",
    "StatefulPlugin",
    "WatchEvent",
    "WatchEventType",
    "__version__",
    "__version_info__",
    "create_flext_plugin",
    "create_flext_plugin_config",
    "create_flext_plugin_metadata",
    "create_flext_plugin_registry",
    "create_hot_reload_manager",
    "create_plugin_config_from_dict",
    "create_plugin_from_dict",
    "create_plugin_manager",
    "create_registry",
    "load_plugin",
]
