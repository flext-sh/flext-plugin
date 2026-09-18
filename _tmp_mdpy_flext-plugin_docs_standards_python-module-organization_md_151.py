# from flext-plugin_docs/standards/python-module-organization.md:151
# Plugin application services and handlers
from __future__ import annotations

├── application/
│   ├── __init__.py          # 📤 Application layer exports
│   ├── services.py          # 📤 Plugin management services
│   └── handlers.py          # 📤 CQRS command/query handlers```
**Responsibility**: Orchestrate plugin business logic and coordinate between layers.

**Service Pattern**:

