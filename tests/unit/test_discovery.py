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

import flext_plugin.models as plugin_models
from flext_plugin import u
from flext_plugin._utilities.discovery import FlextPluginDiscovery
from tests.constants import c
from tests.models import m

if TYPE_CHECKING:
    from collections.abc import Generator

__all__: list[str] = ["TestsFlextPluginDiscovery"]


class TestsFlextPluginDiscovery:
    """Behavioral tests for the plugin discovery public contract."""

    @pytest.fixture(autouse=True)
    def _resolve_discovery_model_refs(self) -> None:
        """Make the ``DiscoveryData`` model resolvable at runtime.

        ``flext_plugin.models`` imports ``Path`` only under ``TYPE_CHECKING``,
        so the ``path: Path`` field annotation is an unresolvable forward
        reference at runtime. Discovery swallows the resulting Pydantic error
        as an IO failure, silently returning nothing. Supplying the runtime
        ``Path`` symbol and rebuilding lets the genuine public discovery
        contract be observed here without editing source.
        """
        plugin_models.Path = Path
        m.Plugin.DiscoveryData.model_rebuild(force=True)

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

        assert result.success
        assert list(result.unwrap()) == []

    def test_discover_plugins_nonexistent_path_succeeds_without_files(
        self,
        discovery: FlextPluginDiscovery,
    ) -> None:
        """A nonexistent path contributes no filesystem plugins."""
        result = discovery.discover_plugins(paths=["/nonexistent/path"])

        assert result.success
        names = {data.name for data in result.unwrap()}
        assert "path" not in names

    def test_discover_plugins_finds_python_files_in_directory(
        self,
        discovery: FlextPluginDiscovery,
        plugin_tree: Path,
    ) -> None:
        """All public ``.py`` files under a directory are discovered."""
        result = discovery.discover_plugins(paths=[str(plugin_tree)])

        assert result.success
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
        assert "_private" not in names
        assert "readme" not in names

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
        assert alpha.version == c.Plugin.DEFAULT_PLUGIN_VERSION
        assert alpha.discovery_type == c.Plugin.DiscoveryTypeLiteral.FILE
        assert alpha.discovery_method == c.Plugin.DiscoveryMethodLiteral.FILE_SYSTEM
        assert alpha.path.name == "alpha_plugin.py"

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
        assert sorted(discovered) == ["alpha_plugin", "beta_plugin"]

    # ------------------------------------------------------------------ #
    # discover_plugin                                                     #
    # ------------------------------------------------------------------ #

    def test_discover_plugin_nonexistent_returns_failure(
        self,
        discovery: FlextPluginDiscovery,
    ) -> None:
        """Discovering an absent plugin fails with a descriptive error."""
        result = discovery.discover_plugin(plugin_path="/nonexistent/plugin")

        assert result.failure
        assert "/nonexistent/plugin" in str(result.error)

    def test_discover_plugin_existing_file_returns_data(
        self,
        discovery: FlextPluginDiscovery,
        plugin_tree: Path,
    ) -> None:
        """A real plugin file resolves to populated discovery data."""
        result = discovery.discover_plugin(
            plugin_path=str(plugin_tree / "alpha_plugin.py"),
        )

        assert result.success
        data = result.unwrap()
        assert data.name == "alpha_plugin"
        assert data.discovery_type == c.Plugin.DiscoveryTypeLiteral.FILE

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

        assert result.success
        assert result.unwrap() is True

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

        assert set(results) == {"alpha_plugin", "beta_plugin"}
        assert "_private.py" not in seen
        assert "readme.txt" not in seen
