# from flext-plugin/docs/standards/python-module-organization.md:399
# Plugin state transitions with architectural boundaries
from __future__ import annotations

┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  DISCOVERED  │───▶│    LOADED    │───▶│    ACTIVE    │
│  (Discovery) │    │   (Loader)   │    │  (Platform)  │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        │                    ▼                    ▼
        │            ┌──────────────┐    ┌──────────────┐
        │            │    ERROR     │    │   INACTIVE   │
        │            │  (Handler)   │    │  (Platform)  │
        │            └──────────────┘    └──────────────┘
        │                    │                    │
        ▼                    │                    │
┌──────────────┐            │                    │
│   DISABLED   │◀───────────┴────────────────────┘
│  (Manager)   │
└──────────────┘```
### **Hot-Reload Architecture**

