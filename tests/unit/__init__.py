# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_plugin.tests.unit.test_config import (
        TestsFlextPluginConfig as TestsFlextPluginConfig,
    )
    from flext_plugin.tests.unit.test_constants import (
        TestsFlextPluginConstantsUnit as TestsFlextPluginConstantsUnit,
    )
    from flext_plugin.tests.unit.test_core_types import (
        TestsFlextPluginCoreTypes as TestsFlextPluginCoreTypes,
    )
    from flext_plugin.tests.unit.test_discovery import (
        TestsFlextPluginDiscovery as TestsFlextPluginDiscovery,
    )
    from flext_plugin.tests.unit.test_domain_entities import (
        TestsFlextPluginDomainEntities as TestsFlextPluginDomainEntities,
    )
    from flext_plugin.tests.unit.test_domain_ports import (
        TestsFlextPluginDomainPorts as TestsFlextPluginDomainPorts,
    )
    from flext_plugin.tests.unit.test_examples import (
        TestsFlextPluginExamples as TestsFlextPluginExamples,
    )
    from flext_plugin.tests.unit.test_models import (
        TestsFlextPluginModelsUnit as TestsFlextPluginModelsUnit,
    )
    from flext_plugin.tests.unit.test_plugin import (
        TestsFlextPluginPlugin as TestsFlextPluginPlugin,
    )
    from flext_plugin.tests.unit.test_types import (
        TestsFlextPluginTypesUnit as TestsFlextPluginTypesUnit,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_config": ("TestsFlextPluginConfig",),
        ".test_constants": ("TestsFlextPluginConstantsUnit",),
        ".test_core_types": ("TestsFlextPluginCoreTypes",),
        ".test_discovery": ("TestsFlextPluginDiscovery",),
        ".test_domain_entities": ("TestsFlextPluginDomainEntities",),
        ".test_domain_ports": ("TestsFlextPluginDomainPorts",),
        ".test_examples": ("TestsFlextPluginExamples",),
        ".test_imports": ("test_imports",),
        ".test_models": ("TestsFlextPluginModelsUnit",),
        ".test_plugin": ("TestsFlextPluginPlugin",),
        ".test_types": ("TestsFlextPluginTypesUnit",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
