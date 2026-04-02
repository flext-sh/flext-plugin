"""FLEXT Plugin Docker Integration Example.

This example demonstrates real-world plugin configuration with Docker services integration.
Shows how to create production-ready plugins that work with Docker Compose services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import socket
import sys

from flext_core import FlextContainer
from flext_plugin import FlextPluginApi, FlextPluginConstants, FlextPluginModels, t


def check_service_availability(host: str, port: int, timeout: float = 5.0) -> bool:
    """Check if a network service is available."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except OSError:
        return False


def create_docker_postgres_plugin() -> tuple[
    FlextPluginModels.Plugin.Plugin,
    t.ContainerMapping,
]:
    """Create a Docker-compatible PostgreSQL plugin using domain library patterns."""
    postgres_config: t.ContainerMapping = {
        "host": "localhost",
        "port": 5432,
        "database": "flext_db",
        "user": "flext",
        "password": "flext_dev_password",
        "ssl_mode": "prefer",
        "connection_timeout": 10,
        "max_connections": 20,
        "connection_pool": True,
    }
    postgres_plugin = FlextPluginModels.Plugin.Plugin(
        name="docker-postgres-connector",
        plugin_version="1.0.0",
        description="PostgreSQL database connector for Docker environment",
        author="FLEXT Team",
        plugin_type=FlextPluginConstants.Plugin.PluginType.DATABASE.value,
        is_enabled=True,
        metadata={"dependencies": ["psycopg2-binary"]},
    )
    return (postgres_plugin, postgres_config)


def create_docker_redis_plugin() -> tuple[
    FlextPluginModels.Plugin.Plugin,
    t.ContainerMapping,
]:
    """Create a Docker-compatible Redis plugin using domain library patterns."""
    redis_config: t.ContainerMapping = {
        "host": "localhost",
        "port": 6379,
        "password": "flext_redis_password",
        "db": 0,
        "decode_responses": True,
        "socket_timeout": 5,
        "socket_connect_timeout": 5,
        "socket_keepalive": True,
        "socket_keepalive_options": {str(socket.TCP_KEEPIDLE): 60},
        "health_check_interval": 30,
    }
    redis_plugin = FlextPluginModels.Plugin.Plugin(
        name="docker-redis-cache",
        plugin_version="1.0.0",
        description="Redis cache connector for Docker environment",
        author="FLEXT Team",
        plugin_type=FlextPluginConstants.Plugin.PluginType.DATABASE.value,
        is_enabled=True,
        metadata={"dependencies": ["redis"]},
    )
    return (redis_plugin, redis_config)


def create_docker_ldap_plugin() -> tuple[
    FlextPluginModels.Plugin.Plugin,
    t.ContainerMapping,
]:
    """Create a Docker-compatible LDAP plugin using domain library patterns."""
    ldap_config: t.ContainerMapping = {
        "host": "localhost",
        "port": 389,
        "use_ssl": False,
        "user_dn": "cn=flext_ldap_REDACTED_LDAP_BIND_PASSWORD,dc=flext,dc=dev",
        "password": "flext_ldap_password",
        "base_dn": "dc=flext,dc=dev",
        "search_timeout": 10,
        "connection_timeout": 5,
        "pool_size": 10,
        "pool_lifetime": 3600,
    }
    ldap_plugin = FlextPluginModels.Plugin.Plugin(
        name="docker-ldap-directory",
        plugin_version="1.0.0",
        description="LDAP directory connector for Docker environment",
        author="FLEXT Team",
        plugin_type=FlextPluginConstants.Plugin.PluginType.AUTHENTICATION.value,
        is_enabled=True,
        metadata={"dependencies": ["ldap3"]},
    )
    return (ldap_plugin, ldap_config)


def test_connections() -> bool:
    """Test connectivity to all Docker services."""
    services = [
        ("PostgreSQL", "localhost", 5432),
        ("Redis", "localhost", 6379),
        ("LDAP", "localhost", 389),
    ]
    all_available = True
    for _service_name, host, port in services:
        available = check_service_availability(host, port)
        if not available:
            all_available = False
    return all_available


def main() -> None:
    """Main entry point for the Docker integration example."""
    parser = argparse.ArgumentParser(
        description="FLEXT Plugin Docker Integration Example",
    )
    _ = parser.add_argument(
        "--test-connections",
        action="store_true",
        help="Test connectivity to Docker services before creating plugins",
    )
    args = parser.parse_args()
    if args.test_connections:
        services_available = test_connections()
        if not services_available:
            sys.exit(1)
    postgres_plugin, _postgres_config = create_docker_postgres_plugin()
    redis_plugin, _redis_config = create_docker_redis_plugin()
    ldap_plugin, _ldap_config = create_docker_ldap_plugin()
    container = FlextContainer()
    FlextPluginApi(container)
    if postgres_plugin and hasattr(postgres_plugin, "validate_business_rules"):
        validation_result = postgres_plugin.validate_business_rules()
        if validation_result.is_success:
            pass
        else:
            sys.exit(1)
    if redis_plugin and hasattr(redis_plugin, "validate_business_rules"):
        validation_result = redis_plugin.validate_business_rules()
    else:
        sys.exit(1)
    if ldap_plugin and hasattr(ldap_plugin, "validate_business_rules"):
        validation_result = ldap_plugin.validate_business_rules()
        if validation_result.is_success:
            pass
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
