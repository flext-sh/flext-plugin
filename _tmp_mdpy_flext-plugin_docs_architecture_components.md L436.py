# from flext-plugin/docs/architecture/components.md:436
# Services operate on domain entities
from __future__ import annotations

service = FlextPluginService()
plugin = service.create_plugin(settings)  # Service operation
    ↓
entity = FlextPluginModels.Plugin()   # Domain entity
entity.validate_business_rules()        # Business rules
    ↓
protocol = FlextPluginProtocols.Plugin  # Domain contract
# Structural typing ensures compatibility```
#### **Infrastructure → Adapters → External Systems**

