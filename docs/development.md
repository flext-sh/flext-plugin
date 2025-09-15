# Development Guide

**Contributing to FLEXT Plugin**

---

## Development Setup

### Prerequisites

- **Python 3.13+**
- **Poetry** for dependency management
- **FLEXT Workspace** environment

### Setup Commands

```bash
# Clone and setup
git clone https://github.com/flext-sh/flext.git
cd flext/flext-plugin

# Development environment
make setup                 # Complete setup
make info                  # Project information

# Verification
python -c "import flext_plugin; print('Setup successful')"
```

---

## Code Standards

### FLEXT-Core Compliance

- **FlextResult<T>**: All operations must return FlextResult
- **Single Class Per Module**: Each module has one main class with nested helpers
- **Clean Architecture**: Proper layer separation
- **Type Safety**: 100% MyPy compliance

### Quality Gates

```bash
# Required before commits
make validate              # Complete validation pipeline
make check                 # Quick lint and type check

# Testing
make test                  # Full test suite (85% coverage target)
make coverage-html         # Detailed coverage report
```

---

## Architecture Compliance

### Current Issues

1. **Multi-Class Modules**: 54 classes across 23 files need consolidation
2. **CLI Integration**: Disabled functionality needs enabling
3. **Test Coverage**: Currently 33%, target 85%

### Consolidation Pattern

```python
# Before (violation)
# entities.py with 8 separate classes

# After (compliant)
class FlextPluginEntities:
    """Unified plugin entities"""

    class Plugin(FlextModels.Entity):
        """Main plugin entity"""

    class Config(FlextModels.Entity):
        """Plugin configuration"""

    class _ValidationHelper:
        """Nested helper class"""
```

---

## Testing

### Test Structure

```
tests/
├── unit/              # Domain and application tests
├── integration/       # Cross-layer integration
├── e2e/              # End-to-end scenarios
└── fixtures/         # Test utilities
```

### Testing Commands

```bash
make test              # All tests with coverage
make test-unit         # Fast unit tests only
pytest -m "not slow"   # Skip slow tests
```

### Test Guidelines

- Use real dependencies over mocks when possible
- Follow AAA pattern (Arrange, Act, Assert)
- Test FlextResult success and failure paths
- Maintain 85% minimum coverage

---

## Plugin Development

### Creating Plugins

```python
from flext_plugin import FlextPlugin, PluginType

class MyPlugin(FlextPlugin):
    def __init__(self, **kwargs):
        super().__init__(
            name="my-plugin",
            version="0.9.0",
            config={"plugin_type": PluginType.UTILITY},
            **kwargs
        )

    async def execute(self, data: dict) -> FlextResult[dict]:
        """Plugin business logic"""
        try:
            # Process data
            return FlextResult[dict].ok(processed_data)
        except Exception as e:
            return FlextResult[dict].fail(str(e))
```

### Hot Reload Development

```bash
# Enable hot reload for development
make plugin-watch

# Environment variables
export FLEXT_PLUGIN_HOT_RELOAD=true
export FLEXT_PLUGIN_WATCH_INTERVAL=2
```

---

## Contributing Process

### 1. Issue Discussion

- Discuss significant changes in GitHub issues
- Get alignment on approach before implementation

### 2. Development

- Create feature branch from main
- Follow code standards and architecture patterns
- Add tests for new functionality

### 3. Quality Validation

```bash
make validate          # All quality gates must pass
make test             # 85% coverage required
```

### 4. Pull Request

- Clear description of changes
- Reference related issues
- Pass all CI checks

---

## Debugging

### Common Issues

#### Import Errors

```bash
# Verify Python path
export PYTHONPATH="src:$PYTHONPATH"

# Check dependencies
poetry show --tree
```

#### Plugin Loading Issues

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use platform validation
result = platform.validate_plugin(plugin)
if result.is_failure:
    print(f"Validation error: {result.error}")
```

#### Hot Reload Problems

```bash
# Check watchdog integration
make plugin-validate

# Verify file permissions
ls -la plugins/
```

---

## Release Process

### Version Management

- Follow semantic versioning (SemVer)
- Update version in `__version__.py`
- Update CHANGELOG.md

### Quality Requirements

- All quality gates passing
- 85% test coverage
- Architecture compliance verified
- Documentation updated

---

## Getting Help

- **Documentation**: Complete docs in [docs/](.)
- **Issues**: [GitHub Issues](https://github.com/flext-sh/flext/issues)
- **Code Review**: Submit PRs for review and feedback

---

For specific plugin development patterns and examples, see [examples/](examples/) directory.
