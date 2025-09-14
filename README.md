# flext-plugin

**Plugin management system** for the FLEXT ecosystem, providing dynamic loading and lifecycle management using **Clean Architecture patterns** with domain-driven design.

> **⚠️ STATUS**: Active development with architectural compliance issues requiring resolution before production use.

---

## 🎯 Purpose and Role in FLEXT Ecosystem

### **For the FLEXT Ecosystem**

flext-plugin serves as the plugin management infrastructure for the FLEXT ecosystem's 33 interconnected projects, enabling dynamic component loading and extensibility across data integration services.

### **Key Responsibilities**

1. **Plugin Lifecycle Management** - Discovery, loading, activation, and hot reload capabilities
2. **FLEXT Integration** - Native integration with flext-core patterns and dependency injection
3. **Singer Ecosystem Support** - Plugin framework for Singer taps, targets, and transforms

### **Integration Points**

- **flext-core** → Base patterns, FlextResult, domain models, dependency injection
- **flext-cli** → Command-line plugin management (currently disabled)
- **Singer Projects (15)** → Plugin framework for data pipeline components
- **All 33 FLEXT Projects** → Extensibility and component management

---

## 🏗️ Architecture and Patterns

### **FLEXT-Core Integration Status**

| Pattern             | Status    | Description                     |
| ------------------- | --------- | ------------------------------- |
| **FlextResult<T>**  | 🟢 85%    | Domain operations and API calls |
| **FlextService**    | 🟢 90%    | Application service layer       |
| **FlextContainer**  | 🟢 80%    | Dependency injection container  |
| **Domain Patterns** | 🟢 85%    | DDD entities and business rules |

> **Status**: 🔴 Critical | 🟡 Partial | 🟢 Complete

### **Current Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLEXT ECOSYSTEM (33 Projects)                │
├─────────────────────────────────────────────────────────────────┤
│ Services: FlexCore(Go) | FLEXT Service(Go/Python) | Clients     │
├─────────────────────────────────────────────────────────────────┤
│ Applications: API | Auth | Web | CLI | Quality | Observability  │
├═════════════════════════════════════════════════════════════════┤
│ Infrastructure: Oracle | LDAP | LDIF | gRPC | [FLEXT-PLUGIN]   │
├─────────────────────────────────────────────────────────────────┤
│ Singer Ecosystem: Taps(5) | Targets(5) | DBT(4) | Extensions(1) │
├─────────────────────────────────────────────────────────────────┤
│ Foundation: FLEXT-CORE (FlextResult | DI | Domain Patterns)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### **Installation**

```bash
# Clone FLEXT workspace
git clone https://github.com/flext-sh/flext.git
cd flext/flext-plugin

# Setup development environment
make setup

# Verify installation
python -c "import flext_plugin; print(f'FLEXT Plugin v{flext_plugin.__version__}')"
```

### **Basic Usage**

```python
from flext_plugin import FlextPluginPlatform, create_flext_plugin
from flext_plugin.typings import PluginStatus

# Create plugin platform
platform = FlextPluginPlatform()

# Create a plugin
plugin = create_flext_plugin(
    name="data-processor",
    version="0.9.0",
    config={"description": "Data processing plugin"}
)

# Plugin lifecycle management
result = platform.load_plugin(plugin)
if result.success:
    activation = platform.enable_plugin("data-processor")
    if activation.success:
        print("Plugin loaded and activated")
```

---

## 🔧 Development

### **Essential Commands**

```bash
# Setup and validation
make setup                 # Complete development environment
make validate              # Full validation pipeline
make check                 # Quick health check (lint + type)

# Testing
make test                  # Full test suite (33% coverage currently)
make test-unit             # Unit tests only
make coverage-html         # Detailed coverage report

# Plugin development
make plugin-validate       # Validate plugin system
make plugin-watch          # Hot reload development mode
```

### **Quality Gates**

- **Type Safety**: MyPy strict mode with 100% coverage target
- **Code Quality**: Ruff linting with comprehensive rules
- **Security**: Bandit + pip-audit scanning
- **Coverage**: 85% minimum (currently 33%)

---

## 🧪 Testing

### **Test Structure**

```
tests/
├── unit/              # Domain and application layer tests
├── integration/       # Cross-layer integration tests
├── e2e/              # End-to-end plugin scenarios
└── fixtures/         # Shared test data and utilities
```

### **Testing Commands**

```bash
make test              # Full suite with coverage
make test-unit         # Fast unit tests
make test-integration  # Integration tests
pytest -m "not slow"   # Skip slow tests
```

---

## 📊 Status and Metrics

### **Quality Standards**

- **Coverage**: 85% minimum (currently 33%)
- **Type Safety**: MyPy strict mode compliance
- **Security**: Zero vulnerabilities via Bandit + pip-audit
- **FLEXT-Core Compliance**: 85% (architecture issues pending)

### **Ecosystem Integration**

- **Direct Dependencies**: Singer taps/targets, flext-web, flext-api
- **Service Dependencies**: flext-core, flext-observability
- **Integration Points**: 15+ connections across ecosystem

---

## 🗺️ Roadmap

### **Current Version (v0.9.0)**

Focus on architectural compliance and core plugin functionality:
- Fix multi-class-per-module issues (54 classes across 23 files)
- Enable CLI integration via flext-cli
- Improve test coverage and documentation

### **Next Version (v0.10.0)**

Enhanced plugin discovery and security:
- Entry points implementation alongside manual discovery
- Basic process isolation for plugin security
- Plugin packaging and distribution system

---

## 📚 Documentation

- **[Getting Started](docs/getting-started.md)** - Installation and basic usage
- **[Architecture](docs/architecture.md)** - Design patterns and structure
- **[API Reference](docs/api-reference.md)** - Complete API documentation
- **[Development](docs/development.md)** - Contributing and workflows
- **[Integration](docs/integration.md)** - Ecosystem integration patterns
- **[Examples](docs/examples/)** - Working code examples
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions
- **[TODO & Roadmap](docs/TODO.md)** - Development status and plans

---

## 🤝 Contributing

### **FLEXT-Core Compliance Checklist**

- [ ] Use FlextResult<T> for all operations
- [ ] Implement single class per module
- [ ] Follow Clean Architecture patterns
- [ ] Use dependency injection via FlextContainer
- [ ] Maintain 85%+ test coverage

### **Quality Standards**

- All code must pass MyPy strict mode
- Zero linting violations via Ruff
- Security scanning via Bandit + pip-audit
- Integration with flext-core patterns
- Professional English in all documentation

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/flext-sh/flext/issues)
- **Security**: Report security issues privately to maintainers

---

**flext-plugin v0.9.0** - Plugin management infrastructure enabling dynamic component loading across the FLEXT ecosystem.

**Mission**: Provide reliable, secure, and extensible plugin management capabilities that integrate seamlessly with FLEXT ecosystem patterns and standards.