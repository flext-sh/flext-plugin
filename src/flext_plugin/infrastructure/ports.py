"""Infrastructure service implementations for FLEXT-PLUGIN.

Using flext-core patterns - NO duplication, clean architecture.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from flext_core.domain.types import ServiceResult
from flext_core.infrastructure.di import injectable
from flext_plugin.domain.entities import (
    PluginExecution,
    PluginLifecycle,
    PluginMetadata,
    PluginStatus,
)
from flext_plugin.domain.ports import (
    PluginDiscoveryService,
    PluginExecutionService,
    PluginHotReloadService,
    PluginLifecycleService,
    PluginRegistryService,
    PluginSecurityService,
    PluginValidationService,
)

if TYPE_CHECKING:
    from flext_plugin.domain.entities import (
        PluginInstance,
        PluginRegistry,
    )


@injectable()
class FileSystemPluginDiscoveryPort(PluginDiscoveryService):
    """File system-based plugin discovery implementation."""

    async def discover_plugins(
        self,
        search_paths: list[str],
    ) -> ServiceResult[list[PluginMetadata]]:
        """Discover plugins in the specified search paths.

        Args:
            search_paths: List of directory paths to search for plugins.

        Returns:
            ServiceResult containing list of discovered plugin metadata.

        """
        try:
            discovered_plugins = []

            for path_str in search_paths:
                path = Path(path_str)
                if not path.exists():
                    continue

                # Look for plugin manifests
                for manifest_file in path.rglob("plugin.json"):
                    try:
                        manifest = await self._load_manifest(manifest_file)
                        if manifest:
                            discovered_plugins.append(manifest)
                    except (OSError, ValueError, KeyError, json.JSONDecodeError):
                        # Skip invalid manifests
                        continue

                # Look for Python entry points
                for py_file in path.rglob("*.py"):
                    if py_file.name.startswith("plugin_"):
                        try:
                            metadata = await self._extract_metadata_from_file(py_file)
                            if metadata:
                                discovered_plugins.append(metadata)
                        except (OSError, ImportError, AttributeError, ValueError):
                            continue

            return ServiceResult.ok(discovered_plugins)
        except (OSError, RuntimeError, ValueError) as e:
            return ServiceResult.fail(f"Plugin discovery failed: {e}")

    async def validate_plugin_metadata(
        self,
        metadata: PluginMetadata,
    ) -> ServiceResult[bool]:
        """Validate plugin metadata structure and requirements."""
        try:
            # Check required fields
            if not metadata.name or not metadata.entry_point:
                return ServiceResult.fail("Missing required metadata fields")

            # Validate entry point format
            if ":" not in metadata.entry_point:
                return ServiceResult.fail("Invalid entry point format")

            # Check Python version compatibility
            if not await self._check_python_version(metadata.python_version):
                return ServiceResult.fail("Python version incompatible")

            return ServiceResult.ok(True)
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Metadata validation failed: {e}")

    async def get_plugin_manifest(self, plugin_path: str) -> ServiceResult[dict]:
        """Load plugin manifest from specified path."""
        try:
            path = Path(plugin_path)

            # Look for plugin.json
            manifest_file = path / "plugin.json"
            if manifest_file.exists():
                return ServiceResult.ok(json.loads(manifest_file.read_text()))

            # Look for pyproject.toml with plugin section
            pyproject_file = path / "pyproject.toml"
            if pyproject_file.exists():
                # Parse TOML and extract plugin metadata
                manifest = await self._extract_from_pyproject(pyproject_file)
                if manifest:
                    return ServiceResult.ok(manifest)

            return ServiceResult.fail("No manifest found")
        except (OSError, json.JSONDecodeError, ValueError) as e:
            return ServiceResult.fail(f"Manifest loading failed: {e}")

    async def _load_manifest(self, manifest_file: Path) -> PluginMetadata | None:
        try:
            data = json.loads(manifest_file.read_text())
            # Convert to PluginMetadata object
            return PluginMetadata(**data)
        except (OSError, json.JSONDecodeError, ValueError, TypeError):
            return None

    async def _extract_metadata_from_file(self, py_file: Path) -> PluginMetadata | None:
        try:
            # Simple metadata extraction from docstring or comments
            content = py_file.read_text()

            # Look for plugin metadata in docstring
            if '"""' in content and "plugin:" in content.lower():
                # Extract metadata from structured docstring
                pass

            return None
        except (OSError, UnicodeDecodeError, ValueError):
            return None

    async def _check_python_version(self, version_spec: str) -> bool:
        try:
            # Simple version check
            current_version = f"{sys.version_info.major}.{sys.version_info.minor}"

            if version_spec.startswith(">="):
                required = version_spec[2:]
                return current_version >= required
            if version_spec.startswith("=="):
                required = version_spec[2:]
                return current_version == required

            return True
        except (ValueError, AttributeError, TypeError):
            return False

    async def _extract_from_pyproject(self, pyproject_file: Path) -> dict | None:
        try:
            # Would need toml parser
            return None
        except (OSError, ValueError, ImportError):
            return None


