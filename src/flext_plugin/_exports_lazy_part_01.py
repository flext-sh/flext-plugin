# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_PLUGIN_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        "._utilities.discovery": ("FlextPluginDiscovery",),
        "._utilities.plugin_platform": ("FlextPluginPlatform",),
        ".api": (
            "FlextPluginApi",
            "plugin",
        ),
        ".constants": (
            "FlextPluginConstants",
            "c",
        ),
        ".models": (
            "FlextPluginModels",
            "m",
        ),
        ".protocols": (
            "FlextPluginProtocols",
            "p",
        ),
        ".settings": ("FlextPluginSettings",),
        ".typings": (
            "FlextPluginTypes",
            "t",
        ),
        ".utilities": (
            "FlextPluginUtilities",
            "u",
        ),
    },
)

__all__: list[str] = ["FLEXT_PLUGIN_LAZY_IMPORTS_PART_01"]
