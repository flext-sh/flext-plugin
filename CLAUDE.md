# flext-plugin - FLEXT Data Integration

**Hierarchy**: PROJECT
**Parent**: [../CLAUDE.md](../CLAUDE.md) - Workspace standards
**Last Update**: 2025-12-07

---

## Project Overview

**FLEXT-Plugin** is the enterprise-grade plugin management system and extensibility foundation for the entire FLEXT ecosystem. It provides comprehensive plugin lifecycle management with hot-reload capabilities, security validation, and Clean Architecture patterns.

**Version**: 0.9.0  
**Status**: Production-ready  
**Python**: 3.13+  
**Coverage Target**: 90%

---

## Essential Commands

```bash
# Setup
make setup                    # Install deps + pre-commit hooks

# Quality gates (MANDATORY before commit)
make validate                 # Full validation: lint + type + security + test
make check                    # Quick check: lint + type only

# Individual checks
make lint                     # Ruff linting (ZERO violations)
make type-check              # Pyrefly type checking (ZERO errors)
make test                    # Full test suite (90% coverage minimum)
make format                  # Auto-format code with Ruff
```

---

## Key Patterns

### Plugin Management

```python
from flext_core import FlextResult
from flext_plugin import FlextPluginManager

manager = FlextPluginManager()

# Load plugin
result = manager.load_plugin("path/to/plugin")
if result.is_success:
    plugin = result.unwrap()
```

---

## Critical Development Rules

### ZERO TOLERANCE Policies

**ABSOLUTELY FORBIDDEN**:

- ❌ Exception-based error handling (use FlextResult)
- ❌ Type ignores or `Any` types
- ❌ Mockpatch in tests

**MANDATORY**:

- ✅ Use `FlextResult[T]` for all operations
- ✅ Complete type annotations
- ✅ Zero Ruff violations
- ✅ 90%+ test coverage

---

**See Also**:

- [Workspace Standards](../CLAUDE.md)
- [flext-core Patterns](../flext-core/CLAUDE.md)
- [flext-meltano Patterns](../flext-meltano/CLAUDE.md)
