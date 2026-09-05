"""Utility functions for flextplugin."""

from __future__ import annotations

from flext_plugin import FlextPluginUtilities  # Why: FlextPluginUtilities is owned by flext_plugin, not flext_core (pyrefly missing-module-attribute)

class ExamplesFlextPluginUtilities(FlextPluginUtilities):
    """Utility functions for flextplugin."""


__all__: list[str] = ["ExamplesFlextPluginUtilities"]
