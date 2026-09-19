"""FLEXT Plugin Constants - public facade re-exporting from _constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import c as cli_c

from ._constants import (
    FlextPluginConstantsApi,
    FlextPluginConstantsBase,
    FlextPluginConstantsConfig,
    FlextPluginConstantsPlugin,
)


class FlextPluginConstantsFacade(
    cli_c,
    FlextPluginConstantsBase,
    FlextPluginConstantsPlugin,
    FlextPluginConstantsApi,
    FlextPluginConstantsConfig,
):
    """Plugin constants facade composed via MRO over flext_cli and internal constants."""


c = FlextPluginConstantsFacade

__all__: list[str] = ["FlextPluginConstantsFacade", "c"]
