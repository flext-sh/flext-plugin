# FLEXT Plugin Examples

This directory contains comprehensive examples demonstrating the FLEXT Plugin system functionality with 100% working code and enterprise-grade patterns.

## Available Examples

### 1. Basic Plugin Example (`01_basic_plugin.py`)

**Purpose**: Minimal functional plugin demonstration without external dependencies.

**Features**:

- Plugin creation with configuration
- Domain validation
- Status transitions (INACTIVE → ACTIVE)
- Basic lifecycle management

**Usage**:

```bash
python examples/01_basic_plugin.py
```

**Output**: Complete plugin creation and activation workflow with validation.

### 2. Plugin Configuration Example (`02_plugin_configuration.py`)

**Purpose**: Advanced plugin configuration patterns for complex enterprise scenarios.

**Features**:

- Database plugin configuration (PostgreSQL)
- LDAP plugin configuration with authentication
- Standalone configuration entities
- Plugin metadata with licensing and compatibility
- Configuration validation

**Usage**:

```bash
python examples/02_plugin_configuration.py
```

**Docker Integration**:

```bash
# Optional: Start PostgreSQL for enhanced testing
cd ..docker
docker-compose up -d postgres
python examples/02_plugin_configuration.py --with-db
```

### 3. Docker Integration Example (`03_docker_integration.py`)

**Purpose**: Real-world plugin configuration with Docker services integration.

**Features**:

- Docker-compatible PostgreSQL plugin (matches docker-compose.yml)
- Docker-compatible Redis cache plugin with connection pooling
- Docker-compatible LDAP directory plugin with authentication
- Service connectivity testing
- Production-ready configuration patterns
- Comprehensive monitoring and performance settings

**Usage**:

```bash
# Basic usage (configuration only)
python examples/03_docker_integration.py

# With connectivity testing
python examples/03_docker_integration.py --test-connections
```

**Docker Setup**:

```bash
# Start all required services
cd ..docker
docker-compose up -d postgres redis openldap

# Verify services are running
docker-compose ps

# Test with all services available
python examples/03_docker_integration.py --test-connections
```

## Configuration Compatibility

### Docker Service Mapping

All examples use configurations that are compatible with the FLEXT Docker development environment at `..docker/docker-compose.yml`:

| Service    | Docker Container | Host Port | Plugin Configuration                                                |
| ---------- | ---------------- | --------- | ------------------------------------------------------------------- |
| PostgreSQL | `flext-postgres` | 5432      | Database: `flext_db`, User: `flext`, Password: `flext_dev_password` |
| Redis      | `flext-redis`    | 6379      | Password: `flext_redis_password`, DB: 0                             |
| LDAP       | `flext-ldap`     | 389       | Domain: `dc=flext,dc=dev`, Admin: `flext_ldap_REDACTED_LDAP_BIND_PASSWORD`                |

### Environment Variables

The examples support environment-based configuration for production deployments:

```bash
# Database configuration
export FLEXT_DB_HOST=localhost
export FLEXT_DB_PORT=5432
export FLEXT_DB_NAME=flext_db
export FLEXT_DB_USER=flext
export FLEXT_DB_PASSWORD=flext_dev_password

# Redis configuration
export FLEXT_REDIS_HOST=localhost
export FLEXT_REDIS_PORT=6379
export FLEXT_REDIS_PASSWORD=flext_redis_password

# LDAP configuration
export FLEXT_LDAP_HOST=localhost
export FLEXT_LDAP_PORT=389
export FLEXT_LDAP_BASE_DN=dc=flext,dc=dev
export FLEXT_LDAP_BIND_PASSWORD=readonly
```

## Testing

All examples have comprehensive test coverage in `tests/test_examples.py`:

```bash
# Run all example tests
python -m pytest tests/test_examples.py -v

# Run specific example tests
python -m pytest tests/test_examples.py::test_basic_plugin_example_execution -v
python -m pytest tests/test_examples.py::test_plugin_configuration_example_functionality -v
python -m pytest tests/test_examples.py::test_docker_integration_example_functionality -v
```

## Architecture Integration

### Clean Architecture Compliance

All examples follow Clean Architecture patterns:

- **Domain Layer**: Plugin entities with business logic
- **Application Layer**: Service orchestration and validation
- **Infrastructure Layer**: Docker service configurations
- **Platform Layer**: Unified API access through `simple_api.py`

### Domain-Driven Design (DDD)

Examples demonstrate DDD concepts:

- **Entities**: `FlextPlugin`, `FlextPluginModels.Config`, `FlextPluginModels.Metadata`
- **Value Objects**: Plugin types, status enums, configuration objects
- **Domain Services**: Validation and lifecycle management
- **Repositories**: Plugin registry patterns

### FLEXT Ecosystem Integration

Examples integrate with the broader FLEXT platform:

- **FlexCore (Go)**: Runtime container service (port 8080)
- **FLEXT Service (Go/Python)**: Data platform service (port 8081)
- **Singer Integration**: Plugin types for tap/target/transform patterns
- **Meltano Orchestration**: Plugin discovery and execution patterns

## Development Workflow

### Creating New Examples

1. **Follow Naming Convention**: `{purpose}_example.py`
2. **Include Comprehensive Docstring**: Purpose, features, usage, prerequisites
3. **Add Direct Execution Support**: `sys.path.insert()` for `src/` access
4. **Create Corresponding Tests**: In `tests/test_examples.py`
5. **Validate Docker Compatibility**: Test with Docker services when applicable
6. **Update This README**: Add to examples list with features and usage

### Quality Standards

- **100% Functional**: All examples must execute without errors
- **Enterprise-Grade**: Professional configuration patterns
- **Docker-Ready**: Compatible with FLEXT Docker development environment
- **Comprehensive Testing**: Script execution and functionality testing
- **Clear Documentation**: Usage instructions and feature descriptions

## Integration with Main Project

Examples demonstrate real functionality from the main FLEXT Plugin system:

- **Domain Entities**: Direct usage of `src/flext_plugin/domain/entities.py`
- **Simple API**: Factory functions from `src/flext_plugin/simple_api.py`
- **Type System**: Plugin types and status from `src/flext_plugin/core/types.py`
- **Validation**: Domain rules and business logic validation

## Troubleshooting

### Common Issues

**Import Errors**:

```python
# Examples handle path setup automatically
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
```

**Docker Service Unavailable**:

```bash
# Check service status
cd ..docker
docker-compose ps

# Start required services
docker-compose up -d postgres redis openldap

# View service logs
docker-compose logs postgres
```

**Configuration Mismatch**:

- Verify Docker service environment variables match example configurations
- Check `docker-compose.yml` for correct service names and ports
- Ensure network connectivity between host and containers

### Support

For issues with examples:

1. Check test suite: `python -m pytest tests/test_examples.py -v`
2. Verify Docker services: `docker-compose ps`
3. Review main project documentation: `../README.md` and `../CLAUDE.md`
4. Check integration with workspace: `..README.md`

---

**Status**: 1.0.0 Release Preparation | **Coverage**: Functional | **Docker Integration**: In Progress
