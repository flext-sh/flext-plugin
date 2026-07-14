# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_api_direct": ("TestsFlextPluginApi",),
        ".test_config": ("TestsFlextPluginConfig",),
        ".test_constants": ("TestsFlextPluginConstantsUnit",),
        ".test_core_types": ("TestsFlextPluginCoreTypes",),
        ".test_discovery": ("TestsFlextPluginDiscovery",),
        ".test_domain_entities": ("TestsFlextPluginDomainEntities",),
        ".test_domain_ports": ("TestsFlextPluginDomainPorts",),
        ".test_examples": ("TestsFlextPluginExamples",),
        ".test_imports": ("TestsFlextPluginImports",),
        ".test_models": ("TestsFlextPluginModelsUnit",),
        ".test_platform_service": (
            "TestsFlextPluginPlatformExecution",
            "TestsFlextPluginPlatformRegistry",
            "TestsFlextPluginPlatformService",
        ),
        ".test_plugin": ("TestsFlextPluginPlugin",),
        ".test_types": ("TestsFlextPluginTypesUnit",),
        ".test_utilities_direct": ("TestsFlextPluginUtilities",),
        "flext_tests": (
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "t",
            "td",
            "tf",
            "tk",
            "tm",
            "tv",
            "u",
            "x",
        ),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
