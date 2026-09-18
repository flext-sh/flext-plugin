# from flext-plugin/docs/architecture/implementation.md:774
# flext_plugin/settings.py
from __future__ import annotations

from pydantic import BaseModel, u.Field, validator
from flext_plugin import FlextPluginConstants


class FlextPluginSettings:
    """Plugin system configuration using Pydantic."""

    # Plugin discovery settings
    plugin_paths: t.StringList = u.Field(
        default_factory=lambda: ["./plugins", "~/.flext/plugins", "/opt/flext/plugins"]
    )

    # Security settings
    security_level: str = u.Field(default="HIGH", regex="^(LOW|MEDIUM|HIGH)$")

    enable_plugin_validation: bool = u.Field(default=True)
    enable_sandboxing: bool = u.Field(default=True)

    # Performance settings
    max_concurrent_plugins: int = u.Field(default=100, ge=1, le=1000)
    plugin_timeout_seconds: int = u.Field(default=300, ge=1, le=3600)

    # Hot reload settings
    enable_hot_reload: bool = u.Field(default=True)
    hot_reload_interval: int = u.Field(default=2, ge=1, le=60)

    # Monitoring settings
    enable_metrics: bool = u.Field(default=True)
    enable_tracing: bool = u.Field(default=True)
    metrics_interval: int = u.Field(default=60, ge=10, le=3600)

    @validator("plugin_paths")
    def validate_plugin_paths(cls, paths):
        """Validate plugin paths exist or are valid."""
        for path in paths:
            if not (
                path.startswith("./") or path.startswith("~/") or path.startswith("/")
            ):
                raise ValueError(f"Invalid plugin path format: {path}")
        return paths

    def get_plugin_paths(self) -> t.StringList:
        """Get resolved plugin paths."""
        import os
        from pathlib import Path

        resolved_paths = []
        for path in self.plugin_paths:
            resolved = os.path.expanduser(path)
            if Path(resolved).exists() or path.startswith("./"):
                resolved_paths.append(resolved)

        return resolved_paths

    def is_security_enabled(self) -> bool:
        """Check if security features are enabled."""
        return self.security_level in ["MEDIUM", "HIGH"]

    def is_monitoring_enabled(self) -> bool:
        """Check if monitoring features are enabled."""
        return self.enable_metrics or self.enable_tracing```
______________________________________________________________________

## 🚀 Deployment and Operations

### Container Configuration

#### **Docker Deployment**

