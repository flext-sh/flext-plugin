# from flext-plugin/docs/standards/python-module-organization.md:377
# Plugin-specific Clean Architecture layers
from __future__ import annotations

┌─────────────────────────────────────────┐
│         Platform Integration            │  # platform.py, simple_api.py
│    (External Plugin Interfaces)         │  # hot_reload.py, loader.py
├─────────────────────────────────────────┤
│         Application Layer               │  # services.py, handlers.py
│  (Plugin Management, CQRS Handlers)     │  # workflow orchestration
├─────────────────────────────────────────┤
│          Domain Layer                   │  # entities.py, ports.py
│   (Plugin Business Logic, DDD)          │  # value_objects.py
├─────────────────────────────────────────┤
│           Core Layer                    │
│    (Plugin Types, Base Patterns)        │  # error handling
├─────────────────────────────────────────┤
│        Foundation Layer                 │  # flext-core integration
│   (r, FlextContainer)         │  # base patterns
└─────────────────────────────────────────┘```
### **Plugin Lifecycle Architecture**

