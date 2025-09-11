#!/usr/bin/env python3
"""Plugin Configuration Example - Demonstrates advanced plugin configuration patterns.

This example shows how to create plugins with complex configurations,
including database connections, environment-specific settings, and validation.

Usage:
    python examples/02_plugin_configuration.py

Docker Usage:
    # Start services: docker-compose up -d postgres
    # Run with database: python examples/02_plugin_configuration.py --with-db
"""

from __future__ import annotations

import sys
from typing import cast

from flext_core import FlextTypes

from flext_plugin import (
    PluginType,
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
)


def create_database_plugin_config() -> FlextTypes.Core.Dict:
    """Create configuration for a database plugin."""
    return {
        "database": {
            "host": "localhost",
            "port": 5432,
            "database": "flext_dev",
            "username": "flext",
            "password": "flext_pass",  # In production, use environment variables
            "pool_size": 5,
            "pool_recycle": 3600,
        },
        "retry_config": {
            "max_retries": 3,
            "retry_delay": 1.0,
            "exponential_backoff": True,
        },
        "logging": {
            "level": "INFO",
            "format": "json",
            "include_sql": False,
        },
        "features": {
            "enable_metrics": True,
            "enable_tracing": True,
            "enable_health_checks": True,
        },
    }


def create_ldap_plugin_config() -> FlextTypes.Core.Dict:
    """Create configuration for an LDAP plugin."""
    return {
        "ldap": {
            "server": "localhost",
            "port": 389,
            "base_dn": "dc=flext,dc=dev",
            "bind_dn": "cn=readonly,dc=flext,dc=dev",
            "bind_password": "readonly",
            "use_ssl": False,
            "timeout": 30,
        },
        "search": {
            "user_filter": "(objectClass=person)",
            "group_filter": "(objectClass=group)",
            "attributes": ["cn", "mail", "memberOf"],
            "page_size": 1000,
        },
        "cache": {
            "enabled": True,
            "ttl_seconds": 300,
            "max_entries": 10000,
        },
    }


def main() -> None:
    """Demonstrate plugin configuration patterns."""
    print("FLEXT Plugin Configuration Example")
    print("=" * 50)

    # 1. Create a database plugin with complex configuration
    db_config = create_database_plugin_config()

    db_plugin = create_flext_plugin(
        name="postgres-connector",
        version="2.1.0",
        config={
            "description": "PostgreSQL database connector plugin",
            "author": "FLEXT Team",
            "plugin_type": PluginType.DATABASE,
            "tags": ["database", "postgres", "sql"],
            **db_config,  # Merge configuration
        },
    )

    print(f"Database plugin: {db_plugin.name} v{db_plugin.plugin_version}")
    cast("FlextTypes.Core.Dict", db_config["database"])

    # 2. Create LDAP plugin with service configuration
    ldap_config = create_ldap_plugin_config()

    ldap_plugin = create_flext_plugin(
        name="ldap-directory",
        version="1.5.0",
        config={
            "description": "LDAP directory service plugin",
            "author": "FLEXT Team",
            "plugin_type": PluginType.AUTHENTICATION,
            "tags": ["ldap", "directory", "auth"],
            **ldap_config,
        },
    )

    print(f"LDAP plugin: {ldap_plugin.name} v{ldap_plugin.plugin_version}")
    cast("FlextTypes.Core.Dict", ldap_config["ldap"])

    # 3. Create standalone plugin configuration entity
    standalone_config = create_flext_plugin_config(
        plugin_name="api-gateway",
        config_data={
            "routes": {
                "/api/v1/health": {"method": "GET", "auth": False},
                "/api/v1/plugins": {"method": "GET", "auth": True},
                "/api/v1/metrics": {"method": "GET", "auth": True},
            },
            "middleware": ["cors", "rate_limit", "auth"],
            "rate_limiting": {
                "requests_per_minute": 100,
                "burst_size": 10,
            },
        },
    )

    print(f"Config for: {standalone_config.plugin_name}")
    standalone_config.config_data.get("routes", {})

    # 4. Create plugin metadata
    metadata = create_flext_plugin_metadata(
        plugin_name="data-processor",
        metadata={
            "tags": ["etl", "transform", "batch"],
            "categories": ["data-processing", "transformation"],
            "homepage_url": "https://github.com/flext-sh/flext-plugin",
            "documentation_url": "https://docs.flext.sh/plugins/data-processor",
            "license": "MIT",
            "compatibility": {
                "python": ">=3.13",
                "flext": ">=0.9.0",
            },
            "performance": {
                "max_memory_mb": 512,
                "max_cpu_percent": 80,
                "batch_size": 1000,
            },
        },
    )

    print(f"Metadata for: {metadata.plugin_name}")

    # 5. Demonstrate configuration validation
    print("Configuration validation...")

    plugins_to_validate = [db_plugin, ldap_plugin]
    for plugin in plugins_to_validate:
        validation_result = plugin.validate_business_rules()
        if validation_result.success:
            pass

    print("Configuration example completed successfully")


def test_database_connection() -> bool:
    """Test database connectivity (requires Docker services)."""
    try:
        # This would normally test actual database connection
        # For now, just validate configuration structure
        config = create_database_plugin_config()
        required_keys = ["database", "retry_config", "logging", "features"]
        return all(key in config for key in required_keys)
    except Exception:
        return False


if __name__ == "__main__":
    main()

    # Optional: Test database connection if --with-db flag provided
    if len(sys.argv) > 1 and "--with-db" in sys.argv and test_database_connection():
        pass
