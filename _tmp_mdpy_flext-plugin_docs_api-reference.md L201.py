# from flext-plugin/docs/api-reference.md:201
from __future__ import annotations


class FlextPluginDiscoveryService:
    """Plugin discovery and validation service"""

    def scan_directory(self, path: str) -> p.Result[Sequence[FlextPluginModels.Entity]]:
        """Scan directory for plugins"""

    def validate_plugin_integrity(
        self, plugin: FlextPluginModels.Entity
    ) -> p.Result[bool]:
        """Validate plugin integrity"""```
______________________________________________________________________

## Hot Reload

### Hot Reload Configuration

