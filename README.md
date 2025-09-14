# flext-plugin

**Plugin discovery, loading, and lifecycle management** for the FLEXT ecosystem, providing **dynamic component loading** using **Clean Architecture patterns** with domain-driven design.

> **⚠️ STATUS**: Functional implementation with architectural compliance violations requiring resolution

---

## 🎯 Purpose and Role in FLEXT Ecosystem

### **For the FLEXT Ecosystem**

flext-plugin provides plugin management infrastructure for dynamic component loading across FLEXT projects. Current implementation includes plugin discovery, lifecycle management, and hot reload capabilities.

### **Key Responsibilities**

1. **Plugin Lifecycle Management** - Discovery, loading, activation, deactivation operations
2. **FLEXT Integration** - Uses FlextResult, FlextContainer, FlextModels.Entity patterns
3. **Extensibility Framework** - Foundation for Singer taps, targets, and custom extensions

### **Integration Points**

- **flext-core** → FlextResult, FlextContainer, FlextModels, FlextUtilities
- **flext-cli** → Command-line plugin management (currently disabled)
- **Singer Projects** → Plugin framework for data pipeline components
- **FLEXT Projects** → Extensibility infrastructure

---

## 🏗️ Architecture and Patterns

### **FLEXT-Core Integration Status**

| Pattern             | Status         | Description                     |
| ------------------- | -------------- | ------------------------------- |
| **FlextResult<T>**  | 🟢 Complete | Operations return FlextResult |
| **FlextService**    | 🟢 Complete | FlextPluginService inheritance  |
| **FlextContainer**  | 🟢 Complete | Dependency injection throughout |
| **Domain Patterns** | 🟢 Complete | FlextModels.Entity inheritance  |

> **Status**: 🔴 Critical Issues | 🟡 Partial Implementation | 🟢 Implemented

### **Implementation Metrics**

- **Source Code**: 6,562 lines across 20 modules
- **Classes**: 54 classes (violates FLEXT single-class-per-module standard)
- **Platform Methods**: 14 public methods (discover, load, unload, install, etc.)
- **Test Coverage**: 339 test methods

### **Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                FlextPluginPlatform (Facade)                     │
│  • discover_plugins()  • load_plugin()  • unload_plugin()       │
│  • install_plugin()   • enable_plugin() • disable_plugin()     │
├─────────────────────────────────────────────────────────────────┤
│ FlextPluginService | FlextPluginDiscoveryService               │
├─────────────────────────────────────────────────────────────────┤
│ FlextPluginEntity | FlextPluginConfig | FlextPluginMetadata     │
├─────────────────────────────────────────────────────────────────┤
│ PluginDiscovery | HotReload | RealAdapters                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### **Installation**

```bash
# FLEXT workspace development
git clone https://github.com/flext-sh/flext.git
cd flext/flext-plugin

# Setup development environment
make setup

# Verify installation
python -c "import flext_plugin; print(f'Version: {flext_plugin.__version__}')"
```

### **Basic Usage**

```python
from flext_plugin import FlextPluginPlatform
from flext_core import FlextContainer

# Initialize platform
container = FlextContainer()
platform = FlextPluginPlatform(container)

# Discover plugins (file-based only currently)
result = platform.discover_plugins("./plugins")
if result.success:
    plugins = result.data
    print(f"Found {len(plugins)} plugins")
```

---

## 🔧 Development

### **Essential Commands**

```bash
# Quality validation
make validate                   # Complete validation pipeline
make test                      # Run 339 test methods
make lint                      # Code quality checks
make type-check               # Type safety validation

# Development workflow
make format                   # Auto-format code
make check                    # Quick lint and type check
```

### **Quality Gates**

- **Test Suite**: 339 test methods across multiple test files
- **Type Safety**: MyPy compliance throughout codebase
- **Architecture**: Single-class-per-module compliance required
- **Coverage**: 90% minimum target configured

---

## 🧪 Testing

### **Test Structure**

```
tests/
├── unit/              # Domain and application tests
├── integration/       # Cross-layer integration
├── test_*.py         # Various test modules
└── conftest.py       # Test configuration
```

### **Testing Commands**

```bash
pytest tests/                  # Run all 339 tests
pytest --cov=flext_plugin     # Run with coverage reporting
pytest -m "not slow"          # Skip slow tests
```

---

## 📊 Status and Metrics

### **Quality Standards**

- **Coverage**: 90% minimum target (339 test methods)
- **Type Safety**: Complete MyPy compliance
- **Security**: File-based discovery only (no sandboxing)
- **FLEXT-Core Compliance**: Complete patterns, architecture issues remain

### **Ecosystem Integration**

- **Direct Dependencies**: All FLEXT projects can use plugin system
- **Service Dependencies**: flext-core (mandatory), flext-cli (disabled)
- **Integration Points**: Platform facade provides ecosystem-wide plugin management

---

## 🗺️ Roadmap

### **Current Version (0.9.0)**

Functional implementation with limitations:
- FlextPluginPlatform with 14 public methods
- Clean Architecture implementation
- Hot reload capabilities with file monitoring
- **Critical Issue**: 54 classes violate FLEXT single-class-per-module standard

### **Next Version (0.10.0)**

Required fixes:
- Architectural consolidation to FLEXT compliance
- Entry points discovery implementation (currently empty)
- CLI integration restoration
- Test failure resolution

---

## 📚 Documentation

- **[Getting Started](docs/getting-started.md)** - Installation and basic usage
- **[Architecture](docs/architecture.md)** - Design patterns and structure
- **[API Reference](docs/api-reference.md)** - Complete API documentation
- **[Development](docs/development.md)** - Contributing and workflows
- **[TODO & Roadmap](TODO.md)** - Development status and plans

---

## 🤝 Contributing

This project follows FLEXT ecosystem development standards:

1. **Code Standards**: Single class per module (compliance required)
2. **Quality Gates**: 90% test coverage, zero lint errors, type safety
3. **Architecture**: Clean Architecture with domain-driven design
4. **Integration**: Proper FLEXT-core pattern usage

See [CLAUDE.md](CLAUDE.md) for technical development guidance.

---

## 📄 License

MIT License - Copyright (c) 2025 FLEXT Team. All rights reserved.

---

**FLEXT Plugin System** - Extensibility foundation for the FLEXT data integration ecosystem.