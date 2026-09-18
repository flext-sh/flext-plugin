# from flext-plugin_docs/standards/python-module-organization.md:118
# Plugin domain modeling (DDD)
from __future__ import annotations

├── domain/
│   ├── __init__.py          # 🏛️ Domain exports
│   ├── entities.py          # 🏛️ Plugin entities (FlextPlugin, FlextPluginModels.Registry)
│   ├── ports.py             # 🏛️ Domain interfaces and contracts
│   └── value_objects.py     # 🏛️ Plugin metadata and configuration```
**Responsibility**: Rich domain modeling following Domain-Driven Design principles.

**Entity Pattern**:

