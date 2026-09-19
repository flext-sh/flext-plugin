"""FLEXT Plugin Constants - public facade re-exporting from _constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import c as cli_c

from ._constants import (
    FlextPluginConstantsBase,
    FlextPluginConstantsConfig,
    FlextPluginConstantsPlugin,
)


class FlextPluginConstants(cli_c):
    """FlextPlugin domain constants extending FlextCliConstants via MRO."""

    class Plugin(
        FlextPluginConstantsBase, FlextPluginConstantsConfig, FlextPluginConstantsPlugin
    ):
        """Plugin domain constants namespace."""


c = FlextPluginConstants

__all__: list[str] = ["FlextPluginConstants", "c"]
