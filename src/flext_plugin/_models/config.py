"""flext-plugin config models — typed business-rule shapes.

Frozen Pydantic shapes for the ``config/plugin.yaml`` business-rule SSOT.
The config declaration validates these shapes at construction and exposes
the ready objects under ``config.Plugin``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import m, u


class FlextPluginConfigModels:
    """Namespace of typed flext-plugin config models."""

    class Version(m.BaseModel):
        """Plugin version defaults and validation."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        default: str = u.Field(description="Default plugin version string.")
        pattern: str = u.Field(description="Regex validating a semantic version.")

    class NameValidation(m.BaseModel):
        """Plugin name validation thresholds."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        min_length: int = u.Field(ge=1, description="Minimum plugin name length.")
        max_length: int = u.Field(ge=1, description="Maximum plugin name length.")
        pattern: str = u.Field(description="Regex validating a plugin name.")

    class DescriptionValidation(m.BaseModel):
        """Plugin description validation thresholds."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        max_length: int = u.Field(
            ge=1, description="Maximum plugin description length."
        )

    class AuthorValidation(m.BaseModel):
        """Plugin author validation thresholds."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        max_length: int = u.Field(ge=1, description="Maximum author string length.")

    class DocstringValidation(m.BaseModel):
        """Plugin docstring extraction rules."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        pattern: str = u.Field(
            description="Regex extracting the first triple-quoted docstring.",
        )

    class Validation(m.BaseModel):
        """Plugin validation rule namespace."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        name: FlextPluginConfigModels.NameValidation = u.Field(
            description="Plugin name validation thresholds.",
        )
        description: FlextPluginConfigModels.DescriptionValidation = u.Field(
            description="Plugin description validation thresholds.",
        )
        author: FlextPluginConfigModels.AuthorValidation = u.Field(
            description="Plugin author validation thresholds.",
        )
        docstring: FlextPluginConfigModels.DocstringValidation = u.Field(
            description="Plugin docstring extraction rules.",
        )

    class Files(m.BaseModel):
        """Plugin file and directory defaults."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        python_extension: str = u.Field(description="Python source file extension.")
        yaml_extension: str = u.Field(description="YAML file extension.")
        json_extension: str = u.Field(description="JSON file extension.")
        toml_extension: str = u.Field(description="TOML file extension.")
        default_plugin_dir: str = u.Field(description="Default plugin directory.")
        default_cache_dir: str = u.Field(description="Default plugin cache directory.")

    class Plugin(m.BaseModel):
        """Root plugin business-rule namespace."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        version: FlextPluginConfigModels.Version = u.Field(
            description="Plugin version defaults and validation.",
        )
        validation: FlextPluginConfigModels.Validation = u.Field(
            description="Plugin validation rule namespace.",
        )
        files: FlextPluginConfigModels.Files = u.Field(
            description="Plugin file and directory defaults.",
        )


__all__: list[str] = ["FlextPluginConfigModels"]
