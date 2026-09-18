# from flext-plugin/docs/standards/python-module-organization.md:197
from __future__ import annotations

from flext_plugin import PluginSystemSettings
from flext_core import FlextSettings


class PluginSystemSettings(FlextSettings):
    """Plugin system configuration with environment support"""

    discovery_paths: t.StringList = ["./plugins", "~/.flext/plugins"]
    hot_reload_enabled: bool = True
    watch_interval: int = 2
    max_workers: int = 10
    cache_dir: str = ".plugin_cache"

    class Config:
        env_prefix = "FLEXT_PLUGIN_"
        env_file = ".env"


# Environment variables:
# FLEXT_PLUGIN_DISCOVERY_PATHS=/opt/plugins:/usr/local/plugins
# FLEXT_PLUGIN_HOT_RELOAD_ENABLED=true
# FLEXT_PLUGIN_WATCH_INTERVAL=1```
______________________________________________________________________

## 🎯 **Semantic Naming Conventions**

### **Public API Naming (FlextPlugin prefix)**

All plugin-related exports use consistent prefixing to avoid namespace conflicts:

