"""Behavioral contract tests for the shipped example scripts.

The examples under ``examples/`` are executable documentation. Their public
contract is: running them terminates successfully (exit code 0) and emits no
runtime error to stderr. These tests exercise that contract end-to-end through
the process boundary, asserting only observable outcomes (exit code, stderr
cleanliness, stdout content) — never internal implementation details.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from flext_tests import tm

from tests import u

__all__ = ["TestsFlextPluginExamples"]


def _examples_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "examples"


class TestsFlextPluginExamples:
    """Observable contract of the example scripts run as processes."""

    @pytest.mark.parametrize(
        ("script", "args"),
        [
            pytest.param("01_basic_plugin.py", (), id="basic-plugin"),
            pytest.param("02_plugin_configuration.py", (), id="plugin-configuration"),
            pytest.param(
                "03_docker_integration.py", ("run",), id="docker-integration-run"
            ),
        ],
    )
    def test_example_script_runs_to_success(
        self, script: str, args: tuple[str, ...]
    ) -> None:
        """Each example exits 0 and emits no traceback to stderr."""
        example_path = _examples_dir() / script
        result = u.Cli.run_raw(
            [sys.executable, str(example_path), *args],
            cwd=_examples_dir().parent,
        )

        tm.ok(result)
        output = result.value
        tm.that(output.exit_code, eq=0)
        tm.that(output.stderr, lacks="Traceback (most recent call last)")

    def test_unknown_example_path_fails_with_nonzero_exit(self) -> None:
        """Running a non-existent example surfaces a failure, not silent success."""
        missing_path = _examples_dir() / "does_not_exist.py"
        result = u.Cli.run_raw(
            [sys.executable, str(missing_path)],
            cwd=_examples_dir().parent,
        )

        tm.ok(result)
        tm.that(result.value.exit_code, ne=0)

    def test_docker_integration_reports_service_connectivity(self) -> None:
        """With connection testing, the docker example prints a connectivity report."""
        example_path = _examples_dir() / "03_docker_integration.py"
        result = u.Cli.run_raw(
            [sys.executable, str(example_path), "run", "--test-connections"],
            cwd=_examples_dir().parent,
        )

        tm.ok(result)
        tm.that(result.value.exit_code, eq=0)
        output = result.value.stdout
        tm.that(output, has="Service Connectivity Check")
        assert "Available" in output or "Unavailable" in output
        tm.that(output, lacks="Skipped")
