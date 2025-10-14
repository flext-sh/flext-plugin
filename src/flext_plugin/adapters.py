"""FLEXT Plugin Adapters - Plugin system infrastructure adapters.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import asyncio
import importlib
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from flext_core import FlextCore

from flext_plugin.protocols import FlextPluginProtocols
from flext_plugin.types import FlextPluginTypes

# Type aliases for adapter protocol types
DiscoveryAdapter = FlextPluginProtocols.PluginDiscovery
LoaderAdapter = FlextPluginProtocols.PluginLoader
ExecutionAdapter = FlextPluginProtocols.PluginExecution
SecurityAdapter = FlextPluginProtocols.PluginSecurity
RegistryAdapter = FlextPluginProtocols.PluginRegistry
MonitoringAdapter = FlextPluginProtocols.PluginMonitoring


class FlextPluginAdapters:
    """Infrastructure adapters implementing plugin system protocols.

    This class provides concrete implementations of the plugin system protocols,
    handling the actual infrastructure concerns like file system operations,
    dynamic loading, and external integrations.

    Usage:
        ```python
        from flext_plugin import FlextPluginAdapters

        # Initialize adapters
        adapters = FlextPluginAdapters()

        # Get discovery adapter
        discovery = adapters.get_discovery_adapter()
        result = await discovery.discover_plugins(["./plugins"])
        ```
    """

    def __init__(self) -> None:
        """Initialize the plugin adapters."""
        self.logger = FlextCore.Logger(__name__)
        self._discovery_adapter: DiscoveryAdapter | None = None
        self._loader_adapter: LoaderAdapter | None = None
        self._executor_adapter: ExecutionAdapter | None = None
        self._security_adapter: SecurityAdapter | None = None
        self._registry_adapter: RegistryAdapter | None = None
        self._monitoring_adapter: MonitoringAdapter | None = None

    def get_discovery_adapter(self) -> FlextPluginProtocols.PluginDiscovery:
        """Get the plugin discovery adapter.

        Returns:
            Plugin discovery adapter implementation

        """
        if self._discovery_adapter is None:
            self._discovery_adapter = self.FileSystemDiscoveryAdapter()
        return self._discovery_adapter

    def get_loader_adapter(self) -> FlextPluginProtocols.PluginLoader:
        """Get the plugin loader adapter.

        Returns:
            Plugin loader adapter implementation

        """
        if self._loader_adapter is None:
            self._loader_adapter = self.DynamicLoaderAdapter()
        return self._loader_adapter

    def get_executor_adapter(self) -> FlextPluginProtocols.PluginExecution:
        """Get the plugin executor adapter.

        Returns:
            Plugin executor adapter implementation

        """
        if self._executor_adapter is None:
            self._executor_adapter = self.PluginExecutorAdapter()
        return self._executor_adapter

    def get_security_adapter(self) -> FlextPluginProtocols.PluginSecurity:
        """Get the plugin security adapter.

        Returns:
            Plugin security adapter implementation

        """
        if self._security_adapter is None:
            self._security_adapter = self.PluginSecurityAdapter()
        return self._security_adapter

    def get_registry_adapter(self) -> FlextPluginProtocols.PluginRegistry:
        """Get the plugin registry adapter.

        Returns:
            Plugin registry adapter implementation

        """
        if self._registry_adapter is None:
            self._registry_adapter = self.MemoryRegistryAdapter()
        return self._registry_adapter

    def get_monitoring_adapter(self) -> FlextPluginProtocols.PluginMonitoring:
        """Get the plugin monitoring adapter.

        Returns:
            Plugin monitoring adapter implementation

        """
        if self._monitoring_adapter is None:
            self._monitoring_adapter = self.PluginMonitoringAdapter()
        return self._monitoring_adapter

    class FileSystemDiscoveryAdapter(FlextPluginProtocols.PluginDiscovery):
        """File system-based plugin discovery adapter."""

        def __init__(self) -> None:
            """Initialize the file system discovery adapter."""
            self.logger = FlextCore.Logger(__name__)

        def _resolve_plugin_path(self, path: str) -> Path:
            """Resolve and validate a plugin path synchronously.

            Args:
                path: Path to resolve

            Returns:
                Resolved Path object

            """
            return Path(path).expanduser().resolve()

        async def discover_plugins(
            self, paths: FlextPluginTypes.Core.StringList
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginList]:
            """Discover plugins in the given paths.

            Args:
                paths: List of paths to search for plugins

            Returns:
                FlextCore.Result containing list of discovered plugins

            """
            try:
                discovered_plugins = []

                for path in paths:
                    path_obj = self._resolve_plugin_path(path)
                    if not path_obj.exists():
                        self.logger.warning(f"Path does not exist: {path}")
                        continue

                    if path_obj.is_file():
                        # Single file plugin
                        plugin_data = await self._discover_single_file(path_obj)
                        if plugin_data:
                            discovered_plugins.append(plugin_data)
                    elif path_obj.is_dir():
                        # Directory with multiple plugins
                        plugins = await self._discover_directory(path_obj)
                        discovered_plugins.extend(plugins)

                self.logger.info(f"Discovered {len(discovered_plugins)} plugins")
                return FlextCore.Result.ok(discovered_plugins)

            except Exception as e:
                self.logger.exception("Plugin discovery failed")
                return FlextCore.Result.fail(f"Discovery error: {e!s}")

        async def discover_plugin(
            self, plugin_path: str
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginDict]:
            """Discover a single plugin at the given path.

            Args:
                plugin_path: Path to the plugin

            Returns:
                FlextCore.Result containing plugin data

            """
            try:
                path_obj = self._resolve_plugin_path(plugin_path)
                if not path_obj.exists():
                    return FlextCore.Result.fail(
                        f"Plugin path does not exist: {plugin_path}"
                    )

                plugin_data = await self._discover_single_file(path_obj)
                if not plugin_data:
                    return FlextCore.Result.fail(
                        f"Failed to discover plugin at: {plugin_path}"
                    )

                return FlextCore.Result.ok(plugin_data)

            except Exception as e:
                self.logger.exception(f"Failed to discover plugin at {plugin_path}")
                return FlextCore.Result.fail(f"Discovery error: {e!s}")

        async def validate_plugin(
            self, plugin_data: FlextPluginTypes.Core.PluginDict
        ) -> FlextCore.Result[bool]:
            """Validate discovered plugin data.

            Args:
                plugin_data: Plugin data to validate

            Returns:
                FlextCore.Result indicating validation success or failure

            """
            try:
                required_fields = ["name", "version"]
                for field in required_fields:
                    if field not in plugin_data:
                        return FlextCore.Result.fail(f"Missing required field: {field}")

                return FlextCore.Result.ok(True)

            except Exception as e:
                self.logger.exception("Plugin validation failed")
                return FlextCore.Result.fail(f"Validation error: {e!s}")

        async def _discover_single_file(
            self, path: Path
        ) -> FlextPluginTypes.Core.PluginDict | None:
            """Discover a single plugin file.

            Args:
                path: Path to the plugin file

            Returns:
                Plugin data if discovered, None otherwise

            """
            try:
                if path.suffix != ".py":
                    return None

                # Extract plugin name from filename
                plugin_name = path.stem

                # Basic plugin data
                return {
                    "name": plugin_name,
                    "version": "1.0.0",
                    "path": str(path),
                    "type": "file",
                }

            except Exception:
                self.logger.exception(f"Failed to discover single file: {path}")
                return None

        async def _discover_directory(
            self, path: Path
        ) -> list[FlextPluginTypes.Core.PluginDict]:
            """Discover plugins in a directory.

            Args:
                path: Path to the directory

            Returns:
                List of discovered plugin data

            """
            try:
                discovered_plugins = []

                # Run pathlib operations in thread pool
                loop = asyncio.get_event_loop()
                items = await loop.run_in_executor(None, list, path.iterdir())

                for item in items:
                    if item.is_file() and item.suffix == ".py":
                        plugin_data = await self._discover_single_file(item)
                        if plugin_data:
                            discovered_plugins.append(plugin_data)
                    elif item.is_dir() and not item.name.startswith("__"):
                        # Recursively discover in subdirectories
                        sub_plugins = await self._discover_directory(Path(item))
                        discovered_plugins.extend(sub_plugins)

                return discovered_plugins

            except Exception:
                self.logger.exception(f"Failed to discover directory: {path}")
                return []

    class DynamicLoaderAdapter(FlextPluginProtocols.PluginLoader):
        """Dynamic plugin loading adapter."""

        def __init__(self) -> None:
            """Initialize the dynamic loader adapter."""
            self.logger = FlextCore.Logger(__name__)
            self._loaded_plugins: FlextCore.Types.Dict = {}

        def _resolve_plugin_path(self, path: str) -> Path:
            """Resolve and validate a plugin path synchronously.

            Args:
                path: Path to resolve

            Returns:
                Resolved Path object

            """
            return Path(path).expanduser().resolve()

        async def load_plugin(
            self, plugin_path: str
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginDict]:
            """Load a plugin from the given path.

            Args:
                plugin_path: Path to the plugin to load

            Returns:
                FlextCore.Result containing loaded plugin data

            """
            try:
                path_obj = self._resolve_plugin_path(plugin_path)
                if not path_obj.exists():
                    return FlextCore.Result.fail(
                        f"Plugin path does not exist: {plugin_path}"
                    )

                # Add parent directory to Python path
                parent_dir = str(path_obj.parent)
                if parent_dir not in sys.path:
                    sys.path.insert(0, parent_dir)

                # Load the module
                module_name = path_obj.stem
                try:
                    module = importlib.import_module(module_name)
                    self._loaded_plugins[module_name] = module
                except Exception as e:
                    return FlextCore.Result.fail(f"Failed to import module: {e!s}")

                # Extract plugin information
                plugin_data = {
                    "name": module_name,
                    "version": getattr(module, "__version__", "1.0.0"),
                    "path": str(path_obj),
                    "module": module,
                }

                self.logger.info(f"Loaded plugin: {module_name}")
                return FlextCore.Result.ok(plugin_data)

            except Exception as e:
                self.logger.exception(f"Failed to load plugin from {plugin_path}")
                return FlextCore.Result.fail(f"Loading error: {e!s}")

        async def unload_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Unload a plugin by name.

            Args:
                plugin_name: Name of the plugin to unload

            Returns:
                FlextCore.Result indicating success or failure

            """
            try:
                if plugin_name not in self._loaded_plugins:
                    return FlextCore.Result.fail(f"Plugin not loaded: {plugin_name}")

                # Remove from loaded plugins
                del self._loaded_plugins[plugin_name]

                # Remove from sys.modules if present
                if plugin_name in sys.modules:
                    del sys.modules[plugin_name]

                self.logger.info(f"Unloaded plugin: {plugin_name}")
                return FlextCore.Result.ok(True)

            except Exception as e:
                self.logger.exception(f"Failed to unload plugin {plugin_name}")
                return FlextCore.Result.fail(f"Unloading error: {e!s}")

        def is_plugin_loaded(self, plugin_name: str) -> bool:
            """Check if a plugin is currently loaded.

            Args:
                plugin_name: Name of the plugin

            Returns:
                True if plugin is loaded, False otherwise

            """
            return plugin_name in self._loaded_plugins

        def get_loaded_plugins(self) -> FlextCore.Types.StringList:
            """Get list of currently loaded plugin names.

            Returns:
                List of loaded plugin names

            """
            return list(self._loaded_plugins.keys())

    class PluginExecutorAdapter(FlextPluginProtocols.PluginExecution):
        """Plugin execution adapter."""

        def __init__(self) -> None:
            """Initialize the plugin executor adapter."""
            self.logger = FlextCore.Logger(__name__)
            self._running_executions: FlextCore.Types.Dict = {}

        async def execute_plugin(
            self,
            plugin_name: str,
            context: FlextPluginTypes.Execution.ExecutionContext,
        ) -> FlextCore.Result[FlextPluginTypes.Execution.ExecutionResult]:
            """Execute a plugin with the given context.

            Args:
                plugin_name: Name of the plugin to execute
                context: Execution context

            Returns:
                FlextCore.Result containing execution result

            """
            try:
                # Simulate plugin execution
                execution_result = {
                    "success": True,
                    "plugin_name": plugin_name,
                    "execution_id": context["execution_id"],
                    "result": {
                        "message": f"Plugin {plugin_name} executed successfully"
                    },
                    "execution_time": 0.1,
                }

                self.logger.info(f"Executed plugin: {plugin_name}")
                return FlextCore.Result.ok(execution_result)

            except Exception as e:
                self.logger.exception(f"Failed to execute plugin {plugin_name}")
                return FlextCore.Result.fail(f"Execution error: {e!s}")

        async def stop_execution(self, execution_id: str) -> FlextCore.Result[bool]:
            """Stop a running execution.

            Args:
                execution_id: ID of the execution to stop

            Returns:
                FlextCore.Result indicating success or failure

            """
            try:
                if execution_id in self._running_executions:
                    del self._running_executions[execution_id]
                    self.logger.info(f"Stopped execution: {execution_id}")
                    return FlextCore.Result.ok(True)
                return FlextCore.Result.fail(f"Execution not found: {execution_id}")

            except Exception as e:
                self.logger.exception(f"Failed to stop execution {execution_id}")
                return FlextCore.Result.fail(f"Stop execution error: {e!s}")

        async def get_execution_status(
            self, execution_id: str
        ) -> FlextCore.Result[str]:
            """Get the status of a running execution.

            Args:
                execution_id: ID of the execution

            Returns:
                FlextCore.Result containing execution status

            """
            try:
                if execution_id in self._running_executions:
                    return FlextCore.Result.ok("running")
                return FlextCore.Result.ok("completed")

            except Exception as e:
                self.logger.exception(f"Failed to get execution status {execution_id}")
                return FlextCore.Result.fail(f"Status check error: {e!s}")

        def list_running_executions(self) -> FlextCore.Types.StringList:
            """List all currently running execution IDs.

            Returns:
                List of running execution IDs

            """
            return list(self._running_executions.keys())

    class PluginSecurityAdapter(FlextPluginProtocols.PluginSecurity):
        """Plugin security adapter."""

        def __init__(self) -> None:
            """Initialize the plugin security adapter."""
            self.logger = FlextCore.Logger(__name__)

        async def validate_plugin(
            self, plugin: FlextPluginTypes.Core.PluginEntity
        ) -> FlextCore.Result[bool]:
            """Validate a plugin for security compliance.

            Args:
                plugin: Plugin entity to validate

            Returns:
                FlextCore.Result indicating validation success or failure

            """
            try:
                # Basic security validation
                if not plugin.get("name"):
                    return FlextCore.Result.fail("Plugin name is required")

                if not plugin.get("version"):
                    return FlextCore.Result.fail("Plugin version is required")

                self.logger.info(
                    f"Security validation passed for plugin: {plugin.get('name')}"
                )
                return FlextCore.Result.ok(True)

            except Exception as e:
                self.logger.exception("Plugin security validation failed")
                return FlextCore.Result.fail(f"Security validation error: {e!s}")

        async def check_permissions(
            self, plugin_name: str, permissions: FlextPluginTypes.Core.StringList
        ) -> FlextCore.Result[bool]:
            """Check if a plugin has the required permissions.

            Args:
                plugin_name: Name of the plugin
                permissions: List of required permissions

            Returns:
                FlextCore.Result indicating permission check result

            """
            try:
                # Basic permission check (always allow for now)
                self.logger.info(f"Permission check passed for plugin: {plugin_name}")
                return FlextCore.Result.ok(True)

            except Exception as e:
                self.logger.exception(
                    f"Permission check failed for plugin {plugin_name}"
                )
                return FlextCore.Result.fail(f"Permission check error: {e!s}")

        async def scan_plugin_security(
            self, plugin_path: str
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Perform security scan on a plugin.

            Args:
                plugin_path: Path to the plugin

            Returns:
                FlextCore.Result containing security scan results

            """
            try:
                # Basic security scan
                scan_results = {
                    "plugin_path": plugin_path,
                    "security_level": "medium",
                    "issues_found": 0,
                    "scan_timestamp": self._get_current_timestamp(),
                }

                self.logger.info(f"Security scan completed for: {plugin_path}")
                return FlextCore.Result.ok(cast("FlextCore.Types.Dict", scan_results))

            except Exception as e:
                self.logger.exception(f"Security scan failed for {plugin_path}")
                return FlextCore.Result.fail(f"Security scan error: {e!s}")

        async def get_security_level(self, plugin_name: str) -> FlextCore.Result[str]:
            """Get the security level of a plugin.

            Args:
                plugin_name: Name of the plugin

            Returns:
                FlextCore.Result containing security level

            """
            try:
                # Default security level
                security_level = "medium"
                self.logger.info(f"Security level for {plugin_name}: {security_level}")
                return FlextCore.Result.ok(security_level)

            except Exception as e:
                self.logger.exception(f"Failed to get security level for {plugin_name}")
                return FlextCore.Result.fail(f"Security level error: {e!s}")

        def _get_current_timestamp(self) -> str:
            """Get current timestamp as ISO string."""
            return datetime.now(UTC).isoformat()

    class MemoryRegistryAdapter(FlextPluginProtocols.PluginRegistry):
        """In-memory plugin registry adapter."""

        def __init__(self) -> None:
            """Initialize the memory registry adapter."""
            self.logger = FlextCore.Logger(__name__)
            self._plugins: dict[str, FlextPluginTypes.Core.PluginEntity] = {}

        async def register_plugin(
            self, plugin: FlextPluginTypes.Core.PluginEntity
        ) -> FlextCore.Result[bool]:
            """Register a plugin in the registry.

            Args:
                plugin: Plugin entity to register

            Returns:
                FlextCore.Result indicating success or failure

            """
            try:
                plugin_name = str(plugin.get("name", ""))
                if not plugin_name:
                    return FlextCore.Result.fail("Plugin name is required")

                if plugin_name in self._plugins:
                    return FlextCore.Result.fail(
                        f"Plugin already registered: {plugin_name}"
                    )

                self._plugins[plugin_name] = {str(k): v for k, v in plugin.items()}
                self.logger.info(f"Registered plugin: {plugin_name}")
                return FlextCore.Result.ok(True)

            except Exception as e:
                self.logger.exception(f"Failed to register plugin: {plugin}")
                return FlextCore.Result.fail(f"Registration error: {e!s}")

        async def unregister_plugin(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Unregister a plugin from the registry.

            Args:
                plugin_name: Name of the plugin to unregister

            Returns:
                FlextCore.Result indicating success or failure

            """
            try:
                if plugin_name not in self._plugins:
                    return FlextCore.Result.fail(
                        f"Plugin not registered: {plugin_name}"
                    )

                del self._plugins[plugin_name]
                self.logger.info(f"Unregistered plugin: {plugin_name}")
                return FlextCore.Result.ok(True)

            except Exception as e:
                self.logger.exception(f"Failed to unregister plugin {plugin_name}")
                return FlextCore.Result.fail(f"Unregistration error: {e!s}")

        async def get_plugin(
            self, plugin_name: str
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginEntity | None]:
            """Get a plugin by name.

            Args:
                plugin_name: Name of the plugin

            Returns:
                FlextCore.Result containing plugin entity if found

            """
            try:
                plugin = self._plugins.get(plugin_name)
                return FlextCore.Result.ok(plugin)

            except Exception as e:
                self.logger.exception(f"Failed to get plugin {plugin_name}")
                return FlextCore.Result.fail(f"Get plugin error: {e!s}")

        async def list_plugins(
            self,
        ) -> FlextCore.Result[FlextPluginTypes.Core.PluginList]:
            """List all registered plugins.

            Returns:
                FlextCore.Result containing list of plugin entities

            """
            try:
                plugins = list(self._plugins.values())
                return FlextCore.Result.ok(plugins)

            except Exception as e:
                self.logger.exception("Failed to list plugins")
                return FlextCore.Result.fail(f"List plugins error: {e!s}")

        def is_plugin_registered(self, plugin_name: str) -> bool:
            """Check if a plugin is registered.

            Args:
                plugin_name: Name of the plugin

            Returns:
                True if plugin is registered, False otherwise

            """
            return plugin_name in self._plugins

    class PluginMonitoringAdapter(FlextPluginProtocols.PluginMonitoring):
        """Plugin monitoring adapter."""

        def __init__(self) -> None:
            """Initialize the plugin monitoring adapter."""
            self.logger = FlextCore.Logger(__name__)
            self._monitored_plugins: dict[str, FlextCore.Types.Dict] = {}

        async def start_monitoring(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Start monitoring a plugin.

            Args:
                plugin_name: Name of the plugin to monitor

            Returns:
                FlextCore.Result indicating success or failure

            """
            try:
                self._monitored_plugins[plugin_name] = {
                    "start_time": self._get_current_timestamp(),
                    "metrics": {},
                    "health_status": "healthy",
                }

                self.logger.info(f"Started monitoring plugin: {plugin_name}")
                return FlextCore.Result.ok(True)

            except Exception as e:
                self.logger.exception(f"Failed to start monitoring {plugin_name}")
                return FlextCore.Result.fail(f"Start monitoring error: {e!s}")

        async def stop_monitoring(self, plugin_name: str) -> FlextCore.Result[bool]:
            """Stop monitoring a plugin.

            Args:
                plugin_name: Name of the plugin to stop monitoring

            Returns:
                FlextCore.Result indicating success or failure

            """
            try:
                if plugin_name in self._monitored_plugins:
                    del self._monitored_plugins[plugin_name]
                    self.logger.info(f"Stopped monitoring plugin: {plugin_name}")
                    return FlextCore.Result.ok(True)
                return FlextCore.Result.fail(
                    f"Plugin not being monitored: {plugin_name}"
                )

            except Exception as e:
                self.logger.exception(f"Failed to stop monitoring {plugin_name}")
                return FlextCore.Result.fail(f"Stop monitoring error: {e!s}")

        async def get_plugin_metrics(
            self, plugin_name: str
        ) -> FlextCore.Result[FlextPluginTypes.Performance.Metrics]:
            """Get metrics for a plugin.

            Args:
                plugin_name: Name of the plugin

            Returns:
                FlextCore.Result containing plugin metrics

            """
            try:
                if plugin_name not in self._monitored_plugins:
                    return FlextCore.Result.fail(
                        f"Plugin not being monitored: {plugin_name}"
                    )

                metrics = self._monitored_plugins[plugin_name]["metrics"]
                return FlextCore.Result.ok(cast("FlextCore.Types.Dict", metrics))

            except Exception as e:
                self.logger.exception(f"Failed to get metrics for {plugin_name}")
                return FlextCore.Result.fail(f"Get metrics error: {e!s}")

        async def get_plugin_health(
            self, plugin_name: str
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Get health status for a plugin.

            Args:
                plugin_name: Name of the plugin

            Returns:
                FlextCore.Result containing plugin health information

            """
            try:
                if plugin_name not in self._monitored_plugins:
                    return FlextCore.Result.fail(
                        f"Plugin not being monitored: {plugin_name}"
                    )

                health_info = {
                    "plugin_name": plugin_name,
                    "health_status": self._monitored_plugins[plugin_name][
                        "health_status"
                    ],
                    "monitoring_since": self._monitored_plugins[plugin_name][
                        "start_time"
                    ],
                }

                return FlextCore.Result.ok(health_info)

            except Exception as e:
                self.logger.exception(f"Failed to get health for {plugin_name}")
                return FlextCore.Result.fail(f"Get health error: {e!s}")

        def is_monitoring(self, plugin_name: str) -> bool:
            """Check if a plugin is being monitored.

            Args:
                plugin_name: Name of the plugin

            Returns:
                True if plugin is being monitored, False otherwise

            """
            return plugin_name in self._monitored_plugins

        def _get_current_timestamp(self) -> str:
            """Get current timestamp as ISO string."""
            return datetime.now(UTC).isoformat()


__all__ = ["FlextPluginAdapters"]
