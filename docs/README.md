# FLEXT Plugin Documentation

Welcome to the comprehensive documentation for FLEXT Plugin, the enterprise-grade plugin management system for the FLEXT data integration platform.

## Documentation Structure

### 📚 Core Documentation

- **[Architecture Guide](architecture/README.md)** - Clean Architecture and DDD implementation
- **[API Reference](api/README.md)** - Complete API documentation and interfaces
- **[Development Guides](guides/README.md)** - Step-by-step development workflows
- **[Examples](examples/README.md)** - Practical implementation examples

### 🏗️ Architecture & Design

- **[Architecture Overview](architecture/README.md)** - Clean Architecture and DDD foundations
- **[Python Module Standards](standards/python-module-organization.md)** - Code organization patterns

### 🛠️ Development Guides

- **[Quick Start](guides/quick-start.md)** - Get up and running in minutes
- **[Plugin Development](guides/plugin-development.md)** - Creating custom plugins
- **[Development Overview](guides/README.md)** - Development workflow and best practices

### 📖 API Reference

- **[API Overview](api/README.md)** - Complete API documentation and usage patterns

### 💡 Examples & Use Cases

- **[Basic Plugin](examples/basic-plugin.md)** - Simple plugin implementation
- **[Examples Overview](examples/README.md)** - Collection of practical examples

## Getting Started

### Prerequisites

- **Python 3.13+**: Modern Python with type hints and async support
- **Poetry**: Dependency management and packaging
- **Git**: Version control and repository management

### Installation

```bash
# Install FLEXT Plugin
poetry add flext-plugin

# Or for development
git clone https://github.com/flext-sh/flext.git
cd flext/flext-plugin
make setup
```

### First Steps

1. **[Quick Start Guide](guides/quick-start.md)** - Basic plugin creation and usage
2. **[Architecture Overview](architecture/README.md)** - Understand the system design
3. **[Plugin Development](guides/plugin-development.md)** - Create your first plugin
4. **[Integration Examples](examples/README.md)** - See real-world usage patterns

## FLEXT Ecosystem Integration

FLEXT Plugin serves as the foundational plugin system for the entire FLEXT ecosystem:

### Core Services Integration

- **FlexCore (Go)**: Runtime container service with plugin proxy adapters
- **FLEXT Service (Go/Python)**: Data platform service with Python bridge
- **Plugin Communication**: Go ↔ Python plugin interaction protocols

### Foundation Libraries

- **flext-core**: Base patterns, FlextResult, dependency injection container
- **flext-observability**: Monitoring, metrics, tracing, health checks

### Singer Ecosystem (15 Projects)

- **Taps (5)**: Data extraction plugins (Oracle, LDAP, LDIF, OIC, WMS)
- **Targets (5)**: Data loading plugins with matching sources
- **DBT Projects (4)**: Data transformation models and business logic
- **Extensions (1)**: Oracle OIC specialized extensions

### Application Services (5 Projects)

- **flext-api**: REST API services with plugin endpoints
- **flext-auth**: Authentication plugins and strategies
- **flext-web**: Web interface with plugin management
- **flext-quality**: Code quality plugins and analysis
- **flext-cli**: Command-line plugin management tools

## Development Workflow

### Quality Standards

- **Test Coverage**: Currently 33% (83/253 tests passing), systematic improvement in progress
- **Type Safety**: MyPy strict mode target; aiming for 100% coverage
- **Code Quality**: Ruff linting with ALL rules enabled
- **Security**: Bandit scanning and pip-audit dependency checks

### Development Commands

```bash
# Setup development environment
make setup

# Quality gates (required before commit)
make validate              # Complete validation pipeline
make check                 # Quick health check
make fix                   # Auto-fix issues

# Testing
make test                  # Full test suite
make test-unit             # Unit tests only
make test-integration      # Integration tests
make coverage-html         # Coverage report

# Plugin development
make plugin-watch          # Hot reload development
make plugin-validate       # Validate plugin system
```

## Architecture Principles

### Clean Architecture

- **Dependency Rule**: Dependencies point inward toward business logic
- **Layer Separation**: Core → Domain → Application → Infrastructure
- **Interface Segregation**: Small, focused interfaces for better testability

### Domain-Driven Design

- **Bounded Contexts**: Plugin management as a distinct business domain
- **Entities**: Rich business objects with behavior and identity
- **Value Objects**: Immutable data structures for plugin metadata
- **Aggregates**: Consistency boundaries for plugin operations

### CQRS Pattern

- **Command Handlers**: Plugin lifecycle operations (create, activate, deactivate)
- **Query Handlers**: Plugin discovery and status retrieval
- **Event Sourcing**: Plugin state changes as event streams

## Support & Contributing

### Getting Help

- **GitHub Issues**: [Report bugs and request features](https://github.com/flext-sh/flext/issues)
- **Discussions**: [Community Q&A and ideas](https://github.com/flext-sh/flext/discussions)
- **Documentation**: Browse this documentation for detailed guides

### Contributing

- **Development**: Follow Clean Architecture and quality standards
- **Testing**: Maintain 85%+ coverage with quality test cases
- **Documentation**: Update docs for public APIs and patterns
- **Code Review**: All changes require review and quality gate passage

### Commercial Support

Enterprise support and consulting available through [team@flext.sh](mailto:team@flext.sh).

---

**Next Steps**: Start with the [Quick Start Guide](guides/quick-start.md) or explore the [Architecture Overview](architecture/README.md) to understand the system design.
