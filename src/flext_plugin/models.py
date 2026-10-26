# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Plugin Models - public facade composing from _models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import m, m as flext_cli_m

from flext_plugin._models import (
    FlextPluginConfigModels,
    FlextPluginModelsBase,
    FlextPluginModelsPlugin,
)


class FlextPluginModels(flext_cli_m):
    """Plugin domain models extending flext-cli patterns via MRO.

    Provides standardized models for all plugin operations including plugin
    entities, configurations, execution results, and monitoring data.

    All models inherit flext-core validation and patterns following
    Railway-Oriented Programming with r[T] error handling.

    """

    class Plugin(
        FlextPluginModelsBase, FlextPluginConfigModels, FlextPluginModelsPlugin
    ):
        """Plugin domain models namespace composed via MRO."""


m = FlextPluginModels
__all__: list[str] = ["FlextPluginModels", "m"]
