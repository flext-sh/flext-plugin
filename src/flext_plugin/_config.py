"""FlextPluginConfig — frozen, validated config singleton for flext-plugin.

Every ``config/*.yaml`` file is auto-discovered and deep-merged at first
``fetch_global`` call (model-less, ``extra=allow`` at the FlextCliConfig base).
The flat YAML is then validated into the pure-Pydantic ``_models.config``
shapes and exposed as typed domain objects under ``config.Plugin`` — never a
model-less dict subscript.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import ClassVar

from flext_cli import FlextCliConfig
from flext_plugin._models.config import FlextPluginConfigModels


class FlextPluginConfig(FlextCliConfig):
    """Plugin config auto-loaded from ``config/*.yaml`` and validated via models."""

    CONFIG_DIR: ClassVar[str] = str(Path(__file__).resolve().parents[2] / "config")

    @cached_property
    def Plugin(self) -> FlextPluginConfigModels.Plugin:
        """Validated ``Plugin`` business-rule config namespace."""
        root = FlextPluginConfigModels.Root.model_validate(dict(self.model_extra or {}))
        return root.Plugin


config: FlextPluginConfig = FlextPluginConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_plugin import config``."""

__all__: list[str] = ["FlextPluginConfig", "config"]
