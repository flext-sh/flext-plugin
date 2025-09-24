#!/usr/bin/env python3
"""Docker Integration Example - Demonstrates plugin configuration with actual Docker services.

This example shows how to create plugins that connect to actual Docker services
running in the FLEXT development environment. It tests real database and LDAP
connectivity using the Docker Compose setup.

Prerequisites:
    # Start Docker services first:
    cd /home/marlonsc/flext/docker
    docker-compose up -d postgres redis openldap

Usage:
    python examples/03_docker_integration.py
    python examples/03_docker_integration.py --test-connections
"""

from __future__ import annotations

import socket
import sys
from typing import cast

from flext_core import FlextTypes
from flext_plugin import FlextPluginEntity, PluginType, create_flext_plugin


def check_service_availability(host: str, port: int, timeout: float = 5.0) -> bool:
    """Check if a service is available on host:port.

    Args:
      host: Service hostname
      port: Service port
      timeout: Connection timeout in seconds

    Returns:
      True if service is reachable, False otherwise

    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def create_docker_postgres_plugin() -> tuple[FlextPluginEntity, FlextTypes.Core.Dict]:
    """Create a PostgreSQL plugin configured for Docker services."""
    config: FlextTypes.Core.Dict = {
        "database": {
            "host": "localhost",
            "port": 5434,  # Actual Docker container port (flext-postgres-test-1)
            "database": "flext_db",  # Matches docker-compose.yml POSTGRES_DB
            "username": "flext",  # Matches docker-compose.yml POSTGRES_USER
            "password": "flext_dev_password",  # Matches POSTGRES_PASSWORD
            "pool_size": 10,
            "pool_recycle": 3600,
            "pool_pre_ping": True,
        },
        "connection": {
            "ssl_mode": "prefer",
            "application_name": "flext-plugin-docker-integration",
            "connect_timeout": 30,
            "command_timeout": 60,
        },
        "performance": {
            "statement_timeout": 30000,  # 30 seconds
            "lock_timeout": 5000,  # 5 seconds
            "idle_in_transaction_session_timeout": 60000,  # 1 minute
        },
        "monitoring": {
            "enable_metrics": True,
            "enable_query_logging": False,  # Disable in production
            "log_slow_queries": True,
            "slow_query_threshold": 1000,  # 1 second
        },
    }

    plugin = create_flext_plugin(
        name="docker-postgres-connector",
        version="2.1.0",
        config={
            "description": "PostgreSQL connector for Docker development environment",
            "author": "FLEXT Team",
            "plugin_type": PluginType.DATABASE,
            "environment": "development",
            "docker_compatible": True,
            **config,
        },
    )

    return plugin, config


def create_docker_redis_plugin() -> tuple[FlextPluginEntity, FlextTypes.Core.Dict]:
    """Create a Redis plugin configured for Docker services."""
    config: FlextTypes.Core.Dict = {
        "redis": {
            "host": "localhost",
            "port": 6381,  # Actual Docker container port (flext-redis-test-1)
            "password": "flext_redis_password",  # Matches docker-compose.yml
            "db": 0,
            "socket_timeout": 30,
            "socket_connect_timeout": 30,
            "socket_keepalive": True,
            "socket_keepalive_options": {},
        },
        "connection_pool": {
            "max_connections": 50,
            "retry_on_timeout": True,
            "health_check_interval": 30,
        },
        "cache": {
            "default_ttl": 300,  # 5 minutes
            "key_prefix": "flext:plugin:",
            "serializer": "json",
            "compression": False,
        },
        "monitoring": {
            "enable_metrics": True,
            "track_commands": True,
            "log_slow_commands": True,
            "slow_command_threshold": 100,  # 100ms
        },
    }

    plugin = create_flext_plugin(
        name="docker-redis-cache",
        version="1.2.0",
        config={
            "description": "Redis cache service for Docker development environment",
            "author": "FLEXT Team",
            "plugin_type": PluginType.DATABASE,
            "environment": "development",
            "docker_compatible": True,
            **config,
        },
    )

    return plugin, config


def create_docker_ldap_plugin() -> tuple[FlextPluginEntity, FlextTypes.Core.Dict]:
    """Create an LDAP plugin configured for Docker services."""
    config: FlextTypes.Core.Dict = {
        "ldap": {
            "server": "localhost",
            "port": 389,
            "base_dn": "dc=flext,dc=dev",  # Matches LDAP_DOMAIN
            "bind_dn": "cn=readonly,dc=flext,dc=dev",
            "bind_password": "readonly",  # Matches LDAP_READONLY_USER_PASSWORD
            "use_ssl": False,
            "use_tls": False,
            "timeout": 30,
            "network_timeout": 10,
        },
        "REDACTED_LDAP_BIND_PASSWORD": {
            "REDACTED_LDAP_BIND_PASSWORD_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=flext,dc=dev",
            "REDACTED_LDAP_BIND_PASSWORD_password": "flext_ldap_REDACTED_LDAP_BIND_PASSWORD",  # Matches LDAP_ADMIN_PASSWORD
        },
        "search": {
            "user_filter": "(objectClass=inetOrgPerson)",
            "group_filter": "(objectClass=groupOfNames)",
            "attributes": ["cn", "mail", "memberOf", "uid", "sn", "givenName"],
            "page_size": 1000,
            "size_limit": 0,  # No limit
            "time_limit": 30,  # 30 seconds
        },
        "connection_pool": {
            "pool_size": 5,
            "pool_lifetime": 3600,  # 1 hour
            "retry_max": 3,
            "retry_delay": 1.0,
        },
        "monitoring": {
            "enable_metrics": True,
            "log_bind_attempts": True,
            "log_search_operations": True,
        },
    }

    plugin = create_flext_plugin(
        name="docker-ldap-directory",
        version="1.5.0",
        config={
            "description": "LDAP directory service for Docker development environment",
            "author": "FLEXT Team",
            "plugin_type": PluginType.AUTHENTICATION,
            "environment": "development",
            "docker_compatible": True,
            **config,
        },
    )

    return plugin, config


def test_service_connections(*, test_connections: bool) -> dict[str, bool | None]:
    """Test connectivity to Docker services."""
    services: dict[str, tuple[str, int]] = {
        "PostgreSQL": ("localhost", 5434),  # Actual Docker container port
        "Redis": ("localhost", 6381),  # Actual Docker container port
        "LDAP": ("localhost", 389),  # LDAP service (disabled - has issues)
    }

    results: dict[str, bool | None] = {}

    for service_name, (host, port) in services.items():
        if test_connections:
            available = check_service_availability(host, port)
            results[service_name] = available
        else:
            results[service_name] = None

    return results


def main() -> None:
    """Demonstrate Docker-integrated plugin configuration."""
    print("FLEXT Plugin Docker Integration Example")
    print("=" * 50)

    # Check command line arguments
    test_connections = len(sys.argv) > 1 and "--test-connections" in sys.argv

    # Test service connectivity
    connectivity_results = test_service_connections(test_connections=test_connections)

    # 1. Create PostgreSQL plugin
    print("\nCreating Docker PostgreSQL plugin")
    postgres_plugin, postgres_config = create_docker_postgres_plugin()

    cast("FlextTypes.Core.Dict", postgres_config["database"])
    cast("FlextTypes.Core.Dict", postgres_config["monitoring"])

    # Validate PostgreSQL plugin
    postgres_validation = postgres_plugin.validate_business_rules()
    if postgres_validation.success:
        print("PostgreSQL plugin validation passed")
        # Test activation
        postgres_activation = postgres_plugin.activate()
        if postgres_activation:
            pass

    # 2. Create Redis plugin
    print("Creating Docker Redis plugin")
    redis_plugin, redis_config = create_docker_redis_plugin()

    cast("FlextTypes.Core.Dict", redis_config["cache"])
    cast("FlextTypes.Core.Dict", redis_config["connection_pool"])

    # Validate Redis plugin
    redis_validation = redis_plugin.validate_business_rules()
    if redis_validation.success:
        print("Redis plugin validation passed")
        # Test activation
        redis_activation = redis_plugin.activate()
        if redis_activation:
            pass

    # 3. Create LDAP plugin
    print("Creating Docker LDAP plugin")
    ldap_plugin, ldap_config = create_docker_ldap_plugin()

    cast("FlextTypes.Core.Dict", ldap_config["ldap"])
    cast("FlextTypes.Core.Dict", ldap_config["connection_pool"])

    # Validate LDAP plugin
    ldap_validation = ldap_plugin.validate_business_rules()
    if ldap_validation.success:
        print("LDAP plugin validation passed")
        # Test activation
        ldap_activation = ldap_plugin.activate()
        if ldap_activation:
            pass

    # 4. Summary
    plugins = [
        ("PostgreSQL", postgres_plugin, connectivity_results.get("PostgreSQL")),
        ("Redis", redis_plugin, connectivity_results.get("Redis")),
        ("LDAP", ldap_plugin, connectivity_results.get("LDAP")),
    ]

    if test_connections:
        print("\nService Connectivity Check:")
        for service_name, _plugin, connectivity in plugins:
            status = "Available" if connectivity else "Unavailable"
            print(f"  {service_name}: {status}")

    print("\nDocker Integration example completed successfully")


if __name__ == "__main__":
    main()
