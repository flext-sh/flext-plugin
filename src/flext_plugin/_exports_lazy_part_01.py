# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_PLUGIN_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        "._utilities": ("_utilities",),
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
        "flext_core._root_typing_parts": (
            "d",
            "e",
            "h",
            "r",
            "s",
            "x",
        ),
    },
)

__all__: list[str] = ["FLEXT_PLUGIN_LAZY_IMPORTS_PART_01"]
