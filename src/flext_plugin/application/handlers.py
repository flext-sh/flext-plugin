"""Application handlers for FLEXT-PLUGIN.

Using flext-core CommandHandler pattern - NO duplication, clean architecture.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.application.base import CommandHandler
from flext_core.domain.types import ServiceResult

if TYPE_CHECKING:
    from flext_plugin.domain.entities import (
        PluginExecution,
        PluginInstance,
        PluginMetadata,
        PluginRegistry,
    )
    from flext_plugin.domain.ports import (
        PluginDiscoveryService,
        PluginExecutionService,
        PluginLifecycleService,
        PluginRegistryService,
        PluginValidationService,
    )


class PluginDiscoveryHandler(CommandHandler):
    """Plugin discovery command handler."""

    def __init__(self, discovery_service: PluginDiscoveryService) -> None:
        super().__init__()
        self.discovery_service = discovery_service

    async def discover_plugins(self, search_paths: list[str]) -> ServiceResult[list[PluginMetadata]]:
        try:
            self.logger.info(
                "Starting plugin discovery",
                extra={"search_paths": search_paths},
            )

            result = await self.discovery_service.discover_plugins(search_paths)

            if result.success:
                self.logger.info(
                    "Plugin discovery completed",
                    extra={"plugin_count": len(result.value)},
                )
            else:
                self.logger.error(
                    "Plugin discovery failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin discovery handler error")
            return ServiceResult.fail(f"Discovery handler failed: {e}")

    async def validate_plugin_metadata(self, metadata: PluginMetadata) -> ServiceResult[bool]:
        try:
            self.logger.debug(
                "Validating plugin metadata",
                extra={"plugin_name": metadata.name},
            )

            result = await self.discovery_service.validate_plugin_metadata(metadata)

            if result.success:
                self.logger.debug("Plugin metadata validation successful")
            else:
                self.logger.warning(
                    "Plugin metadata validation failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin metadata validation handler error")
            return ServiceResult.fail(f"Validation handler failed: {e}")

    async def get_plugin_manifest(self, plugin_path: str) -> ServiceResult[dict]:
        try:
            self.logger.debug(
                "Getting plugin manifest",
                extra={"plugin_path": plugin_path},
            )

            result = await self.discovery_service.get_plugin_manifest(plugin_path)

            if result.success:
                self.logger.debug("Plugin manifest retrieved successfully")
            else:
                self.logger.warning(
                    "Plugin manifest retrieval failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin manifest handler error")
            return ServiceResult.fail(f"Manifest handler failed: {e}")


class PluginValidationHandler(CommandHandler):
    """Plugin validation command handler."""

    def __init__(self, validation_service: PluginValidationService) -> None:
        super().__init__()
        self.validation_service = validation_service

    async def validate_plugin(self, plugin: PluginInstance) -> ServiceResult[bool]:
        try:
            self.logger.info(
                "Starting plugin validation",
                extra={"plugin_id": str(plugin.plugin_id)},
            )

            result = await self.validation_service.validate_plugin(plugin)

            if result.success:
                self.logger.info("Plugin validation successful")
            else:
                self.logger.error(
                    "Plugin validation failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin validation handler error")
            return ServiceResult.fail(f"Validation handler failed: {e}")

    async def validate_configuration(self, plugin: PluginInstance, config: dict) -> ServiceResult[bool]:
        try:
            self.logger.debug(
                "Validating plugin configuration",
                extra={"plugin_id": str(plugin.plugin_id)},
            )

            result = await self.validation_service.validate_configuration(
                plugin,
                config,
            )

            if result.success:
                self.logger.debug("Plugin configuration validation successful")
            else:
                self.logger.warning(
                    "Plugin configuration validation failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin configuration validation handler error")
            return ServiceResult.fail(f"Configuration validation handler failed: {e}")

    async def validate_dependencies( self, plugin: PluginInstance, ) -> ServiceResult[bool]:
        try:
            self.logger.debug(
                "Validating plugin dependencies",
                extra={"plugin_id": str(plugin.plugin_id)},
            )

            result = await self.validation_service.validate_dependencies(plugin)

            if result.success:
                self.logger.debug("Plugin dependencies validation successful")
            else:
                self.logger.warning(
                    "Plugin dependencies validation failed",
                    extra={"error": result.error},
                )
            return result
        except Exception as e:
            self.logger.exception("Plugin dependencies validation handler error")
            return ServiceResult.fail(f"Dependencies validation handler failed: {e}")


class PluginLifecycleHandler(CommandHandler):
    """Plugin lifecycle command handler."""

    def __init__(self, lifecycle_service: PluginLifecycleService) -> None:
        super().__init__()
        self.lifecycle_service = lifecycle_service

    async def register_plugin( self, plugin: PluginInstance, ) -> ServiceResult[PluginInstance]:
        try:
            self.logger.info(
                "Registering plugin",
                extra={"plugin_id": str(plugin.plugin_id)},
            )

            result = await self.lifecycle_service.register_plugin(plugin)

            if result.success:
                self.logger.info("Plugin registered successfully")
            else:
                self.logger.error(
                    "Plugin registration failed",
                    extra={"error": result.error},
                )
        except Exception as e:
            self.logger.exception("Plugin registration handler error")
            return ServiceResult.fail(f"Registration handler failed: {e}")

    async def load_plugin( self, plugin: PluginInstance, ) -> ServiceResult[PluginInstance]:
        try:
            self.logger.info(
                "Loading plugin",
                extra={"plugin_id": str(plugin.plugin_id)},
            )

            result = await self.lifecycle_service.load_plugin(plugin)

            if result.success:
                self.logger.info("Plugin loaded successfully")
            else:
                self.logger.error(
                    "Plugin loading failed",
                    extra={"error": result.error},
                )
        except Exception as e:
            self.logger.exception("Plugin loading handler error")
            return ServiceResult.fail(f"Loading handler failed: {e}")

    async def initialize_plugin( self, plugin: PluginInstance, ) -> ServiceResult[PluginInstance]:
        try:
            self.logger.info(
                "Initializing plugin",
                extra={"plugin_id": str(plugin.plugin_id)},
            )

            result = await self.lifecycle_service.initialize_plugin(plugin)

            if result.success:
            self.logger.info("Plugin initialized successfully")
            else:
            self.logger.error(
                    "Plugin initialization failed",
                    extra={"error": result.error},
                )
        except Exception as e:
        self.logger.exception("Plugin initialization handler error")
            return ServiceResult.fail(f"Initialization handler failed: {e}")

    async def activate_plugin( self, plugin: PluginInstance, ) -> ServiceResult[PluginInstance]:
        try:
            self.logger.info(
                "Activating plugin",
                extra={"plugin_id": str(plugin.plugin_id)},
            )

            result = await self.lifecycle_service.activate_plugin(plugin)

            if result.success:
            self.logger.info("Plugin activated successfully")
            else:
            self.logger.error(
                    "Plugin activation failed",
                    extra={"error": result.error},
                )
        except Exception as e:
        self.logger.exception("Plugin activation handler error")
            return ServiceResult.fail(f"Activation handler failed: {e}")

    async def suspend_plugin( self, plugin: PluginInstance, ) -> ServiceResult[PluginInstance]:
        try:
            self.logger.info(
                "Suspending plugin",
                extra={"plugin_id": str(plugin.plugin_id)},
            )

            result = await self.lifecycle_service.suspend_plugin(plugin)

            if result.success:
            self.logger.info("Plugin suspended successfully")
            else:
            self.logger.error(
                    "Plugin suspension failed",
                    extra={"error": result.error},
                )
        except Exception as e:
        self.logger.exception("Plugin suspension handler error")
            return ServiceResult.fail(f"Suspension handler failed: {e}")

    async def unload_plugin( self, plugin: PluginInstance, ) -> ServiceResult[PluginInstance]:
        try:
            self.logger.info(
                "Unloading plugin",
                extra={"plugin_id": str(plugin.plugin_id)},
            )

            result = await self.lifecycle_service.unload_plugin(plugin)

            if result.success:
            self.logger.info("Plugin unloaded successfully")
            else:
            self.logger.error(
                    "Plugin unloading failed",
                    extra={"error": result.error},
                )
        except Exception as e:
        self.logger.exception("Plugin unloading handler error")
            return ServiceResult.fail(f"Unloading handler failed: {e}")


class PluginExecutionHandler(CommandHandler):
         """Plugin execution command handler."""

    def __init__(self, execution_service: PluginExecutionService) -> None:
        super().__init__()
        self.execution_service = execution_service

    async def execute_plugin( self, plugin: PluginInstance, input_data: dict, execution_context: dict | None = None, ) -> ServiceResult[PluginExecution]:
        try:
            self.logger.info(
                "Executing plugin",
                extra={
                    "plugin_id": str(plugin.plugin_id),
                    "input_size": len(input_data),
                },
            )

            result = await self.execution_service.execute_plugin(
                plugin,
                input_data,
                execution_context,
            )

            if result.success:
            self.logger.info(
                    "Plugin execution completed",
                    extra={
                        "execution_id": result.value.execution_id,
                        "success": result.value.success,
                        "duration_ms": result.value.duration_ms,
                    },
                )
            else:
            self.logger.error(
                    "Plugin execution failed",
                    extra={"error": result.error},
                )
        except Exception as e:
        self.logger.exception("Plugin execution handler error")
            return ServiceResult.fail(f"Execution handler failed: {e}")

    async def get_execution_status( self, execution_id: str, ) -> ServiceResult[PluginExecution]:
        try:
            self.logger.debug(
                "Getting execution status",
                extra={"execution_id": execution_id},
            )

            result = await self.execution_service.get_execution_status(execution_id)

            if result.success:
            self.logger.debug("Execution status retrieved successfully")
            else:
            self.logger.warning(
                    "Execution status retrieval failed",
                    extra={"error": result.error},
                )
        except Exception as e:
        self.logger.exception("Execution status handler error")
            return ServiceResult.fail(f"Status handler failed: {e}")

    async def cancel_execution(self, execution_id: str) -> ServiceResult[bool]:
        try:
            self.logger.info(
                "Cancelling execution",
                extra={"execution_id": execution_id},
            )

            result = await self.execution_service.cancel_execution(execution_id)

            if result.success:
            self.logger.info("Execution cancelled successfully")
            else:
            self.logger.error(
                    "Execution cancellation failed",
                    extra={"error": result.error},
                )
        except Exception as e:
        self.logger.exception("Execution cancellation handler error")
            return ServiceResult.fail(f"Cancellation handler failed: {e}")


class PluginRegistryHandler(CommandHandler):
         """Plugin registry command handler."""

    def __init__(self, registry_service: PluginRegistryService) -> None:
        super().__init__()
        self.registry_service = registry_service

    async def register_registry( self, registry: PluginRegistry, ) -> ServiceResult[PluginRegistry]:
        try:
            self.logger.info(
                "Registering plugin registry",
                extra={"registry_name": registry.name},
            )

            result = await self.registry_service.register_registry(registry)

            if result.success:
            self.logger.info("Plugin registry registered successfully")
            else:
            self.logger.error(
                    "Plugin registry registration failed",
                    extra={"error": result.error},
                )
        except Exception as e:
        self.logger.exception("Plugin registry registration handler error")
            return ServiceResult.fail(f"Registry registration handler failed: {e}")

    async def sync_registry(self, registry: PluginRegistry) -> ServiceResult[bool]:
        try:
            self.logger.info(
                "Synchronizing registry",
                extra={"registry_name": registry.name},
            )

            result = await self.registry_service.sync_registry(registry)

            if result.success:
            self.logger.info("Registry synchronization successful")
            else:
            self.logger.error(
                    "Registry synchronization failed",
                    extra={"error": result.error},
                )
        except Exception as e:
        self.logger.exception("Registry synchronization handler error")
            return ServiceResult.fail(f"Sync handler failed: {e}")

    async def search_plugins( self, registry: PluginRegistry, query: str, ) -> ServiceResult[list[PluginMetadata]]:
        try:
            self.logger.info(
                "Searching plugins in registry",
                extra={"registry_name": registry.name, "query": query},
            )

            result = await self.registry_service.search_plugins(registry, query)

            if result.success:
            self.logger.info(
                    "Plugin search completed",
                    extra={"result_count": len(result.value)},
                )
            else:
            self.logger.error(
                    "Plugin search failed",
                    extra={"error": result.error},
                )
        except Exception as e:
        self.logger.exception("Plugin search handler error")
            return ServiceResult.fail(f"Search handler failed: {e}")

    async def download_plugin( self, registry: PluginRegistry, plugin_id: str, ) -> ServiceResult[str]:
        try:
            self.logger.info(
                "Downloading plugin from registry",
                extra={"registry_name": registry.name, "plugin_id": plugin_id},
            )

            result = await self.registry_service.download_plugin(registry, plugin_id)

            if result.success:
            self.logger.info(
                    "Plugin downloaded successfully",
                    extra={"download_path": result.value},
                )
            else:
            self.logger.error(
                    "Plugin download failed",
                    extra={"error": result.error},
                )
        except Exception as e:
        self.logger.exception("Plugin download handler error")
            return ServiceResult.fail(f"Download handler failed: {e}")
