# from flext-plugin/docs/api-reference.md:122
from __future__ import annotations

class FlextPluginModels.Config(FlextModels.Entity):
    """Plugin configuration with validation"""

    name: str                          # Plugin name
    version: str                       # Plugin version
    description: str                   # Plugin description
    author: str                        # Plugin author
    dependencies: t.StringList            # Plugin dependencies
    metadata: FlextPluginModels.Metadata      # Additional metadata

    def validate_business_rules(self) -> p.Result[bool]:
        """Validate configuration business rules"""```
______________________________________________________________________

## Enumerations

### PluginStatus

