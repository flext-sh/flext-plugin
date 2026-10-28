"""CLI facade for flext-plugin — thin transport adapter.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence

from flext_cli.services.cli import FlextCliCli


class FlextPluginCli(FlextCliCli):
    """Flext-plugin CLI facade — extends flext-cli CLI."""


def main(args: Sequence[str] | None = None) -> int:
    """Console-script entry point — commands are not implemented yet.

    Args:
        args: Command-line arguments; accepted but currently ignored.

    Returns:
        Process exit code; always ``0`` until commands are implemented.

    """
    _ = args
    return 0


__all__: tuple[str, ...] = ("FlextPluginCli", "main")
