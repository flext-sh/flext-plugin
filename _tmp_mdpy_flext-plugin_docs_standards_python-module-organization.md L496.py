# from flext-plugin/docs/standards/python-module-organization.md:496
from __future__ import annotations

from flext_plugin import FlextPlugin
from flext_plugin import PluginStatus


class PluginLifecycleManager:
    """Manages plugin lifecycle with state transitions."""

    def initialize_plugin(self, plugin: FlextPlugin) -> p.Result[bool]:
        """Initialize plugin with resource allocation."""
        if plugin.status != PluginStatus.LOADED:
            return r[bool].fail("Plugin must be loaded before initialization")

        try:
            # Allocate resources
            self._allocate_plugin_resources(plugin)

            # Run initialization logic
            init_result = plugin.initialize()
            if init_result.failure:
                self._cleanup_plugin_resources(plugin)
                return init_result

            # Update status
            plugin.status = PluginStatus.INACTIVE
            self._emit_plugin_event("PluginInitialized", plugin)

            return r[bool].ok(True)

        except Exception as e:
            self._cleanup_plugin_resources(plugin)
            return r[bool].fail(f"Plugin initialization failed: {e}")

    def activate_plugin(self, plugin: FlextPlugin) -> p.Result[bool]:
        """Activate plugin with dependency checking."""
        if plugin.status not in [PluginStatus.INACTIVE, PluginStatus.LOADED]:
            return r[bool].fail("Plugin not ready for activation")

        # Check dependencies
        dependency_check = self._validate_plugin_dependencies(plugin)
        if dependency_check.failure:
            return dependency_check

        # Activate plugin
        activation_result = plugin.activate()
        if activation_result.success:
            plugin.status = PluginStatus.ACTIVE
            self._emit_plugin_event("PluginActivated", plugin)

        return activation_result

    def hot_reload_plugin(self, plugin_id: str) -> p.Result[FlextPlugin]:
        """Hot reload plugin with state preservation."""
        try:
            # Get current plugin
            current_plugin = self._get_plugin(plugin_id)
            if current_plugin.failure:
                return current_plugin

            plugin = current_plugin.data

            # Save current state
            state_backup = self._backup_plugin_state(plugin)

            # Deactivate and unload
            self.deactivate_plugin(plugin)
            self._unload_plugin(plugin)

            # Reload plugin
            reload_result = self._reload_plugin_from_file(plugin_id)
            if reload_result.failure:
                # Restore from backup
                self._restore_plugin_state(plugin, state_backup.data)
                return reload_result

            new_plugin = reload_result.value

            # Restore state and reactivate
            self._restore_plugin_state(new_plugin, state_backup.data)
            self.activate_plugin(new_plugin)

            return r[bool].ok(new_plugin)

        except Exception as e:
            return r[bool].fail(f"Hot reload failed: {e}")```
### **Plugin Discovery Patterns**

