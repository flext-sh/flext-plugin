"""FLEXT Plugin Utilities - Domain-specific utilities for plugin management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from collections.abc import Callable, MutableSequence, Sequence
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import ClassVar, Self

from flext_cli import FlextCliUtilities
from pydantic import model_validator

from flext_core import FlextUtilities
from flext_plugin import c, m, r, t


class FlextPluginUtilities(FlextUtilities):
    """composition-based utilities using Python 3.13+ patterns."""

    class Plugin:
        """Plugin discovery and validation utilities."""

        PLUGIN_EXTENSIONS: ClassVar[t.StrSequence] = [".py", ".yaml", ".yml", ".json"]
        PLUGIN_MANIFESTS: ClassVar[t.StrSequence] = [
            "plugin.yaml",
            "plugin.yml",
            "plugin.json",
            "setup.py",
        ]
        MAX_SIZE_MB: ClassVar[int] = 100
        NAME_PATTERN: ClassVar[str] = "^[a-zA-Z][a-zA-Z0-9_-]*$"

        PLUGIN_FILE_EXTENSIONS: ClassVar[t.Plugin.StringList] = [
            ".py",
            ".yaml",
            ".yml",
            ".json",
        ]
        PLUGIN_MANIFEST_FILES: ClassVar[t.Plugin.StringList] = [
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
        ) -> r[Sequence[m.Plugin.PluginMetadata]]:
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
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                return r[Sequence[m.Plugin.PluginMetadata]].fail(
                    f"Plugin discovery failed: {e}",
                )

        @staticmethod
        def extract_plugin_metadata(
            plugin_path: Path,
        ) -> r[m.Plugin.PluginMetadata]:
            """Extract metadata from plugin file.

            Args:
            plugin_path: Path to the plugin file

            Returns:
            r containing plugin metadata

            """
            try:
                version = c.Plugin.Discovery.DEFAULT_PLUGIN_VERSION
                description = f"Plugin from {plugin_path.name}"
                if plugin_path.suffix == ".py":
                    content = plugin_path.read_text(encoding="utf-8")
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
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                return r[m.Plugin.PluginMetadata].fail(
                    f"Metadata extraction failed: {e}",
                )

        @staticmethod
        def validate_plugin_file(plugin_path: Path) -> r[None]:
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
                    content = plugin_path.read_text(encoding="utf-8")
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
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                return r[None].fail(f"Plugin file validation failed: {e}")

        @staticmethod
        def validate_plugin_name(name: str) -> r[None]:
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

        class HotReloadManager:
            """Hot reload management utilities."""

            DEFAULT_WATCH_INTERVAL: ClassVar[float] = 1.0
            MAX_RELOAD_ATTEMPTS: ClassVar[int] = 3
            RELOAD_TIMEOUT_SECONDS: ClassVar[int] = 30

            @staticmethod
            def create_file_watcher(
                watch_path: Path | str,
                callback_function: Callable[..., t.NormalizedValue] | None = None,
            ) -> r[t.ContainerMapping]:
                """Create file system watcher for plugin hot reload.

                Args:
                watch_path: Path to watch for changes
                callback_function: Function to call on file changes

                Returns:
                r containing watcher configuration

                """
                try:
                    path = Path(watch_path)
                    if not path.exists():
                        return r[t.ContainerMapping].fail(
                            f"Watch path does not exist: {path}",
                        )
                    watcher_config: t.ContainerMapping = {
                        "watch_path": str(path),
                        "callback": callback_function.__name__
                        if callback_function
                        else None,
                        "watch_interval": FlextPluginUtilities.Plugin.HotReloadManager.DEFAULT_WATCH_INTERVAL,
                        "last_modified": dict[str, t.ContainerValue](),
                        "active": False,
                        "created_at": datetime.now(UTC).isoformat(),
                    }
                    return r[t.ContainerMapping].ok(watcher_config)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    return r[t.ContainerMapping].fail(
                        f"File watcher creation failed: {e}",
                    )

            @staticmethod
            def detect_file_changes(
                watcher_config: t.ContainerMapping,
            ) -> r[t.Plugin.StringList]:
                """Detect file changes in watched directory.

                Args:
                watcher_config: Watcher configuration from create_file_watcher

                Returns:
                r containing list of changed files

                """
                try:
                    watch_path = Path(str(watcher_config["watch_path"]))
                    last_modified_raw = watcher_config.get("last_modified", {})
                    last_modified: t.MutableContainerMapping = (
                        dict(
                            t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_python(
                                last_modified_raw,
                            ),
                        )
                        if FlextUtilities.dict_like(last_modified_raw)
                        else {}
                    )
                    changed_files: MutableSequence[str] = []
                    for file_path in watch_path.rglob("*"):
                        if (
                            file_path.is_file()
                            and file_path.suffix
                            in FlextPluginUtilities.Plugin.PLUGIN_FILE_EXTENSIONS
                        ):
                            file_key = str(file_path)
                            current_mtime = file_path.stat().st_mtime
                            if (
                                file_key not in last_modified
                                or last_modified[file_key] != current_mtime
                            ):
                                changed_files.append(file_path.as_posix())
                                last_modified[file_key] = current_mtime
                    return r[t.Plugin.StringList].ok(changed_files)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    return r[t.Plugin.StringList].fail(
                        f"File change detection failed: {e}"
                    )

            @staticmethod
            def validate_reload_safety(plugin_path: Path) -> r[None]:
                """Validate that plugin can be safely reloaded.

                Args:
                plugin_path: Path to plugin being reloaded

                Returns:
                r indicating reload safety

                """
                try:
                    validation_result = (
                        FlextPluginUtilities.Plugin.validate_plugin_file(
                            plugin_path,
                        )
                    )
                    if validation_result.failure:
                        return r[None].fail(
                            f"Plugin validation failed: {validation_result.error}",
                        )
                    if plugin_path.suffix == ".py":
                        try:
                            content = plugin_path.read_text(encoding="utf-8")
                            _ = compile(content, str(plugin_path), "exec")
                        except SyntaxError as e:
                            return r[None].fail(f"Python syntax error in plugin: {e}")
                    return r[None].ok(None)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    return r[None].fail(f"Reload safety validation failed: {e}")

        class SecurityValidation:
            """Plugin security validation and sandboxing utilities."""

            ALLOWED_IMPORTS: ClassVar[t.Plugin.StringList] = [
                "flext_core",
                "flext_api",
                "flext_observability",
                "flext_auth",
                "json",
                "datetime",
                "pathlib",
                "typing",
                "pydantic",
            ]
            DANGEROUS_OPERATIONS: ClassVar[t.Plugin.StringList] = [
                "exec",
                "eval",
                "__import__",
                "subprocess",
                "os.system",
                "open",
            ]
            MAX_MEMORY_MB: ClassVar[int] = 512
            MAX_EXECUTION_TIME_SECONDS: ClassVar[int] = 300

            @staticmethod
            def calculate_plugin_hash(plugin_content: str) -> r[str]:
                """Calculate secure hash of plugin content for integrity verification.

                Args:
                plugin_content: Plugin source code content

                Returns:
                r containing SHA-256 hash of plugin content

                """

                def _calculate_plugin_hash() -> str:
                    content_bytes = plugin_content.encode("utf-8")
                    hash_object = hashlib.sha256(content_bytes)
                    return hash_object.hexdigest()

                return FlextPluginUtilities.try_(
                    _calculate_plugin_hash,
                    catch=(
                        ValueError,
                        TypeError,
                        KeyError,
                        AttributeError,
                        OSError,
                        RuntimeError,
                        ImportError,
                    ),
                ).map_error(lambda e: f"Plugin hash calculation failed: {e}")

            @staticmethod
            def create_sandbox_config(
                plugin_name: str,
            ) -> r[t.ContainerMapping]:
                """Create sandbox configuration for plugin execution.

                Args:
                plugin_name: Name of the plugin to sandbox

                Returns:
                r containing sandbox configuration

                """

                def _create_sandbox_config() -> t.ContainerMapping:
                    sandbox_config: t.ContainerMapping = {
                        "plugin_name": plugin_name,
                        "max_memory_mb": FlextPluginUtilities.Plugin.SecurityValidation.MAX_MEMORY_MB,
                        "max_execution_time": FlextPluginUtilities.Plugin.SecurityValidation.MAX_EXECUTION_TIME_SECONDS,
                        "allowed_modules": list(
                            FlextPluginUtilities.Plugin.SecurityValidation.ALLOWED_IMPORTS,
                        ),
                        "network_access": False,
                        "file_system_access": "read-only",
                        "environment_variables": {
                            "PYTHONDONTWRITEBYTECODE": "1",
                            "PYTHONUNBUFFERED": "1",
                        },
                        "created_at": datetime.now(UTC).isoformat(),
                    }
                    return sandbox_config

                return FlextPluginUtilities.try_(
                    _create_sandbox_config,
                    catch=(
                        ValueError,
                        TypeError,
                        KeyError,
                        AttributeError,
                        OSError,
                        RuntimeError,
                        ImportError,
                    ),
                ).map_error(lambda e: f"Sandbox configuration creation failed: {e}")

            @staticmethod
            def validate_plugin_security(
                plugin_content: str,
            ) -> r[t.ContainerMapping]:
                """Validate plugin security before execution.

                Args:
                plugin_content: Plugin source code content

                Returns:
                r containing security validation results

                """
                try:
                    security_report: t.MutableContainerMapping = {
                        "safe": True,
                        "violations": list[str](),
                        "warnings": list[str](),
                        "analysis_time": datetime.now(UTC).isoformat(),
                    }
                    for dangerous_op in FlextPluginUtilities.Plugin.SecurityValidation.DANGEROUS_OPERATIONS:
                        if dangerous_op in plugin_content:
                            security_report["safe"] = False
                            violations = security_report["violations"]
                            if FlextUtilities.list_like(violations) and isinstance(
                                violations, list
                            ):
                                violations.append(
                                    f"Dangerous operation detected: {dangerous_op}",
                                )
                    import_pattern = "(?:from\\s+(\\w+)|import\\s+(\\w+))"
                    imports = re.findall(import_pattern, plugin_content)
                    for imp in imports:
                        module_name = imp[0] or imp[1]
                        if module_name and (
                            not any(
                                allowed in module_name
                                for allowed in FlextPluginUtilities.Plugin.SecurityValidation.ALLOWED_IMPORTS
                            )
                        ):
                            warnings = security_report["warnings"]
                            if FlextUtilities.list_like(warnings) and isinstance(
                                warnings, list
                            ):
                                warnings.append(
                                    f"Potentially unsafe import: {module_name}"
                                )
                    if (
                        "network" in plugin_content.lower()
                        or "socket" in plugin_content
                    ):
                        warnings = security_report["warnings"]
                        if FlextUtilities.list_like(warnings) and isinstance(
                            warnings, list
                        ):
                            warnings.append("Plugin may perform network operations")
                    if "file" in plugin_content.lower() or "write" in plugin_content:
                        warnings = security_report["warnings"]
                        if FlextUtilities.list_like(warnings) and isinstance(
                            warnings, list
                        ):
                            warnings.append("Plugin may perform file operations")
                    return r[t.ContainerMapping].ok(dict(security_report))
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    return r[t.ContainerMapping].fail(
                        f"Security validation failed: {e}",
                    )

        class ConfigurationManager:
            """Plugin configuration management utilities."""

            DEFAULT_CONFIG_FILE: ClassVar[str] = c.Plugin.Files.DEFAULT_CONFIG_FILE
            CONFIG_SCHEMA_VERSION: ClassVar[str] = c.Plugin.Files.CONFIG_SCHEMA_VERSION
            MAX_CONFIG_SIZE_KB: ClassVar[int] = 1024

            @staticmethod
            def load_plugin_config(
                config_path: Path | str,
            ) -> r[t.ContainerMapping]:
                """Load plugin configuration from file.

                Args:
                config_path: Path to plugin configuration file

                Returns:
                r containing plugin configuration

                """
                try:
                    path = Path(config_path)
                    if not path.exists():
                        return r[t.ContainerMapping].fail(
                            f"Configuration file not found: {path}",
                        )
                    file_size_kb = path.stat().st_size / 1024
                    if (
                        file_size_kb
                        > FlextPluginUtilities.Plugin.ConfigurationManager.MAX_CONFIG_SIZE_KB
                    ):
                        return r[t.ContainerMapping].fail(
                            f"Configuration file too large: {file_size_kb:.1f}KB",
                        )
                    content = path.read_text(encoding="utf-8")
                    if path.suffix in {".yaml", ".yml"}:
                        settings = FlextCliUtilities.Cli.yaml_parse(content).unwrap_or(
                            {},
                        )
                    elif path.suffix == ".json":
                        settings = t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_json(
                            content,
                        )
                    else:
                        return r[t.ContainerMapping].fail(
                            f"Unsupported configuration format: {path.suffix}",
                        )
                    if (
                        FlextUtilities.dict_like(settings)
                        and settings.get("schema_version")
                        != FlextPluginUtilities.Plugin.ConfigurationManager.CONFIG_SCHEMA_VERSION
                    ):
                        return r[t.ContainerMapping].fail(
                            f"Unsupported configuration schema version: {settings.get('schema_version')}",
                        )
                    config_mapping: t.ContainerMapping = (
                        t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_python(settings)
                    )
                    return r[t.ContainerMapping].ok(config_mapping)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    return r[t.ContainerMapping].fail(
                        f"Configuration loading failed: {e}",
                    )

            @staticmethod
            def merge_plugin_configs(
                base_config: t.ContainerMapping,
                override_config: t.ContainerMapping,
            ) -> r[t.ContainerMapping]:
                """Merge plugin configurations with override precedence.

                Args:
                base_config: Base plugin configuration
                override_config: Configuration values to override

                Returns:
                r containing merged configuration

                """
                try:
                    merged_config = dict(base_config)
                    for key, value in override_config.items():
                        existing_value = merged_config.get(key)
                        if isinstance(value, dict) and isinstance(existing_value, dict):
                            base_nested_config: t.ContainerMapping = (
                                t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_python(
                                    existing_value
                                )
                            )
                            override_value: t.ContainerMapping = (
                                t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_python(value)
                            )
                            nested_merge = FlextPluginUtilities.Plugin.ConfigurationManager.merge_plugin_configs(
                                base_nested_config,
                                override_value,
                            )
                            if nested_merge.success:
                                merged_config[key] = nested_merge.value
                            else:
                                return r[t.ContainerMapping].fail(
                                    f"Failed to merge nested settings for key '{key}': {nested_merge.error}",
                                )
                        else:
                            merged_config[key] = value
                    return r[t.ContainerMapping].ok(merged_config)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    return r[t.ContainerMapping].fail(
                        f"Configuration merge failed: {e}",
                    )

            @staticmethod
            def validate_plugin_config(settings: t.ContainerMapping) -> r[None]:
                """Validate plugin configuration structure and values.

                Args:
                settings: Plugin configuration to validate

                Returns:
                r indicating validation success or failure

                """
                try:
                    required_fields = ["name", "version", "description", "entry_point"]
                    for field in required_fields:
                        if field not in settings:
                            return r[None].fail(
                                f"Missing required configuration field: {field}",
                            )
                    name_validation = FlextPluginUtilities.Plugin.validate_plugin_name(
                        str(settings["name"]),
                    )
                    if name_validation.failure:
                        return r[None].fail(
                            name_validation.error or "Plugin name validation failed",
                        )
                    version_pattern = "^\\d+\\.\\d+\\.\\d+$"
                    if not re.match(version_pattern, str(settings["version"])):
                        return r[None].fail(
                            f"Invalid version format: {settings['version']}. Expected semantic version (x.y.z)",
                        )
                    return r[None].ok(None)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    return r[None].fail(f"Configuration validation failed: {e}")

        class PluginExecution:
            """Plugin execution and lifecycle management utilities."""

            DEFAULT_TIMEOUT_SECONDS: ClassVar[int] = 300
            MAX_RETRY_ATTEMPTS: ClassVar[int] = 3
            EXECUTION_LOG_LEVELS: ClassVar[t.Plugin.StringList] = [
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ]

            @staticmethod
            def execute_plugin_function(
                plugin_module: ModuleType,
                function_name: str,
                args: t.ContainerList | None = None,
                kwargs: t.ContainerMapping | None = None,
            ) -> r[t.NormalizedValue]:
                """Execute a specific function within a plugin module.

                Args:
                plugin_module: Loaded plugin module
                function_name: Name of function to execute
                args: Positional arguments for function
                kwargs: Keyword arguments for function

                Returns:
                r containing function execution result

                """
                plugin_function = getattr(plugin_module, function_name, None)
                if plugin_function is None:
                    return r[t.NormalizedValue].fail(
                        f"Function '{function_name}' not found in plugin module",
                    )
                if not callable(plugin_function):
                    return r[t.NormalizedValue].fail(
                        f"'{function_name}' is not callable"
                    )

                def _execute_plugin_function() -> t.NormalizedValue:
                    execution_args = args or []
                    execution_kwargs = kwargs or {}
                    raw_result = plugin_function(
                        *execution_args,
                        **execution_kwargs,
                    )
                    if isinstance(raw_result, (str, int, float, bool)):
                        return raw_result
                    if raw_result is None:
                        return None
                    return str(raw_result)

                return FlextPluginUtilities.try_(
                    _execute_plugin_function,
                    catch=(
                        ValueError,
                        TypeError,
                        KeyError,
                        AttributeError,
                        OSError,
                        RuntimeError,
                        ImportError,
                    ),
                ).map_error(lambda e: f"Plugin function execution failed: {e}")

            @staticmethod
            def load_plugin_module(plugin_path: Path | str) -> r[ModuleType]:
                """Load plugin module from file path.

                Args:
                plugin_path: Path to plugin Python file

                Returns:
                r containing loaded plugin module

                """
                try:
                    path = Path(plugin_path)
                    if not path.exists():
                        return r[ModuleType].fail(f"Plugin file not found: {path}")
                    if path.suffix != ".py":
                        return r[ModuleType].fail(
                            f"Only Python plugins are supported: {path}",
                        )
                    spec = importlib.util.spec_from_file_location(path.stem, path)
                    if spec is None or spec.loader is None:
                        return r[ModuleType].fail(
                            f"Failed to create module spec for: {path}",
                        )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    return r[ModuleType].ok(module)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    return r[ModuleType].fail(f"Plugin module loading failed: {e}")

            @staticmethod
            def validate_plugin_interface(
                plugin_module: ModuleType,
                required_functions: t.Plugin.StringList,
            ) -> r[None]:
                """Validate that plugin module implements required interface.

                Args:
                plugin_module: Loaded plugin module
                required_functions: List of required function names

                Returns:
                r indicating interface validation success or failure

                """

                def _validate_plugin_interface() -> None:
                    missing_functions = [
                        func_name
                        for func_name in required_functions
                        if getattr(plugin_module, func_name, None) is None
                    ]
                    if missing_functions:
                        missing_msg = (
                            f"Plugin missing required functions: {missing_functions}"
                        )
                        raise ValueError(missing_msg)
                    non_callable = [
                        func_name
                        for func_name in required_functions
                        if not callable(getattr(plugin_module, func_name, None))
                    ]
                    if non_callable:
                        non_callable_msg = (
                            f"Plugin attributes not callable: {non_callable}"
                        )
                        raise ValueError(non_callable_msg)

                return FlextPluginUtilities.try_(
                    _validate_plugin_interface,
                    catch=(
                        ValueError,
                        TypeError,
                        KeyError,
                        AttributeError,
                        OSError,
                        RuntimeError,
                        ImportError,
                    ),
                ).map_error(lambda e: f"Plugin interface validation failed: {e}")

        class RegistryOperations:
            """Plugin registry management utilities."""

            REGISTRY_FILE_NAME: ClassVar[str] = "plugin_registry.json"
            REGISTRY_BACKUP_COUNT: ClassVar[int] = 5
            MAX_REGISTRY_SIZE_MB: ClassVar[int] = 10

            @staticmethod
            def cleanup_registry_backups(registry_directory: Path) -> r[None]:
                """Clean up old registry backup files.

                Args:
                registry_directory: Directory containing registry backups

                Returns:
                r indicating cleanup success or failure

                """

                def _cleanup_registry_backups() -> None:
                    backup_pattern = f"{FlextPluginUtilities.Plugin.RegistryOperations.REGISTRY_FILE_NAME.split('.')[0]}.backup.*.json"
                    backup_files = list(registry_directory.glob(backup_pattern))
                    backup_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
                    for backup_file in backup_files[
                        FlextPluginUtilities.Plugin.RegistryOperations.REGISTRY_BACKUP_COUNT :
                    ]:
                        backup_file.unlink()

                return FlextPluginUtilities.try_(
                    _cleanup_registry_backups,
                    catch=(
                        ValueError,
                        TypeError,
                        KeyError,
                        AttributeError,
                        OSError,
                        RuntimeError,
                        ImportError,
                    ),
                ).map_error(lambda e: f"Registry backup cleanup failed: {e}")

            @staticmethod
            def load_plugin_registry(
                registry_path: Path | str,
            ) -> r[t.ContainerMapping]:
                """Load plugin registry from file.

                Args:
                registry_path: Path to plugin registry file

                Returns:
                r containing plugin registry data

                """
                try:
                    path = Path(registry_path)
                    if not path.exists():
                        registry: t.ContainerMapping = {
                            "version": c.Plugin.Files.CONFIG_SCHEMA_VERSION,
                            "plugins": dict[str, t.ContainerValue](),
                            "last_updated": datetime.now(UTC).isoformat(),
                            "created_at": datetime.now(UTC).isoformat(),
                        }
                        return r[t.ContainerMapping].ok(registry)
                    file_size_mb = path.stat().st_size / (1024 * 1024)
                    if (
                        file_size_mb
                        > FlextPluginUtilities.Plugin.RegistryOperations.MAX_REGISTRY_SIZE_MB
                    ):
                        return r[t.ContainerMapping].fail(
                            f"Registry file too large: {file_size_mb:.1f}MB",
                        )
                    content = path.read_text(encoding="utf-8")
                    registry = t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_json(
                        content,
                    )
                    return r[t.ContainerMapping].ok(registry)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    return r[t.ContainerMapping].fail(
                        f"Registry loading failed: {e}",
                    )

            @staticmethod
            def register_plugin(
                registry: t.ContainerMapping,
                plugin_metadata: m.Plugin.PluginMetadata,
            ) -> r[t.ContainerMapping]:
                """Register plugin in registry.

                Args:
                registry: Plugin registry data
                plugin_metadata: Metadata of plugin to register

                Returns:
                r containing updated registry

                """
                try:
                    mutable_registry: t.MutableContainerMapping = dict(registry)
                    if "plugins" not in mutable_registry:
                        mutable_registry["plugins"] = dict[str, t.NormalizedValue]()
                    plugin_info = {
                        "name": plugin_metadata.name,
                        "version": getattr(plugin_metadata, "plugin_version", "1.0.0"),
                        "description": plugin_metadata.description,
                        "author": getattr(plugin_metadata, "author", ""),
                        "plugin_type": plugin_metadata.plugin_type,
                        "entry_point": plugin_metadata.entry_point,
                        "dependencies": plugin_metadata.dependencies,
                        "registered_at": datetime.now(UTC).isoformat(),
                        "status": "registered",
                        "metadata": getattr(plugin_metadata, "metadata", {}),
                    }
                    plugins = mutable_registry["plugins"]
                    if isinstance(plugins, dict):
                        plugins[plugin_metadata.name] = plugin_info
                    return r[t.ContainerMapping].ok(mutable_registry)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    return r[t.ContainerMapping].fail(
                        f"Plugin registration failed: {e}",
                    )

            @staticmethod
            def save_plugin_registry(
                registry: t.ContainerMapping,
                registry_path: Path | str,
            ) -> r[None]:
                """Save plugin registry to file with backup.

                Args:
                registry: Plugin registry data to save
                registry_path: Path to save registry file

                Returns:
                r indicating save success or failure

                """
                try:
                    path = Path(registry_path)
                    if path.exists():
                        backup_path = path.with_suffix(
                            f".backup.{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json",
                        )
                        _ = path.rename(backup_path)
                        _ = FlextPluginUtilities.Plugin.RegistryOperations.cleanup_registry_backups(
                            path.parent,
                        )
                    validated: t.ContainerValueMapping = (
                        t.CONTAINER_VALUE_MAPPING_ADAPTER.validate_python(registry)
                    )
                    mutable_registry: t.ContainerValueMapping = {
                        **validated,
                        "last_updated": datetime.now(UTC).isoformat(),
                    }
                    _ = path.write_text(
                        t.CONTAINER_VALUE_MAPPING_ADAPTER.dump_json(
                            mutable_registry, indent=2
                        ).decode(
                            "utf-8",
                        ),
                        encoding="utf-8",
                    )
                    return r[None].ok(None)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    return r[None].fail(f"Registry save failed: {e}")

    @model_validator(mode="after")
    def validate_utilities_configuration(self) -> Self:
        """Validate the complete utilities configuration."""
        required_classes = ["Plugin"]
        for class_name in required_classes:
            if getattr(self.__class__, class_name, None) is None:
                msg = f"Missing required nested class: {class_name}"
                raise ValueError(msg)
        return self


u = FlextPluginUtilities

__all__ = ["FlextPluginUtilities", "u"]
