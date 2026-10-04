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
from typing import Self

from flext_cli import FlextCliConfig

from flext_core import FlextSettings
from flext_plugin._models.config import FlextPluginConfigModels


class FlextPluginConfig(FlextSettings, FlextCliConfig):
    """Plugin config auto-loaded from ``config/*.yaml`` and validated via models.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton.
    """

    # ENFORCE-042 namespace-holder contract: ``FlextSettings`` contributes
    # namespacing only — instance machinery stays plain object semantics so the
    # settings singleton ``__new__`` cannot leak into the config singleton.
    # The inherited pydantic ``__init__`` still runs the frozen, YAML-validated
    # construction, and the inherited pydantic ``__setattr__`` keeps the frozen
    # guard.
    def __new__(cls, *args: object, **kwargs: object) -> Self:
        _ = args, kwargs
        return object.__new__(cls)

    __eq__ = object.__eq__

    __hash__ = object.__hash__

    @cached_property
    def Plugin(self) -> FlextPluginConfigModels.Plugin:
        """Validated ``Plugin`` business-rule config namespace."""
        root = FlextPluginConfigModels.Root.model_validate(dict(self.model_extra or {}))
        return root.Plugin


config: FlextPluginConfig = FlextPluginConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_plugin import config``."""

__all__: list[str] = ["FlextPluginConfig", "config"]
