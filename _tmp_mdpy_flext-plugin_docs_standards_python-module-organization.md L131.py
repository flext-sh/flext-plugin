# from flext-plugin/docs/standards/python-module-organization.md:131
from __future__ import annotations

from flext_plugin import FlextPlugin, FlextPluginModels.Registry
from flext_plugin import FlextPlugins.Manager

class CustomPlugin(FlextPlugin):
    """Rich plugin entity with business logic"""

    def activate(self) -> p.Result[bool]:
        """Business operation with domain validation"""
        if self.status == PluginStatus.ACTIVE:
            return r[bool].fail("Plugin already active")

        # Business logic and domain events
        self.status = PluginStatus.ACTIVE
        self.add_domain_event("PluginActivated", {"plugin_id": self.id})
        return r[bool].ok(True)```
### **Application Layer** (`src/flext_plugin/application/`)

