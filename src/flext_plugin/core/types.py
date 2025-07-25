"""FLEXT Plugin Core Types - Core plugin type definitions.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Core type definitions for the plugin system.
"""

from __future__ import annotations

from enum import Enum


class PluginType(Enum):
    """Plugin type enumeration."""

    # Plugin architecture types
    EXTENSION = "extension"
    SERVICE = "service"
    MIDDLEWARE = "middleware"
    TRANSFORMER = "transformer"

    # Plugin integration types
    API = "api"
    DATABASE = "database"
    NOTIFICATION = "notification"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"

    # Plugin utility types
    UTILITY = "utility"
    TOOL = "tool"
    HANDLER = "handler"
    PROCESSOR = "processor"

    # Plugin system types
    CORE = "core"
    ADDON = "addon"
    THEME = "theme"
    LANGUAGE = "language"


__all__ = [
    "PluginType",
]
