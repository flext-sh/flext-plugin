"""Behavioral tests for the flext_plugin public import contract.

The package promises a stable public surface through ``__all__``: the seven
``FlextPlugin*`` facades, the ``plugin`` alias, the short facade aliases
(``c``/``m``/``p``/``t``/``u`` and the re-exported ``flext_core`` kernel
aliases), and version metadata. These tests assert that contract as observable
behavior — every advertised name imports and resolves to a real object — rather
than poking module internals.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import importlib

import pytest

import flext_plugin
from flext_plugin import (
    FlextPluginApi,
    FlextPluginConstants,
    FlextPluginModels,
    FlextPluginProtocols,
    FlextPluginSettings,
    FlextPluginTypes,
    FlextPluginUtilities,
)
from flext_tests import tm

__all__: list[str] = ["TestsFlextPluginImports"]


class TestsFlextPluginImports:
    """Contract for the flext_plugin package public export surface."""

    def test_all_is_a_nonempty_tuple(self) -> None:
        """The package publishes an immutable, non-empty ``__all__`` contract."""
        tm.that(flext_plugin.__all__, is_=tuple)
        tm.that(len(flext_plugin.__all__) > 0, eq=True)

    @pytest.mark.parametrize("public_name", list(flext_plugin.__all__))
    def test_every_public_name_resolves(self, public_name: str) -> None:
        """Every name advertised in ``__all__`` is importable and non-None."""
        tm.that(hasattr(flext_plugin, public_name), eq=True)
        tm.that(getattr(flext_plugin, public_name) is not None, eq=True)

    @pytest.mark.parametrize(
        ("facade_name", "expected"),
        [
            ("FlextPluginApi", FlextPluginApi),
            ("FlextPluginConstants", FlextPluginConstants),
            ("FlextPluginModels", FlextPluginModels),
            ("FlextPluginProtocols", FlextPluginProtocols),
            ("FlextPluginSettings", FlextPluginSettings),
            ("FlextPluginTypes", FlextPluginTypes),
            ("FlextPluginUtilities", FlextPluginUtilities),
        ],
    )
    def test_facade_classes_are_classes_and_stable(
        self, facade_name: str, expected: type
    ) -> None:
        """Each ``FlextPlugin*`` facade is a class and a stable singleton."""
        resolved = getattr(flext_plugin, facade_name)
        tm.that(isinstance(resolved, type), eq=True)
        tm.that(resolved is expected, eq=True)

    def test_plugin_alias_is_the_api_facade(self) -> None:
        """The ``plugin`` alias is exactly the ``FlextPluginApi`` facade."""
        tm.that(flext_plugin.plugin is FlextPluginApi, eq=True)

    @pytest.mark.parametrize(
        "alias", ["c", "d", "e", "h", "m", "p", "r", "s", "t", "u", "x"]
    )
    def test_short_facade_aliases_are_exposed(self, alias: str) -> None:
        """Each short facade alias is published and resolves to an object."""
        tm.that(alias in flext_plugin.__all__, eq=True)
        tm.that(getattr(flext_plugin, alias) is not None, eq=True)

    @pytest.mark.parametrize(
        "version_attr",
        [
            "__version__",
            "__title__",
            "__description__",
            "__author__",
            "__license__",
            "__url__",
        ],
    )
    def test_version_metadata_is_non_empty_string(self, version_attr: str) -> None:
        """Version metadata is exposed as non-empty strings."""
        value = getattr(flext_plugin, version_attr)
        tm.that(isinstance(value, str), eq=True)
        tm.that(len(value) > 0, eq=True)

    def test_version_info_is_a_tuple(self) -> None:
        """``__version_info__`` is exposed as a tuple companion to the string."""
        tm.that(flext_plugin.__version_info__, is_=tuple)

    def test_package_reimport_is_idempotent(self) -> None:
        """Re-importing the package yields the same module object."""
        reimported = importlib.import_module("flext_plugin")
        tm.that(reimported is flext_plugin, eq=True)
        tm.that(reimported.FlextPluginApi is FlextPluginApi, eq=True)


test_imports = TestsFlextPluginImports
