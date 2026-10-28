"""flext-plugin config models — typed business-rule shapes.

Frozen Pydantic shapes for the ``config/plugin.yaml`` business-rule SSOT.
The config declaration validates these shapes at construction and exposes
the ready objects under ``config.Plugin``.

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

from pydantic import BaseModel, ConfigDict, Field


class FlextPluginModelsConfig:
    """Namespace of typed flext-plugin config models."""

    class Version(BaseModel):
        """Plugin version defaults and validation."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        default: str = Field(description="Default plugin version string.")
        pattern: str = Field(description="Regex validating a semantic version.")

    class NameValidation(BaseModel):
        """Constraints applied when validating plugin names."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        min_length: int = Field(ge=1, description="Minimum plugin name length.")
        max_length: int = Field(ge=1, description="Maximum plugin name length.")
        pattern: str = Field(description="Regex validating a plugin name.")

    class DescriptionValidation(BaseModel):
        """Constraints applied when validating plugin descriptions."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        max_length: int = Field(ge=1, description="Maximum plugin description length.")

    class AuthorValidation(BaseModel):
        """Constraints applied when validating plugin authors."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        max_length: int = Field(ge=1, description="Maximum author string length.")

    class DocstringValidation(BaseModel):
        """Rules for extracting plugin documentation strings."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        pattern: str = Field(
            description="Regex extracting the first triple-quoted docstring.",
        )

    class Validation(BaseModel):
        """Namespace grouping the plugin validation rule models."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        name: FlextPluginModelsConfig.NameValidation = Field(
            description="Plugin name validation thresholds.",
        )
        description: FlextPluginModelsConfig.DescriptionValidation = Field(
            description="Plugin description validation thresholds.",
        )
        author: FlextPluginModelsConfig.AuthorValidation = Field(
            description="Plugin author validation thresholds.",
        )
        docstring: FlextPluginModelsConfig.DocstringValidation = Field(
            description="Plugin docstring extraction rules.",
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
        """Root namespace grouping plugin business-rule models."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        version: FlextPluginModelsConfig.Version = Field(
            description="Plugin version defaults and validation.",
        )
        validation: FlextPluginModelsConfig.Validation = Field(
            description="Plugin validation rule namespace.",
        )
        files: FlextPluginModelsConfig.Files = Field(
            description="Plugin file and directory defaults.",
        )


__all__: list[str] = ["FlextPluginModelsConfig"]
