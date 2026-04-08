# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.models as _tests_models
    from tests.constants import (
        TestsFlextPluginConstants,
        TestsFlextPluginConstants as c,
    )

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import TestsFlextPluginModels, TestsFlextPluginModels as m

    protocols = _tests_protocols
    import tests.test_application_handlers as _tests_test_application_handlers
    from tests.protocols import (
        TestsFlextPluginProtocols,
        TestsFlextPluginProtocols as p,
    )

    test_application_handlers = _tests_test_application_handlers
    import tests.test_application_services as _tests_test_application_services

    test_application_services = _tests_test_application_services
    import tests.test_core_types as _tests_test_core_types

    test_core_types = _tests_test_core_types
    import tests.test_discovery as _tests_test_discovery

    test_discovery = _tests_test_discovery
    import tests.test_domain_entities as _tests_test_domain_entities

    test_domain_entities = _tests_test_domain_entities
    import tests.test_domain_ports as _tests_test_domain_ports

    test_domain_ports = _tests_test_domain_ports
    import tests.test_examples as _tests_test_examples

    test_examples = _tests_test_examples
    import tests.test_handlers as _tests_test_handlers

    test_handlers = _tests_test_handlers
    import tests.test_hot_reload as _tests_test_hot_reload

    test_hot_reload = _tests_test_hot_reload
    import tests.test_hot_reload_package as _tests_test_hot_reload_package

    test_hot_reload_package = _tests_test_hot_reload_package
    import tests.test_imports as _tests_test_imports

    test_imports = _tests_test_imports
    import tests.test_loader as _tests_test_loader

    test_loader = _tests_test_loader
    import tests.test_manager as _tests_test_manager

    test_manager = _tests_test_manager
    import tests.test_plugin as _tests_test_plugin

    test_plugin = _tests_test_plugin
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.unit as _tests_unit
    from tests.typings import TestsFlextPluginTypes, TestsFlextPluginTypes as t

    unit = _tests_unit
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
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
