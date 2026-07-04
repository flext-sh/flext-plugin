"""FLEXT Plugin Utilities - Domain-specific utilities for plugin management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    MutableSequence,
    Sequence,
)
from pathlib import Path
from typing import ClassVar

from flext_cli import u
from flext_core import (
    FlextUtilitiesConversion,
    FlextUtilitiesGuardsTypeCore,
    FlextUtilitiesModelRuntime,
)
from flext_plugin import c, m, p, r, t
from flext_plugin._utilities.discovery import FlextPluginDiscovery
from flext_plugin._utilities.plugin_platform import FlextPluginPlatform


class FlextPluginUtilities(
    u,
    FlextUtilitiesConversion,
    FlextUtilitiesGuardsTypeCore,
    FlextUtilitiesModelRuntime,
):
    """composition-based utilities using Python 3.13+ patterns."""

    class Plugin:
        """Plugin discovery and validation utilities."""

        DEFAULT_WATCH_INTERVAL: ClassVar[float] = 1.0

        PLUGIN_EXTENSIONS: ClassVar[t.StrSequence] = [".py", ".yaml", ".yml", ".json"]
        PLUGIN_MANIFESTS: ClassVar[t.StrSequence] = [
            "plugin.yaml",
            "plugin.yml",
            "plugin.json",
            "setup.py",
        ]
        MAX_SIZE_MB: ClassVar[int] = 100
        NAME_PATTERN: ClassVar[str] = "^[a-zA-Z][a-zA-Z0-9_-]*$"

        PLUGIN_FILE_EXTENSIONS: ClassVar[t.StrSequence] = [
            ".py",
            ".yaml",
            ".yml",
            ".json",
        ]
        PLUGIN_MANIFEST_FILES: ClassVar[t.StrSequence] = [
            "plugin.yaml",
            "plugin.yml",
            "plugin.json",
            "setup.py",
        ]
        MAX_PLUGIN_SIZE_MB: ClassVar[int] = 100
        PLUGIN_NAME_PATTERN: ClassVar[str] = "^[a-zA-Z][a-zA-Z0-9_-]*$"
        DANGEROUS_PLUGIN_PATTERNS: ClassVar[t.StrSequence] = [
            "exec(",
            "eval(",
            "__import__",
            "subprocess",
            "os.system",
        ]
        Discovery: ClassVar[type[FlextPluginDiscovery]]
        Platform: ClassVar[type[FlextPluginPlatform]]

        @classmethod
        def discover_plugins(
            cls,
            directory: Path | str,
        ) -> p.Result[Sequence[m.Plugin.PluginMetadata]]:
            """Discover plugins in the specified directory.

            Args:
            directory: Directory to search for plugins

            Returns:
            r containing list of discovered plugin metadata

            """
            try:
                search_path = Path(directory)
                if not search_path.exists():
                    return r[Sequence[m.Plugin.PluginMetadata]].fail(
                        f"Plugin directory does not exist: {search_path}",
                    )
                plugins = cls._discover_metadata(search_path)
                return r[Sequence[m.Plugin.PluginMetadata]].ok(plugins)
            except c.EXC_BROAD_IO_TYPE as e:
                return r[Sequence[m.Plugin.PluginMetadata]].fail_op(
                    "Plugin discovery",
                    e,
                )

        @classmethod
        def extract_plugin_metadata(
            cls,
            plugin_path: Path,
        ) -> p.Result[m.Plugin.PluginMetadata]:
            """Extract metadata from plugin file.

            Args:
            plugin_path: Path to the plugin file

            Returns:
            r containing plugin metadata

            """
            try:
                return r[m.Plugin.PluginMetadata].ok(cls._build_metadata(plugin_path))
            except c.EXC_BROAD_IO_TYPE as e:
                return r[m.Plugin.PluginMetadata].fail_op("Metadata extraction", e)

        @classmethod
        def validate_plugin_file(cls, plugin_path: Path) -> p.Result[None]:
            """Validate plugin file structure and safety.

            Args:
            plugin_path: Path to the plugin file

            Returns:
            r indicating validation success or failure

            """
            try:
                precheck = cls._validate_plugin_path(plugin_path)
                if precheck.failure or plugin_path.suffix != ".py":
                    return precheck
                return cls._validate_python_plugin_file(plugin_path)
            except c.EXC_BROAD_IO_TYPE as e:
                return r[None].fail_op("Plugin file validation", e)

        @staticmethod
        def validate_plugin_name(name: str) -> p.Result[None]:
            """Validate plugin name follows naming conventions.

            Args:
            name: Plugin name to validate

            Returns:
            r indicating validation success or failure

            """
            if not c.Plugin.PluginValidation.PLUGIN_NAME_RE.match(name):
                return r[None].fail(
                    f"Invalid plugin name '{name}'. Must start with letter and contain only letters, numbers, hyphens, and underscores.",
                )
            return r[None].ok(None)

        @classmethod
        def _build_metadata(cls, plugin_path: Path) -> m.Plugin.PluginMetadata:
            """Build plugin metadata for one plugin file."""
            version, description = cls._metadata_fields(plugin_path)
            return m.Plugin.PluginMetadata(
                name=plugin_path.stem,
                version=version,
                description=description,
                author="Unknown",
                plugin_type="extension",
                entry_point=str(plugin_path),
                dependencies=[],
                metadata={"discovered_at": u.now().isoformat()},
            )

        @classmethod
        def _discover_metadata(
            cls,
            search_path: Path,
        ) -> Sequence[m.Plugin.PluginMetadata]:
            """Discover plugin metadata under one search path."""
            plugins: MutableSequence[m.Plugin.PluginMetadata] = []
            for plugin_file in search_path.rglob("*"):
                if not cls._is_candidate_file(plugin_file):
                    continue
                validation_result = cls.validate_plugin_file(plugin_file)
                if validation_result.failure:
                    continue
                metadata_result = cls.extract_plugin_metadata(plugin_file)
                if metadata_result.success:
                    plugins.append(metadata_result.value)
            return plugins

        @classmethod
        def _is_candidate_file(cls, plugin_file: Path) -> bool:
            """Return whether a file is a plugin metadata candidate."""
            return (
                plugin_file.is_file()
                and plugin_file.suffix in cls.PLUGIN_FILE_EXTENSIONS
            )

        @staticmethod
        def _metadata_fields(plugin_path: Path) -> tuple[str, str]:
            """Extract version and description fields for metadata."""
            version = c.Plugin.DEFAULT_PLUGIN_VERSION
            description = f"Plugin from {plugin_path.name}"
            if plugin_path.suffix != ".py":
                return version, description
            read = u.Cli.files_read_text(plugin_path)
            if read.failure:
                msg = read.error or "plugin metadata read failed"
                raise OSError(msg)
            content = read.value
            version_match = c.Plugin.PluginValidation.VERSION_DUNDER_RE.search(content)
            doc_match = c.Plugin.PluginValidation.DOCSTRING_TRIPLE_RE.search(content)
            if version_match:
                version = version_match.group(1)
            if doc_match:
                description = doc_match.group(1).strip()
            return version, description

        @classmethod
        def _validate_plugin_path(cls, plugin_path: Path) -> p.Result[None]:
            """Validate file existence and size constraints."""
            if not plugin_path.exists():
                return r[None].fail(f"Plugin file does not exist: {plugin_path}")
            file_size_mb = plugin_path.stat().st_size / (1024 * 1024)
            if file_size_mb > cls.MAX_PLUGIN_SIZE_MB:
                return r[None].fail(
                    f"Plugin file too large: {file_size_mb:.1f}MB > {cls.MAX_PLUGIN_SIZE_MB}MB",
                )
            return r[None].ok(None)

        @classmethod
        def _validate_python_plugin_file(cls, plugin_path: Path) -> p.Result[None]:
            """Validate Python plugin source for disallowed execution patterns."""
            read = u.Cli.files_read_text(plugin_path)
            if read.failure:
                return r[None].fail_op("Plugin validation", read.error)
            content = read.value
            for pattern in cls.DANGEROUS_PLUGIN_PATTERNS:
                if pattern in content:
                    return r[None].fail(
                        f"Plugin contains potentially dangerous code: {pattern}",
                    )
            return r[None].ok(None)


u = FlextPluginUtilities

FlextPluginUtilities.Plugin.Discovery = FlextPluginDiscovery
FlextPluginUtilities.Plugin.Platform = FlextPluginPlatform

__all__: list[str] = ["FlextPluginUtilities", "u"]
