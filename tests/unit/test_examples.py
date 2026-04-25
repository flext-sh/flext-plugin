"""Test suite for examples to ensure they work correctly.

These tests verify that example scripts execute successfully via subprocess.
Source examples are truth — tests only verify exit code 0 and no stderr errors.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from tests import u


def _examples_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "examples"


class TestsFlextPluginExamples:
    """Behavior contract for test_examples."""

    def test_basic_plugin_example_execution(self) -> None:
        """Test that basic_plugin_example.py runs successfully without errors."""
        example_path = _examples_dir() / "01_basic_plugin.py"
        result = u.Cli.run_raw(
            [sys.executable, str(example_path)],
            cwd=_examples_dir().parent,
        )
        assert result.success, result.error
        assert result.value.exit_code == 0, (
            f"Example failed with error: {result.value.stderr}"
        )

    def test_plugin_configuration_example_execution(self) -> None:
        """Test that plugin_configuration_example.py runs successfully without errors."""
        example_path = _examples_dir() / "02_plugin_configuration.py"
        result = u.Cli.run_raw(
            [sys.executable, str(example_path)],
            cwd=_examples_dir().parent,
        )
        assert result.success, result.error
        assert result.value.exit_code == 0, (
            f"Configuration example failed with error: {result.value.stderr}"
        )

    def test_docker_integration_example_execution(self) -> None:
        """Test that 03_docker_integration.py runs successfully without errors."""
        example_path = _examples_dir() / "03_docker_integration.py"
        result = u.Cli.run_raw(
            [sys.executable, str(example_path)],
            cwd=_examples_dir().parent,
        )
        assert result.success, result.error
        assert result.value.exit_code == 0, (
            f"Docker integration example failed with error: {result.value.stderr}"
        )

    @pytest.mark.skip(reason="Requires Docker services to be running")
    def test_docker_integration_example_with_connection_testing(self) -> None:
        """Test docker integration example with connection testing enabled."""
        example_path = _examples_dir() / "03_docker_integration.py"
        result = u.Cli.run_raw(
            [sys.executable, str(example_path), "--test-connections"],
            cwd=_examples_dir().parent,
        )
        assert result.success, result.error
        assert result.value.exit_code == 0, (
            f"Docker integration example with connections failed: {result.value.stderr}"
        )
        output = result.value.stdout
        assert "Service Connectivity Check" in output
        assert "Available" in output or "Unavailable" in output
        assert "Skipped" not in output
