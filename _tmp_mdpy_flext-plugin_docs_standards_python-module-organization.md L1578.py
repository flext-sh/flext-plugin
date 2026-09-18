# from flext-plugin/docs/standards/python-module-organization.md:1578
# ✅ Extend plugin configuration patterns consistently
from __future__ import annotations

from flext_plugin import PluginSystemSettings
from flext_core import FlextSettings


class OraclePluginSettings(FlextSettings):
    """Oracle plugin configuration extending FLEXT patterns."""

    connection_string: str
    schema: str = "HR"
    pool_size: int = 10
    timeout: int = 30

    class Config:
        env_prefix = "ORACLE_PLUGIN_"


class ProjectPluginConfig(PluginSystemSettings):
    """Project plugin configuration composing ecosystem settings."""

    oracle: OraclePluginSettings = field(default_factory=OraclePluginSettings)
    ldap: LdapPluginSettings = field(default_factory=LdapPluginSettings)

    # Inherit base plugin settings
    # discovery_paths, hot_reload_enabled, etc.```
### **Plugin Registry Integration**

