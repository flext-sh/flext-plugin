# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_cli import d, e, h, r, s, x

    from flext_plugin.__version__ import (
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_plugin._utilities.discovery import FlextPluginDiscovery
    from flext_plugin._utilities.plugin_platform import FlextPluginPlatform
    from flext_plugin.api import FlextPluginApi, plugin
    from flext_plugin.constants import FlextPluginConstants, c
    from flext_plugin.models import FlextPluginModels, m
    from flext_plugin.protocols import FlextPluginProtocols, p
    from flext_plugin.settings import FlextPluginSettings
    from flext_plugin.typings import FlextPluginTypes, t
    from flext_plugin.utilities import FlextPluginUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    ("._utilities",),
    build_lazy_import_map(
        {
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
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
            "flext_cli": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "FlextPluginApi",
    "FlextPluginConstants",
    "FlextPluginDiscovery",
    "FlextPluginModels",
    "FlextPluginPlatform",
    "FlextPluginProtocols",
    "FlextPluginSettings",
    "FlextPluginTypes",
    "FlextPluginUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "plugin",
    "r",
    "s",
    "t",
    "u",
    "x",
]
