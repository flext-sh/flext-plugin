"""flext-plugin config models — typed business-rule shapes.

Frozen Pydantic shapes for the ``config/plugin.yaml`` business-rule SSOT.
The config declaration validates these shapes at construction and exposes
the ready objects under ``config.Plugin``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import m


class FlextPluginConfigModels:
    """Namespace of typed flext-plugin config models."""

    class Version(m.BaseModel):
        """Plugin version defaults and validation."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        default: str = m.Field(description="Default plugin version string.")
        pattern: str = m.Field(description="Regex validating a semantic version.")

    class NameValidation(m.BaseModel):
        """Constraints applied when validating plugin names."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        min_length: int = m.Field(ge=1, description="Minimum plugin name length.")
        max_length: int = m.Field(ge=1, description="Maximum plugin name length.")
        pattern: str = m.Field(description="Regex validating a plugin name.")

    class DescriptionValidation(m.BaseModel):
        """Constraints applied when validating plugin descriptions."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        max_length: int = m.Field(
            ge=1, description="Maximum plugin description length."
        )

    class AuthorValidation(m.BaseModel):
        """Constraints applied when validating plugin authors."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        max_length: int = m.Field(ge=1, description="Maximum author string length.")

    class DocstringValidation(m.BaseModel):
        """Rules for extracting plugin documentation strings."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        pattern: str = m.Field(
            description="Regex extracting the first triple-quoted docstring.",
        )

    class Validation(m.BaseModel):
        """Namespace grouping the plugin validation rule models."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        name: FlextPluginConfigModels.NameValidation = m.Field(
            description="Plugin name validation thresholds.",
        )
        description: FlextPluginConfigModels.DescriptionValidation = m.Field(
            description="Plugin description validation thresholds.",
        )
        author: FlextPluginConfigModels.AuthorValidation = m.Field(
            description="Plugin author validation thresholds.",
        )
        docstring: FlextPluginConfigModels.DocstringValidation = m.Field(
            description="Plugin docstring extraction rules.",
        )

    class Files(m.BaseModel):
        """Plugin file and directory defaults."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        python_extension: str = m.Field(description="Python source file extension.")
        yaml_extension: str = m.Field(description="YAML file extension.")
        json_extension: str = m.Field(description="JSON file extension.")
        toml_extension: str = m.Field(description="TOML file extension.")
        default_plugin_dir: str = m.Field(description="Default plugin directory.")
        default_cache_dir: str = m.Field(description="Default plugin cache directory.")

    class Plugin(m.BaseModel):
        """Root namespace grouping plugin business-rule models."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        version: FlextPluginConfigModels.Version = m.Field(
            description="Plugin version defaults and validation.",
        )
        validation: FlextPluginConfigModels.Validation = m.Field(
            description="Plugin validation rule namespace.",
        )
        files: FlextPluginConfigModels.Files = m.Field(
            description="Plugin file and directory defaults.",
        )


__all__: list[str] = ["FlextPluginConfigModels"]
