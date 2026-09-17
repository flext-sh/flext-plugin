"""FLEXT Plugin Models - public facade composing from _models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import m as cli_m

from ._models.plugin import FlextPluginModelsPlugin


class FlextPluginModels(cli_m):
    """Plugin domain models extending flext-cli patterns via MRO.

    Provides standardized models for all plugin operations including plugin
    entities, configurations, execution results, and monitoring data.

    All models inherit flext-core validation and patterns following
    Railway-Oriented Programming with r[T] error handling.
    """

    class Plugin(FlextPluginModelsPlugin):
        """Plugin domain namespace."""


m = FlextPluginModels

__all__: list[str] = ["FlextPluginModels", "m"]
