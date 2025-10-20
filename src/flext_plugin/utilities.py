"""FLEXT Plugin Utilities - Domain-specific utilities for plugin management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import ClassVar

import yaml
from flext_core import FlextResult, FlextUtilities
from pydantic import field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from flext_plugin.models import FlextPluginModels
from flext_plugin.types import FlextPluginTypes


@dataclass
class FlextPluginUtilities(FlextUtilities):
    """Advanced composition-based utilities using Python 3.13+ patterns."""

    # Constants using advanced type syntax
    PLUGIN_EXTENSIONS: ClassVar[list[str]] = [".py", ".yaml", ".yml", ".json"]
    PLUGIN_MANIFESTS: ClassVar[list[str]] = [
        "plugin.yaml",
        "plugin.yml",
        "plugin.json",
        "setup.py",
    ]
    MAX_SIZE_MB: ClassVar[int] = 100
    NAME_PATTERN: ClassVar[str] = r"^[a-zA-Z][a-zA-Z0-9_-]*$"

    class PluginDiscovery:
        """Plugin discovery and validation utilities."""

        PLUGIN_FILE_EXTENSIONS: ClassVar[FlextPluginTypes.PluginCore.StringList] = [
            ".py",
            ".yaml",
            ".yml",
            ".json",
        ]
        PLUGIN_MANIFEST_FILES: ClassVar[FlextPluginTypes.PluginCore.StringList] = [
            "plugin.yaml",
            "plugin.yml",
            "plugin.json",
            "setup.py",
        ]
        MAX_PLUGIN_SIZE_MB: ClassVar[int] = 100
        PLUGIN_NAME_PATTERN: ClassVar[str] = r"^[a-zA-Z][a-zA-Z0-9_-]*$"

        @staticmethod
        def discover_plugins(
            directory: Path | str,
        ) -> FlextResult[list[FlextPluginModels.PluginMetadata]]:
            """Discover plugins in the specified directory.

            Args:
                directory: Directory to search for plugins

            Returns:
                FlextResult containing list of discovered plugin metadata

            """
            try:
                search_path = Path(directory)
                if not search_path.exists():
                    return FlextResult[list[FlextPluginModels.PluginMetadata]].fail(
                        f"Plugin directory does not exist: {search_path}",
                    )

                plugins = []
                for plugin_file in search_path.rglob("*"):
                    if (
                        plugin_file.is_file()
                        and plugin_file.suffix
                        in FlextPluginUtilities.PluginDiscovery.PLUGIN_FILE_EXTENSIONS
                    ):
                        validation_result = (
                            FlextPluginUtilities.PluginDiscovery.validate_plugin_file(
                                plugin_file,
                            )
                        )
                        if validation_result.is_success:
                            metadata_result = FlextPluginUtilities.PluginDiscovery.extract_plugin_metadata(
                                plugin_file,
                            )
                            if metadata_result.is_success:
                                plugins.append(metadata_result.unwrap())

                return FlextResult[list[FlextPluginModels.PluginMetadata]].ok(plugins)
            except Exception as e:
                return FlextResult[list[FlextPluginModels.PluginMetadata]].fail(
                    f"Plugin discovery failed: {e}",
                )

        @staticmethod
        def validate_plugin_file(plugin_path: Path) -> FlextResult[None]:
            """Validate plugin file structure and safety.

            Args:
                plugin_path: Path to the plugin file

            Returns:
                FlextResult indicating validation success or failure

            """
            try:
                if not plugin_path.exists():
                    return FlextResult[None].fail(
                        f"Plugin file does not exist: {plugin_path}",
                    )

                # Check file size
                file_size_mb = plugin_path.stat().st_size / (1024 * 1024)
                if (
                    file_size_mb
                    > FlextPluginUtilities.PluginDiscovery.MAX_PLUGIN_SIZE_MB
                ):
                    return FlextResult[None].fail(
                        f"Plugin file too large: {file_size_mb:.1f}MB > {FlextPluginUtilities.PluginDiscovery.MAX_PLUGIN_SIZE_MB}MB",
                    )

                # Basic security check for Python files
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
                            return FlextResult[None].fail(
                                f"Plugin contains potentially dangerous code: {pattern}",
                            )

                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(f"Plugin file validation failed: {e}")

        @staticmethod
        def extract_plugin_metadata(
            plugin_path: Path,
        ) -> FlextResult[FlextPluginModels.PluginMetadata]:
            """Extract metadata from plugin file.

            Args:
                plugin_path: Path to the plugin file

            Returns:
                FlextResult containing plugin metadata

            """
            try:
                metadata = FlextPluginModels.PluginMetadata(
                    name=plugin_path.stem,
                    version="1.0.0",
                    description=f"Plugin from {plugin_path.name}",
                    author="Unknown",
                    plugin_type="extension",
                    entry_point=str(plugin_path),
                    dependencies=[],
                    metadata={"discovered_at": datetime.now(UTC).isoformat()},
                )

                # Try to extract metadata from Python files
                if plugin_path.suffix == ".py":
                    content = plugin_path.read_text(encoding="utf-8")

                    # Extract version
                    version_match = re.search(
                        r'__version__\s*=\s*["\']([^"\']+)["\']',
                        content,
                    )
                    if version_match:
                        metadata.version = version_match.group(1)

                    # Extract description from docstring
                    doc_match = re.search(r'"""([^"]+)"""', content)
                    if doc_match:
                        metadata.description = doc_match.group(1).strip()

                return FlextResult[FlextPluginModels.PluginMetadata].ok(metadata)
            except Exception as e:
                return FlextResult[FlextPluginModels.PluginMetadata].fail(
                    f"Metadata extraction failed: {e}",
                )

        @staticmethod
        def validate_plugin_name(name: str) -> FlextResult[None]:
            """Validate plugin name follows naming conventions.

            Args:
                name: Plugin name to validate

            Returns:
                FlextResult indicating validation success or failure

            """
            if not re.match(
                FlextPluginUtilities.PluginDiscovery.PLUGIN_NAME_PATTERN,
                name,
            ):
                return FlextResult[None].fail(
                    f"Invalid plugin name '{name}'. Must start with letter and contain only letters, numbers, hyphens, and underscores.",
                )
            return FlextResult[None].ok(None)

    class HotReloadManager:
        """Hot reload management utilities."""

        DEFAULT_WATCH_INTERVAL: ClassVar[float] = 1.0
        MAX_RELOAD_ATTEMPTS: ClassVar[int] = 3
        RELOAD_TIMEOUT_SECONDS: ClassVar[int] = 30

        @staticmethod
        def create_file_watcher(
            watch_path: Path | str,
            callback_function: Callable[..., object] | None = None,
        ) -> FlextResult[dict[str, object]]:
            """Create file system watcher for plugin hot reload.

            Args:
                watch_path: Path to watch for changes
                callback_function: Function to call on file changes

            Returns:
                FlextResult containing watcher configuration

            """
            try:
                path = Path(watch_path)
                if not path.exists():
                    return FlextResult[dict[str, object]].fail(
                        f"Watch path does not exist: {path}",
                    )

                watcher_config = {
                    "watch_path": str(path),
                    "callback": callback_function,
                    "watch_interval": FlextPluginUtilities.HotReloadManager.DEFAULT_WATCH_INTERVAL,
                    "last_modified": {},
                    "active": False,
                    "created_at": datetime.now(UTC).isoformat(),
                }

                return FlextResult[dict[str, object]].ok(dict(watcher_config))
            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"File watcher creation failed: {e}",
                )

        @staticmethod
        def detect_file_changes(
            watcher_config: dict[str, object],
        ) -> FlextResult[FlextPluginTypes.PluginCore.StringList]:
            """Detect file changes in watched directory.

            Args:
                watcher_config: Watcher configuration from create_file_watcher

            Returns:
                FlextResult containing list of changed files

            """
            try:
                watch_path = Path(str(watcher_config["watch_path"]))
                last_modified = watcher_config.get("last_modified", {})
                if not isinstance(last_modified, dict):
                    last_modified = {}
                changed_files = []

                for file_path in watch_path.rglob("*"):
                    if (
                        file_path.is_file()
                        and file_path.suffix
                        in FlextPluginUtilities.PluginDiscovery.PLUGIN_FILE_EXTENSIONS
                    ):
                        file_key = str(file_path)
                        current_mtime = file_path.stat().st_mtime

                        if (
                            file_key not in last_modified
                            or last_modified[file_key] != current_mtime
                        ):
                            changed_files.append(file_key)
                            last_modified[file_key] = current_mtime

                watcher_config["last_modified"] = last_modified
                return FlextResult[FlextPluginTypes.PluginCore.StringList].ok(
                    changed_files
                )
            except Exception as e:
                return FlextResult[FlextPluginTypes.PluginCore.StringList].fail(
                    f"File change detection failed: {e}",
                )

        @staticmethod
        def validate_reload_safety(plugin_path: Path) -> FlextResult[None]:
            """Validate that plugin can be safely reloaded.

            Args:
                plugin_path: Path to plugin being reloaded

            Returns:
                FlextResult indicating reload safety

            """
            try:
                # Check if plugin exists and is valid
                validation_result = (
                    FlextPluginUtilities.PluginDiscovery.validate_plugin_file(
                        plugin_path,
                    )
                )
                if validation_result.is_failure:
                    return FlextResult[None].fail(
                        f"Plugin validation failed: {validation_result.error}",
                    )

                # Additional reload-specific checks
                if plugin_path.suffix == ".py":
                    try:
                        # Try to compile the Python file
                        content = plugin_path.read_text(encoding="utf-8")
                        compile(content, str(plugin_path), "exec")
                    except SyntaxError as e:
                        return FlextResult[None].fail(
                            f"Python syntax error in plugin: {e}",
                        )

                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(f"Reload safety validation failed: {e}")

    class SecurityValidation:
        """Plugin security validation and sandboxing utilities."""

        ALLOWED_IMPORTS: ClassVar[FlextPluginTypes.PluginCore.StringList] = [
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
        DANGEROUS_OPERATIONS: ClassVar[FlextPluginTypes.PluginCore.StringList] = [
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
        def validate_plugin_security(
            plugin_content: str,
        ) -> FlextResult[dict[str, object]]:
            """Validate plugin security before execution.

            Args:
                plugin_content: Plugin source code content

            Returns:
                FlextResult containing security validation results

            """
            try:
                security_report: dict[str, object] = {
                    "safe": True,
                    "violations": [],
                    "warnings": [],
                    "analysis_time": datetime.now(UTC).isoformat(),
                }

                # Check for dangerous operations
                for (
                    dangerous_op
                ) in FlextPluginUtilities.SecurityValidation.DANGEROUS_OPERATIONS:
                    if dangerous_op in plugin_content:
                        security_report["safe"] = False
                        violations = security_report["violations"]
                        if isinstance(violations, list):
                            violations.append(
                                f"Dangerous operation detected: {dangerous_op}",
                            )

                # Check imports
                import_pattern = r"(?:from\s+(\w+)|import\s+(\w+))"
                imports = re.findall(import_pattern, plugin_content)
                for imp in imports:
                    module_name = imp[0] or imp[1]
                    if module_name and not any(
                        allowed in module_name
                        for allowed in FlextPluginUtilities.SecurityValidation.ALLOWED_IMPORTS
                    ):
                        warnings = security_report["warnings"]
                        if isinstance(warnings, list):
                            warnings.append(f"Potentially unsafe import: {module_name}")

                # Basic code analysis
                if "network" in plugin_content.lower() or "socket" in plugin_content:
                    warnings = security_report["warnings"]
                    if isinstance(warnings, list):
                        warnings.append("Plugin may perform network operations")

                if "file" in plugin_content.lower() or "write" in plugin_content:
                    warnings = security_report["warnings"]
                    if isinstance(warnings, list):
                        warnings.append("Plugin may perform file operations")

                return FlextResult[dict[str, object]].ok(dict(security_report))
            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Security validation failed: {e}",
                )

        @staticmethod
        def create_sandbox_config(
            plugin_name: str,
        ) -> FlextResult[dict[str, object]]:
            """Create sandbox configuration for plugin execution.

            Args:
                plugin_name: Name of the plugin to sandbox

            Returns:
                FlextResult containing sandbox configuration

            """
            try:
                sandbox_config = {
                    "plugin_name": plugin_name,
                    "max_memory_mb": FlextPluginUtilities.SecurityValidation.MAX_MEMORY_MB,
                    "max_execution_time": FlextPluginUtilities.SecurityValidation.MAX_EXECUTION_TIME_SECONDS,
                    "allowed_modules": FlextPluginUtilities.SecurityValidation.ALLOWED_IMPORTS.copy(),
                    "network_access": False,
                    "file_system_access": "read-only",
                    "environment_variables": {
                        "PYTHONDONTWRITEBYTECODE": "1",
                        "PYTHONUNBUFFERED": "1",
                    },
                    "created_at": datetime.now(UTC).isoformat(),
                }

                return FlextResult[dict[str, object]].ok(dict(sandbox_config))
            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Sandbox configuration creation failed: {e}",
                )

        @staticmethod
        def calculate_plugin_hash(plugin_content: str) -> FlextResult[str]:
            """Calculate secure hash of plugin content for integrity verification.

            Args:
                plugin_content: Plugin source code content

            Returns:
                FlextResult containing SHA-256 hash of plugin content

            """
            try:
                content_bytes = plugin_content.encode("utf-8")
                hash_object = hashlib.sha256(content_bytes)
                plugin_hash = hash_object.hexdigest()

                return FlextResult[str].ok(plugin_hash)
            except Exception as e:
                return FlextResult[str].fail(f"Plugin hash calculation failed: {e}")

    class ConfigurationManager:
        """Plugin configuration management utilities."""

        DEFAULT_CONFIG_FILE: ClassVar[str] = "plugin.yaml"
        CONFIG_SCHEMA_VERSION: ClassVar[str] = "1.0"
        MAX_CONFIG_SIZE_KB: ClassVar[int] = 1024

        @staticmethod
        def load_plugin_config(
            config_path: Path | str,
        ) -> FlextResult[dict[str, object]]:
            """Load plugin configuration from file.

            Args:
                config_path: Path to plugin configuration file

            Returns:
                FlextResult containing plugin configuration

            """
            try:
                path = Path(config_path)
                if not path.exists():
                    return FlextResult[dict[str, object]].fail(
                        f"Configuration file not found: {path}",
                    )

                # Check file size
                file_size_kb = path.stat().st_size / 1024
                if (
                    file_size_kb
                    > FlextPluginUtilities.ConfigurationManager.MAX_CONFIG_SIZE_KB
                ):
                    return FlextResult[dict[str, object]].fail(
                        f"Configuration file too large: {file_size_kb:.1f}KB",
                    )

                content = path.read_text(encoding="utf-8")

                if path.suffix in {".yaml", ".yml"}:
                    config = yaml.safe_load(content)
                elif path.suffix == ".json":
                    config = json.loads(content)
                else:
                    return FlextResult[dict[str, object]].fail(
                        f"Unsupported configuration format: {path.suffix}",
                    )

                # Validate schema version
                if (
                    isinstance(config, dict)
                    and config.get("schema_version")
                    != FlextPluginUtilities.ConfigurationManager.CONFIG_SCHEMA_VERSION
                ):
                    return FlextResult[dict[str, object]].fail(
                        f"Unsupported configuration schema version: {config.get('schema_version')}",
                    )

                return FlextResult[dict[str, object]].ok(config)
            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Configuration loading failed: {e}",
                )

        @staticmethod
        def validate_plugin_config(
            config: dict[str, object],
        ) -> FlextResult[None]:
            """Validate plugin configuration structure and values.

            Args:
                config: Plugin configuration to validate

            Returns:
                FlextResult indicating validation success or failure

            """
            try:
                required_fields = ["name", "version", "description", "entry_point"]
                for field in required_fields:
                    if field not in config:
                        return FlextResult[None].fail(
                            f"Missing required configuration field: {field}",
                        )

                # Validate plugin name
                name_validation = (
                    FlextPluginUtilities.PluginDiscovery.validate_plugin_name(
                        str(config["name"]),
                    )
                )
                if name_validation.is_failure:
                    return FlextResult[None].fail(name_validation.error)

                # Validate version format
                version_pattern = r"^\d+\.\d+\.\d+$"
                if not re.match(version_pattern, str(config["version"])):
                    return FlextResult[None].fail(
                        f"Invalid version format: {config['version']}. Expected semantic version (x.y.z)",
                    )

                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(f"Configuration validation failed: {e}")

        @staticmethod
        def merge_plugin_configs(
            base_config: dict[str, object],
            override_config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Merge plugin configurations with override precedence.

            Args:
                base_config: Base plugin configuration
                override_config: Configuration values to override

            Returns:
                FlextResult containing merged configuration

            """
            try:
                merged_config = base_config.copy()

                for key, value in override_config.items():
                    if (
                        isinstance(value, dict)
                        and key in merged_config
                        and isinstance(merged_config[key], dict)
                    ):
                        # Recursively merge nested dictionaries
                        if isinstance(merged_config[key], dict):
                            base_nested_config = dict(merged_config[key])
                        else:
                            base_nested_config = {}
                        override_value = value.copy() if isinstance(value, dict) else {}
                        nested_merge = FlextPluginUtilities.ConfigurationManager.merge_plugin_configs(
                            base_nested_config,
                            override_value,
                        )
                        if nested_merge.is_success:
                            merged_config[key] = nested_merge.unwrap()
                        else:
                            return FlextResult[dict[str, object]].fail(
                                f"Failed to merge nested config for key '{key}': {nested_merge.error}",
                            )
                    else:
                        merged_config[key] = value

                return FlextResult[dict[str, object]].ok(merged_config)
            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Configuration merge failed: {e}",
                )

    class PluginExecution:
        """Plugin execution and lifecycle management utilities."""

        DEFAULT_TIMEOUT_SECONDS: ClassVar[int] = 300
        MAX_RETRY_ATTEMPTS: ClassVar[int] = 3
        EXECUTION_LOG_LEVELS: ClassVar[FlextPluginTypes.PluginCore.StringList] = [
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
            args: list[object] | None = None,
            kwargs: dict[str, object] | None = None,
        ) -> FlextResult[object]:
            """Execute a specific function within a plugin module.

            Args:
                plugin_module: Loaded plugin module
                function_name: Name of function to execute
                args: Positional arguments for function
                kwargs: Keyword arguments for function

            Returns:
                FlextResult containing function execution result

            """
            try:
                if not hasattr(plugin_module, function_name):
                    return FlextResult[object].fail(
                        f"Function '{function_name}' not found in plugin module",
                    )

                plugin_function = getattr(plugin_module, function_name)
                if not callable(plugin_function):
                    return FlextResult[object].fail(
                        f"'{function_name}' is not callable",
                    )

                # Execute function with provided arguments
                execution_args = args or []
                execution_kwargs = kwargs or {}

                result = plugin_function(*execution_args, **execution_kwargs)
                return FlextResult[object].ok(result)
            except Exception as e:
                return FlextResult[object].fail(
                    f"Plugin function execution failed: {e}",
                )

        @staticmethod
        def load_plugin_module(plugin_path: Path | str) -> FlextResult[ModuleType]:
            """Load plugin module from file path.

            Args:
                plugin_path: Path to plugin Python file

            Returns:
                FlextResult containing loaded plugin module

            """
            try:
                path = Path(plugin_path)
                if not path.exists():
                    return FlextResult[ModuleType].fail(
                        f"Plugin file not found: {path}",
                    )

                if path.suffix != ".py":
                    return FlextResult[ModuleType].fail(
                        f"Only Python plugins are supported: {path}",
                    )

                # Load module using importlib
                spec = importlib.util.spec_from_file_location(path.stem, path)
                if spec is None or spec.loader is None:
                    return FlextResult[ModuleType].fail(
                        f"Failed to create module spec for: {path}",
                    )

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                return FlextResult[ModuleType].ok(module)
            except Exception as e:
                return FlextResult[ModuleType].fail(
                    f"Plugin module loading failed: {e}",
                )

        @staticmethod
        def validate_plugin_interface(
            plugin_module: ModuleType,
            required_functions: FlextPluginTypes.PluginCore.StringList,
        ) -> FlextResult[None]:
            """Validate that plugin module implements required interface.

            Args:
                plugin_module: Loaded plugin module
                required_functions: List of required function names

            Returns:
                FlextResult indicating interface validation success or failure

            """
            try:
                missing_functions = [
                    func_name
                    for func_name in required_functions
                    if not hasattr(plugin_module, func_name)
                ]

                if missing_functions:
                    return FlextResult[None].fail(
                        f"Plugin missing required functions: {missing_functions}",
                    )

                # Validate that required attributes are callable
                non_callable = [
                    func_name
                    for func_name in required_functions
                    if not callable(getattr(plugin_module, func_name))
                ]

                if non_callable:
                    return FlextResult[None].fail(
                        f"Plugin attributes not callable: {non_callable}",
                    )

                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(
                    f"Plugin interface validation failed: {e}",
                )

    class RegistryOperations:
        """Plugin registry management utilities."""

        REGISTRY_FILE_NAME: ClassVar[str] = "plugin_registry.json"
        REGISTRY_BACKUP_COUNT: ClassVar[int] = 5
        MAX_REGISTRY_SIZE_MB: ClassVar[int] = 10

        @staticmethod
        def load_plugin_registry(
            registry_path: Path | str,
        ) -> FlextResult[dict[str, object]]:
            """Load plugin registry from file.

            Args:
                registry_path: Path to plugin registry file

            Returns:
                FlextResult containing plugin registry data

            """
            try:
                path = Path(registry_path)
                if not path.exists():
                    # Create empty registry
                    registry = {
                        "version": "1.0",
                        "plugins": {},
                        "last_updated": datetime.now(UTC).isoformat(),
                        "created_at": datetime.now(UTC).isoformat(),
                    }
                    return FlextResult[dict[str, object]].ok(dict(registry))

                # Check file size
                file_size_mb = path.stat().st_size / (1024 * 1024)
                if (
                    file_size_mb
                    > FlextPluginUtilities.RegistryOperations.MAX_REGISTRY_SIZE_MB
                ):
                    return FlextResult[dict[str, object]].fail(
                        f"Registry file too large: {file_size_mb:.1f}MB",
                    )

                content = path.read_text(encoding="utf-8")
                registry = json.loads(content)

                return FlextResult[dict[str, object]].ok(registry)
            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Registry loading failed: {e}",
                )

        @staticmethod
        def save_plugin_registry(
            registry: dict[str, object],
            registry_path: Path | str,
        ) -> FlextResult[None]:
            """Save plugin registry to file with backup.

            Args:
                registry: Plugin registry data to save
                registry_path: Path to save registry file

            Returns:
                FlextResult indicating save success or failure

            """
            try:
                path = Path(registry_path)

                # Create backup if registry exists
                if path.exists():
                    backup_path = path.with_suffix(
                        f".backup.{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json",
                    )
                    path.rename(backup_path)

                    # Clean up old backups
                    FlextPluginUtilities.RegistryOperations.cleanup_registry_backups(
                        path.parent,
                    )

                # Update timestamp
                registry["last_updated"] = datetime.now(UTC).isoformat()

                # Save registry
                path.write_text(json.dumps(registry, indent=2), encoding="utf-8")

                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(f"Registry save failed: {e}")

        @staticmethod
        def register_plugin(
            registry: dict[str, object],
            plugin_metadata: FlextPluginModels.PluginMetadata,
        ) -> FlextResult[dict[str, object]]:
            """Register plugin in registry.

            Args:
                registry: Plugin registry data
                plugin_metadata: Metadata of plugin to register

            Returns:
                FlextResult containing updated registry

            """
            try:
                if "plugins" not in registry:
                    registry["plugins"] = {}

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

                plugins = registry["plugins"]
                if isinstance(plugins, dict):
                    plugins[plugin_metadata.name] = plugin_info

                return FlextResult[dict[str, object]].ok(registry)
            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Plugin registration failed: {e}",
                )

        @staticmethod
        def cleanup_registry_backups(
            registry_directory: Path,
        ) -> FlextResult[None]:
            """Clean up old registry backup files.

            Args:
                registry_directory: Directory containing registry backups

            Returns:
                FlextResult indicating cleanup success or failure

            """
            try:
                backup_pattern = f"{FlextPluginUtilities.RegistryOperations.REGISTRY_FILE_NAME.split('.')[0]}.backup.*.json"
                backup_files = list(registry_directory.glob(backup_pattern))

                # Sort by modification time and keep only recent backups
                backup_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

                for backup_file in backup_files[
                    FlextPluginUtilities.RegistryOperations.REGISTRY_BACKUP_COUNT :
                ]:
                    backup_file.unlink()

                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(f"Registry backup cleanup failed: {e}")

    # Pydantic 2.11+ field validators
    @field_validator("model_config")
    @classmethod
    def validate_model_config(cls, v: SettingsConfigDict) -> SettingsConfigDict:
        """Validate model configuration."""
        if not isinstance(v, dict):
            msg = "model_config must be a SettingsConfigDict instance"
            raise TypeError(msg)
        return v

    @model_validator(mode="after")
    def validate_utilities_configuration(self) -> FlextPluginUtilities:
        """Validate the complete utilities configuration."""
        # Validate that all nested classes are accessible
        required_classes = [
            "PluginDiscovery",
            "HotReloadManager",
            "SecurityValidation",
            "ConfigurationManager",
            "PluginExecution",
            "RegistryOperations",
        ]

        for class_name in required_classes:
            if not hasattr(self.__class__, class_name):
                msg = f"Missing required nested class: {class_name}"
                raise ValueError(msg)

        return self


__all__ = [
    "FlextPluginUtilities",
]
