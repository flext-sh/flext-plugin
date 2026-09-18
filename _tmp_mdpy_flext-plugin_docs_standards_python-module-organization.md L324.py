# from flext-plugin/docs/standards/python-module-organization.md:324
# Import from specific modules for clarity
from __future__ import annotations

from flext_plugin import FlextPlugin, FlextPluginModels.Registry
from flext_plugin import FlextPluginService
from flext_plugin import PluginStatus, PluginType

# More explicit but verbose
service = FlextPluginService(registry)
plugin = FlextPlugin(name="custom", version="0.9.9")```
#### **3. Factory Function Pattern**

