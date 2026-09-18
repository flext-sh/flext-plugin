# from flext-plugin/docs/architecture/implementation.md:121
# flext_plugin/services.py - Application services
from __future__ import annotations

from flext_plugin import FlextPluginModels


class FlextPluginServices:
    """Application services following Clean Architecture."""

    def __init__(self, container: FlextContainer) -> None:
        self.container = container

    async def discover_plugins(
        self, paths: t.StringList, discovery_service: PluginDiscovery
    ) -> p.Result[list[FlextPluginModels.Plugin]]:
        """Application service orchestrating plugin discovery."""
        try:
            # Use domain service (infrastructure adapter)
            discovery_result = await discovery_service.discover_plugins(paths)
            if discovery_result.failure:
                return discovery_result

            plugin_configs = discovery_result.unwrap()
            plugins = []

            for settings in plugin_configs:
                # Create domain entity
                plugin = FlextPluginModels.Plugin.create(
                    name=settings["name"],
                    plugin_version=settings.get("version", "1.0.0"),
                    settings=settings,
                )

                # Validate business rules
                validation = plugin.validate_business_rules()
                if validation.success:
                    plugins.append(plugin)
                else:
                    # Log validation failure but continue
                    self.logger.warning(
                        f"Plugin {plugin.name} validation failed: {validation.error}"
                    )

            return r.ok(plugins)

        except Exception as e:
            return r.fail(f"Plugin discovery failed: {e!s}")

    async def execute_plugin(
        self, plugin: FlextPluginModels.Plugin, context: dict, executor: PluginExecution
    ) -> p.Result[FlextPluginModels.Execution]:
        """Application service orchestrating plugin execution."""
        try:
            # Create execution entity
            execution = FlextPluginModels.Execution.create(
                plugin_name=plugin.name, context=context
            )

            # Mark as started
            execution.mark_started()

            # Execute via infrastructure
            execution_result = await executor.execute_plugin(plugin, context)
            if execution_result.success:
                execution.mark_completed(execution_result.unwrap())
            else:
                execution.mark_failed(execution_result.error)

            return r.ok(execution)

        except Exception as e:
            return r.fail(f"Plugin execution failed: {e!s}")```
#### **Infrastructure Layer Implementation**

