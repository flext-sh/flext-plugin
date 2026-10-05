"""FlextPluginConfig — frozen, validated config singleton for flext-plugin.

Every ``config/*.yaml`` file is auto-discovered and deep-merged at first
``fetch_global`` call. The ``Plugin:`` YAML section is validated at
construction into the pure-Pydantic ``_models.config`` shape and exposed as
the typed ``config.Plugin`` namespace — never a model-less dict subscript.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Self

from flext_cli import FlextCliConfig
from pydantic import Field

from flext_core import FlextSettings
from flext_plugin._models.config import FlextPluginConfigModels


class FlextPluginConfig(FlextSettings, FlextCliConfig):
    """Plugin config auto-loaded from ``config/*.yaml`` and validated via models.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton. ``Plugin`` follows the family
    Field-namespace form (flext-auth ``config.Auth``): pydantic-settings
    validates the YAML section into the typed model at construction — no lazy
    cached_property, no PascalCase accessor method.
    """

    Plugin: Annotated[
        FlextPluginConfigModels.Plugin,
        Field(
            default_factory=FlextPluginConfigModels.Plugin,
            description="Plugin business-rule config namespace.",
        ),
    ]

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


config: FlextPluginConfig = FlextPluginConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_plugin import config``."""

__all__: list[str] = ["FlextPluginConfig", "config"]
