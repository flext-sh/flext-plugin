"""Plugin lifecycle operations over an explicitly injected canonical registry.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_plugin import c, m, p, r, s, t, u


class FlextPluginPlatform:
    """Plugin behavior composed by the public API."""

    class Rules:
        """Business validation for registered plugin implementations."""

        @staticmethod
        def validate_business_rules(plugin: p.Plugin.Instance) -> p.Result[bool]:
            """Validate the plugin's public name and version."""
            if not plugin.name or not plugin.name.strip():
                return r[bool].fail("Plugin name cannot be empty")
            parts = plugin.plugin_version.split(".")
            if len(parts) not in {2, 3} or not all(part.isdigit() for part in parts):
                return r[bool].fail(
                    f"Invalid semantic version: {plugin.plugin_version}"
                )
            return r[bool].ok(True)

    class PluginPlatformService(s[p.Plugin.Snapshot], m.Plugin.PortOptions):
        """Use cases sharing one required registry, with no mirrored plugin store."""

        def register_plugin(self, plugin: p.Plugin.Instance) -> p.Result[bool]:
            """Register the original payload; conflicts remain registry failures."""
            validation = FlextPluginPlatform.Rules.validate_business_rules(plugin)
            if validation.failure:
                return validation
            return self.registry.register_plugin(
                c.Plugin.REGISTRY_CATEGORY, plugin.name, plugin
            )

        def unregister_plugin(self, plugin_name: str) -> p.Result[bool]:
            """Remove the actual canonical entry before allowing reuse of its name."""
            return self.registry.unregister_plugin(
                c.Plugin.REGISTRY_CATEGORY, plugin_name
            )

        def fetch_plugin(self, plugin_name: str) -> p.Result[p.Plugin.Instance]:
            """Fetch the original plugin without serialization or reconstruction."""
            result = self.registry.fetch_plugin(c.Plugin.REGISTRY_CATEGORY, plugin_name)
            if result.failure:
                return r[p.Plugin.Instance].from_failure(result)
            plugin = result.value
            if not isinstance(plugin, p.Plugin.Instance):
                return r[p.Plugin.Instance].fail(
                    f"Plugin '{plugin_name}' is not a plugin implementation"
                )
            return r[p.Plugin.Instance].ok(plugin)

        def fetch_plugin_status(self, plugin_name: str) -> p.Result[str]:
            """Project status from the registered instance's enabled flag."""
            return self.fetch_plugin(plugin_name).map(
                lambda plugin: str(
                    c.Plugin.PluginStatus.ACTIVE
                    if plugin.is_enabled
                    else c.Plugin.PluginStatus.INACTIVE
                )
            )

        def resolve_plugin_active(self, plugin_name: str) -> p.Result[bool]:
            """Resolve enabled state without hiding lookup failures."""
            return self.fetch_plugin(plugin_name).map(lambda plugin: plugin.is_enabled)

        def list_plugins(self) -> p.Result[t.SequenceOf[p.Plugin.Instance]]:
            """Resolve the canonical names, failing on invalid stored payloads."""
            names = self.registry.list_plugins(c.Plugin.REGISTRY_CATEGORY)
            if names.failure:
                return r[t.SequenceOf[p.Plugin.Instance]].from_failure(names)
            plugins: t.MutableSequenceOf[p.Plugin.Instance] = []
            for name in names.value:
                plugin = self.fetch_plugin(name)
                if plugin.failure:
                    return r[t.SequenceOf[p.Plugin.Instance]].from_failure(plugin)
                plugins.append(plugin.value)
            return r[t.SequenceOf[p.Plugin.Instance]].ok(plugins)

        def discover_plugins(
            self, paths: t.StrSequence
        ) -> p.Result[t.SequenceOf[p.Plugin.Instance]]:
            """Discover and validate all payloads before publishing any entries."""
            if self.discovery is None:
                return r[t.SequenceOf[p.Plugin.Instance]].fail(
                    "Discovery protocol not configured"
                )
            discovered = self.discovery.discover_plugins(paths)
            if discovered.failure:
                return r[t.SequenceOf[p.Plugin.Instance]].from_failure(discovered)
            plugins: t.MutableSequenceOf[p.Plugin.Instance] = []
            for data in discovered.value:
                candidate = u.validate_value(
                    m.Plugin.Entity,
                    {
                        "name": data.name,
                        "plugin_version": data.version,
                        "metadata": data.metadata,
                    },
                )
                if candidate.failure:
                    return r[t.SequenceOf[p.Plugin.Instance]].from_failure(candidate)
                plugins.append(candidate.value)
            for plugin in plugins:
                registered = self.register_plugin(plugin)
                if registered.failure:
                    return r[t.SequenceOf[p.Plugin.Instance]].from_failure(registered)
            return r[t.SequenceOf[p.Plugin.Instance]].ok(plugins)

        def load_plugin(self, plugin_path: str) -> p.Result[p.Plugin.Instance]:
            """Validate loader ingress once, then register the owned plugin."""
            if self.loader is None:
                return r[p.Plugin.Instance].fail("Loader protocol not configured")
            loaded = self.loader.load_plugin(plugin_path)
            if loaded.failure:
                return r[p.Plugin.Instance].from_failure(loaded)
            candidate = u.validate_value(
                m.Plugin.Entity,
                {
                    "name": loaded.value["name"],
                    "plugin_version": loaded.value.get(
                        "version", c.Plugin.DEFAULT_PLUGIN_VERSION
                    ),
                    "metadata": loaded.value,
                },
            )
            if candidate.failure:
                return r[p.Plugin.Instance].from_failure(candidate)
            registered = self.register_plugin(candidate.value)
            if registered.failure:
                return r[p.Plugin.Instance].from_failure(registered)
            return r[p.Plugin.Instance].ok(candidate.value)

        def execute_plugin(
            self,
            plugin_name: str,
            context: t.JsonMapping,
            execution_id: str | None = None,
        ) -> p.Result[p.Plugin.Run]:
            """Run a registered plugin once and retain the original failure cause."""
            plugin = self.fetch_plugin(plugin_name)
            if plugin.failure:
                return r[p.Plugin.Run].from_failure(plugin)
            if self.executor is None:
                return r[p.Plugin.Run].fail("Executor not configured")
            execution = (
                m.Plugin.Execution(
                    plugin_name=plugin.value.name,
                    input_data=context,
                    execution_id=execution_id,
                )
                if execution_id is not None
                else m.Plugin.Execution(
                    plugin_name=plugin.value.name, input_data=context
                )
            )
            execution.is_running = True
            execution.started_at = u.generate_iso_timestamp()
            self.executions[execution.execution_id] = execution
            result = self.executor.execute_plugin(
                plugin_name,
                {
                    "plugin_id": plugin_name,
                    "execution_id": execution.execution_id,
                    "input_data": context,
                },
            )
            execution.is_running = False
            execution.is_completed = True
            execution.success = result.success
            execution.completed_at = u.generate_iso_timestamp()
            if result.failure:
                execution.error_message = result.error
                return r[p.Plugin.Run].from_failure(result)
            execution.result = result.value
            return r[p.Plugin.Run].ok(execution)

        def fetch_execution(self, eid: str) -> p.Plugin.Run | None:
            """Return tracked execution state."""
            return self.executions.get(eid)

        def list_executions(self) -> t.SequenceOf[p.Plugin.Run]:
            """Return a snapshot of execution references."""
            return list(self.executions.values())

        def list_running_executions(self) -> t.SequenceOf[p.Plugin.Run]:
            """Return the currently running executions."""
            return [run for run in self.executions.values() if run.is_running]

        def cleanup_executions(self) -> int:
            """Remove only finished execution records."""
            completed = [
                eid for eid, run in self.executions.items() if run.is_completed
            ]
            for eid in completed:
                del self.executions[eid]
            return len(completed)

        @property
        def platform_status(self) -> t.JsonMapping:
            """Summarize the canonical plugin store and execution records."""
            plugins = self.list_plugins().unwrap()
            return {
                "total_plugins": len(plugins),
                "active_plugins": sum(plugin.is_enabled for plugin in plugins),
                "total_executions": len(self.executions),
                "running_executions": len(self.list_running_executions()),
            }

        @override
        def execute(self) -> p.Result[p.Plugin.Snapshot]:
            """Produce a transport snapshot without changing stored identities."""
            plugins = self.list_plugins()
            if plugins.failure:
                return r[p.Plugin.Snapshot].from_failure(plugins)
            return r[p.Plugin.Snapshot].ok(
                m.Plugin.Registry(
                    version=c.Plugin.DEFAULT_PLUGIN_VERSION,
                    plugins={
                        plugin.name: dict(
                            u.json_mapping_adapter().validate_python(
                                plugin.model_dump(mode="json")
                            )
                        )
                        for plugin in plugins.value
                    },
                )
            )

        @staticmethod
        def start_hot_reload(paths: t.StrSequence) -> p.Result[bool]:
            """Preserve the existing hot-reload lifecycle contract."""
            _ = paths
            return r[bool].ok(True)

        @staticmethod
        def stop_hot_reload() -> p.Result[bool]:
            """Preserve the existing hot-reload lifecycle contract."""
            return r[bool].ok(True)


__all__: list[str] = ["FlextPluginPlatform"]
