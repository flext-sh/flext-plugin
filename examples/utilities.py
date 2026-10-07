"""Utility functions for flextplugin.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

# Why: FlextPluginUtilities is owned by flext_plugin, not flext_core (pyrefly).


if TYPE_CHECKING:
    from flext_plugin.utilities import FlextPluginUtilities

    ExamplesFlextPluginUtilities = FlextPluginUtilities


def __getattr__(name: str) -> object:
    """Lazily expose the flext_plugin utilities under the example alias.

    Args:
        name: Requested module attribute name.

    Returns:
        The requested exported object.

    Raises:
        AttributeError: If the name is not an exported alias.

    """
    if name == "ExamplesFlextPluginUtilities":
        module = importlib.import_module("flext_plugin.utilities")
        return module.FlextPluginUtilities
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


__all__: list[str] = ["ExamplesFlextPluginUtilities"]
