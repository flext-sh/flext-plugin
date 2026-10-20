"""Behavioral contract tests for the shipped example scripts.

The examples under ``examples/`` are executable documentation. Their public
contract is: running them terminates successfully (exit code 0) and emits no
runtime error to stderr. These tests exercise that contract end-to-end through
the process boundary, asserting only observable outcomes (exit code, stderr
cleanliness, stdout content) — never internal implementation details.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from tests import m, t, tm, u


def _examples_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "examples"


class TestsFlextPluginExamples:
    """Observable contract of the example scripts run as processes."""

    @staticmethod
    @pytest.mark.parametrize(
        ("module", "args"),
        [
            pytest.param("examples.basic_plugin", (), id="basic-plugin"),
            pytest.param(
                "examples.plugin_configuration",
                (),
                id="plugin-configuration",
            ),
            pytest.param(
                "examples.docker_integration",
                ("run",),
                id="docker-integration-run",
            ),
        ],
    )
    def test_example_script_runs_to_success(
        module: str,
        args: t.VariadicTuple[str],
    ) -> None:
        """Each example exits 0 and emits no traceback to stderr."""
        result = u.Cli.run_raw(
            [sys.executable, "-m", module, *args],
            cwd=_examples_dir().parent,
            options=m.Cli.ProcessOptions(remove_env_keys=("PYTHONPATH",)),
        )

        tm.ok(result)
        output = result.value
        tm.ok(u.Cli.process_succeeded(output.outcome))
        tm.that(output.stderr, lacks="Traceback (most recent call last)")

    @staticmethod
    def test_unknown_example_path_fails_with_nonzero_exit() -> None:
        """Running a non-existent example surfaces a failure, not silent success."""
        missing_path = _examples_dir() / "does_not_exist.py"
        result = u.Cli.run_raw(
            [sys.executable, str(missing_path)],
            cwd=_examples_dir().parent,
        )

        tm.ok(result)
        tm.that(result.value.outcome.raw_return_code, ne=0)

    @staticmethod
    def test_docker_integration_reports_service_connectivity() -> None:
        """With connection testing, the docker example prints a connectivity report."""
        result = u.Cli.run_raw(
            [
                sys.executable,
                "-m",
                "examples.docker_integration",
                "run",
                "--test-connections",
            ],
            cwd=_examples_dir().parent,
            options=m.Cli.ProcessOptions(remove_env_keys=("PYTHONPATH",)),
        )

        tm.ok(result)
        tm.ok(u.Cli.process_succeeded(result.value.outcome))
        output = result.value.stdout
        tm.that(output, has="Service Connectivity Check")
        assert "Available" in output or "Unavailable" in output
        tm.that(output, lacks="Skipped")
