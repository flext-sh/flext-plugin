"""Simple API for FLEXT plugin system setup and configuration.

Provides a simple interface for setting up the plugin system.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from flext_core.domain.shared_types import Environment, LogLevel
from flext_core.domain.types import ServiceResult

from flext_plugin.config import PluginSettings

if TYPE_CHECKING:
    from flext_plugin.types import ConfigurationDict


def setup_plugin_system(
    settings: PluginSettings | None = None,
) -> ServiceResult[PluginSettings]:
    """Setup the plugin system with configuration."""
    try:
        # Setup logging using flext-infrastructure.monitoring.flext-observability
        try:
            from flext_core.domain.shared_models import LogLevel
            from flext_observability.logging import LoggingConfig, setup_logging

            log_level_str = settings.log_level if settings else "INFO"
            log_level = (
                LogLevel(log_level_str)
                if hasattr(LogLevel, log_level_str)
                else LogLevel.INFO
            )
            log_config = LoggingConfig(
                log_level=log_level,
                json_logs=False,
            )
            setup_logging(log_config)
        except ImportError:
            # Fallback to basic logging configuration
            logging.basicConfig(
                level=getattr(logging, settings.log_level if settings else "INFO"),
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )

        if settings is None:
            settings = create_development_plugin_config()

        # Ensure plugin directories exist
        settings.plugin_directory.mkdir(parents=True, exist_ok=True)
        settings.registry_cache_dir.mkdir(parents=True, exist_ok=True)

        if settings.hot_reload_enabled:
            settings.hot_reload_state_backup_dir.mkdir(parents=True, exist_ok=True)

        return ServiceResult.ok(settings)

    except (OSError, ImportError, RuntimeError, ValueError) as e:
        return ServiceResult.fail(f"Failed to setup plugin system: {e}")


def create_development_plugin_config(**overrides: ConfigurationDict) -> PluginSettings:
    """Create development plugin configuration with defaults."""
    # Create base settings with all required fields
    settings = PluginSettings(
        project_name="flext-infrastructure.plugins.flext-plugin",
        project_version="0.7.0",
        plugin_directory=Path.cwd() / "plugins",
        discovery_timeout=5,
        discovery_pattern="*.py",
        load_timeout=30,
        max_concurrent_loads=10,
        enable_lazy_loading=True,
        cache_loaded_plugins=True,
        hot_reload_enabled=True,
        hot_reload_poll_interval=500,
        verify_signatures=False,
        health_check_enabled=True,
        health_check_interval=10,
        log_plugin_events=True,
        log_level=LogLevel.DEBUG,
        environment=Environment.DEVELOPMENT,
        debug=True,
    )

    # Apply overrides for supported fields only
    supported_fields = {name for name, field in PluginSettings.model_fields.items()}

    for key, value in overrides.items():
        if key in supported_fields:
            setattr(settings, key, value)

    return settings


def create_production_plugin_config(**overrides: ConfigurationDict) -> PluginSettings:
    """Create production plugin configuration with defaults."""
    # Create base settings with all required fields
    settings = PluginSettings(
        project_name="flext-infrastructure.plugins.flext-plugin",
        project_version="0.7.0",
        plugin_directory=Path("/opt/flext/plugins"),
        discovery_timeout=10,
        discovery_pattern="*.py",
        load_timeout=60,
        max_concurrent_loads=5,
        enable_lazy_loading=False,
        cache_loaded_plugins=True,
        hot_reload_enabled=False,
        hot_reload_poll_interval=1000,
        verify_signatures=True,
        health_check_enabled=True,
        health_check_interval=30,
        log_plugin_events=True,
        log_level=LogLevel.INFO,
        environment=Environment.PRODUCTION,
        debug=False,
    )

    # Apply overrides for supported fields only
    supported_fields = {name for name, field in PluginSettings.model_fields.items()}

    for key, value in overrides.items():
        if key in supported_fields:
            setattr(settings, key, value)

    return settings


def create_testing_plugin_config(**overrides: ConfigurationDict) -> PluginSettings:
    """Create testing plugin configuration with defaults."""
    # Create base settings with all required fields
    settings = PluginSettings(
        project_name="flext-infrastructure.plugins.flext-plugin",
        project_version="0.7.0",
        plugin_directory=Path.cwd() / "test_plugins",
        discovery_timeout=1,
        discovery_pattern="*.py",
        load_timeout=5,
        max_concurrent_loads=2,
        enable_lazy_loading=False,
        cache_loaded_plugins=False,
        hot_reload_enabled=False,
        hot_reload_poll_interval=1000,
        verify_signatures=False,
        health_check_enabled=False,
        health_check_interval=60,
        log_plugin_events=False,
        log_level=LogLevel.WARNING,
        environment=Environment.TEST,
        debug=False,
    )

    # Apply overrides for supported fields only
    supported_fields = {name for name, field in PluginSettings.model_fields.items()}

    for key, value in overrides.items():
        if key in supported_fields:
            setattr(settings, key, value)

    return settings


def create_minimal_plugin_config(**overrides: ConfigurationDict) -> PluginSettings:
    """Create minimal plugin configuration with defaults."""
    # Create base settings with minimal required fields
    settings = PluginSettings(
        project_name="flext-infrastructure.plugins.flext-plugin",
        project_version="0.7.0",
        plugin_directory=Path.cwd() / "plugins",
        discovery_timeout=5,
        discovery_pattern="*.py",
        load_timeout=30,
        max_concurrent_loads=1,
        enable_lazy_loading=False,
        cache_loaded_plugins=False,
        hot_reload_enabled=False,
        hot_reload_poll_interval=1000,
        verify_signatures=False,
        health_check_enabled=False,
        health_check_interval=60,
        log_plugin_events=False,
        log_level=LogLevel.WARNING,
        environment=Environment.DEVELOPMENT,
        debug=False,
    )

    # Apply overrides for supported fields only
    supported_fields = {name for name, field in PluginSettings.model_fields.items()}

    for key, value in overrides.items():
        if key in supported_fields:
            setattr(settings, key, value)

    return settings


# Export convenience functions
__all__ = [
    "create_development_plugin_config",
    "create_minimal_plugin_config",
    "create_production_plugin_config",
    "create_testing_plugin_config",
    "setup_plugin_system",
]
