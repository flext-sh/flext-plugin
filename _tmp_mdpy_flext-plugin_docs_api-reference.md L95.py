# from flext-plugin/docs/api-reference.md:95
from __future__ import annotations


class FlextPlugin(FlextModels.Entity):
    """Plugin entity with business rules"""

    # Properties
    name: str  # Plugin identifier
    plugin_version: str  # Plugin version
    status: PluginStatus  # Current lifecycle status
    settings: dict  # Plugin configuration
    metadata: FlextPluginModels.Metadata  # Plugin metadata

    # Business Methods
    def activate(self) -> bool:
        """Activate plugin (business rule: must be loaded first)"""

    def deactivate(self) -> bool:
        """Deactivate plugin"""

    def validate_business_rules(self) -> p.Result[bool]:
        """Validate plugin business rules"""```
### FlextPluginModels.Config (Entity)

Plugin configuration entity.

