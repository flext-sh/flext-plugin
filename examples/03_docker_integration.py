"""FLEXT Plugin Docker Integration Example.

This example demonstrates real-world plugin configuration with Docker services integration.
Shows how to create production-ready plugins that work with Docker Compose services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import socket
import sys
from typing import Annotated, override

from flext_cli import cli, m as cli_m, u as cli_u

from flext_core import p, r, s
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
    FlextPluginModels.Plugin.Entity,
    t.JsonMapping,
]:
    """Create a Docker-compatible PostgreSQL plugin using domain library patterns."""
    postgres_config: t.JsonMapping = {
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
    postgres_plugin = FlextPluginModels.Plugin.Entity(
        name="docker-postgres-connector",
        plugin_version="1.0.0",
        description="PostgreSQL database connector for Docker environment",
        author="FLEXT Team",
        plugin_type=FlextPluginConstants.Plugin.Type.DATABASE.value,
        is_enabled=True,
        metadata={"dependencies": ["psycopg2-binary"]},
    )
    return (postgres_plugin, postgres_config)


def create_docker_redis_plugin() -> tuple[
    FlextPluginModels.Plugin.Entity,
    t.JsonMapping,
]:
    """Create a Docker-compatible Redis plugin using domain library patterns."""
    redis_config: t.JsonMapping = {
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
    redis_plugin = FlextPluginModels.Plugin.Entity(
        name="docker-redis-cache",
        plugin_version="1.0.0",
        description="Redis cache connector for Docker environment",
        author="FLEXT Team",
        plugin_type=FlextPluginConstants.Plugin.Type.DATABASE.value,
        is_enabled=True,
        metadata={"dependencies": ["redis"]},
    )
    return (redis_plugin, redis_config)


def create_docker_ldap_plugin() -> tuple[
    FlextPluginModels.Plugin.Entity,
    t.JsonMapping,
]:
    """Create a Docker-compatible LDAP plugin using domain library patterns."""
    ldap_config: t.JsonMapping = {
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
    ldap_plugin = FlextPluginModels.Plugin.Entity(
        name="docker-ldap-directory",
        plugin_version="1.0.0",
        description="LDAP directory connector for Docker environment",
        author="FLEXT Team",
        plugin_type=FlextPluginConstants.Plugin.Type.AUTHENTICATION.value,
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


class _DockerIntegrationCommand(s[bool]):
    """CLI command for the FLEXT Plugin Docker integration example."""

    test_connections: Annotated[
        bool,
        cli_u.Field(
            default=False,
            description=(
                "Test connectivity to Docker services before creating plugins."
            ),
        ),
    ] = False

    @override
    def execute(self) -> p.Result[bool]:
        """Run the Docker integration smoke flow and return success/failure."""
        if self.test_connections and not test_connections():
            return r[bool].fail("docker services unavailable")
        postgres_plugin, _postgres_config = create_docker_postgres_plugin()
        redis_plugin, _redis_config = create_docker_redis_plugin()
        ldap_plugin, _ldap_config = create_docker_ldap_plugin()
        _ = FlextPluginApi.fetch_global()
        for plugin in (postgres_plugin, redis_plugin, ldap_plugin):
            if not hasattr(plugin, "validate_business_rules"):
                return r[bool].fail("plugin validation surface unavailable")
            validation_result = plugin.validate_business_rules()
            if validation_result.failure:
                return r[bool].fail(validation_result.error or "validation failed")
        return r[bool].ok(value=True)


def main(args: t.StrSequence | None = None) -> int:
    """Main entry point for the Docker integration example."""
    app = cli.create_app_with_common_params(
        name="flext-plugin-docker-integration",
        help_text="FLEXT Plugin Docker Integration Example",
    )
    cli.register_result_routes(
        app,
        [
            cli_m.Cli.ResultCommandRoute(
                name="run",
                help_text="Create the example plugins and validate them.",
                model_cls=_DockerIntegrationCommand,
                handler=lambda params: params.execute(),
            ),
        ],
    )
    outcome = cli.execute_app(
        app,
        prog_name="flext-plugin-docker-integration",
        args=list(args) if args is not None else sys.argv[1:],
    )
    return 0 if outcome.success else 1


if __name__ == "__main__":
    cli.exit(main())
