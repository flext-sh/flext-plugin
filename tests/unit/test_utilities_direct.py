"""Behavioral tests for plugin-specific utilities.

Exercises the public contract of ``u.Plugin`` (``FlextPluginUtilities.Plugin``):
discovery, metadata extraction, file validation, and name validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_plugin import u


class TestsFlextPluginUtilities:
    """Behavioral tests for plugin utility helpers."""

    def test_discover_plugins_fails_for_missing_directory(self) -> None:
        """discover_plugins() fails when the directory does not exist."""
        result = u.Plugin.discover_plugins("/definitely/not/a/real/path")

        assert result.failure is True
        assert "does not exist" in (result.error or "").lower()

    def test_discover_plugins_finds_python_files(self, tmp_path: Path) -> None:
        """discover_plugins() returns metadata for valid Python plugin files."""
        (tmp_path / "alpha_plugin.py").write_text(
            '"""Alpha plugin."""\n__version__ = "2.0.0"\n',
            encoding="utf-8",
        )

        result = u.Plugin.discover_plugins(tmp_path)

        assert result.success is True
        metadata_list = list(result.unwrap())
        assert len(metadata_list) == 1
        assert metadata_list[0].name == "alpha_plugin"
        assert metadata_list[0].version == "2.0.0"

    def test_discover_plugins_skips_private_files(self, tmp_path: Path) -> None:
        """discover_plugins() ignores underscore-prefixed Python files."""
        (tmp_path / "_private.py").write_text("x = 1", encoding="utf-8")
        (tmp_path / "public.py").write_text("x = 1", encoding="utf-8")

        result = u.Plugin.discover_plugins(tmp_path)

        assert result.success is True
        names = {metadata.name for metadata in result.unwrap()}
        assert "public" in names
        assert "_private" not in names

    def test_discover_plugins_skips_non_python_files(self, tmp_path: Path) -> None:
        """discover_plugins() ignores files without the .py extension."""
        (tmp_path / "readme.txt").write_text("hello", encoding="utf-8")

        result = u.Plugin.discover_plugins(tmp_path)

        assert result.success is True
        assert list(result.unwrap()) == []

    def test_extract_plugin_metadata_from_python_file(self, tmp_path: Path) -> None:
        """extract_plugin_metadata() reads version and docstring from a .py file."""
        plugin_path = tmp_path / "demo.py"
        plugin_path.write_text(
            '"""Demo plugin description."""\n__version__ = "1.2.3"\n',
            encoding="utf-8",
        )

        result = u.Plugin.extract_plugin_metadata(plugin_path)

        assert result.success is True
        metadata = result.unwrap()
        assert metadata.name == "demo"
        assert metadata.version == "1.2.3"
        assert metadata.description == "Demo plugin description."

    def test_extract_plugin_metadata_from_yaml_file(self, tmp_path: Path) -> None:
        """extract_plugin_metadata() builds metadata for non-Python files."""
        plugin_path = tmp_path / "config.yaml"
        plugin_path.write_text("key: value", encoding="utf-8")

        result = u.Plugin.extract_plugin_metadata(plugin_path)

        assert result.success is True
        metadata = result.unwrap()
        assert metadata.name == "config"
        assert metadata.plugin_type == "extension"

    def test_extract_plugin_metadata_fails_for_missing_file(self) -> None:
        """extract_plugin_metadata() fails when the file does not exist."""
        result = u.Plugin.extract_plugin_metadata(Path("/missing/file.py"))

        assert result.failure is True

    def test_validate_plugin_file_accepts_safe_python(self, tmp_path: Path) -> None:
        """validate_plugin_file() succeeds for Python files without dangerous patterns."""
        plugin_path = tmp_path / "safe.py"
        plugin_path.write_text("x = 1\n", encoding="utf-8")

        result = u.Plugin.validate_plugin_file(plugin_path)

        assert result.success is True

    def test_validate_plugin_file_rejects_dangerous_python(
        self, tmp_path: Path
    ) -> None:
        """validate_plugin_file() fails for Python files containing dangerous code."""
        plugin_path = tmp_path / "dangerous.py"
        plugin_path.write_text("exec('bad')\n", encoding="utf-8")

        result = u.Plugin.validate_plugin_file(plugin_path)

        assert result.failure is True
        assert "dangerous" in (result.error or "").lower()

    def test_validate_plugin_file_rejects_non_python(self, tmp_path: Path) -> None:
        """validate_plugin_file() returns the precheck result for non-Python files."""
        plugin_path = tmp_path / "data.yaml"
        plugin_path.write_text("key: value", encoding="utf-8")

        result = u.Plugin.validate_plugin_file(plugin_path)

        assert result.success is True

    def test_validate_plugin_file_fails_for_missing_file(self) -> None:
        """validate_plugin_file() fails when the file does not exist."""
        result = u.Plugin.validate_plugin_file(Path("/missing/file.py"))

        assert result.failure is True

    def test_validate_plugin_name_accepts_valid_name(self) -> None:
        """validate_plugin_name() succeeds for valid plugin names."""
        result = u.Plugin.validate_plugin_name("valid-plugin")

        assert result.success is True

    @pytest.mark.parametrize(
        "bad_name",
        [
            "123-invalid",
            "",
            "no spaces",
            "invalid!",
        ],
    )
    def test_validate_plugin_name_rejects_invalid_names(self, bad_name: str) -> None:
        """validate_plugin_name() fails for names violating the pattern."""
        result = u.Plugin.validate_plugin_name(bad_name)

        assert result.failure is True

    def test_validate_plugin_file_fails_for_oversized_file(
        self,
        tmp_path: Path,
    ) -> None:
        """validate_plugin_file() fails when the file exceeds the size limit."""
        plugin_path = tmp_path / "huge.py"
        plugin_path.write_text("x" * (101 * 1024 * 1024), encoding="utf-8")

        result = u.Plugin.validate_plugin_file(plugin_path)

        assert result.failure is True
        assert "too large" in (result.error or "").lower()


__all__: list[str] = ["TestsFlextPluginUtilities"]
