# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Utilities package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .discovery import FlextPluginDiscovery
    from .plugin_platform import FlextPluginPlatform
__all__: tuple[str, ...] = ("FlextPluginDiscovery", "FlextPluginPlatform")

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".discovery": ("FlextPluginDiscovery",),
            ".plugin_platform": ("FlextPluginPlatform",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
