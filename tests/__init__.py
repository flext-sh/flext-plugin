# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map(
        {
            ".base": (
                "TestsFlextPluginServiceBase",
                "s",
            ),
            ".conftest": ("conftest",),
            ".constants": (
                "TestsFlextPluginConstants",
                "c",
            ),
            ".models": (
                "TestsFlextPluginModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextPluginProtocols",
                "p",
            ),
            ".settings": ("TestsFlextPluginSettings",),
            ".typings": (
                "TestsFlextPluginTypes",
                "t",
            ),
            ".unit": ("unit",),
            ".unit.test_config": ("TestsFlextPluginConfig",),
            ".unit.test_constants": ("TestsFlextPluginConstantsUnit",),
            ".unit.test_core_types": ("TestsFlextPluginCoreTypes",),
            ".unit.test_discovery": ("TestsFlextPluginDiscovery",),
            ".unit.test_domain_entities": ("TestsFlextPluginDomainEntities",),
            ".unit.test_domain_ports": ("TestsFlextPluginDomainPorts",),
            ".unit.test_examples": ("TestsFlextPluginExamples",),
            ".unit.test_models": ("TestsFlextPluginModelsUnit",),
            ".unit.test_plugin": ("TestsFlextPluginPlugin",),
            ".unit.test_types": ("TestsFlextPluginTypesUnit",),
            ".utilities": (
                "TestsFlextPluginUtilities",
                "u",
            ),
            "flext_tests": (
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
