# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests import (
        conftest,
        constants,
        models,
        protocols,
        test_application_handlers,
        test_application_services,
        test_core_types,
        test_discovery,
        test_domain_entities,
        test_domain_ports,
        test_examples,
        test_handlers,
        test_hot_reload,
        test_hot_reload_package,
        test_imports,
        test_loader,
        test_manager,
        test_plugin,
        typings,
        unit,
        utilities,
    )
    from tests.constants import (
        TestsFlextPluginConstants,
        TestsFlextPluginConstants as c,
    )
    from tests.models import TestsFlextPluginModels, TestsFlextPluginModels as m
    from tests.protocols import (
        TestsFlextPluginProtocols,
        TestsFlextPluginProtocols as p,
    )
    from tests.typings import TestsFlextPluginTypes, TestsFlextPluginTypes as t
    from tests.utilities import (
        TestsFlextPluginUtilities,
        TestsFlextPluginUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    ("tests.unit",),
    {
        "TestsFlextPluginConstants": ("tests.constants", "TestsFlextPluginConstants"),
        "TestsFlextPluginModels": ("tests.models", "TestsFlextPluginModels"),
        "TestsFlextPluginProtocols": ("tests.protocols", "TestsFlextPluginProtocols"),
        "TestsFlextPluginTypes": ("tests.typings", "TestsFlextPluginTypes"),
        "TestsFlextPluginUtilities": ("tests.utilities", "TestsFlextPluginUtilities"),
        "c": ("tests.constants", "TestsFlextPluginConstants"),
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("tests.models", "TestsFlextPluginModels"),
        "models": "tests.models",
        "p": ("tests.protocols", "TestsFlextPluginProtocols"),
        "protocols": "tests.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "t": ("tests.typings", "TestsFlextPluginTypes"),
        "test_application_handlers": "tests.test_application_handlers",
        "test_application_services": "tests.test_application_services",
        "test_core_types": "tests.test_core_types",
        "test_discovery": "tests.test_discovery",
        "test_domain_entities": "tests.test_domain_entities",
        "test_domain_ports": "tests.test_domain_ports",
        "test_examples": "tests.test_examples",
        "test_handlers": "tests.test_handlers",
        "test_hot_reload": "tests.test_hot_reload",
        "test_hot_reload_package": "tests.test_hot_reload_package",
        "test_imports": "tests.test_imports",
        "test_loader": "tests.test_loader",
        "test_manager": "tests.test_manager",
        "test_plugin": "tests.test_plugin",
        "typings": "tests.typings",
        "u": ("tests.utilities", "TestsFlextPluginUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("logger", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "TestsFlextPluginConstants",
    "TestsFlextPluginModels",
    "TestsFlextPluginProtocols",
    "TestsFlextPluginTypes",
    "TestsFlextPluginUtilities",
    "c",
    "conftest",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "t",
    "test_application_handlers",
    "test_application_services",
    "test_core_types",
    "test_discovery",
    "test_domain_entities",
    "test_domain_ports",
    "test_examples",
    "test_handlers",
    "test_hot_reload",
    "test_hot_reload_package",
    "test_imports",
    "test_loader",
    "test_manager",
    "test_plugin",
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
