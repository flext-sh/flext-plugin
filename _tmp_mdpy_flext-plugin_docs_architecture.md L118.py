# from flext-plugin/docs/architecture.md:118
from __future__ import annotations


class FlextPluginPlatform:
    """Main facade for plugin system"""

    def __init__(self, container: FlextContainer | None = None):
        self.container = container or FlextContainer()
        self._setup_services()

    def load_plugin(self, plugin: FlextPluginModels.Entity) -> p.Result[bool]:
        """Coordinate plugin loading across services"""

    def discover_plugins(
        self, path: str
    ) -> p.Result[Sequence[FlextPluginModels.Entity]]:
        """Coordinate plugin discovery"""```
### Application Services

- **FlextPluginService**: Core plugin operations
- **FlextPluginDiscoveryService**: Plugin discovery and validation
- **Hot Reload Services**: File watching and reload logic

______________________________________________________________________

## Infrastructure Layer

### Adapters

#### File System Discovery

