# from flext-plugin/docs/architecture.md:207
from __future__ import annotations


class SingerTapPlugin(FlextPlugin):
    """Plugin implementing Singer tap protocol"""

    def create_tap(self) -> SingerTap:
        """Create Singer tap instance"""```
______________________________________________________________________

## Current Architecture Status ✅ COMPLIANT

### FLEXT Single-Class-Per-Module Compliance Achieved

All modules follow the FLEXT single-class-per-module standard with nested helper classes:

- ✅ `entities.py`: Unified `FlextPluginModels` class (domain entities)
- ✅ `implementations.py`: Unified `FlextPluginImplementations` class (concrete implementations)
- ✅ `hot_reload.py`: Unified `FlextPluginHotReload` class (file monitoring)
- ✅ All 20 modules: Single main class following FLEXT ecosystem patterns

### Architecture Achievements

- ✅ **Clean Architecture**: Proper domain/application/infrastructure layer separation
- ✅ **Domain-Driven Design**: Entities with business rules and validation
- ✅ **FLEXT Compliance**: Single-class-per-module standard achieved across all modules
- ✅ **Type Safety**: Complete MyPy compliance with Python 3.13+ features
- ✅ **Railway Pattern**: p.Result[T] throughout for composable error handling

______________________________________________________________________

## Future Architecture Enhancements

### Version 0.10.0 Enhancements

1. **Entry Points Discovery**: Python 3.13 `importlib.metadata` for pip-installable plugins
1. **CLI Integration**: Complete command-line interface with flext-cli integration
1. **Performance Optimization**: Enhanced plugin loading and execution efficiency
1. **Security Framework**: Plugin sandboxing and validation mechanisms

### Version 1.0.0 Enterprise Features

1. **Multi-Format Discovery**: Entry points + file-based + setuptools integration
1. **Advanced Security**: Process/container isolation for high-security environments
1. **Plugin Marketplace**: Registry integration for plugin distribution and discovery
1. **Enterprise Monitoring**: Comprehensive plugin metrics and health checks

### Integration Points

- **flext-cli**: Command-line plugin management
- **flext-web**: Web interface for plugin REDACTED_LDAP_BIND_PASSWORDistration
- **flext-api**: REST API for plugin operations
- **Singer Projects**: Plugin framework for data pipeline components

______________________________________________________________________

This architecture enables the plugin system to serve as reliable infrastructure for the entire FLEXT ecosystem while maintaining clean separation of concerns and integration with FLEXT-core patterns.

## Related Documentation

**Within Project**:

- Getting Started - Installation and basic usage
- API Reference - Complete API documentation
- Examples - Working code examples
- Development - Contributing guidelines

**Across Projects**:

- [flext-core Foundation](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-core/docs/architecture/overview.md) - Clean architecture and CQRS patterns
- [flext-core Service Patterns](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-core/docs/guides/service-patterns.md) - Service patterns and dependency injection
- [flext-meltano Pipelines](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-meltano/AGENTS.md) - Data integration and ELT orchestration

**External Resources**:

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
