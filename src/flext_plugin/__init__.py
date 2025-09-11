"""FLEXT Plugin System - Enterprise-grade plugin management for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes

# Import all from each module following flext-core pattern
from flext_plugin.__version__ import *
from flext_plugin.cli import *
from flext_plugin.discovery import *
from flext_plugin.entities import *
from flext_plugin.exceptions import *
from flext_plugin.fields import *
from flext_plugin.flext_plugin_constants import *
from flext_plugin.flext_plugin_handlers import *
from flext_plugin.flext_plugin_models import *
from flext_plugin.flext_plugin_platform import *
from flext_plugin.flext_plugin_services import *
from flext_plugin.flext_plugin_types import *
from flext_plugin.handlers import *  # Legacy facade
from flext_plugin.hot_reload import *
from flext_plugin.implementations import *
from flext_plugin.legacy import *
from flext_plugin.loader import *
from flext_plugin.models import *  # Legacy facade
from flext_plugin.ports import *
from flext_plugin.real_adapters import *
from flext_plugin.services import *  # Legacy facade
from flext_plugin.simple_api import *
from flext_plugin.simple_plugin import *
from flext_plugin.type_definitions import *
from flext_plugin.typings import *

# Note: __all__ is constructed dynamically at runtime from imported modules
# This pattern is necessary for library aggregation but causes pyright warnings
__all__: FlextTypes.Core.StringList = []
