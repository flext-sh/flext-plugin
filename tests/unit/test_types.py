"""Unit tests for FlextPluginTypes.

Behavioral tests for the public type-facade contract: MRO composition over
flext_cli types, the Plugin domain namespace, and the EventHandler alias.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_cli import t as cli_t
from flext_plugin import FlextPluginTypes, t as plugin_t
from flext_tests import tm
from tests import t

__all__: list[str] = ["TestsFlextPluginTypesUnit"]


class TestsFlextPluginTypesUnit:
    """Behavioral contract for the FlextPluginTypes facade."""

    def test_facade_composes_cli_types_via_mro(self) -> None:
        """FlextPluginTypes extends the flext_cli type facade via MRO."""
        tm.that(issubclass(FlextPluginTypes, cli_t), eq=True)

    def test_module_alias_is_the_facade(self) -> None:
        """The module-level ``t`` alias exposes the facade itself."""
        tm.that(plugin_t is FlextPluginTypes, eq=True)

    def test_tests_facade_inherits_plugin_facade_via_mro(self) -> None:
        """The tests type facade composes FlextPluginTypes through its MRO."""
        tm.that(FlextPluginTypes in t.__mro__, eq=True)

    @pytest.mark.parametrize(
        "inherited_alias",
        ["JsonMapping"],
    )
    def test_inherits_cli_type_aliases(self, inherited_alias: str) -> None:
        """flext_cli type aliases remain reachable through the facade."""
        tm.that(hasattr(FlextPluginTypes, inherited_alias), eq=True)
        tm.that(
            getattr(FlextPluginTypes, inherited_alias)
            is getattr(cli_t, inherited_alias),
            eq=True,
        )

    def test_plugin_namespace_is_exposed(self) -> None:
        """The Plugin domain namespace is a public attribute of the facade."""
        tm.that(hasattr(FlextPluginTypes, "Plugin"), eq=True)

    def test_event_handler_alias_is_declared(self) -> None:
        """Plugin.EventHandler is published under its declared name."""
        event_handler = FlextPluginTypes.Plugin.EventHandler
        tm.that(event_handler.__name__, eq="EventHandler")

    def test_event_handler_resolves_to_async_json_mapping_signature(
        self,
    ) -> None:
        """EventHandler is a JsonMapping -> Awaitable[JsonMapping] callable."""
        resolved = repr(FlextPluginTypes.Plugin.EventHandler.__value__)
        tm.that("Callable" in resolved, eq=True)
        tm.that("Awaitable" in resolved, eq=True)
        tm.that("JsonMapping" in resolved, eq=True)

    def test_event_handler_is_usable_as_annotation(self) -> None:
        """The alias is a valid, concrete annotation for handler callables."""

        async def handler(payload: cli_t.JsonMapping) -> cli_t.JsonMapping:
            return payload

        annotated: FlextPluginTypes.Plugin.EventHandler = handler
        tm.that(annotated is handler, eq=True)
