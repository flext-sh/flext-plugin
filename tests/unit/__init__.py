# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_application_handlers": ("test_application_handlers",),
        ".test_application_services": ("test_application_services",),
        ".test_config": ("test_config",),
        ".test_constants": ("test_constants",),
        ".test_core_types": ("test_core_types",),
        ".test_discovery": ("test_discovery",),
        ".test_domain_entities": ("test_domain_entities",),
        ".test_domain_ports": ("test_domain_ports",),
        ".test_examples": ("test_examples",),
        ".test_handlers": ("test_handlers",),
        ".test_hot_reload": ("test_hot_reload",),
        ".test_hot_reload_package": ("test_hot_reload_package",),
        ".test_imports": ("test_imports",),
        ".test_loader": ("test_loader",),
        ".test_manager": ("test_manager",),
        ".test_models": ("test_models",),
        ".test_plugin": ("test_plugin",),
        ".test_types": ("test_types",),
        "flext_plugin": (
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "t",
            "u",
            "x",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
