"""FLEXT Plugin Models - public facade composing from _models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import m as cli_m

from ._models import FlextPluginModelsInternal


class FlextPluginModels(cli_m, FlextPluginModelsInternal):
    """Plugin domain models extending flext-core patterns via MRO.

    Provides standardized models for all plugin operations including plugin
    entities, configurations, execution results, and monitoring data.

    All models inherit flext-core validation and patterns following
    Railway-Oriented Programming with r[T] error handling.
    """

    class Plugin(FlextPluginModelsInternal.Plugin):
        """Plugin domain namespace."""


m = FlextPluginModels

__all__: list[str] = ["FlextPluginModels", "m"]
