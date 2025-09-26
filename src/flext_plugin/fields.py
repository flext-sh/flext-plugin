"""Pydantic field definitions for the FLEXT Plugin system.

Centralized field definitions following flext-core patterns for
consistent validation and serialization across the plugin ecosystem.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import Field

from flext_core import FlextTypes
from flext_plugin.flext_plugin_constants import FlextPluginConstants
from flext_plugin.type_definitions import PluginConfigData

# Plugin Name Fields
PluginNameField = Annotated[
    str,
    Field(
        ...,
        min_length=FlextPluginConstants.MIN_PLUGIN_NAME_LENGTH,
        max_length=FlextPluginConstants.MAX_PLUGIN_NAME_LENGTH,
        pattern=FlextPluginConstants.VALID_PLUGIN_NAME_PATTERN,
        description="Plugin name following naming conventions",
        examples=["my_plugin", "data-extractor", "auth_service"],
    ),
]

OptionalPluginNameField = Annotated[
    str,
    Field(
        default="",
        min_length=0,
        max_length=FlextPluginConstants.MAX_PLUGIN_NAME_LENGTH,
        pattern=rf"^$|{FlextPluginConstants.VALID_PLUGIN_NAME_PATTERN}",
        description="Optional plugin name following naming conventions",
    ),
]

# Version Fields
PluginVersionField = Annotated[
    str,
    Field(
        default="1.0.0",
        pattern=r"^\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+)?$",
        description="Plugin version in semantic versioning format",
        examples=["1.0.0", "2.1.3", "1.0.0-alpha"],
    ),
]

# Description Fields
PluginDescriptionField = Annotated[
    str,
    Field(
        default="",
        max_length=500,
        description="Plugin description",
        examples=["A data extraction plugin", "Authentication service plugin"],
    ),
]

PluginLongDescriptionField = Annotated[
    str,
    Field(default="", max_length=2000, description="Detailed plugin description"),
]

# Author Fields
PluginAuthorField = Annotated[
    str,
    Field(
        default="",
        max_length=100,
        description="Plugin author name",
        examples=["John Doe", "FLEXT Team", "Data Engineering Team"],
    ),
]

# URL Fields
PluginUrlField = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"^https?://[^\s]+$",
        description="Valid HTTP/HTTPS URL",
        examples=["https://github.com/user/plugin", "https://plugin-docs.com"],
    ),
]

# Configuration Fields
PluginConfigField = Annotated[
    dict["str", "PluginConfigData"],
    Field(default_factory=dict, description="Plugin-specific configuration dictionary"),
]

PluginRuntimeDataField = Annotated[
    dict["str", "PluginConfigData"],
    Field(default_factory=dict, description="Runtime-specific data dictionary"),
]

# List Fields
PluginTagsField = Annotated[
    FlextTypes.Core.StringList,
    Field(
        default_factory=list,
        max_length=20,
        description="Plugin tags for categorization",
        examples=[["data", "extraction"], ["auth", "security"]],
    ),
]

PluginDependenciesField = Annotated[
    FlextTypes.Core.StringList,
    Field(
        default_factory=list,
        max_length=50,
        description="List of plugin dependencies",
        examples=[["auth_plugin", "db_plugin"], ["base_framework"]],
    ),
]

PluginKeywordsField = Annotated[
    FlextTypes.Core.StringList,
    Field(
        default_factory=list,
        max_length=30,
        description="Plugin keywords for search",
        examples=[["etl", "data", "pipeline"], ["authentication", "oauth"]],
    ),
]

PluginMaintainersField = Annotated[
    FlextTypes.Core.StringList,
    Field(
        default_factory=list,
        max_length=10,
        description="Plugin maintainers list",
        examples=[["john@example.com", "team@company.com"]],
    ),
]

PluginErrorsField = Annotated[
    FlextTypes.Core.StringList,
    Field(default_factory=list, description="List of error messages"),
]

PluginsAffectedField = Annotated[
    FlextTypes.Core.StringList,
    Field(default_factory=list, description="List of affected plugin names"),
]

# Boolean Fields
PluginEnabledField = Annotated[
    bool,
    Field(default=True, description="Whether the plugin is enabled"),
]

PluginAutoStartField = Annotated[
    bool,
    Field(default=False, description="Whether to automatically start the plugin"),
]

PluginSuccessField = Annotated[
    bool,
    Field(default=False, description="Whether operation/execution succeeded"),
]

# Numeric Fields
PluginTimeoutField = Annotated[
    int,
    Field(
        default=FlextPluginConstants.DEFAULT_PLUGIN_TIMEOUT_SECONDS,
        ge=1,
        le=3600,
        description="Timeout in seconds (1-3600)",
    ),
]

PluginExecutionTimeField = Annotated[
    float,
    Field(default=0.0, ge=0.0, description="Execution time in seconds"),
]

PluginExecutionTimeMsField = Annotated[
    float,
    Field(default=0.0, ge=0.0, description="Execution time in milliseconds"),
]

# Identifier Fields
PluginIdField = Annotated[
    str,
    Field(..., min_length=1, max_length=100, description="Unique plugin identifier"),
]

ExecutionIdField = Annotated[
    str,
    Field(..., min_length=1, max_length=100, description="Unique execution identifier"),
]

OperationNameField = Annotated[
    str,
    Field(..., min_length=1, max_length=50, description="Operation name"),
]

# Timestamp Fields
CreatedAtField = Annotated[
    datetime,
    Field(default_factory=datetime.now, description="Creation timestamp"),
]

UpdatedAtField = Annotated[
    datetime | None,
    Field(default=None, description="Last update timestamp"),
]

StartedAtField = Annotated[
    datetime,
    Field(default_factory=datetime.now, description="Start timestamp"),
]

CompletedAtField = Annotated[
    datetime,
    Field(default_factory=datetime.now, description="Completion timestamp"),
]

# Data Fields
InputDataField = Annotated[
    dict["str", "PluginConfigData"],
    Field(default_factory=dict, description="Input data dictionary"),
]

OutputDataField = Annotated[
    PluginConfigData,
    Field(default=None, description="Output data from execution"),
]

ContextDataField = Annotated[
    dict["str", "PluginConfigData"],
    Field(default_factory=dict, description="Context data dictionary"),
]

DetailsDataField = Annotated[
    dict["str", "PluginConfigData"],
    Field(default_factory=dict, description="Additional details dictionary"),
]

# Error Fields
ErrorMessageField = Annotated[
    str,
    Field(default="", max_length=1000, description="Error message"),
]

# License Field
PluginLicenseField = Annotated[
    str | None,
    Field(
        default=None,
        max_length=50,
        description="Plugin license identifier",
        examples=["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause"],
    ),
]

# Platform Version Fields
PlatformVersionField = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"^\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+)?$",
        description="Required platform version",
        examples=["1.0.0", "2.1.3"],
    ),
]

PythonVersionField = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"^[>=<~!^]*\d+\.\d+(?:\.\d+)?$",
        description="Required Python version constraint",
        examples=[">=3.8", "~=3.9.0", ">=3.8,<4.0"],
    ),
]

__all__ = [
    "CompletedAtField",
    "ContextDataField",
    # Timestamp Fields
    "CreatedAtField",
    "DetailsDataField",
    # Error Fields
    "ErrorMessageField",
    "ExecutionIdField",
    # Data Fields
    "InputDataField",
    "OperationNameField",
    "OptionalPluginNameField",
    "OutputDataField",
    # Platform Version Fields
    "PlatformVersionField",
    # Author Fields
    "PluginAuthorField",
    "PluginAutoStartField",
    # Configuration Fields
    "PluginConfigField",
    "PluginDependenciesField",
    # Description Fields
    "PluginDescriptionField",
    # Boolean Fields
    "PluginEnabledField",
    "PluginErrorsField",
    "PluginExecutionTimeField",
    "PluginExecutionTimeMsField",
    # Identifier Fields
    "PluginIdField",
    "PluginKeywordsField",
    # License Field
    "PluginLicenseField",
    "PluginLongDescriptionField",
    "PluginMaintainersField",
    # Name Fields
    "PluginNameField",
    "PluginRuntimeDataField",
    "PluginSuccessField",
    # List Fields
    "PluginTagsField",
    # Numeric Fields
    "PluginTimeoutField",
    # URL Fields
    "PluginUrlField",
    # Version Fields
    "PluginVersionField",
    "PluginsAffectedField",
    "PythonVersionField",
    "StartedAtField",
    "UpdatedAtField",
]
