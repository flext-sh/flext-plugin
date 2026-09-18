# from flext-plugin/docs/architecture.md:94
from __future__ import annotations

class FlextPluginModels.Config(FlextModels.Entity):
    """Plugin configuration with validation"""
    name: str
    version: str
    dependencies: t.StringList
    metadata: FlextPluginModels.Metadata

    class Config:
        frozen = True  # Immutable value object```
### Services

Plugin-specific business logic that doesn't belong to a single entity.

______________________________________________________________________

## Application Layer

### FlextPluginPlatform (Facade)

Coordinates all plugin operations:

