"""FlextPluginConfig — frozen config singleton for flext-plugin (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Plugin:`` key and
are exposed through the open ``config.Plugin`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Plugin.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliConfig, m


class _PluginNamespace(m.BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = m.ConfigDict(extra="allow", frozen=True)


class FlextPluginConfig(FlextCliConfig):
    """Plugin config auto-loaded model-less from ``config/*.yaml``."""

    Plugin: _PluginNamespace = _PluginNamespace()


config: FlextPluginConfig = FlextPluginConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_plugin import config``."""

__all__: list[str] = ["FlextPluginConfig", "config"]
