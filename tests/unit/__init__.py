# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_application_handlers": ("TestFlextPluginHandlers",),
        ".test_application_services": (
            "PluginInterface",
            "TestBackwardsCompatibilityAliasesReal",
            "TestFlextPluginDiscoveryReal",
            "TestFlextPluginServiceReal",
            "TestFlextPluginServiceWithRealAdapters",
            "TestRealPluginDiscoveryAndExecution",
            "TestRealPluginErrorScenarios",
            "TestRealPluginIntegrationWorkflow",
            "TestServiceErrorHandling",
            "TestServicesIntegrationReal",
        ),
        ".test_config": ("TestFlextPluginSettings",),
        ".test_constants": ("TestFlextPluginConstants",),
        ".test_core_types": (
            "TestFlextPluginConstantsLifecycle",
            "TestFlextPluginConstantsPluginType",
            "TestPluginError",
        ),
        ".test_discovery": ("TestFlextPluginDiscovery",),
        ".test_domain_entities": (
            "TestFlextPlugin",
            "TestFlextPluginExecution",
            "TestFlextPluginMetadata",
            "TestFlextPluginRegistryEntity",
            "TestFlextPluginSettingsEntities",
        ),
        ".test_domain_ports": ("TestFlextPluginDiscoveryPorts",),
        ".test_examples": ("test_examples",),
        ".test_handlers": ("TestFlextPluginHandlersHandlers",),
        ".test_hot_reload": ("TestFlextPluginHotReload",),
        ".test_hot_reload_package": ("TestHotReloadPackage",),
        ".test_imports": ("test_imports",),
        ".test_loader": (
            "TestDynamicLoaderAdapter",
            "TestFlextPluginLoader",
        ),
        ".test_manager": (
            "TestFlextPluginService",
            "TestFlextPluginServiceStubBridges",
        ),
        ".test_models": ("TestFlextPluginModels",),
        ".test_plugin": (
            "TestPluginModel",
            "TestPluginPlatform",
            "TestPluginRegistry",
        ),
        ".test_types": ("TestFlextPluginTypes",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
