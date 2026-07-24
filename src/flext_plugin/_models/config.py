"""flext-plugin config models — typed business-rule shapes.

Frozen Pydantic shapes for the ``config/plugin.yaml`` business-rule SSOT.
The ``_config.py`` facade validates the model-less YAML slice into these
classes and exposes the ready objects under ``config.Plugin``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FlextPluginConfigModels:
    """Namespace of typed flext-plugin config models."""

    class Version(BaseModel):
        """Plugin version defaults and validation."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        default: str = Field(description="Default plugin version string.")
        pattern: str = Field(description="Regex validating a semantic version.")

    class NameValidation(BaseModel):
        """Plugin name validation thresholds."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        min_length: int = Field(ge=1, description="Minimum plugin name length.")
        max_length: int = Field(ge=1, description="Maximum plugin name length.")
        pattern: str = Field(description="Regex validating a plugin name.")

    class DescriptionValidation(BaseModel):
        """Plugin description validation thresholds."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        max_length: int = Field(ge=1, description="Maximum plugin description length.")

    class AuthorValidation(BaseModel):
        """Plugin author validation thresholds."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        max_length: int = Field(ge=1, description="Maximum author string length.")

    class DocstringValidation(BaseModel):
        """Plugin docstring extraction rules."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        pattern: str = Field(
            description="Regex extracting the first triple-quoted docstring."
        )

    class Validation(BaseModel):
        """Plugin validation rule namespace."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        name: FlextPluginConfigModels.NameValidation = Field(
            description="Plugin name validation thresholds."
        )
        description: FlextPluginConfigModels.DescriptionValidation = Field(
            description="Plugin description validation thresholds."
        )
        author: FlextPluginConfigModels.AuthorValidation = Field(
            description="Plugin author validation thresholds."
        )
        docstring: FlextPluginConfigModels.DocstringValidation = Field(
            description="Plugin docstring extraction rules."
        )

    class Files(BaseModel):
        """Plugin file and directory defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        python_extension: str = Field(description="Python source file extension.")
        yaml_extension: str = Field(description="YAML file extension.")
        json_extension: str = Field(description="JSON file extension.")
        toml_extension: str = Field(description="TOML file extension.")
        default_plugin_dir: str = Field(description="Default plugin directory.")
        default_cache_dir: str = Field(description="Default plugin cache directory.")

    class Plugin(BaseModel):
        """Root plugin business-rule namespace."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        version: FlextPluginConfigModels.Version = Field(
            description="Plugin version defaults and validation."
        )
        validation: FlextPluginConfigModels.Validation = Field(
            description="Plugin validation rule namespace."
        )
        files: FlextPluginConfigModels.Files = Field(
            description="Plugin file and directory defaults."
        )

    class Root(BaseModel):
        """Root flext-plugin config validated from ``config/*.yaml``."""

        model_config = ConfigDict(frozen=True, extra="ignore")

        Plugin: FlextPluginConfigModels.Plugin = Field(
            description="Plugin business-rule config namespace."
        )


__all__: list[str] = ["FlextPluginConfigModels"]
