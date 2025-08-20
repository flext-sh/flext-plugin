#!/usr/bin/env python3
"""Plugin Configuration Example - Demonstrates advanced plugin configuration patterns.

This example shows how to create plugins with complex configurations,
including database connections, environment-specific settings, and validation.

Usage:
    python examples/plugin_configuration_example.py

Docker Usage:
    # Start services: docker-compose up -d postgres
    # Run with database: python examples/plugin_configuration_example.py --with-db
"""

from __future__ import annotations

import sys
from typing import cast

from flext_plugin import (
    PluginType,
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
)


def create_database_plugin_config() -> dict[str, object]:
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


def create_ldap_plugin_config() -> dict[str, object]:
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
    print("=== FLEXT Plugin Configuration Example ===")

    # 1. Create a database plugin with complex configuration
    print("\n1. Creating database plugin with configuration...")
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

    print(f"   Database plugin: {db_plugin.name} v{db_plugin.plugin_version}")
    print(f"   Type: {db_config.get('plugin_type', 'N/A')}")
    database_config = cast("dict[str, object]", db_config["database"])
    print(f"   Database: {database_config['database']}")
    print(f"   Pool size: {database_config['pool_size']}")

    # 2. Create LDAP plugin with service configuration
    print("\n2. Creating LDAP plugin with service configuration...")
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

    print(f"   LDAP plugin: {ldap_plugin.name} v{ldap_plugin.plugin_version}")
    ldap_server_config = cast("dict[str, object]", ldap_config["ldap"])
    print(f"   Server: {ldap_server_config['server']}:{ldap_server_config['port']}")
    print(f"   Base DN: {ldap_server_config['base_dn']}")

    # 3. Create standalone plugin configuration entity
    print("\n3. Creating standalone plugin configuration...")
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

    print(f"   Config for: {standalone_config.plugin_name}")
    routes_data = standalone_config.config_data.get("routes", {})
    print(
        f"   Routes configured: {len(cast('dict[str, object]', routes_data))}",
    )
    print(f"   Middleware: {standalone_config.config_data.get('middleware', [])}")

    # 4. Create plugin metadata
    print("\n4. Creating plugin metadata...")
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

    print(f"   Metadata for: {metadata.plugin_name}")
    print(f"   Tags: {metadata.tags}")
    print(f"   Categories: {metadata.categories}")
    print(f"   License: {metadata.license_info}")

    # 5. Demonstrate configuration validation
    print("\n5. Configuration validation...")

    plugins_to_validate = [db_plugin, ldap_plugin]
    for plugin in plugins_to_validate:
        validation_result = plugin.validate_business_rules()
        if validation_result.success:
            print(f"   ✅ {plugin.name}: Configuration valid")
        else:
            print(f"   ❌ {plugin.name}: {validation_result.error}")

    print("\n=== Configuration example completed successfully ===")


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
    if len(sys.argv) > 1 and "--with-db" in sys.argv:
        print("\n=== Testing Database Connection ===")
        if test_database_connection():
            print("✅ Database configuration structure valid")
        else:
            print("❌ Database configuration validation failed")
