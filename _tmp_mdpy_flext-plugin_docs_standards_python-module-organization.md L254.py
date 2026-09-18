# from flext-plugin/docs/standards/python-module-organization.md:254
# Core functionality modules
from __future__ import annotations

types.py  # Plugin types, enums, and result objects
entities.py  # Domain entities (FlextPlugin, FlextPluginModels.Registry)
ports.py  # Domain interfaces and contracts
services.py  # Application services and business logic
handlers.py  # CQRS command and query handlers

# Platform integration modules
platform.py  # Main platform orchestration
simple_api.py  # Factory functions and utilities
hot_reload.py  # Hot-reload system integration
discovery.py  # High-level plugin discovery
loader.py  # Dynamic plugin loading mechanisms```
**Pattern**: One primary concern per module with cohesive functionality.

### **Plugin Type Naming**

