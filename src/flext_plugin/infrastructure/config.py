"""Configuration for FLEXT-PLUGIN infrastructure.
Using flext-core configuration system - NO duplication.
"""

from __future__ import annotations

from pathlib import Path

from flext_core.config.base import BaseSettings
from flext_core.domain.constants import LogLevels


class PluginConfig(BaseSettings):
    """Plugin system configuration using flext-core BaseSettings."""

    # Plugin directories
    plugin_directory: str = "/var/lib/flext/plugins"
    plugin_cache_dir: str = "/var/cache/flext/plugins"
    plugin_config_dir: str = "/etc/flext/plugins"
    plugin_log_dir: str = "/var/log/flext/plugins"

    # Discovery settings
    discovery_timeout: int = 5  # seconds
    discovery_patterns: list[str] = ["*.py", "*.yaml", "*.yml"]
    auto_discovery: bool = True
    watch_directories: bool = True

    # Loading settings
    load_timeout: int = 30  # seconds
    max_concurrent_loads: int = 10
    lazy_loading: bool = True
    load_on_startup: bool = False

    # Hot reload settings
    hot_reload_enabled: bool = True
    hot_reload_poll_interval: int = 1000  # milliseconds
    hot_reload_state_backup_dir: str = "/tmp/flext_plugin_states"
    hot_reload_max_retries: int = 3
    hot_reload_grace_period: int = 5  # seconds

    # Registry settings
    plugin_registry_url: str = "https://plugins.flext-platform.com"
    plugin_registry_api_key: str | None = None
    plugin_verify_signatures: bool = True
    registry_timeout: int = 30  # seconds
    registry_cache_ttl: int = 3600  # seconds

    # Security settings
    plugin_sandbox_enabled: bool = True
    plugin_max_memory_mb: int = 512
    plugin_max_cpu_percent: int = 50
    plugin_execution_timeout: int = 300  # seconds
    allowed_imports: list[str] = ["requests", "pandas", "numpy", "json", "os", "sys"]
    restricted_imports: list[str] = ["subprocess", "os.system", "eval", "exec"]

    # Plugin lifecycle settings
    startup_timeout: int = 60  # seconds
    shutdown_timeout: int = 30  # seconds
    health_check_interval: int = 60  # seconds
    health_check_timeout: int = 5  # seconds

    # Logging settings
    log_level: str = LogLevels.DEFAULT
    log_format: str = "json"  # json, text
    log_plugin_executions: bool = True
    log_plugin_lifecycle: bool = True
    log_plugin_errors: bool = True

    # Performance settings
    enable_metrics: bool = True
    metrics_collection_interval: int = 30  # seconds
    enable_tracing: bool = True
    enable_profiling: bool = False  # Only for development

    # Dependency management
    auto_install_dependencies: bool = False
    dependency_resolver: str = "pip"  # pip, conda, poetry
    dependency_timeout: int = 300  # seconds

    # Plugin validation
    validate_plugins: bool = True
    validate_configuration: bool = True
    validate_dependencies: bool = True
    validate_permissions: bool = True

    # Error handling
    error_recovery_enabled: bool = True
    max_error_retries: int = 3
    error_recovery_delay: int = 5  # seconds

    # State management
    state_persistence_enabled: bool = True
    state_backup_interval: int = 300  # seconds
    state_retention_days: int = 7

    @property
    def plugin_directory_path(self) -> Path:
        """Get the plugin directory path.

        Returns:
            The plugin directory path as a Path object.

        """
        return Path(self.plugin_directory).expanduser()

    @property
    def plugin_cache_path(self) -> Path:
        """Get the plugin cache directory path.

        Returns:
            The plugin cache directory path as a Path object.

        """
        return Path(self.plugin_cache_dir).expanduser()

    @property
    def plugin_config_path(self) -> Path:
        """Get the plugin configuration directory path.

        Returns:
            The plugin configuration directory path as a Path object.

        """
        return Path(self.plugin_config_dir).expanduser()

    @property
    def plugin_log_path(self) -> Path:
        """Get the plugin log directory path.

        Returns:
            The plugin log directory path as a Path object.

        """
        return Path(self.plugin_log_dir).expanduser()

    @property
    def hot_reload_backup_path(self) -> Path:
        """Get the hot reload backup directory path.

        Returns:
            The hot reload backup directory path as a Path object.

        """
        return Path(self.hot_reload_state_backup_dir).expanduser()

    @property
    def is_development(self) -> bool:
        """Check if running in development mode.

        Returns:
            True if in development mode, False otherwise.

        """
        return self.log_level == LogLevels.DEBUG

    @property
    def is_production(self) -> bool:
        """Check if running in production mode.

        Returns:
            True if in production mode, False otherwise.

        """
        return not self.is_development

    @property
    def hot_reload_config(self) -> dict[str, int | bool | str]:
        """Get hot reload configuration.

        Returns:
            Dictionary containing hot reload configuration settings.

        """
        return {
            "enabled": self.hot_reload_enabled,
            "poll_interval": self.hot_reload_poll_interval,
            "backup_dir": self.hot_reload_state_backup_dir,
            "max_retries": self.hot_reload_max_retries,
            "grace_period": self.hot_reload_grace_period,
        }

    @property
    def security_config(self) -> dict[str, int | bool | list[str]]:
        """Get security configuration.

        Returns:
            Dictionary containing security configuration settings.

        """
        return {
            "sandbox_enabled": self.plugin_sandbox_enabled,
            "max_memory_mb": self.plugin_max_memory_mb,
            "max_cpu_percent": self.plugin_max_cpu_percent,
            "execution_timeout": self.plugin_execution_timeout,
            "allowed_imports": self.allowed_imports,
            "restricted_imports": self.restricted_imports,
        }

    @property
    def registry_config(self) -> dict[str, str | bool | int | None]:
        """Get registry configuration.

        Returns:
            Dictionary containing registry configuration settings.

        """
        return {
            "url": self.plugin_registry_url,
            "api_key": self.plugin_registry_api_key,
            "verify_signatures": self.plugin_verify_signatures,
            "timeout": self.registry_timeout,
            "cache_ttl": self.registry_cache_ttl,
        }

    def validate_plugin_configuration(self) -> list[str]:
        """Validate plugin configuration settings.

        Returns:
            List of validation error messages, empty if no errors.

        """
        errors = []

        # Validate timeouts
        if self.discovery_timeout < 1:
            errors.append("Discovery timeout must be at least 1 second")

        if self.load_timeout < 1:
            errors.append("Load timeout must be at least 1 second")

        if self.plugin_execution_timeout < 1:
            errors.append("Plugin execution timeout must be at least 1 second")

        # Validate resource limits
        if self.plugin_max_memory_mb < 1:
            errors.append("Plugin max memory must be at least 1 MB")

        if not 1 <= self.plugin_max_cpu_percent <= 100:
            errors.append("Plugin max CPU percent must be between 1 and 100")

        # Validate hot reload settings
        if self.hot_reload_enabled and self.hot_reload_poll_interval < 100:
            errors.append("Hot reload poll interval must be at least 100 milliseconds")

        if self.hot_reload_max_retries < 1:
            errors.append("Hot reload max retries must be at least 1")

        # Validate concurrency settings
        if self.max_concurrent_loads < 1:
            errors.append("Max concurrent loads must be at least 1")

        # Validate registry settings
        if self.plugin_registry_url and not self.plugin_registry_url.startswith(
            ("http://", "https://"),
        ):
            errors.append("Plugin registry URL must start with http:// or https://")

        # Validate directories
        try:
            plugin_dir = self.plugin_directory_path
            if not plugin_dir.exists():
                # Try to create directory
                plugin_dir.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError, ValueError) as e:
            errors.append(f"Cannot create plugin directory: {e}")

        try:
            cache_dir = self.plugin_cache_path
            if not cache_dir.exists():
                cache_dir.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError, ValueError) as e:
            errors.append(f"Cannot create plugin cache directory: {e}")

        # Validate log level
        if self.log_level not in LogLevels.ALL:
            errors.append(f"Invalid log level: {self.log_level}")

        return errors

    def get_plugin_paths(self) -> list[Path]:
        """Get all plugin search paths.

        Returns:
            List of Path objects for plugin discovery.

        """
        paths = [self.plugin_directory_path]

        # Add current directory for development
        if self.is_development:
            paths.append(Path.cwd() / "plugins")

        # Add user plugin directory
        user_plugin_dir = Path.home() / ".flext" / "plugins"
        if user_plugin_dir.exists():
            paths.append(user_plugin_dir)

        return paths

    def get_environment_variables(self) -> dict[str, str]:
        """Get environment variables for plugin system.

        Returns:
            Dictionary of environment variables and their values.

        """
        return {
            "FLEXT_PLUGIN_DIR": str(self.plugin_directory_path),
            "FLEXT_PLUGIN_CACHE": str(self.plugin_cache_path),
            "FLEXT_PLUGIN_CONFIG": str(self.plugin_config_path),
            "FLEXT_PLUGIN_LOG": str(self.plugin_log_path),
            "FLEXT_HOT_RELOAD": str(self.hot_reload_enabled).lower(),
            "FLEXT_SANDBOX": str(self.plugin_sandbox_enabled).lower(),
            "FLEXT_LOG_LEVEL": self.log_level,
        }
