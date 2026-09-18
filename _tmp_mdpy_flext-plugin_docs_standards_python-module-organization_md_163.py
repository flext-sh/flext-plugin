# from flext-plugin_docs/standards/python-module-organization.md:163
from __future__ import annotations

from flext_plugin import FlextPluginService


class PluginWorkflow:
    def __init__(self, service: FlextPluginService):
        self.service = service

    def deploy_plugin(self, plugin_config: dict) -> p.Result[FlextPlugin]:
        """Complete plugin deployment workflow"""
        return (
            self.service
            .validate_plugin_config(plugin_config)
            .flat_map(lambda settings: self.service.create_plugin(settings))
            .flat_map(lambda plugin: self.service.register_plugin(plugin))
            .flat_map(lambda plugin: self.service.activate_plugin(plugin.id))
        )```
### **Configuration Layer** (`src/flext_plugin/settings/`)

