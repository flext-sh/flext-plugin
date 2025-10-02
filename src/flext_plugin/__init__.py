"""FLEXT Plugin System - Enterprise-grade plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_core import FlextTypes

from flext_plugin.version import VERSION, FlextPluginVersion

PROJECT_VERSION: Final[FlextPluginVersion] = VERSION

__version__: str = VERSION.version
__version_info__: tuple[int | str, ...] = VERSION.version_info

from flext_plugin.config import FlextPluginConfig
from flext_plugin.constants import FlextPluginConstants
from flext_plugin.discovery import PluginDiscovery
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
from flext_plugin.flext_plugin_handlers import (
    FlextPluginEventHandler,
    FlextPluginHandler,
    FlextPluginRegistrationHandler,
)
from flext_plugin.flext_plugin_platform import (
    FlextPluginPlatform,
)
from flext_plugin.flext_plugin_services import (
    FlextPluginDiscoveryService,
    FlextPluginService,
    FlextPluginServices,
    PluginDiscoveryService,
    PluginService,
    create_plugin_manager,
)
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
from flext_plugin.implementations import (
    ConcreteDataPlugin,
    ConcreteExecutablePlugin,
    ConcretePlugin,
    ConcretePluginContext,
    ConcretePluginLoader,
    ConcretePluginRegistry,
    ConcreteTransformPlugin,
)
from flext_plugin.loader import (
    CleanupablePlugin,
    PluginLoader,
)
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
from flext_plugin.ports import (
    FlextPluginDiscoveryPort,
    FlextPluginHotReloadPort,
    FlextPluginLoaderPort,
    FlextPluginManagerPort,
    FlextPluginRegistryPort,
)
from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.real_adapters import (
    RealPluginDiscoveryAdapter,
    RealPluginLoaderAdapter,
    RealPluginManagerAdapter,
)
from flext_plugin.simple_api import (
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
    create_flext_plugin_registry,
    create_plugin_config_from_dict,
    create_plugin_from_dict,
)
from flext_plugin.simple_plugin import (
    Plugin as SimplePlugin,
)
from flext_plugin.simple_plugin import (
    PluginRegistry as SimplePluginRegistry,
)
from flext_plugin.simple_plugin import (
    create_registry,
    load_plugin,
)
from flext_plugin.utilities import FlextPluginUtilities

PluginConfig = FlextPluginConfig
PluginConfiguration = FlextPluginConfigPluginInstance = FlextPluginEntity

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
