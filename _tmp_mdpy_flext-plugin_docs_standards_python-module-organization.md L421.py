# from flext-plugin/docs/standards/python-module-organization.md:421
# Hot-reload system with file watching and state preservation
from __future__ import annotations

┌─────────────────────────────────────────────────────────┐
│                File System Watcher                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   plugins/  │  │ ~/.flext/   │  │ /opt/flext/ │    │
│  │   directory │  │   plugins   │  │   plugins   │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                 Change Detection                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Created   │  │  Modified   │  │   Deleted   │    │
│  │    Files    │  │    Files    │  │    Files    │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                 Plugin Reloader                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ State Save  │  │   Reload    │  │State Restore│    │
│  │ & Cleanup   │  │   Plugin    │  │ & Activate  │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────┘```
______________________________________________________________________

## 🔄 **Plugin-Oriented Programming Patterns**

### **Plugin Factory Patterns**

