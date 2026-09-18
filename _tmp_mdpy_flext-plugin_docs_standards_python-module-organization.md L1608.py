# from flext-plugin/docs/standards/python-module-organization.md:1608
# ✅ Use centralized plugin registry across ecosystem
from __future__ import annotations

from flext_plugin import FlextPluginModels.Registry
from flext_plugin import create_flext_plugin_platform

class EcosystemPluginManager:
    """Centralized plugin management for FLEXT ecosystem."""

    def __init__(self):
        self.platform = create_flext_plugin_platform()
        self.registry = self.platform.registry

    def register_ecosystem_plugins(self) -> p.Result[t.StringList]:
        """Register plugins from all ecosystem projects."""
        plugin_sources = [
            "./flext-tap-oracle/plugins",
            "./flext-target-oracle/plugins",
            "./flext-db-oracle/plugins",
            "./flext-ldap/plugins",
            "./flext-api/plugins"
        ]

        registered_plugins = []

        for source_path in plugin_sources:
            discovery_result = self.platform.discover_plugins(source_path)
            if discovery_result.success:
                for plugin in discovery_result.value:
                    register_result = self.registry.register_plugin(plugin)
                    if register_result.success:
                        registered_plugins.append(plugin.name)

        return r[bool].ok(registered_plugins)```
______________________________________________________________________

**Last Updated**: August 3, 2025
**Target Audience**: FLEXT Plugin developers and ecosystem contributors
**Scope**: Python module organization for plugin system development
**Version**: 0.12.0-dev → 0.9.9 development guidelines for plugin architecture
