"""FLEXT Plugin Utilities - Domain-specific utilities for plugin management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from collections.abc import (
    MutableSequence,
    Sequence,
)
from datetime import UTC, datetime
from pathlib import Path
from typing import ClassVar

from flext_cli import u

from flext_plugin import c, m, p, r, t


class FlextPluginUtilities(u):
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

        @staticmethod
        def discover_plugins(
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
                plugins: MutableSequence[m.Plugin.PluginMetadata] = []
                for plugin_file in search_path.rglob("*"):
                    if (
                        plugin_file.is_file()
                        and plugin_file.suffix
                        in FlextPluginUtilities.Plugin.PLUGIN_FILE_EXTENSIONS
                    ):
                        validation_result = (
                            FlextPluginUtilities.Plugin.validate_plugin_file(
                                plugin_file,
                            )
                        )
                        if validation_result.success:
                            metadata_result = (
                                FlextPluginUtilities.Plugin.extract_plugin_metadata(
                                    plugin_file,
                                )
                            )
                            if metadata_result.success:
                                plugins.append(metadata_result.value)
                return r[Sequence[m.Plugin.PluginMetadata]].ok(plugins)
            except c.EXC_BROAD_IO_TYPE as e:
                return r[Sequence[m.Plugin.PluginMetadata]].fail_op("Plugin discovery", e)

        @staticmethod
        def extract_plugin_metadata(
            plugin_path: Path,
        ) -> p.Result[m.Plugin.PluginMetadata]:
            """Extract metadata from plugin file.

            Args:
            plugin_path: Path to the plugin file

            Returns:
            r containing plugin metadata

            """
            try:
                version = c.Plugin.DEFAULT_PLUGIN_VERSION
                description = f"Plugin from {plugin_path.name}"
                if plugin_path.suffix == ".py":
                    content = plugin_path.read_text(encoding=c.DEFAULT_ENCODING)
                    version_match = re.search(
                        r"__version__\\s*=\\s*[\"\\']([^\"\\']+)[\"\\']",
                        content,
                    )
                    if version_match:
                        version = version_match.group(1)
                    doc_match = re.search(r'"""([^"]+)"""', content)
                    if doc_match:
                        description = doc_match.group(1).strip()
                metadata = m.Plugin.PluginMetadata(
                    name=plugin_path.stem,
                    version=version,
                    description=description,
                    author="Unknown",
                    plugin_type="extension",
                    entry_point=str(plugin_path),
                    dependencies=[],
                    metadata={"discovered_at": datetime.now(UTC).isoformat()},
                )
                return r[m.Plugin.PluginMetadata].ok(metadata)
            except c.EXC_BROAD_IO_TYPE as e:
                return r[m.Plugin.PluginMetadata].fail_op("Metadata extraction", e)

        @staticmethod
        def validate_plugin_file(plugin_path: Path) -> p.Result[None]:
            """Validate plugin file structure and safety.

            Args:
            plugin_path: Path to the plugin file

            Returns:
            r indicating validation success or failure

            """
            try:
                if not plugin_path.exists():
                    return r[None].fail(f"Plugin file does not exist: {plugin_path}")
                file_size_mb = plugin_path.stat().st_size / (1024 * 1024)
                if file_size_mb > FlextPluginUtilities.Plugin.MAX_PLUGIN_SIZE_MB:
                    return r[None].fail(
                        f"Plugin file too large: {file_size_mb:.1f}MB > {FlextPluginUtilities.Plugin.MAX_PLUGIN_SIZE_MB}MB",
                    )
                if plugin_path.suffix == ".py":
                    content = plugin_path.read_text(encoding=c.DEFAULT_ENCODING)
                    dangerous_patterns = [
                        "exec(",
                        "eval(",
                        "__import__",
                        "subprocess",
                        "os.system",
                    ]
                    for pattern in dangerous_patterns:
                        if pattern in content:
                            return r[None].fail(
                                f"Plugin contains potentially dangerous code: {pattern}",
                            )
                return r[None].ok(None)
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
            if not re.match(FlextPluginUtilities.Plugin.PLUGIN_NAME_PATTERN, name):
                return r[None].fail(
                    f"Invalid plugin name '{name}'. Must start with letter and contain only letters, numbers, hyphens, and underscores.",
                )
            return r[None].ok(None)


u = FlextPluginUtilities

__all__: list[str] = ["FlextPluginUtilities", "u"]
