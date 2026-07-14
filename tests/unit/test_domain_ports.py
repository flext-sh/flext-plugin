"""Behavioral tests for flext_plugin plugin discovery public contract.

Exercises the observable contract of ``u.Plugin.Discovery`` (the
``FlextPluginDiscovery`` facade): the ``r[T]`` outcomes of ``discover_plugin`` /
``discover_plugins``, the discovery-strategy contract, and the recursive
directory-walk promised by ``discover_python_plugins_in_directory``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

import pytest
from flext_tests import tm

from flext_plugin import p, t, u
from flext_plugin._utilities.discovery import FlextPluginDiscovery

__all__: list[str] = ["TestsFlextPluginDomainPorts"]


class TestsFlextPluginDomainPorts:
    """Public-contract tests for the plugin discovery facade.

    All assertions target observable behavior: ``r[T]`` success/failure,
    returned sequences, and the directory-walk filtering rules. No private
    attribute or internal-collaborator access.
    """

    @pytest.fixture
    def logger(self) -> p.Logger:
        """Return a real logger for strategy/static-method construction."""
        return u.fetch_logger("tests.flext_plugin.discovery")

    @pytest.fixture
    def discovery(self) -> FlextPluginDiscovery:
        """Return a fresh discovery facade instance."""
        return FlextPluginDiscovery()

    @staticmethod
    def _make_tree(root: Path) -> None:
        """Materialize a nested plugin tree with names that test the filters."""
        (root / "alpha.py").write_text("value = 1", encoding="utf-8")
        (root / "_private.py").write_text("value = 1", encoding="utf-8")
        (root / "notes.txt").write_text("ignored", encoding="utf-8")
        package = root / "package"
        package.mkdir()
        (package / "beta.py").write_text("value = 2", encoding="utf-8")
        dunder = root / "__pycache_like__"
        dunder.mkdir()
        (dunder / "gamma.py").write_text("value = 3", encoding="utf-8")

    # ------------------------------------------------------------------ #
    # discover_plugin — single-path fallible contract
    # ------------------------------------------------------------------ #

    @pytest.mark.parametrize(
        "missing_path",
        [
            "definitely/not/here/nope_plugin.py",
            "/tmp/flext-plugin-absent-xyz.py",
            "unresolved-entry-point-name",
        ],
    )
    def test_discover_plugin_fails_when_nothing_resolves(
        self,
        discovery: FlextPluginDiscovery,
        missing_path: str,
    ) -> None:
        """An unresolvable path yields a failure result, never a raised error."""
        result = discovery.discover_plugin(missing_path)

        tm.that(result.success, eq=False)
        tm.that(result.error, is_=str)
        assert result.error

    def test_discover_plugin_failure_unwrap_raises(
        self,
        discovery: FlextPluginDiscovery,
    ) -> None:
        """Unwrapping a failed discovery raises rather than fabricating data."""
        result = discovery.discover_plugin("no/such/plugin_qwerty.py")

        tm.that(result.success, eq=False)
        with pytest.raises(RuntimeError):
            result.unwrap()

    # ------------------------------------------------------------------ #
    # discover_plugins — multi-path aggregate contract
    # ------------------------------------------------------------------ #

    def test_discover_plugins_empty_input_succeeds_with_empty_sequence(
        self,
        discovery: FlextPluginDiscovery,
    ) -> None:
        """No search paths still succeeds and yields an empty sequence."""
        result = discovery.discover_plugins([])

        tm.that(result.success, eq=True)
        tm.that(list(result.unwrap()), eq=[])

    def test_discover_plugins_directory_returns_success_sequence(
        self,
        discovery: FlextPluginDiscovery,
        tmp_path: Path,
    ) -> None:
        """A real directory yields a success whose value is a sequence."""
        self._make_tree(tmp_path)

        result = discovery.discover_plugins([str(tmp_path)])

        tm.that(result.success, eq=True)
        discovered = list(result.unwrap())
        # Names, when present, are unique (facade dedupes by plugin name).
        names = [item.name for item in discovered]
        tm.that(len(names), eq=len(set(names)))

    def test_discover_plugins_is_idempotent_for_empty_input(
        self,
        discovery: FlextPluginDiscovery,
    ) -> None:
        """Repeated empty discovery produces the same observable outcome."""
        first = discovery.discover_plugins([])
        second = discovery.discover_plugins([])

        assert first.success is second.success is True
        tm.that(list(first.unwrap()), eq=list(second.unwrap()))

    # ------------------------------------------------------------------ #
    # discover_python_plugins_in_directory — recursive walk + filters
    # ------------------------------------------------------------------ #

    def test_directory_walk_collects_non_underscore_python_files_recursively(
        self,
        logger: p.Logger,
        tmp_path: Path,
    ) -> None:
        """Walk recurses into plain packages and returns each discovered file."""
        self._make_tree(tmp_path)

        discovered = FlextPluginDiscovery.discover_python_plugins_in_directory(
            tmp_path,
            lambda item: item.stem,
            logger,
        )

        tm.that(sorted(discovered), eq=["alpha", "beta"])

    @pytest.mark.parametrize(
        ("filename", "expected_present"),
        [
            ("plain.py", True),
            ("_private.py", False),
            ("data.txt", False),
            ("README.md", False),
        ],
    )
    def test_directory_walk_filters_files_by_name_and_suffix(
        self,
        logger: p.Logger,
        tmp_path: Path,
        filename: str,
        expected_present: bool,
    ) -> None:
        """Only public ``*.py`` files reach the discover callback."""
        (tmp_path / filename).write_text("x = 1", encoding="utf-8")

        discovered = FlextPluginDiscovery.discover_python_plugins_in_directory(
            tmp_path,
            lambda item: item.name,
            logger,
        )

        assert (filename in discovered) is expected_present

    def test_directory_walk_skips_dunder_directories(
        self,
        logger: p.Logger,
        tmp_path: Path,
    ) -> None:
        """Files inside ``__dunder__`` directories are not descended into."""
        dunder = tmp_path / "__cache__"
        dunder.mkdir()
        (dunder / "hidden.py").write_text("x = 1", encoding="utf-8")

        discovered = FlextPluginDiscovery.discover_python_plugins_in_directory(
            tmp_path,
            lambda item: item.stem,
            logger,
        )

        tm.that(list(discovered), eq=[])

    def test_directory_walk_returns_empty_for_missing_directory(
        self,
        logger: p.Logger,
        tmp_path: Path,
    ) -> None:
        """An unreadable/missing directory yields an empty result, not a raise."""
        discovered = FlextPluginDiscovery.discover_python_plugins_in_directory(
            tmp_path / "does-not-exist",
            lambda item: item.stem,
            logger,
        )

        tm.that(list(discovered), eq=[])

    def test_directory_walk_drops_none_from_callback(
        self,
        logger: p.Logger,
        tmp_path: Path,
    ) -> None:
        """A callback returning ``None`` contributes nothing to the result."""
        (tmp_path / "alpha.py").write_text("x = 1", encoding="utf-8")
        (tmp_path / "beta.py").write_text("x = 1", encoding="utf-8")

        discovered = FlextPluginDiscovery.discover_python_plugins_in_directory(
            tmp_path,
            lambda item: item.stem if item.stem == "alpha" else None,
            logger,
        )

        tm.that(list(discovered), eq=["alpha"])

    # ------------------------------------------------------------------ #
    # Strategy contract — both concrete strategies honor r[Sequence]
    # ------------------------------------------------------------------ #

    def test_filesystem_strategy_empty_paths_succeeds_empty(
        self,
        logger: p.Logger,
    ) -> None:
        """File-system strategy with no paths succeeds with an empty sequence."""
        strategy = FlextPluginDiscovery.FileSystemStrategy(logger)

        result = strategy.discover([])

        tm.that(result.success, eq=True)
        tm.that(list(result.unwrap()), eq=[])

    def test_filesystem_strategy_ignores_blank_path_entries(
        self,
        logger: p.Logger,
    ) -> None:
        """Blank path strings are skipped rather than treated as the cwd."""
        strategy = FlextPluginDiscovery.FileSystemStrategy(logger)

        result = strategy.discover(["   "])

        tm.that(result.success, eq=True)
        tm.that(list(result.unwrap()), eq=[])

    def test_entry_point_strategy_returns_success_sequence(
        self,
        logger: p.Logger,
    ) -> None:
        """Entry-point strategy always succeeds with a sequence value."""
        strategy = FlextPluginDiscovery.EntryPointStrategy(logger)

        result = strategy.discover([])

        tm.that(result.success, eq=True)
        tm.that(list(result.unwrap()), eq=list(result.unwrap()))

    def test_entry_point_strategy_ignores_supplied_paths(
        self,
        logger: p.Logger,
    ) -> None:
        """Entry-point discovery ignores paths: same output regardless of input."""
        strategy = FlextPluginDiscovery.EntryPointStrategy(logger)

        with_paths: t.StrSequence = ["some/path", "another"]
        ignored = strategy.discover(with_paths)
        empty = strategy.discover([])

        assert ignored.success is empty.success is True
        tm.that(list(ignored.unwrap()), eq=list(empty.unwrap()))
