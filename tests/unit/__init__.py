# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_application_handlers": ("TestsFlextPluginApplicationHandlers",),
        ".test_application_services": (
            "PluginInterface",
            "TestsFlextPluginApplicationServices",
        ),
        ".test_config": ("TestsFlextPluginConfig",),
        ".test_constants": ("TestsFlextPluginConstantsUnit",),
        ".test_core_types": ("TestsFlextPluginCoreTypes",),
        ".test_discovery": ("TestsFlextPluginDiscovery",),
        ".test_domain_entities": ("TestsFlextPluginDomainEntities",),
        ".test_domain_ports": ("TestsFlextPluginDomainPorts",),
        ".test_examples": ("TestsFlextPluginExamples",),
        ".test_handlers": ("TestsFlextPluginHandlers",),
        ".test_hot_reload": ("TestsFlextPluginHotReload",),
        ".test_hot_reload_package": ("TestsFlextPluginHotReloadPackage",),
        ".test_imports": ("test_imports",),
        ".test_loader": ("TestsFlextPluginLoader",),
        ".test_manager": ("TestsFlextPluginManager",),
        ".test_models": ("TestsFlextPluginModelsUnit",),
        ".test_plugin": ("TestsFlextPluginPlugin",),
        ".test_types": ("TestsFlextPluginTypesUnit",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