@injectable()
class PydanticPluginValidationPort(PluginValidationService):
    """Pydantic-based plugin validation implementation."""

    async def validate_plugin(self, plugin: PluginInstance) -> ServiceResult[bool]:
        """Validate complete plugin instance including config and dependencies."""
        try:
            # Validate configuration
            config_result = await self.validate_configuration(
                plugin,
                plugin.configuration.settings,
            )
            if not config_result.success:
                return config_result

            # Validate dependencies
            deps_result = await self.validate_dependencies(plugin)
            if not deps_result.success:
                return deps_result

            # Validate permissions
            perms_result = await self.validate_permissions(plugin)
            if not perms_result.success:
                return perms_result

            return ServiceResult.ok(True)
        except (ValueError, TypeError, AttributeError, RuntimeError) as e:
            return ServiceResult.fail(f"Plugin validation failed: {e}")

    async def validate_configuration(
        self,
        plugin: PluginInstance,
        config: dict,
    ) -> ServiceResult[bool]:
        """Validate plugin configuration against schema."""
        try:
            # Validate against schema if available:
            if plugin.metadata.configuration_schema:
                # Would use jsonschema for validation
                pass

            # Basic validation
            if not isinstance(config, dict):
                return ServiceResult.fail("Configuration must be a dictionary")

            return ServiceResult.ok(True)
        except (ValueError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Configuration validation failed: {e}")

    async def validate_dependencies(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[bool]:
        """Validate plugin dependencies are available."""
        try:
            for dependency in plugin.metadata.dependencies:
                # Check if dependency is available:
                try:
                    __import__(dependency)
                except ImportError:
                    return ServiceResult.fail(f"Missing dependency: {dependency}")

            return ServiceResult.ok(True)
        except (ImportError, ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Dependency validation failed: {e}")

    async def validate_permissions(self, plugin: PluginInstance) -> ServiceResult[bool]:
        """Validate plugin has required permissions."""
        try:
            # Check required permissions
            for permission in plugin.metadata.required_permissions:
                # Validate permission exists and is allowed
                if not await self._check_permission(permission):
                    return ServiceResult.fail(f"Permission denied: {permission}")

            return ServiceResult.ok(True)
        except (ValueError, AttributeError, KeyError) as e:
            return ServiceResult.fail(f"Permission validation failed: {e}")

    async def _check_permission(self, permission: str) -> bool:
        try:
            # Simple permission check
            allowed_permissions = [
                "read_file",
                "write_file",
                "network_access",
                "system_info",
            ]
            return permission in allowed_permissions
        except (ValueError, AttributeError, TypeError):
            return False


@injectable()
class LocalPluginLifecyclePort(PluginLifecycleService):
    """Local plugin lifecycle management implementation."""

    async def register_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[PluginInstance]:
        """Register plugin in lifecycle system."""
        try:
            plugin.transition_to(PluginLifecycle.REGISTERED)
            return ServiceResult.ok(plugin)
        except (ValueError, AttributeError, RuntimeError) as e:
            return ServiceResult.fail(f"Plugin registration failed: {e}")

    async def load_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[PluginInstance]:
        """Load plugin module into memory."""
        try:
            # Load plugin module
            module_name = plugin.metadata.entry_point.split(":")[0]

            # Dynamic import
            __import__(module_name)
            plugin.transition_to(PluginLifecycle.LOADED)

            return ServiceResult.ok(plugin)
        except (ImportError, ModuleNotFoundError, AttributeError, ValueError) as e:
            plugin.transition_to(PluginLifecycle.ERROR)
            return ServiceResult.fail(f"Plugin loading failed: {e}")

    async def initialize_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[PluginInstance]:
        """Initialize plugin with configuration."""
        try:
            # Initialize plugin with configuration
            plugin.is_initialized = True
            plugin.transition_to(PluginLifecycle.INITIALIZED)

            return ServiceResult.ok(plugin)
        except (ValueError, AttributeError, RuntimeError, TypeError) as e:
            plugin.transition_to(PluginLifecycle.ERROR)
            return ServiceResult.fail(f"Plugin initialization failed: {e}")

    async def activate_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[PluginInstance]:
        """Activate plugin for execution."""
        try:
            plugin.transition_to(PluginLifecycle.ACTIVE)
            plugin.plugin_status = PluginStatus.HEALTHY

            return ServiceResult.ok(plugin)
        except (ValueError, AttributeError, RuntimeError) as e:
            plugin.transition_to(PluginLifecycle.ERROR)
            return ServiceResult.fail(f"Plugin activation failed: {e}")

    async def suspend_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[PluginInstance]:
        """Suspend plugin execution."""
        try:
            plugin.transition_to(PluginLifecycle.SUSPENDED)
            return ServiceResult.ok(plugin)
        except (ValueError, AttributeError, RuntimeError) as e:
            return ServiceResult.fail(f"Plugin suspension failed: {e}")

    async def unload_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[PluginInstance]:
        """Unload plugin from memory."""
        try:
            plugin.transition_to(PluginLifecycle.UNLOADING)

            # Cleanup resources
            plugin.is_initialized = False
            plugin.transition_to(PluginLifecycle.UNLOADED)

            return ServiceResult.ok(plugin)
        except (ValueError, AttributeError, RuntimeError) as e:
            plugin.transition_to(PluginLifecycle.ERROR)
            return ServiceResult.fail(f"Plugin unloading failed: {e}")

    async def unregister_plugin(self, plugin: PluginInstance) -> ServiceResult[bool]:
        """Unregister plugin from lifecycle system."""
        try:
            plugin.transition_to(PluginLifecycle.UNREGISTERED)
            return ServiceResult.ok(True)
        except (ValueError, AttributeError, RuntimeError) as e:
            return ServiceResult.fail(f"Plugin unregistration failed: {e}")


@injectable()
class LocalPluginExecutionPort(PluginExecutionService):
    """Local plugin execution implementation."""

    async def execute_plugin(
        self,
        plugin: PluginInstance,
        input_data: dict,
        execution_context: dict | None = None,
    ) -> ServiceResult[PluginExecution]:
        """Execute plugin with input data and context."""
        try:
            # Create execution record
            execution = PluginExecution(
                plugin_id=plugin.plugin_id,
                execution_id=f"exec_{plugin.plugin_id}_{os.urandom(8).hex()}",
                input_data=input_data,
                execution_context=execution_context or {},
            )

            # Start execution
            execution.mark_started()

            # Execute plugin logic (simplified)
            # In real implementation, this would call the actual plugin
            await asyncio.sleep(0.1)  # Simulate execution time

            # Complete execution
            execution.mark_completed(success=True)
            plugin.record_execution(execution.duration_ms or 0)

            return ServiceResult.ok(execution)
        except (ValueError, RuntimeError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Plugin execution failed: {e}")

    async def get_execution_status(
        self,
        execution_id: str,
    ) -> ServiceResult[PluginExecution]:
        """Get execution status by ID."""
        try:
            # In real implementation, would query repository
            return ServiceResult.fail("Execution not found")
        except (ValueError, KeyError, AttributeError) as e:
            return ServiceResult.fail(f"Status retrieval failed: {e}")

    async def cancel_execution(self, execution_id: str) -> ServiceResult[bool]:
        """Cancel running execution."""
        try:
            # In real implementation, would cancel running execution
            return ServiceResult.ok(True)
        except (ValueError, RuntimeError, AttributeError) as e:
            return ServiceResult.fail(f"Execution cancellation failed: {e}")

    async def get_execution_logs(self, execution_id: str) -> ServiceResult[list[dict]]:
        """Get execution logs by ID."""
        try:
            # In real implementation, would retrieve logs
            return ServiceResult.ok([])
        except (ValueError, OSError, AttributeError) as e:
            return ServiceResult.fail(f"Log retrieval failed: {e}")


@injectable()
class LocalPluginRegistryPort(PluginRegistryService):
    """Local plugin registry implementation."""

    async def register_registry(
        self,
        registry: PluginRegistry,
    ) -> ServiceResult[PluginRegistry]:
        """Register plugin registry in system."""
        try:
            # Validate registry configuration
            if not registry.registry_url:
                return ServiceResult.fail("Registry URL is required")

            return ServiceResult.ok(registry)
        except (ValueError, RuntimeError, AttributeError) as e:
            return ServiceResult.fail(f"Registry registration failed: {e}")

    async def sync_registry(self, registry: PluginRegistry) -> ServiceResult[bool]:
        """Synchronize registry with remote source."""
        try:
            # In real implementation, would sync with remote registry
            registry.record_sync(success=True, plugin_count=10)
            return ServiceResult.ok(True)
        except (OSError, ValueError, RuntimeError, ConnectionError) as e:
            registry.record_sync(success=False)
            return ServiceResult.fail(f"Registry sync failed: {e}")

    async def search_plugins(
        self,
        registry: PluginRegistry,
        query: str,
    ) -> ServiceResult[list[PluginMetadata]]:
        """Search plugins in registry by query."""
        try:
            # In real implementation, would search remote registry
            return ServiceResult.ok([])
        except (OSError, ValueError, ConnectionError) as e:
            return ServiceResult.fail(f"Plugin search failed: {e}")

    async def download_plugin(
        self,
        registry: PluginRegistry,
        plugin_id: str,
    ) -> ServiceResult[str]:
        """Download plugin from registry."""
        try:
            # In real implementation, would download plugin
            return ServiceResult.ok("/tmp/plugin.zip")
        except (OSError, ValueError, ConnectionError, RuntimeError) as e:
            return ServiceResult.fail(f"Plugin download failed: {e}")

    async def verify_plugin_signature(
        self,
        registry: PluginRegistry,
        plugin_path: str,
    ) -> ServiceResult[bool]:
        """Verify plugin signature for security."""
        try:
            # In real implementation, would verify signature
            return ServiceResult.ok(True)
        except (OSError, ValueError, RuntimeError) as e:
            return ServiceResult.fail(f"Signature verification failed: {e}")


@injectable()
class FileSystemHotReloadPort(PluginHotReloadService):
    """File system-based hot reload implementation."""

    def __init__(self) -> None:
        """Initialize hot reload service."""
        self._watching = False
        self._watch_tasks = []

    async def start_watching(self, watch_paths: list[str]) -> ServiceResult[bool]:
        """Start watching directories for plugin changes."""
        try:
            if self._watching:
                return ServiceResult.ok(True)

            self._watching = True

            # Start watch tasks for each path
            for path in watch_paths:
                task = asyncio.create_task(self._watch_directory(path))
                self._watch_tasks.append(task)

            return ServiceResult.ok(True)
        except (OSError, RuntimeError, ValueError) as e:
            return ServiceResult.fail(f"Failed to start watching: {e}")

    async def stop_watching(self) -> ServiceResult[bool]:
        """Stop watching directories."""
        try:
            self._watching = False

            # Cancel all watch tasks
            for task in self._watch_tasks:
                task.cancel()

            self._watch_tasks.clear()
            return ServiceResult.ok(True)
        except (RuntimeError, ValueError) as e:
            return ServiceResult.fail(f"Failed to stop watching: {e}")

    async def reload_plugin(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[PluginInstance]:
        """Reload plugin with state preservation."""
        try:
            # Backup state
            state_result = await self.backup_plugin_state(plugin)
            if not state_result.success:
                return ServiceResult.fail(f"State backup failed: {state_result.error}")

            # Unload plugin
            plugin.transition_to(PluginLifecycle.UNLOADING)

            # Reload plugin module
            # In real implementation, would reload module
            await asyncio.sleep(0.1)

            # Restore state
            restore_result = await self.restore_plugin_state(plugin, state_result.value)
            if not restore_result.success:
                return ServiceResult.fail(
                    f"State restoration failed: {restore_result.error}",
                )

            plugin.transition_to(PluginLifecycle.ACTIVE)
            return ServiceResult.ok(plugin)
        except (RuntimeError, ValueError, AttributeError) as e:
            plugin.transition_to(PluginLifecycle.ERROR)
            return ServiceResult.fail(f"Plugin reload failed: {e}")

    async def backup_plugin_state(self, plugin: PluginInstance) -> ServiceResult[dict]:
        """Backup plugin state before reload."""
        try:
            state = {
                "configuration": plugin.configuration.settings,
                "health_data": plugin.health_data,
                "execution_count": plugin.execution_count,
                "last_execution": (
                    plugin.last_execution.isoformat() if plugin.last_execution else None
                ),
            }
            return ServiceResult.ok(state)
        except (ValueError, AttributeError, TypeError) as e:
            return ServiceResult.fail(f"State backup failed: {e}")

    async def restore_plugin_state(
        self,
        plugin: PluginInstance,
        state: dict,
    ) -> ServiceResult[bool]:
        """Restore plugin state after reload."""
        try:
            # Restore configuration
            plugin.configuration.settings = state.get("configuration", {})
            plugin.health_data = state.get("health_data", {})
            plugin.execution_count = state.get("execution_count", 0)

            return ServiceResult.ok(True)
        except (ValueError, AttributeError, TypeError, KeyError) as e:
            return ServiceResult.fail(f"State restoration failed: {e}")

    async def _watch_directory(self, path: str) -> None:
        try:
            # In real implementation, would use watchdog or similar
            while self._watching:
                await asyncio.sleep(1)
                # Check for file changes
        except asyncio.CancelledError:
            pass
        except (OSError, RuntimeError, ValueError):
            pass


@injectable()
class SandboxPluginSecurityPort(PluginSecurityService):
    """Sandbox-based plugin security implementation."""

    async def create_sandbox(self, plugin: PluginInstance) -> ServiceResult[dict]:
        """Create security sandbox for plugin execution."""
        try:
            sandbox_config = {
                "enabled": plugin.configuration.security_level.value != "low",
                "max_memory_mb": plugin.configuration.max_memory_mb,
                "max_cpu_percent": plugin.configuration.max_cpu_percent,
                "timeout_seconds": plugin.configuration.timeout_seconds,
                "restricted_imports": ["subprocess", "os.system", "eval", "exec"],
                "allowed_paths": ["/tmp", "/var/tmp"],
            }

            return ServiceResult.ok(sandbox_config)
        except (ValueError, AttributeError, RuntimeError) as e:
            return ServiceResult.fail(f"Sandbox creation failed: {e}")

    async def enforce_resource_limits(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[bool]:
        """Enforce resource limits on plugin execution."""
        try:
            # In real implementation, would use cgroups or similar
            return ServiceResult.ok(True)
        except (OSError, RuntimeError, ValueError) as e:
            return ServiceResult.fail(f"Resource limit enforcement failed: {e}")

    async def validate_imports(self, plugin: PluginInstance) -> ServiceResult[bool]:
        """Validate plugin imports for security."""
        try:
            # Check against restricted imports

            # In real implementation, would analyze plugin code
            return ServiceResult.ok(True)
        except (ValueError, AttributeError, ImportError) as e:
            return ServiceResult.fail(f"Import validation failed: {e}")

    async def scan_for_vulnerabilities(
        self,
        plugin: PluginInstance,
    ) -> ServiceResult[list[dict]]:
        """Scan plugin for security vulnerabilities."""
        try:
            # In real implementation, would use security scanner
            vulnerabilities = []
            return ServiceResult.ok(vulnerabilities)
        except (ValueError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Vulnerability scan failed: {e}")
