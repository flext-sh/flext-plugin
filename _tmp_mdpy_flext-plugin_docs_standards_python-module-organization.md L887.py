# from flext-plugin/docs/standards/python-module-organization.md:887
from __future__ import annotations

from flext_plugin import FlextPluginModels.Metadata, FlextPluginModels.Config
from flext_cli import u
from flext_core import FlextSettings


class FlextPluginModels.Metadata(FlextModels.Value):
    """
    Immutable plugin metadata value object.

    Contains descriptive information about the plugin that doesn't
    change frequently and doesn't affect plugin identity.
    """

    description: str
    author: str
    license: str = "MIT"
    homepage_url: (str | None) = None
    repository_url: (str | None) = None
    documentation_url: (str | None) = None
    tags: t.StringList = field(default_factory=list)
    keywords: t.StringList = field(default_factory=list)

    def __post_init__(self):
        """Validate metadata on creation."""
        if not self.description.strip():
            raise ValueError("Plugin description cannot be empty")

        if not self.author.strip():
            raise ValueError("Plugin author cannot be empty")

        # Validate URLs if provided
        for url_field in ["homepage_url", "repository_url", "documentation_url"]:
            url = getattr(self, url_field)
            if url and not self._is_valid_url(url):
                raise ValueError(f"Invalid {url_field}: {url}")

    def has_tag(self, tag: str) -> bool:
        """Check if metadata contains specific tag."""
        return tag.lower() in [t.lower() for t in self.tags]

    def has_keyword(self, keyword: str) -> bool:
        """Check if metadata contains specific keyword."""
        return keyword.lower() in [k.lower() for k in self.keywords]

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format."""
        return url.startswith(("http://", "https://"))

class FlextPluginModels.Config(FlextModels.Value):
    """
    Immutable plugin configuration value object.

    Contains plugin-specific configuration that affects plugin
    behavior but doesn't change plugin identity.
    """

    config_data: dict
    schema_version: str = "0.9.9"
    environment: str = "production"

    def __post_init__(self):
        """Validate configuration on creation."""
        if not isinstance(self.config_data, dict):
            raise ValueError("Config data must be a dictionary")

        # Validate required configuration keys
        required_keys = self._get_required_keys()
        missing_keys = [key for key in required_keys if key not in self.config_data]
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {missing_keys}")

    def get_value(self, key: str, default = None):
        """Get configuration value with default fallback."""
        return self.config_data.get(key, default)

    def has_key(self, key: str) -> bool:
        """Check if configuration contains specific key."""
        return key in self.config_data

    def with_override(self, overrides: dict) -> 'FlextPluginModels.Config':
        """Create new settings with overridden values."""
        new_config_data = {**self.config_data, **overrides}
        return FlextPluginModels.Config(
            config_data=new_config_data,
            schema_version=self.schema_version,
            environment=self.environment
        )

    def _get_required_keys(self) -> t.StringList:
        """Get required configuration keys based on environment."""
        base_required = ["name", "version"]

        if self.environment == "production":
            return base_required + ["log_level", "metrics_enabled"]
        else:
            return base_required```
______________________________________________________________________

## 🚀 **Performance & Optimization Patterns**

### **Lazy Plugin Loading**

