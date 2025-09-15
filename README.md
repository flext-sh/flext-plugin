# flext-plugin

**Enterprise plugin management system** for the FLEXT ecosystem, providing **comprehensive plugin lifecycle management** with **hot-reload capabilities**, **security validation**, and **Clean Architecture patterns**.

> **📊 STATUS**: Functional plugin system with architectural consolidation needed for FLEXT compliance

---

## 🎯 Purpose and Role in FLEXT Ecosystem

### **For the FLEXT Ecosystem**

flext-plugin provides plugin management infrastructure for dynamic component loading across FLEXT projects. Current implementation includes plugin discovery, lifecycle management, and hot reload capabilities.

### **Key Responsibilities**

1. **Plugin Lifecycle Management** - Discovery, loading, activation, deactivation, and hot-reload
2. **Entry Points & File Discovery** - Dual discovery mechanisms for maximum flexibility
3. **Security & Validation** - Plugin sandboxing and comprehensive validation framework
4. **FLEXT Integration** - Complete FlextResult, FlextContainer, FlextModels patterns
5. **Singer/Meltano Support** - Foundation for data pipeline plugin ecosystem

### **Integration Points**

- **flext-core** → FlextResult, FlextContainer, FlextModels, FlextUtilities, FlextLogger
- **flext-cli** → Command-line plugin management (implemented, disabled in __init__.py)
- **watchdog** → File system monitoring for hot-reload capabilities
- **Singer Projects** → Plugin framework for data pipeline taps and targets
- **Setuptools** → Entry points discovery (stub implementation)
- **FLEXT Ecosystem** → Foundation for all plugin-enabled FLEXT projects

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

- **Source Code**: 6,581 lines across 23 modules
- **Classes**: 114 classes across plugin system components
- **Exports**: 89 public API exports in __init__.py
- **Platform Methods**: 14+ public methods (discover, load, unload, install, hot-reload)
- **Test Coverage**: Comprehensive test suite with real plugin operations
- **Architecture**: Clean Architecture with domain/application/infrastructure layers

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
pytest tests/                  # Run comprehensive test suite (21 test files)
pytest --cov=flext_plugin     # Run with coverage reporting
pytest -m "not slow"          # Skip slow tests
pytest tests/unit/             # Unit tests only
pytest tests/integration/      # Integration tests only
pytest tests/e2e/             # End-to-end tests only
```

---

## 📊 Status and Metrics

### **Quality Standards**

- **Coverage**: 90% minimum target with real plugin operations
- **Type Safety**: Complete MyPy compliance across 23 modules
- **Security**: File-based discovery (sandboxing framework planned)
- **FLEXT-Core Compliance**: Complete FlextResult/Container/Models patterns
- **Architecture**: Clean Architecture with 114 classes requiring consolidation
- **Hot Reload**: Real-time plugin monitoring with watchdog integration

### **Ecosystem Integration**

- **Direct Dependencies**: All FLEXT projects can use plugin system
- **Service Dependencies**: flext-core (mandatory), flext-cli (disabled)
- **Integration Points**: Platform facade provides ecosystem-wide plugin management

---

## 🗺️ Roadmap

### **Current Version (0.9.0)**

Comprehensive plugin ecosystem:
- **FlextPluginPlatform** - Main facade with complete plugin lifecycle
- **Discovery System** - File-based and entry points mechanisms
- **Hot Reload** - Real-time plugin monitoring with watchdog integration
- **Security Framework** - Plugin validation and sandboxing (planned)
- **Clean Architecture** - Domain entities, ports, adapters, services
- **Architecture Consolidation Needed** - Multiple classes per module requiring unification

### **Next Version (0.10.0)**

Architectural consolidation:
- **Single-class-per-module compliance** - Unify 114 classes following FLEXT standards
- **Entry points discovery** - Complete setuptools entry points implementation
- **CLI integration** - Restore flext-cli integration (currently disabled)
- **Security hardening** - Complete plugin sandboxing implementation
- **Performance optimization** - Plugin loading and hot-reload efficiency

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

1. **Code Standards**: Single class per module (consolidation in progress)
2. **Quality Gates**: 90% test coverage, zero lint errors, type safety
3. **Architecture**: Clean Architecture with domain/application/infrastructure layers
4. **Modern Patterns**: Entry points + file discovery, hot reload, security validation
5. **Integration**: Complete FLEXT-core pattern usage with FlextResult throughout

See [CLAUDE.md](CLAUDE.md) for technical development guidance.

---

## 📄 License

MIT License - Copyright (c) 2025 FLEXT Team. All rights reserved.

---

**FLEXT Plugin System** - Extensibility foundation for the FLEXT data integration ecosystem.