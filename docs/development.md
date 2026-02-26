# Development Guide

<!-- TOC START -->

- [Development Setup](#development-setup)
  - [Prerequisites](#prerequisites)
  - [Setup Commands](#setup-commands)
- [Code Standards](#code-standards)
  - [FLEXT-Core Compliance](#flext-core-compliance)
  - [Quality Gates](#quality-gates)
- [Architecture Compliance](#architecture-compliance)
  - [Current Status ✅ COMPLIANT](#current-status-compliant)
  - [Compliance Achieved](#compliance-achieved)
- [Testing](#testing)
  - [Test Structure](#test-structure)
  - [Testing Commands](#testing-commands)
  - [Test Guidelines](#test-guidelines)
- [Plugin Development](#plugin-development)
  - [Creating Plugins](#creating-plugins)
  - [Hot Reload Development](#hot-reload-development)
- [Contributing Process](#contributing-process)
  - [1. Issue Discussion](#1-issue-discussion)
  - [2. Development](#2-development)
  - [3. Quality Validation](#3-quality-validation)
  - [4. Pull Request](#4-pull-request)
- [Debugging](#debugging)
  - [Common Issues](#common-issues)
- [Release Process](#release-process)
  - [Version Management](#version-management)
  - [Quality Requirements](#quality-requirements)
- [Getting Help](#getting-help)

<!-- TOC END -->

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

### Current Status ✅ COMPLIANT

1. **FLEXT Compliance**: ✅ Single-class-per-module standard achieved (19 classes across 20 modules)
1. **CLI Integration**: ⚠️ Implementation exists but disabled (dependency issues to resolve)
1. **Test Coverage**: Target 90% with comprehensive test suite (24 test files)

### Compliance Achieved

All modules follow the FLEXT single-class-per-module pattern:

```python
# ✅ COMPLIANT - Current implementation
class FlextPluginModels:
    """Unified plugin entities following FLEXT standards"""

    class Plugin(FlextModels.Entity):
        """Main plugin entity with business rules"""

    class Config(FlextModels.Entity):
        """Plugin configuration with validation"""

    class _ValidationHelper:
        """Nested helper class for domain logic"""
```

---

## Testing

### Test Structure

```
tests/
├── unit/                    # Unit tests for individual components (12 files)
├── integration/            # Integration tests (4 files)
├── e2e/                    # End-to-end plugin workflows (2 files)
├── fixtures/               # Shared test fixtures
├── conftest.py             # Test configuration and fixtures
└── test_*.py              # Various component tests (6 files)

Total: 24 test files targeting 90% coverage
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
            version="0.9.9",
            config={"plugin_type": PluginType.UTILITY},
            **kwargs
        )

    def execute(self, data: dict) -> FlextResult[t.Dict]:
        """Plugin business logic"""
        try:
            # Process data
            return FlextResult[t.Dict].ok(processed_data)
        except Exception as e:
            return FlextResult[t.Dict].fail(str(e))
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

- **Documentation**: Complete docs in docs/
- **Issues**: [GitHub Issues](https://github.com/flext-sh/flext/issues)
- **Code Review**: Submit PRs for review and feedback

---

For specific plugin development patterns and examples, see examples/ directory.
