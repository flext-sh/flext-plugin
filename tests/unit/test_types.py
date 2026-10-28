"""Unit tests for FlextPluginTypes.

Behavioral tests for the public type-facade contract: MRO composition over
flext_cli types, the Plugin domain namespace, and the EventHandler alias.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import asyncio

import pytest

import flext_plugin
from flext_plugin import FlextPluginTypes
from tests import t, tm


class TestsFlextPluginTypesUnit:
    """Behavioral contract for the FlextPluginTypes facade."""

    @staticmethod
    def test_facade_exposes_inherited_cli_type_aliases() -> None:
        """The facade resolves inherited CLI type aliases to the same objects."""
        tm.ok(FlextPluginTypes.JsonMapping is t.JsonMapping)

    @staticmethod
    def test_module_alias_is_the_facade() -> None:
        """The module-level ``t`` alias exposes the facade itself."""
        tm.ok(flext_plugin.t is FlextPluginTypes)

    @staticmethod
    def test_tests_facade_exposes_plugin_namespace() -> None:
        """The tests facade exposes the inherited plugin event-handler alias."""
        tm.that(
            t.Plugin.EventHandler is FlextPluginTypes.Plugin.EventHandler,
            eq=True,
        )

    @staticmethod
    @pytest.mark.parametrize("inherited_alias", ["JsonMapping"])
    def test_inherits_cli_type_aliases(inherited_alias: str) -> None:
        """flext_cli type aliases remain reachable through the facade."""
        tm.ok(hasattr(FlextPluginTypes, inherited_alias))
        tm.that(
            getattr(FlextPluginTypes, inherited_alias) is getattr(t, inherited_alias),
            eq=True,
        )

    @staticmethod
    def test_plugin_namespace_is_exposed() -> None:
        """The Plugin domain namespace is a public attribute of the facade."""
        tm.ok(hasattr(FlextPluginTypes, "Plugin"))

    @staticmethod
    def test_event_handler_alias_is_declared() -> None:
        """Plugin is published under its declared name."""
        event_handler = FlextPluginTypes.Plugin.EventHandler
        tm.ok(hasattr(event_handler, "__value__"))

    @staticmethod
    def test_event_handler_resolves_to_async_json_mapping_signature() -> None:
        """EventHandler is a JsonMapping -> Awaitable[JsonMapping] callable."""
        resolved = repr(FlextPluginTypes.Plugin.EventHandler.__value__)
        tm.ok("Callable" in resolved)
        tm.ok("Awaitable" in resolved)
        tm.ok("JsonMapping" in resolved)

    @staticmethod
    def test_event_handler_is_usable_as_annotation() -> None:
        """The alias is a valid, concrete annotation for handler callables."""

        async def handler(payload: t.JsonMapping) -> t.JsonMapping:
            await asyncio.sleep(0)
            return payload

        annotated: FlextPluginTypes.Plugin.EventHandler = handler
        tm.ok(annotated is handler)
