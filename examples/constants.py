"""Constants for flextplugin."""

from __future__ import annotations

from flext_plugin import FlextPluginConstants  # Why: FlextPluginConstants is owned by flext_plugin, not flext_core (pyrefly missing-module-attribute)

class ExamplesFlextPluginConstants(FlextPluginConstants):
    """Constants for flextplugin."""


__all__: list[str] = ["ExamplesFlextPluginConstants"]
