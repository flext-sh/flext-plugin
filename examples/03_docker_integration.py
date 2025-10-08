#!/usr/bin/env python3
"""FLEXT Plugin Docker Integration Example.

This example demonstrates real-world plugin configuration with Docker services integration.
Shows how to create production-ready plugins that work with Docker Compose services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import asyncio
import socket
import sys

from flext_plugin import (
    FlextPlugin,
    FlextPluginModels,
)


def check_service_availability(host: str, port: int, timeout: float = 5.0) -> bool:
    """Check if a network service is available."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def create_docker_postgres_plugin() -> tuple[FlextPluginModels.PluginModel, dict]:
    """Create a Docker-compatible PostgreSQL plugin using domain library patterns."""
    postgres_config = {
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

    # Use domain library patterns - create plugin model directly
    postgres_plugin = FlextPluginModels.PluginModel(
        name="docker-postgres-connector",
        plugin_version="1.0.0",
        description="PostgreSQL database connector for Docker environment",
        author="FLEXT Team",
        plugin_type=FlextPluginModels.PluginType.DATABASE,
        status=FlextPluginModels.PluginStatus.DISCOVERED,
        dependencies=["psycopg2-binary"],
        enabled=True,
    )

    return postgres_plugin, postgres_config


def create_docker_redis_plugin() -> tuple[FlextPluginModels.PluginModel, dict]:
    """Create a Docker-compatible Redis plugin using domain library patterns."""
    redis_config = {
        "host": "localhost",
        "port": 6379,
        "password": "flext_redis_password",
        "db": 0,
        "decode_responses": True,
        "socket_timeout": 5,
        "socket_connect_timeout": 5,
        "socket_keepalive": True,
        "socket_keepalive_options": {socket.TCP_KEEPIDLE: 60},
        "health_check_interval": 30,
    }

    # Use domain library patterns - create plugin model directly
    redis_plugin = FlextPluginModels.PluginModel(
        name="docker-redis-cache",
        plugin_version="1.0.0",
        description="Redis cache connector for Docker environment",
        author="FLEXT Team",
        plugin_type=FlextPluginModels.PluginType.DATABASE,
        status=FlextPluginModels.PluginStatus.DISCOVERED,
        dependencies=["redis"],
        enabled=True,
    )

    return redis_plugin, redis_config


def create_docker_ldap_plugin() -> tuple[FlextPluginModels.PluginModel, dict]:
    """Create a Docker-compatible LDAP plugin using domain library patterns."""
    ldap_config = {
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

    # Use domain library patterns - create plugin model directly
    ldap_plugin = FlextPluginModels.PluginModel(
        name="docker-ldap-directory",
        plugin_version="1.0.0",
        description="LDAP directory connector for Docker environment",
        author="FLEXT Team",
        plugin_type=FlextPluginModels.PluginType.AUTHENTICATION,
        status=FlextPluginModels.PluginStatus.DISCOVERED,
        dependencies=["ldap3"],
        enabled=True,
    )

    return ldap_plugin, ldap_config


def test_connections() -> bool:
    """Test connectivity to all Docker services."""
    print("🔍 Testing Docker service connectivity...")

    services = [
        ("PostgreSQL", "localhost", 5432),
        ("Redis", "localhost", 6379),
        ("LDAP", "localhost", 389),
    ]

    all_available = True
    for service_name, host, port in services:
        available = check_service_availability(host, port)
        status = "✅ AVAILABLE" if available else "❌ UNAVAILABLE"
        print(f"  {service_name}: {status}")
        if not available:
            all_available = False

    if not all_available:
        print(
            "\n⚠️  Some services are not available. Make sure Docker services are running:"
        )
        print(
            "   cd /home/marlonsc/flext/docker && docker-compose up -d postgres redis openldap"
        )
        return False

    print("✅ All Docker services are available!")
    return True


def main() -> None:
    """Main entry point for the Docker integration example."""
    parser = argparse.ArgumentParser(
        description="FLEXT Plugin Docker Integration Example"
    )
    parser.add_argument(
        "--test-connections",
        action="store_true",
        help="Test connectivity to Docker services before creating plugins",
    )
    args = parser.parse_args()

    print("🚀 FLEXT Plugin Docker Integration Example")
    print("=" * 50)

    # Test connections if requested
    if args.test_connections:
        print("\nTesting Docker service connectivity...")
        services_available = asyncio.run(test_connections())
        if not services_available:
            sys.exit(1)
    else:
        print(
            "INFO  Skipping connection tests. Use --test-connections to test Docker services."
        )

    print("\n🏗️  Creating Docker PostgreSQL plugin...")
    postgres_plugin, _postgres_config = create_docker_postgres_plugin()
    print(f"  ✅ PostgreSQL plugin created: {postgres_plugin.name}")

    print("\n🏗️  Creating Docker Redis plugin...")
    redis_plugin, _redis_config = create_docker_redis_plugin()
    print(f"  ✅ Redis plugin created: {redis_plugin.name}")

    print("\n🏗️  Creating Docker LDAP plugin...")
    ldap_plugin, _ldap_config = create_docker_ldap_plugin()
    print(f"  ✅ LDAP plugin created: {ldap_plugin.name}")

    print("\n🔍 Validating plugin configurations...")

    # Use FlextPlugin facade for validation (domain library pattern)
    plugin_facade = FlextPlugin()

    # Validate PostgreSQL plugin
    validation_result = plugin_facade.validate_plugin(postgres_plugin)
    if validation_result.success:
        print("  ✅ PostgreSQL plugin validation passed")
    else:
        print(f"  ❌ PostgreSQL plugin validation failed: {validation_result.error}")
        sys.exit(1)

    # Validate Redis plugin
    validation_result = plugin_facade.validate_plugin(redis_plugin)
    if validation_result.success:
        print("  ✅ Redis plugin validation passed")
    else:
        print(f"  ❌ Redis plugin validation failed: {validation_result.error}")
        sys.exit(1)

    # Validate LDAP plugin
    validation_result = plugin_facade.validate_plugin(ldap_plugin)
    if validation_result.success:
        print("  ✅ LDAP plugin validation passed")
    else:
        print(f"  ❌ LDAP plugin validation failed: {validation_result.error}")
        sys.exit(1)

    print("\n🎉 Docker Integration example completed successfully!")
    print("\n📋 Summary:")
    print(f"  - PostgreSQL plugin: {postgres_plugin.name}")
    print(f"  - Redis plugin: {redis_plugin.name}")
    print(f"  - LDAP plugin: {ldap_plugin.name}")
    print(
        "\n💡 All plugins are configured for the FLEXT Docker development environment."
    )
    print("   Make sure Docker services are running for full functionality.")


if __name__ == "__main__":
    main()
