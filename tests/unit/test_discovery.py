"""Behavioral test suite for the plugin discovery public contract.

Exercises the observable contract of ``u.Plugin.Discovery`` (return values,
``r[T]`` outcomes, and public model state) without touching private
attributes, internal collaborators, or line-coverage pokes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from flext_plugin import u
from flext_plugin._utilities.discovery import FlextPluginDiscovery
from tests import c

if TYPE_CHECKING:
    from collections.abc import Generator

__all__: list[str] = ["TestsFlextPluginDiscovery"]


class TestsFlextPluginDiscovery:
    """Behavioral tests for the plugin discovery public contract."""

    @pytest.fixture
    def discovery(self) -> FlextPluginDiscovery:
        """Provide a fresh discovery instance."""
        return FlextPluginDiscovery()

    @pytest.fixture
    def plugin_tree(self) -> Generator[Path]:
        """Create a directory tree with two plugin files and ignored entries."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "alpha_plugin.py").write_text("PLUGIN = 'alpha'\n")
            (root / "beta_plugin.py").write_text("PLUGIN = 'beta'\n")
            # Underscore-prefixed and non-.py files must be ignored.
            (root / "_private.py").write_text("hidden = True\n")
            (root / "readme.txt").write_text("not a plugin\n")
            yield root

    # ------------------------------------------------------------------ #
    # discover_plugins                                                    #
    # ------------------------------------------------------------------ #

    def test_discover_plugins_empty_paths_succeeds_with_empty_result(
        self,
        discovery: FlextPluginDiscovery,
    ) -> None:
        """Empty path list yields a successful, empty discovery."""
        result = discovery.discover_plugins(paths=[])

        tm.ok(result)
        tm.that(list(result.unwrap()), eq=[])

    def test_discover_plugins_nonexistent_path_succeeds_without_files(
        self,
        discovery: FlextPluginDiscovery,
    ) -> None:
        """A nonexistent path contributes no filesystem plugins."""
        result = discovery.discover_plugins(paths=["/nonexistent/path"])

        tm.ok(result)
        names = {data.name for data in result.unwrap()}
        tm.that(names, lacks="path")

    def test_discover_plugins_finds_python_files_in_directory(
        self,
        discovery: FlextPluginDiscovery,
        plugin_tree: Path,
    ) -> None:
        """All public ``.py`` files under a directory are discovered."""
        result = discovery.discover_plugins(paths=[str(plugin_tree)])

        tm.ok(result)
        names = {data.name for data in result.unwrap()}
        assert {"alpha_plugin", "beta_plugin"} <= names

    def test_discover_plugins_ignores_private_and_non_python_files(
        self,
        discovery: FlextPluginDiscovery,
        plugin_tree: Path,
    ) -> None:
        """Underscore-prefixed and non-``.py`` entries are excluded."""
        result = discovery.discover_plugins(paths=[str(plugin_tree)])

        names = {data.name for data in result.unwrap()}
        tm.that(names, lacks="_private")
        tm.that(names, lacks="readme")

    def test_discover_plugins_populates_public_model_state(
        self,
        discovery: FlextPluginDiscovery,
        plugin_tree: Path,
    ) -> None:
        """Discovered filesystem plugins expose the documented field values."""
        result = discovery.discover_plugins(paths=[str(plugin_tree)])

        found = {
            data.name: data
            for data in result.unwrap()
            if data.name in {"alpha_plugin", "beta_plugin"}
        }
        alpha = found["alpha_plugin"]
        tm.that(alpha.version, eq=c.Plugin.DEFAULT_PLUGIN_VERSION)
        tm.that(alpha.discovery_type, eq=c.Plugin.DiscoveryTypeLiteral.FILE)
        tm.that(alpha.discovery_method, eq=c.Plugin.DiscoveryMethodLiteral.FILE_SYSTEM)
        tm.that(alpha.path.name, eq="alpha_plugin.py")

    def test_discover_plugins_deduplicates_repeated_paths(
        self,
        discovery: FlextPluginDiscovery,
        plugin_tree: Path,
    ) -> None:
        """Passing the same path twice does not yield duplicate plugin names."""
        result = discovery.discover_plugins(
            paths=[str(plugin_tree), str(plugin_tree)],
        )

        discovered = [
            data.name
            for data in result.unwrap()
            if data.name in {"alpha_plugin", "beta_plugin"}
        ]
        tm.that(sorted(discovered), eq=["alpha_plugin", "beta_plugin"])

    # ------------------------------------------------------------------ #
    # discover_plugin                                                     #
    # ------------------------------------------------------------------ #

    def test_discover_plugin_nonexistent_returns_failure(
        self,
        discovery: FlextPluginDiscovery,
    ) -> None:
        """Discovering an absent plugin fails with a descriptive error."""
        result = discovery.discover_plugin(plugin_path="/nonexistent/plugin")

        tm.fail(result)
        tm.that(str(result.error), has="/nonexistent/plugin")

    def test_discover_plugin_existing_file_returns_data(
        self,
        discovery: FlextPluginDiscovery,
        plugin_tree: Path,
    ) -> None:
        """A real plugin file resolves to populated discovery data."""
        result = discovery.discover_plugin(
            plugin_path=str(plugin_tree / "alpha_plugin.py"),
        )

        tm.ok(result)
        data = result.unwrap()
        tm.that(data.name, eq="alpha_plugin")
        tm.that(data.discovery_type, eq=c.Plugin.DiscoveryTypeLiteral.FILE)

    # ------------------------------------------------------------------ #
    # validate_plugin                                                     #
    # ------------------------------------------------------------------ #

    def test_validate_plugin_accepts_discovered_data(
        self,
        discovery: FlextPluginDiscovery,
        plugin_tree: Path,
    ) -> None:
        """Validation of a genuinely discovered plugin succeeds with ``True``."""
        discovered = discovery.discover_plugin(
            plugin_path=str(plugin_tree / "alpha_plugin.py"),
        ).unwrap()

        result = discovery.validate_plugin(plugin_data=discovered)

        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    # ------------------------------------------------------------------ #
    # discover_python_plugins_in_directory                                #
    # ------------------------------------------------------------------ #

    def test_directory_scan_collects_only_public_python_files(
        self,
        plugin_tree: Path,
    ) -> None:
        """The recursive scanner returns one entry per public ``.py`` file."""
        seen: list[str] = []

        def collect(path: Path) -> str | None:
            seen.append(path.name)
            return path.stem

        results = FlextPluginDiscovery.discover_python_plugins_in_directory(
            plugin_tree,
            collect,
            u.fetch_logger(__name__),
        )

        tm.that(set(results), eq=frozenset({"alpha_plugin", "beta_plugin"}))
        tm.that(seen, lacks="_private.py")
        tm.that(seen, lacks="readme.txt")
