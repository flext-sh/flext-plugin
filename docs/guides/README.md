# FLEXT Plugin Development Guides

Comprehensive step-by-step guides for developing plugins with the FLEXT Plugin system.

## Guide Categories

### 🚀 Getting Started

- **[Quick Start](quick-start.md)** - Get up and running with FLEXT Plugin in minutes
- **[Installation Guide](installation.md)** - Detailed installation and setup instructions
- **[Your First Plugin](first-plugin.md)** - Create your first plugin step-by-step

### 🔧 Development Workflows

- **[Plugin Development](plugin-development.md)** - Complete plugin development guide
- **[Hot Reload Development](hot-reload.md)** - Development with live reloading
- **[Testing Guide](testing.md)** - Comprehensive testing strategies
- **[Debugging Guide](debugging.md)** - Debugging and troubleshooting plugins

### 🎯 Plugin Types

- **[Singer Integration](singer-integration.md)** - Singer tap/target development
- **[Service Plugins](service-plugins.md)** - Microservice integration patterns
- **[Utility Plugins](utility-plugins.md)** - General-purpose utility plugins
- **[Custom Plugin Types](custom-plugin-types.md)** - Creating custom plugin categories

### 🏗️ Architecture & Integration

- **[Clean Architecture](clean-architecture.md)** - Implementing Clean Architecture patterns
- **[Domain-Driven Design](domain-driven-design.md)** - DDD implementation in plugins
- **[FLEXT Ecosystem Integration](ecosystem-integration.md)** - Integration with FLEXT services
- **[Performance Optimization](performance-optimization.md)** - Plugin performance best practices

### 📋 Best Practices

- **[Code Quality](code-quality.md)** - Quality standards and practices
- **[Security Guidelines](security.md)** - Security best practices for plugins
- **[Configuration Management](configuration.md)** - Plugin configuration patterns
- **[Error Handling](error-handling.md)** - Robust error handling strategies

## Quick Reference

### Essential Commands

```bash
# Setup development environment
make setup

# Quality gates (run before commit)
make validate              # Complete validation
make check                 # Quick health check
make fix                   # Auto-fix issues

# Testing
make test                  # Full test suite
make test-unit             # Unit tests only
make coverage-html         # Coverage report

# Plugin development
make plugin-watch          # Hot reload development
make plugin-validate       # Validate plugin system
```

### Basic Plugin Template

```python
from flext_plugin.domain.entities import FlextPlugin
from flext_plugin.core.types import PluginStatus, PluginType
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import t
from flext_core import u

class MyPlugin(FlextPlugin):
    def __init__(self, **kwargs):
        super().__init__(
            name="my-plugin",
            version="0.9.9",
            config={"plugin_type": PluginType.UTILITY},
            **kwargs
        )

    def initialize(self) -> FlextResult[bool]:
        # Setup plugin resources
        return FlextResult[None].ok(data=True)

    def execute(self, data) -> FlextResult:
        # Core plugin logic
        return FlextResult[None].ok({"processed": True})

    def cleanup(self) -> FlextResult[bool]:
        # Cleanup resources
        return FlextResult[None].ok(data=True)
```

### Development Workflow

1. **Setup**: `make setup` - Initialize development environment
2. **Create**: Implement plugin following Clean Architecture patterns
3. **Test**: Add comprehensive tests following project patterns
4. **Validate**: `make validate` - All quality gates must pass
5. **Integrate**: Register and test with FLEXT platform

## Prerequisites

### System Requirements

- **Python 3.13+**: Modern Python with type hints and support
- **Poetry**: Dependency management and packaging
- **Git**: Version control and repository management

### FLEXT Dependencies

- **flext-core**: Foundation patterns and utilities
- **flext-observability**: Monitoring and health checks

### Development Tools

- **pytest**: Testing framework with comprehensive plugin support
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checking with strict mode
- **bandit**: Security vulnerability scanning

## Learning Path

### Beginner

1. **[Quick Start](quick-start.md)** - Basic concepts and first plugin
2. **[Plugin Development](plugin-development.md)** - Core development patterns
3. **[Testing Guide](testing.md)** - Testing your plugins

### Intermediate

1. **[Singer Integration](singer-integration.md)** - Data pipeline plugins
2. **[Service Plugins](service-plugins.md)** - Microservice integration
3. **[Hot Reload Development](hot-reload.md)** - Development optimization

### Advanced

1. **[Clean Architecture](clean-architecture.md)** - Architectural patterns
2. **[Performance Optimization](performance-optimization.md)** - Scaling plugins
3. **[Custom Plugin Types](custom-plugin-types.md)** - Extending the system

## Support & Resources

### Documentation

- **[API Reference](../api/README.md)** - Complete API documentation
- **[Architecture Guide](../architecture/README.md)** - System architecture
- **[Examples](../examples/README.md)** - Practical implementation examples

### Community

- **GitHub Issues**: [Report bugs and request features](https://github.com/flext-sh/flext/issues)
- **Discussions**: [Community Q&A and ideas](https://github.com/flext-sh/flext/discussions)

### Commercial Support

Enterprise support and consulting available through [team@flext.sh](mailto:team@flext.sh).

---

**Next Steps**: Start with the [Quick Start Guide](quick-start.md) to create your first plugin, then explore specific guides based on your use case.
