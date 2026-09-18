# from flext-plugin_docs/standards/python-module-organization.md:585
from __future__ import annotations

from flext_plugin import FlextPluginDiscoveryService
from flext_plugin import PluginDiscovery


class AdvancedPluginDiscovery:
    """Advanced plugin discovery with filtering and validation."""

    def __init__(self, discovery_service: FlextPluginDiscoveryService):
        self.discovery_service = discovery_service
        self.core_discovery = PluginDiscovery()

    def discover_plugins_by_type(
        self, plugin_type: PluginType, paths: t.StringList
    ) -> p.Result[list[FlextPlugin]]:
        """Discover plugins filtered by type."""
        try:
            all_plugins = []

            for path in paths:
                result = self.discovery_service.discover_plugins(path)
                if result.success:
                    # Filter by type
                    typed_plugins = [
                        p
                        for p in result.value
                        if hasattr(p, "plugin_type") and p.plugin_type == plugin_type
                    ]
                    all_plugins.extend(typed_plugins)

            return r[bool].ok(all_plugins)

        except Exception as e:
            return r[bool].fail(f"Plugin discovery failed: {e}")

    def discover_singer_plugins(
        self, meltano_path: str
    ) -> p.Result[dict[str, list[FlextPlugin]]]:
        """Discover Singer plugins from Meltano project structure."""
        try:
            meltano_yml_path = Path(meltano_path) / "meltano.yml"
            if not meltano_yml_path.exists():
                return r[bool].fail("meltano.yml not found")

            # Parse meltano.yml
            meltano_config = self._parse_meltano_config(meltano_yml_path)

            # Discover by Singer plugin type
            singer_plugins = {
                "taps": self.discover_plugins_by_type(PluginType.TAP, [meltano_path]),
                "targets": self.discover_plugins_by_type(
                    PluginType.TARGET, [meltano_path]
                ),
                "transforms": self.discover_plugins_by_type(
                    PluginType.TRANSFORM, [meltano_path]
                ),
            }

            # Validate against meltano.yml
            validated_plugins = {}
            for category, plugins_result in singer_plugins.items():
                if plugins_result.success:
                    validated = self._validate_against_meltano_config(
                        plugins_result.value, meltano_config.get(category, [])
                    )
                    validated_plugins[category] = (
                        validated.data if validated.success else []
                    )

            return r[bool].ok(validated_plugins)

        except Exception as e:
            return r[bool].fail(f"Singer plugin discovery failed: {e}")```
______________________________________________________________________

## 🎯 **Domain-Driven Design Patterns**

### **Plugin Entity Patterns**

