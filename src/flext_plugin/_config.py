"""FlextPluginConfig — frozen, validated config singleton for flext-plugin.

The business rules in ``config/plugin.yaml`` are validated at construction
and exposed under ``config.Plugin``. The distribution projects that same
authored YAML into the installed package's config directory.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Self

from flext_cli import FlextCliConfig, u

from flext_core import FlextSettings
from flext_plugin._models.config import FlextPluginConfigModels


class FlextPluginConfig(FlextSettings, FlextCliConfig):
    """Plugin config auto-loaded from ``config/*.yaml`` and validated via models.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton.
    """

    CONFIG_FILENAMES: ClassVar[tuple[str, ...]] = ("plugin.yaml",)

    Plugin: FlextPluginConfigModels.Plugin = u.Field(
        description="Validated plugin business-rule config namespace.",
    )

    # Preserve the canonical generated allocation contract while inherited
    # Pydantic construction validates the declared namespace.
    def __new__(cls, *args: object, **kwargs: object) -> Self:
        _ = args, kwargs
        return object.__new__(cls)

    def __eq__(self, other: object) -> bool:
        """Identity equality per the frozen-config singleton contract.

        Returns:
            The resulting ``bool``.
        """
        return object.__eq__(self, other)

    def __hash__(self) -> int:
        """Identity hash per the frozen-config singleton contract.

        Returns:
            The resulting ``int``.
        """
        return object.__hash__(self)


config: FlextPluginConfig = FlextPluginConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_plugin import config``."""

__all__: list[str] = ["FlextPluginConfig", "config"]
