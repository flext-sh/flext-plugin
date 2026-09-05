"""Domain models for flextplugin."""

from __future__ import annotations

from flext_plugin import FlextPluginModels  # Why: FlextPluginModels is owned by flext_plugin, not flext_core (pyrefly missing-module-attribute)

class ExamplesFlextPluginModels(FlextPluginModels):
    """Domain models for flextplugin."""


__all__: list[str] = ["ExamplesFlextPluginModels"]
