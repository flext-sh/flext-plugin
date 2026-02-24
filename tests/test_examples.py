"""Test suite for examples to ensure they work correctly.

These tests verify that example scripts execute successfully via subprocess.
Source examples are truth — tests only verify exit code 0 and no stderr errors.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


def test_basic_plugin_example_execution() -> None:
    """Test that basic_plugin_example.py runs successfully without errors."""
    example_path = Path(__file__).parent.parent / "examples" / "01_basic_plugin.py"

    # Execute the example script
    result = subprocess.run(
        [sys.executable, str(example_path)],
        check=False,
        cwd=str(Path(__file__).parent.parent),
        capture_output=True,
        text=True,
    )

    # Verify successful execution
    assert result.returncode == 0, f"Example failed with error: {result.stderr}"


def test_plugin_configuration_example_execution() -> None:
    """Test that plugin_configuration_example.py runs successfully without errors."""
    example_path = (
        Path(__file__).parent.parent / "examples" / "02_plugin_configuration.py"
    )

    # Execute the example script
    result = subprocess.run(
        [sys.executable, str(example_path)],
        check=False,
        cwd=str(Path(__file__).parent.parent),
        capture_output=True,
        text=True,
    )

    # Verify successful execution
    assert result.returncode == 0, (
        f"Configuration example failed with error: {result.stderr}"
    )


def test_docker_integration_example_execution() -> None:
    """Test that 03_docker_integration.py runs successfully without errors."""
    example_path = (
        Path(__file__).parent.parent / "examples" / "03_docker_integration.py"
    )

    # Execute the example script
    result = subprocess.run(
        [sys.executable, str(example_path)],
        check=False,
        cwd=str(Path(__file__).parent.parent),
        capture_output=True,
        text=True,
    )

    # Verify successful execution
    assert result.returncode == 0, (
        f"Docker integration example failed with error: {result.stderr}"
    )


@pytest.mark.skip(reason="Requires Docker services to be running")
def test_docker_integration_example_with_connection_testing() -> None:
    """Test docker integration example with connection testing enabled."""
    example_path = (
        Path(__file__).parent.parent / "examples" / "03_docker_integration.py"
    )

    # Execute the example script with connection testing
    result = subprocess.run(
        [sys.executable, str(example_path), "--test-connections"],
        check=False,
        cwd=str(Path(__file__).parent.parent),
        capture_output=True,
        text=True,
    )

    # Verify successful execution
    assert result.returncode == 0, (
        f"Docker integration example with connections failed: {result.stderr}"
    )

    # Verify connection testing output appears
    output = result.stdout
    assert "Service Connectivity Check" in output
    # Should show either Available or Unavailable (not Skipped)
    assert ("Available" in output) or ("Unavailable" in output)
    assert (
        "Skipped" not in output
    )  # No services should be skipped with --test-connections
