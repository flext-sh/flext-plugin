"""Type aliases for flextplugin."""

from __future__ import annotations

from flext_plugin import FlextPluginTypes  # Why: FlextPluginTypes is owned by flext_plugin, not flext_core (pyrefly missing-module-attribute)

class ExamplesFlextPluginTypes(FlextPluginTypes):
    """Type aliases for flextplugin."""


__all__: list[str] = ["ExamplesFlextPluginTypes"]
