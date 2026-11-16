# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin._utilities.base import FlextPluginUtilitiesBase
    from flext_plugin._utilities.implementations import FlextPluginImplementations
    from flext_plugin._utilities.metadata import FlextPluginUtilitiesMetadata
    from flext_plugin._utilities.plugin_platform import FlextPluginPlatform


__all__: tuple[str, ...] = (
    "FlextPluginImplementations",
    "FlextPluginPlatform",
    "FlextPluginUtilitiesBase",
    "FlextPluginUtilitiesMetadata",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextPluginImplementations": ".implementations",
        "FlextPluginPlatform": ".plugin_platform",
        "FlextPluginUtilitiesBase": ".base",
        "FlextPluginUtilitiesMetadata": ".metadata",
    },
    public_exports=__all__,
    deferred_members={
        "FlextPluginImplementations": (
            "PluginDiscovery",
            "FilePluginLoader",
            "EchoExecutor",
            "FailingExecutor",
            "FailingDiscovery",
        ),
        "FlextPluginPlatform": (
            "Rules",
            "PluginPlatformService",
        ),
        "FlextPluginUtilitiesMetadata": (
            "DEFAULT_WATCH_INTERVAL",
            "PLUGIN_EXTENSIONS",
            "PLUGIN_MANIFESTS",
            "MAX_SIZE_MB",
            "NAME_PATTERN",
            "PLUGIN_FILE_EXTENSIONS",
            "PLUGIN_MANIFEST_FILES",
            "MAX_PLUGIN_SIZE_MB",
            "PLUGIN_NAME_PATTERN",
            "DANGEROUS_PLUGIN_PATTERNS",
            "discover_plugin_metadata",
            "extract_plugin_metadata",
            "validate_plugin_file",
            "validate_plugin_name",
            "_build_metadata",
            "_discover_metadata",
            "_is_candidate_file",
            "_metadata_fields",
            "_validate_plugin_path",
            "_validate_python_plugin_file",
        ),
    },
)
