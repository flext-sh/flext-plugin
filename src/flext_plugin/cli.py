"""CLI facade for flext-plugin — thin transport adapter.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli.services.cli import FlextCliCli


class FlextPluginCli(FlextCliCli):
    """Flext-plugin CLI facade — extends flext-cli CLI."""


__all__: tuple[str, ...] = ("FlextPluginCli",)
