# from flext-plugin_docs/standards/python-module-organization.md:789
from __future__ import annotations

from flext_plugin import FlextPluginModels.Registry
from flext_cli import u
from flext_core import FlextSettings

class FlextPluginModels.Registry(FlextModels.AggregateRoot):
    """
    Plugin registry aggregate managing plugin collections.

    Serves as the consistency boundary for plugin operations,
    ensuring business rules and maintaining registry integrity.
    """

    plugins: dict[str, FlextPlugin] = field(default_factory=dict)
    discovery_paths: t.StringList = field(default_factory=list)
    last_discovery: (datetime | None) = None
    registry_version: str = "0.9.9"

    # Registry-level business rules
    MAX_PLUGINS_PER_TYPE = 100
    RESERVED_PLUGIN_NAMES = ["system", "core", "REDACTED_LDAP_BIND_PASSWORD", "flext"]

    def register_plugin(self, plugin: FlextPlugin) -> p.Result[FlextPlugin]:
        """Register plugin with business rule validation."""
        try:
            # Validate plugin name
            if plugin.name in self.RESERVED_PLUGIN_NAMES:
                return r[bool].fail(f"Plugin name '{plugin.name}' is reserved")

            # Check for duplicates
            if plugin.name in self.plugins:
                existing = self.plugins[plugin.name]
                if existing.plugin_version == plugin.plugin_version:
                    return r[bool].fail(f"Plugin {plugin.name} v{plugin.plugin_version} already registered")

            # Validate plugin type limits
            type_count = len([p for p in self.plugins.values() if p.plugin_type == plugin.plugin_type])
            if type_count >= self.MAX_PLUGINS_PER_TYPE:
                return r[bool].fail(f"Maximum plugins of type {plugin.plugin_type} exceeded")

            # Register plugin
            self.plugins[plugin.name] = plugin
            plugin.status = PluginStatus.LOADED

            # Generate registry event
            self.add_domain_event({
                "type": "PluginRegistered",
                "registry_id": str(self.id),
                "plugin_id": str(plugin.id),
                "plugin_name": plugin.name,
                "plugin_type": plugin.plugin_type.value,
                "timestamp": datetime.utcnow().isoformat()
            })

            return r[bool].ok(plugin)

        except Exception as e:
            return r[bool].fail(f"Plugin registration failed: {e}")

    def get_plugins_by_type(self, plugin_type: PluginType) -> list[FlextPlugin]:
        """Get all plugins of specified type."""
        return [p for p in self.plugins.values() if p.plugin_type == plugin_type]

    def get_active_plugins(self) -> list[FlextPlugin]:
        """Get all currently active plugins."""
        return [p for p in self.plugins.values() if p.status == PluginStatus.ACTIVE]

    def get_registry_health(self) -> dict:
        """Get overall registry health metrics."""
        total_plugins = len(self.plugins)
        active_plugins = len(self.get_active_plugins())

        # Calculate health by plugin type
        type_distribution = {}
        for plugin_type in PluginType:
            count = len(self.get_plugins_by_type(plugin_type))
            type_distribution[plugin_type.value] = count

        # Calculate overall health score
        unhealthy_plugins = len([
            p for p in self.plugins.values()
            if p.get_health_status()["health"] == "unhealthy"
        ])

        health_score = (total_plugins - unhealthy_plugins) / total_plugins if total_plugins > 0 else 1.0

        return {
            "total_plugins": total_plugins,
            "active_plugins": active_plugins,
            "type_distribution": type_distribution,
            "health_score": health_score,
            "last_discovery": self.last_discovery.isoformat() if self.last_discovery else None,
            "registry_version": self.registry_version
        }```
### **Plugin Value Object Patterns**

