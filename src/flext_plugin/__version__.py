# AUTO-GENERATED FILE — Regenerate with: make gen
"""Package version and metadata for flext-plugin.

Subclass of ``FlextVersion`` — overrides only ``_metadata``.
All derived attributes (``__version__``, ``__title__``, etc.) are
computed automatically via ``FlextVersion.__init_subclass__``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from importlib.metadata import PackageMetadata, metadata

from flext_core import FlextVersion


class FlextPluginVersion(FlextVersion):
    """flext-plugin version — MRO-derived from FlextVersion."""

    _metadata: PackageMetadata | Mapping[str, str] = metadata("flext-plugin")


__version__ = FlextPluginVersion.__version__
__version_info__ = FlextPluginVersion.__version_info__
__title__ = FlextPluginVersion.__title__
__description__ = FlextPluginVersion.__description__
__author__ = FlextPluginVersion.__author__
__author_email__ = FlextPluginVersion.__author_email__
__license__ = FlextPluginVersion.__license__
__url__ = FlextPluginVersion.__url__
__all__: list[str] = [
    "FlextPluginVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
]
