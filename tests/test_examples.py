"""Test suite for examples to ensure they work correctly and maintain 100% functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import cast

from flext_core import FlextCore

from flext_plugin import (
    PluginStatus,
    PluginType,
    create_flext_plugin,
    create_flext_plugin_config,
    create_flext_plugin_metadata,
)

# Load examples from examples directory
examples_path = Path(__file__).parent.parent / "examples"

# Load docker integration helpers from numerically prefixed example via importlib

_docker_path = examples_path / "03_docker_integration.py"
_spec = importlib.util.spec_from_file_location("docker_integration", _docker_path)
assert _spec
assert _spec.loader
_docker_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_docker_mod)
check_service_availability = _docker_mod.check_service_availability
create_docker_ldap_plugin = _docker_mod.create_docker_ldap_plugin
create_docker_postgres_plugin = _docker_mod.create_docker_postgres_plugin
create_docker_redis_plugin = _docker_mod.create_docker_redis_plugin


def _run(
    cmd_list: FlextCore.Types.StringList,
    cwd: str | None = None,
) -> tuple[int, str, str]:
    """Run a command and return (return_code, stdout, stderr)."""
    process = subprocess.Popen(
        *cmd_list,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout_bytes, stderr_bytes = process.communicate()
    return (
        process.returncode or 0,
        stdout_bytes.decode("utf-8"),
        stderr_bytes.decode("utf-8"),
    )


def test_basic_plugin_example_execution() -> None:
    """Test that basic_plugin_example.py runs successfully without errors."""
    example_path = Path(__file__).parent.parent / "examples" / "01_basic_plugin.py"

    # Execute the example script
    result = FlextCore.Utilities.run_external_command(
        [sys.executable, str(example_path)],
        cwd=str(Path(__file__).parent.parent),
        capture_output=True,
        text=True,
    )

    # Verify successful execution
    assert result.returncode == 0, f"Example failed with error: {result.stderr}"

    # Verify expected output content
    output = result.stdout
    assert "FLEXT Plugin Basic Example" in output
    assert "Plugin created: example-plugin" in output
    assert "Version: 1.0.0" in output
    assert "Plugin validation passed" in output
    assert "Plugin activation successful" in output
    assert "Example completed successfully" in output


def test_basic_plugin_example_functionality() -> None:
    """Test the actual functionality demonstrated in basic_plugin_example.py."""
    # Import the functionality directly

    # Test plugin creation
    plugin = create_flext_plugin(
        name="test-plugin",
        version="1.0.0",
        config={
            "description": "Test plugin",
            "author": "Test Author",
        },
    )

    # Verify plugin properties
    assert plugin.name == "test-plugin"
    assert plugin.plugin_version == "1.0.0"
    assert plugin.description == "Test plugin"
    assert plugin.author == "Test Author"
    assert plugin.status == PluginStatus.INACTIVE
    assert not plugin.is_active()

    # Test domain validation
    validation_result = plugin.validate_business_rules()
    assert validation_result.success

    # Test activation
    activate_result = plugin.activate()
    assert activate_result is True
    assert plugin.status == PluginStatus.ACTIVE
    assert plugin.is_active()


def test_plugin_configuration_example_execution() -> None:
    """Test that plugin_configuration_example.py runs successfully without errors."""
    example_path = (
        Path(__file__).parent.parent / "examples" / "02_plugin_configuration.py"
    )

    # Execute the example script
    result = FlextCore.Utilities.run_external_command(
        [sys.executable, str(example_path)],
        cwd=str(Path(__file__).parent.parent),
        capture_output=True,
        text=True,
    )

    # Verify successful execution
    assert result.returncode == 0, (
        f"Configuration example failed with error: {result.stderr}"
    )

    # Verify expected output content
    output = result.stdout
    assert "FLEXT Plugin Configuration Example" in output
    assert "Database plugin: postgres-connector v2.1.0" in output
    assert "LDAP plugin: ldap-directory v1.5.0" in output
    assert "Config for: api-gateway" in output
    assert "Metadata for: data-processor" in output
    assert "Configuration validation..." in output
    assert "Configuration example completed successfully" in output


def test_plugin_configuration_example_functionality() -> None:
    """Test the actual functionality demonstrated in plugin_configuration_example.py."""
    # Import the functionality directly

    # Test database plugin creation with complex configuration
    db_config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "database": "test_db",
            "username": "test_user",
            "password": "test_pass",
            "pool_size": 5,
        },
        "retry_config": {
            "max_retries": 3,
            "retry_delay": 1.0,
            "exponential_backoff": True,
        },
        "features": {
            "enable_metrics": True,
            "enable_tracing": True,
        },
    }

    db_plugin = create_flext_plugin(
        name="test-postgres-connector",
        version="2.1.0",
        config={
            "description": "Test PostgreSQL connector",
            "author": "Test Team",
            "plugin_type": PluginType.DATABASE,
            **db_config,
        },
    )

    # Verify database plugin properties
    assert db_plugin.name == "test-postgres-connector"
    assert db_plugin.plugin_version == "2.1.0"
    assert db_plugin.description == "Test PostgreSQL connector"

    # Test LDAP plugin creation
    ldap_config = {
        "ldap": {
            "server": "localhost",
            "port": 389,
            "base_dn": "dc=test,dc=dev",
            "bind_dn": "cn=readonly,dc=test,dc=dev",
        },
        "search": {
            "user_filter": "(objectClass=person)",
            "group_filter": "(objectClass=group)",
            "attributes": ["cn", "mail", "memberOf"],
        },
    }

    ldap_plugin = create_flext_plugin(
        name="test-ldap-directory",
        version="1.5.0",
        config={
            "description": "Test LDAP directory service",
            "plugin_type": PluginType.AUTHENTICATION,
            **ldap_config,
        },
    )

    # Verify LDAP plugin properties
    assert ldap_plugin.name == "test-ldap-directory"
    assert ldap_plugin.plugin_version == "1.5.0"

    # Test standalone configuration creation
    standalone_config = create_flext_plugin_config(
        plugin_name="test-api-gateway",
        config_data={
            "routes": {
                "/api/v1/health": {"method": "GET", "auth": False},
                "/api/v1/plugins": {"method": "GET", "auth": True},
            },
            "middleware": ["cors", "rate_limit", "auth"],
        },
    )

    # Verify standalone configuration
    assert standalone_config.plugin_name == "test-api-gateway"
    routes = cast(
        "FlextCore.Types.Dict",
        standalone_config.config_data.get("routes", {}),
    )
    assert len(routes) == 2
    middleware = cast(
        "FlextCore.Types.StringList",
        standalone_config.config_data.get("middleware", []),
    )
    assert "cors" in middleware

    # Test metadata creation
    metadata = create_flext_plugin_metadata(
        plugin_name="test-data-processor",
        metadata={
            "tags": ["etl", "transform", "test"],
            "categories": ["data-processing"],
            "license_info": "MIT",  # Correct field name
            "compatibility": {
                "python": ">=3.13",
                "flext": ">=0.9.0",
            },
        },
    )

    # Verify metadata properties
    assert metadata.plugin_name == "test-data-processor"
    assert "etl" in metadata.tags
    assert "data-processing" in metadata.categories
    assert metadata.license_info == "MIT"

    # Test validation on complex plugins
    for plugin in [db_plugin, ldap_plugin]:
        validation_result = plugin.validate_business_rules()
        assert validation_result.success, (
            f"Plugin {plugin.name} validation failed: {validation_result.error}"
        )


def test_plugin_configuration_docker_compatibility() -> None:
    """Test plugin configuration compatibility with Docker services."""
    # Import the functionality directly

    # Test Docker-compatible database configuration
    # These settings match ..docker/docker-compose.yml
    docker_db_config = {
        "database": {
            "host": "localhost",  # Would be flext-postgres in Docker network
            "port": 5432,
            "database": "flext_db",  # Matches POSTGRES_DB in docker-compose.yml
            "username": "flext",  # Matches POSTGRES_USER
            "password": "flext_dev_password",  # Matches POSTGRES_PASSWORD
            "pool_size": 5,
            "pool_recycle": 3600,
        },
        "connection": {
            "ssl_mode": "prefer",
            "application_name": "flext-plugin-test",
            "connect_timeout": 30,
        },
    }

    docker_db_plugin = create_flext_plugin(
        name="docker-postgres-connector",
        version="2.1.0",
        config={
            "description": "Docker-compatible PostgreSQL connector",
            "author": "FLEXT Team",
            "plugin_type": PluginType.DATABASE,
            **docker_db_config,
        },
    )

    # Verify Docker database plugin
    assert docker_db_plugin.name == "docker-postgres-connector"
    validation_result = docker_db_plugin.validate_business_rules()
    assert validation_result.success

    # Test Docker-compatible LDAP configuration
    # These settings match the OpenLDAP service in docker-compose.yml
    docker_ldap_config = {
        "ldap": {
            "server": "localhost",  # Would be flext-ldap in Docker network
            "port": 389,
            "base_dn": "dc=flext,dc=dev",  # Matches LDAP_DOMAIN
            "bind_dn": "cn=readonly,dc=flext,dc=dev",  # Matches readonly user
            "bind_password": "readonly",  # Matches LDAP_READONLY_USER_PASSWORD
            "use_ssl": False,
            "timeout": 30,
        },
        "REDACTED_LDAP_BIND_PASSWORD": {
            "REDACTED_LDAP_BIND_PASSWORD_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=flext,dc=dev",
            "REDACTED_LDAP_BIND_PASSWORD_password": "flext_ldap_REDACTED_LDAP_BIND_PASSWORD",  # Matches LDAP_ADMIN_PASSWORD
        },
        "search": {
            "user_filter": "(objectClass=inetOrgPerson)",
            "group_filter": "(objectClass=groupOfNames)",
            "attributes": ["cn", "mail", "memberOf", "uid"],
            "page_size": 1000,
        },
    }

    docker_ldap_plugin = create_flext_plugin(
        name="docker-ldap-directory",
        version="1.5.0",
        config={
            "description": "Docker-compatible LDAP directory service",
            "author": "FLEXT Team",
            "plugin_type": PluginType.AUTHENTICATION,
            **docker_ldap_config,
        },
    )

    # Verify Docker LDAP plugin
    assert docker_ldap_plugin.name == "docker-ldap-directory"
    validation_result = docker_ldap_plugin.validate_business_rules()
    assert validation_result.success

    # Test Redis cache configuration (also available in Docker)
    docker_redis_config = {
        "redis": {
            "host": "localhost",  # Would be flext-redis in Docker network
            "port": 6379,
            "password": "flext_redis_password",  # Matches docker-compose.yml
            "db": 0,
            "socket_timeout": 30,
            "socket_connect_timeout": 30,
        },
        "cache": {
            "default_ttl": 300,
            "max_connections": 50,
            "retry_on_timeout": True,
        },
    }

    docker_redis_plugin = create_flext_plugin(
        name="docker-redis-cache",
        version="1.0.0",
        config={
            "description": "Docker-compatible Redis cache service",
            "author": "FLEXT Team",
            "plugin_type": PluginType.DATABASE,
            **docker_redis_config,
        },
    )

    # Verify Docker Redis plugin
    assert docker_redis_plugin.name == "docker-redis-cache"
    validation_result = docker_redis_plugin.validate_business_rules()
    assert validation_result.success


def test_docker_integration_example_execution() -> None:
    """Test that 03_docker_integration.py runs successfully without errors."""
    example_path = (
        Path(__file__).parent.parent / "examples" / "03_docker_integration.py"
    )

    # Execute the example script
    result = FlextCore.Utilities.run_external_command(
        _run(
            [sys.executable, str(example_path)],
            cwd=str(Path(__file__).parent.parent),
        ),
    )

    # Verify successful execution
    assert result.returncode == 0, (
        f"Docker integration example failed with error: {result.stderr}"
    )

    # Verify expected output content
    output = result.stdout
    assert "FLEXT Plugin Docker Integration Example" in output
    assert "Creating Docker PostgreSQL plugin" in output
    assert "Creating Docker Redis plugin" in output
    assert "Creating Docker LDAP plugin" in output
    assert "PostgreSQL plugin validation passed" in output
    assert "Redis plugin validation passed" in output
    assert "LDAP plugin validation passed" in output
    assert "Docker Integration example completed successfully" in output


def test_docker_integration_example_functionality() -> None:
    """Test the actual functionality demonstrated in 03_docker_integration.py."""
    # Import the functionality directly

    # Test PostgreSQL plugin creation
    postgres_plugin, postgres_config = create_docker_postgres_plugin()

    # Verify PostgreSQL plugin properties
    assert postgres_plugin.name == "docker-postgres-connector"
    assert postgres_plugin.plugin_version == "2.1.0"
    assert (
        postgres_plugin.description
        == "PostgreSQL connector for Docker development environment"
    )
    assert postgres_config["database"]["host"] == "localhost"
    assert postgres_config["database"]["port"] == 5434  # Actual Docker container port
    assert postgres_config["database"]["database"] == "flext_db"
    assert postgres_config["database"]["username"] == "flext"
    assert postgres_config["database"]["password"] == "flext_dev_password"
    assert postgres_config["database"]["pool_size"] == 10

    # Test PostgreSQL plugin validation and activation
    validation_result = postgres_plugin.validate_business_rules()
    assert validation_result.success

    activation_result = postgres_plugin.activate()
    assert activation_result is True
    assert postgres_plugin.status == PluginStatus.ACTIVE

    # Test Redis plugin creation
    redis_plugin, redis_config = create_docker_redis_plugin()

    # Verify Redis plugin properties
    assert redis_plugin.name == "docker-redis-cache"
    assert redis_plugin.plugin_version == "1.2.0"
    assert (
        redis_plugin.description
        == "Redis cache service for Docker development environment"
    )
    assert redis_config["redis"]["host"] == "localhost"
    assert redis_config["redis"]["port"] == 6381  # Actual Docker container port
    assert redis_config["redis"]["password"] == "flext_redis_password"
    assert redis_config["connection_pool"]["max_connections"] == 50
    assert redis_config["cache"]["default_ttl"] == 300

    # Test Redis plugin validation and activation
    validation_result = redis_plugin.validate_business_rules()
    assert validation_result.success

    activation_result = redis_plugin.activate()
    assert activation_result is True
    assert redis_plugin.status == PluginStatus.ACTIVE

    # Test LDAP plugin creation
    ldap_plugin, ldap_config = create_docker_ldap_plugin()

    # Verify LDAP plugin properties
    assert ldap_plugin.name == "docker-ldap-directory"
    assert ldap_plugin.plugin_version == "1.5.0"
    assert (
        ldap_plugin.description
        == "LDAP directory service for Docker development environment"
    )
    assert ldap_config["ldap"]["server"] == "localhost"
    assert ldap_config["ldap"]["port"] == 389
    assert ldap_config["ldap"]["base_dn"] == "dc=flext,dc=dev"
    assert ldap_config["ldap"]["bind_dn"] == "cn=readonly,dc=flext,dc=dev"
    assert ldap_config["ldap"]["bind_password"] == "readonly"
    assert ldap_config["REDACTED_LDAP_BIND_PASSWORD"]["REDACTED_LDAP_BIND_PASSWORD_password"] == "flext_ldap_REDACTED_LDAP_BIND_PASSWORD"

    # Test LDAP plugin validation and activation
    validation_result = ldap_plugin.validate_business_rules()
    assert validation_result.success

    activation_result = ldap_plugin.activate()
    assert activation_result is True
    assert ldap_plugin.status == PluginStatus.ACTIVE

    # Test service availability check function
    # Test with a service that should always be available (local)
    localhost_available = check_service_availability("127.0.0.1", 80, timeout=1.0)
    # We don't assert the result since it depends on system state
    assert isinstance(localhost_available, bool)

    # Test with an invalid service that should never be available
    invalid_available = check_service_availability(
        "192.0.2.1",
        99999,
        timeout=0.1,
    )  # RFC5737 test address
    assert invalid_available is False


def test_docker_integration_example_with_connection_testing() -> None:
    """Test docker integration example with connection testing enabled."""
    example_path = (
        Path(__file__).parent.parent / "examples" / "03_docker_integration.py"
    )

    # Execute the example script with connection testing
    result = FlextCore.Utilities.run_external_command(
        [sys.executable, str(example_path), "--test-connections"],
        cwd=str(Path(__file__).parent.parent),
        capture_output=True,
        text=True,
    )

    # Verify successful execution
    assert result.returncode == 0, (
        f"Docker integration example with connections failed: {result.stderr}"
    )

    # Verify connection testing output appears
    output = result.stdout
    assert "Service Connectivity Check" in output
    # Should show either Available or Unavailable (not Skipped)
    assert ("Available" in output) or ("Unavailable" in output)
    assert (
        "Skipped" not in output
    )  # No services should be skipped with --test-connections
