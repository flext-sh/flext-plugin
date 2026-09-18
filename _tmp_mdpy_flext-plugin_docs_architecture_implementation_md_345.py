# from flext-plugin_docs/architecture/implementation.md:345
# Example protocol implementation
from __future__ import annotations

from flext_plugin import FlextPluginProtocols


class FilePluginDiscovery(FlextPluginProtocols.PluginDiscovery):
    """Concrete implementation of plugin discovery protocol."""

    async def discover_plugins(
        self, paths: t.StringList
    ) -> p.Result[list[dict[str, t.JsonValue]]]:
        """File-based plugin discovery implementation."""
        # Implementation details...
        return r.ok([])```
### Railway Pattern Implementation

#### **r[T] Error Handling**

