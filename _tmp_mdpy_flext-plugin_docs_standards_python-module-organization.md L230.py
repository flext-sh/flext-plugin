# from flext-plugin/docs/standards/python-module-organization.md:230
# Core plugin patterns
from __future__ import annotations

FlextPlugin  # Main plugin entity
FlextPluginModels.Config  # Plugin configuration entity
FlextPluginModels.Metadata  # Plugin metadata value object
FlextPluginModels.Registry  # Plugin collection aggregate
FlextPluginPlatform  # Main platform orchestrator

# Plugin management patterns
FlextPluginService  # Core plugin management service
FlextPluginDiscoveryService  # Plugin discovery and scanning
FlextPluginHandler  # CQRS command/query handler
FlextPlugins.Manager  # Plugin management interface

# Plugin lifecycle patterns
FlextPluginLoader  # Dynamic plugin loading
FlextPluginWatcher  # File system watching
FlextPluginReloader  # Hot-reload management```
**Rationale**: Clear namespace separation prevents conflicts across FLEXT's 32 projects.

### **Module-Level Naming**

