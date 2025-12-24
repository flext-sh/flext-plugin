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

from flext import FlextContainer
from flext_plugin import (
    FlextPluginApi,
    FlextPluginConstants,
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
    # 1. Create a database plugin with complex configuration
    db_config = create_database_plugin_config()

    # Initialize plugin API
    container = FlextContainer()
    FlextPluginApi(container)

    print("Plugin configuration patterns demonstration")
    print(f"Available plugin types: {FlextPluginConstants.Types.ALL_PLUGIN_TYPES}")
    print(f"Plugin status constants: {FlextPluginConstants.Lifecycle.STATUS_ACTIVE}")

    print(f"Database config created: {db_config}")

    # 2. Create LDAP plugin with service configuration
    ldap_config = create_ldap_plugin_config()

    print(f"LDAP config created: {ldap_config}")
    print("✅ Plugin configuration demonstration complete")


if __name__ == "__main__":
    main()
