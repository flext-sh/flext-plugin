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

from flext_core import FlextContainer
from flext_plugin import FlextPluginApi, t


def create_database_plugin_config() -> t.RecursiveContainerMapping:
    """Create configuration for a database plugin."""
    return {
        "database": {
            "host": "localhost",
            "port": 5432,
            "database": "flext_dev",
            "username": "flext",
            "password": "flext_pass",
            "pool_size": 5,
            "pool_recycle": 3600,
        },
        "retry_config": {
            "max_retries": 3,
            "retry_delay": 1.0,
            "exponential_backoff": True,
        },
        "logging": {"level": "INFO", "format": "json", "include_sql": False},
        "features": {
            "enable_metrics": True,
            "enable_tracing": True,
            "enable_health_checks": True,
        },
    }


def create_ldap_plugin_config() -> t.RecursiveContainerMapping:
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
        "cache": {"enabled": True, "ttl_seconds": 300, "max_entries": 10000},
    }


def main() -> None:
    """Demonstrate plugin configuration patterns."""
    create_database_plugin_config()
    container = FlextContainer()
    FlextPluginApi(container)
    create_ldap_plugin_config()


if __name__ == "__main__":
    main()
