"""Unit tests for FlextPluginTypes.

Behavioral tests for the public type-facade contract: MRO composition over
flext_cli types, the Plugin domain namespace, and the EventHandler alias.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import asyncio

import pytest
from flext_cli import t as cli_t

from flext_plugin import FlextPluginTypes, t as plugin_t
from tests import t, tm


class TestsFlextPluginTypesUnit:
    """Behavioral contract for the FlextPluginTypes facade."""

    @staticmethod
    def test_facade_composes_cli_types_via_mro() -> None:
        """FlextPluginTypes extends the flext_cli type facade via MRO."""
        tm.that(cli_t in FlextPluginTypes.__mro__, eq=True)

    @staticmethod
    def test_module_alias_is_the_facade() -> None:
        """The module-level ``t`` alias exposes the facade itself."""
        tm.that(plugin_t is FlextPluginTypes, eq=True)

    @staticmethod
    def test_tests_facade_inherits_plugin_facade_via_mro() -> None:
        """The tests type facade composes FlextPluginTypes through its MRO."""
        tm.that(FlextPluginTypes in t.__mro__, eq=True)

    @staticmethod
    @pytest.mark.parametrize("inherited_alias", ["JsonMapping"])
    def test_inherits_cli_type_aliases(inherited_alias: str) -> None:
        """flext_cli type aliases remain reachable through the facade."""
        tm.that(hasattr(FlextPluginTypes, inherited_alias), eq=True)
        tm.that(
            getattr(FlextPluginTypes, inherited_alias)
            is getattr(cli_t, inherited_alias),
            eq=True,
        )

    @staticmethod
    def test_plugin_namespace_is_exposed() -> None:
        """The Plugin domain namespace is a public attribute of the facade."""
        tm.that(hasattr(FlextPluginTypes, "Plugin"), eq=True)

    @staticmethod
    def test_event_handler_alias_is_declared() -> None:
        """Plugin.EventHandler is published under its declared name."""
        event_handler = FlextPluginTypes.Plugin.EventHandler
        tm.that(hasattr(event_handler, "__value__"), eq=True)

    @staticmethod
    def test_event_handler_resolves_to_async_json_mapping_signature() -> None:
        """EventHandler is a JsonMapping -> Awaitable[JsonMapping] callable."""
        resolved = repr(FlextPluginTypes.Plugin.EventHandler.__value__)
        tm.that("Callable" in resolved, eq=True)
        tm.that("Awaitable" in resolved, eq=True)
        tm.that("JsonMapping" in resolved, eq=True)

    @staticmethod
    def test_event_handler_is_usable_as_annotation() -> None:
        """The alias is a valid, concrete annotation for handler callables."""

        async def handler(payload: cli_t.JsonMapping) -> cli_t.JsonMapping:
            await asyncio.sleep(0)
            return payload

        annotated: FlextPluginTypes.Plugin.EventHandler = handler
        tm.that(annotated is handler, eq=True)
