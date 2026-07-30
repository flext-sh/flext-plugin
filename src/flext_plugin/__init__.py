# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Plugin package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from flext_cli import d as d
    from flext_cli import e as e
    from flext_cli import h as h
    from flext_cli import r as r
    from flext_cli import s as s
    from flext_cli import x as x

    from ._config import FlextPluginConfig as FlextPluginConfig
    from ._config import config as config
    from ._settings import FlextPluginSettings as FlextPluginSettings
    from ._settings import settings as settings
    from .api import FlextPluginApi as FlextPluginApi
    from .api import plugin as plugin
    from .constants import FlextPluginConstants as FlextPluginConstants

    c: type[FlextPluginConstants]
    from .models import FlextPluginModels as FlextPluginModels

    m: type[FlextPluginModels]
    from .protocols import FlextPluginProtocols as FlextPluginProtocols

    p: type[FlextPluginProtocols]
    from .typings import FlextPluginTypes as FlextPluginTypes

    t: type[FlextPluginTypes]
    from .utilities import FlextPluginUtilities as FlextPluginUtilities

    u: type[FlextPluginUtilities]

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextPluginConfig", "config"),
    "._settings": ("FlextPluginSettings", "settings"),
    ".api": ("FlextPluginApi", "plugin"),
    ".constants": ("FlextPluginConstants", "c"),
    ".models": ("FlextPluginModels", "m"),
    ".protocols": ("FlextPluginProtocols", "p"),
    ".typings": ("FlextPluginTypes", "t"),
    ".utilities": ("FlextPluginUtilities", "u"),
    "flext_cli": ("d", "e", "h", "r", "s", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextPluginApi",
    "FlextPluginConfig",
    "FlextPluginConstants",
    "FlextPluginModels",
    "FlextPluginProtocols",
    "FlextPluginSettings",
    "FlextPluginTypes",
    "FlextPluginUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "p",
    "plugin",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
