"""Simple API for FLEXT plugin system setup and configuration.

Provides a simple interface for setting up the plugin system.
"""

from __future__ import annotations

import logging
from pathlib import Path

from flext_core.domain.types import ServiceResult
from flext_plugin.config import PluginSettings
from flext_plugin.types import ConfigurationDict


def setup_plugin_system(settings: PluginSettings | None = None) -> ServiceResult[PluginSettings]:
    """Setup the plugin system with configuration."""
    try:
        # Setup logging using flext-observability
        try:
            from flext_observability.logging import setup_logging
            setup_logging(
                log_level=settings.log_level if settings else "INFO",
                json_logs=False,
            )
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
    defaults = {
        "plugin_directory": Path.cwd() / "plugins",
        "hot_reload_enabled": True,
        "hot_reload_poll_interval": 500,
        "enable_sandbox": False,
        "verify_signatures": False,
        "log_level": "DEBUG",
        "enable_profiling": True,
        "profiling_sample_rate": 0.5,
        "health_check_interval": 10,
        "registry_enabled": False,
    }

    # Override with provided values
    defaults.update(overrides)

    return PluginSettings(**defaults)


def create_production_plugin_config(**overrides: ConfigurationDict) -> PluginSettings:
    """Create production plugin configuration with defaults."""
    defaults = {
        "plugin_directory": Path("/opt/flext/plugins"),
        "hot_reload_enabled": False,
        "enable_sandbox": True,
        "verify_signatures": True,
        "log_level": "INFO",
        "enable_profiling": False,
        "health_check_interval": 30,
        "registry_enabled": True,
        "max_memory_mb": 1024,
        "max_cpu_percent": 75,
        "execution_timeout": 120,
    }

    # Override with provided values
    defaults.update(overrides)

    return PluginSettings(**defaults)


def create_testing_plugin_config(**overrides: ConfigurationDict) -> PluginSettings:
    """Create testing plugin configuration with defaults."""
    defaults = {
        "plugin_directory": Path("/tmp/test_plugins"),
        "hot_reload_enabled": False,
        "enable_sandbox": False,
        "verify_signatures": False,
        "log_level": "WARNING",
        "enable_profiling": False,
        "health_check_enabled": False,
        "registry_enabled": False,
        "discovery_timeout": 1,
        "load_timeout": 5,
        "execution_timeout": 10,
    }

    # Override with provided values
    defaults.update(overrides)

    return PluginSettings(**defaults)


def create_minimal_plugin_config(**overrides: ConfigurationDict) -> PluginSettings:
    """Create minimal plugin configuration with defaults."""
    defaults = {
        "hot_reload_enabled": False,
        "enable_sandbox": False,
        "verify_signatures": False,
        "registry_enabled": False,
        "health_check_enabled": False,
        "enable_metrics": False,
        "enable_profiling": False,
        "log_plugin_events": False,
        "log_plugin_executions": False,
    }

    # Override with provided values
    defaults.update(overrides)

    return PluginSettings(**defaults)


# Export convenience functions
__all__ = [
    "create_development_plugin_config",
    "create_minimal_plugin_config",
    "create_production_plugin_config",
    "create_testing_plugin_config",
    "setup_plugin_system",
]
