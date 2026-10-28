# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Plugin Constants - public facade re-exporting from _constants.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_cli import c as flext_cli_c

from flext_plugin._constants import (
    FlextPluginConstantsApi,
    FlextPluginConstantsBase,
    FlextPluginConstantsConfig,
    FlextPluginConstantsPlugin,
)


class FlextPluginConstants(flext_cli_c):
    """FlextPlugin domain constants extending FlextCliConstants via MRO."""

    class Plugin(
        FlextPluginConstantsApi,
        FlextPluginConstantsBase,
        FlextPluginConstantsConfig,
        FlextPluginConstantsPlugin,
    ):
        """Plugin domain constants namespace composed via MRO.

        Aggregates the API, base, configuration, and plugin constant
        shards into one resolved surface.

        """


c = FlextPluginConstants
__all__: list[str] = ["FlextPluginConstants", "c"]
