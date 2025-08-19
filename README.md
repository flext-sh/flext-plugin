# flext-plugin

**Type**: Infrastructure Library | **Status**: Active Development | **Dependencies**: flext-core

Plugin management system for the FLEXT ecosystem with dynamic loading and lifecycle management.

> ⚠️ Development Status: Core domain entities working; CLI implementation missing; ~33% test coverage.

## Quick Start

```bash
# Install dependencies
poetry install

# Test basic functionality
python -c "from flext_plugin import FlextPluginPlatform; platform = FlextPluginPlatform(); print('✅ Working')"

# Development setup
make setup
```

## Current Reality

**What Actually Works:**

- Domain entities (FlextPlugin, FlextPluginConfig, FlextPluginRegistry)
- Plugin lifecycle management (discover → load → activate)
- Clean Architecture implementation with DDD patterns
- FlextResult pattern integration

**What Needs Work:**

- CLI implementation missing (entry point defined but no cli.py file)
- Hot reload system incomplete
- Test coverage improvement (33% → 90% target)
- Singer/Meltano integration superficial

## Architecture Role in FLEXT Ecosystem

### **Infrastructure Component**

FLEXT Plugin provides plugin management infrastructure for distributed services:

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLEXT ECOSYSTEM (32 Projects)                 │
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

### **Core Responsibilities**

1. **Plugin Discovery**: Dynamic loading of plugins from directories
2. **Lifecycle Management**: Plugin activation, deactivation, hot-reload
3. **Singer Integration**: Support for Singer taps, targets, transforms

## Key Features

### **Current Capabilities**

- **Dynamic Plugin Loading**: Hot-pluggable components with runtime discovery
- **Lifecycle Management**: Plugin activation, deactivation, lifecycle states
- **Clean Architecture**: Domain/application/infrastructure layer separation
- **FlextResult Pattern**: Type-safe error handling throughout

### **FLEXT Core Integration**

- **FlextResult Pattern**: Railway-oriented programming for error handling
- **FlextEntity**: Domain entities with validation and business rules
- **Dependency Injection**: Global container integration (via flext-core)

## Installation & Usage

### Installation

```bash
# Clone and install
cd /path/to/flext-plugin
poetry install

# Development setup
make setup
```

### Basic Usage

```python
from flext_plugin import FlextPluginPlatform, create_flext_plugin
from flext_plugin.core.types import PluginType

# Create plugin platform
platform = FlextPluginPlatform()

# Create a plugin
plugin = create_flext_plugin(
    name="my-data-extractor",
    version="1.0.0",
    plugin_type=PluginType.TAP
)

# Register plugin
result = platform.register_plugin(plugin)
if result.success:
    print(f"Plugin {plugin.name} registered successfully")
else:
    print(f"Registration failed: {result.error}")
```

## Development Commands

### Quality Gates (Zero Tolerance)

```bash
# Complete validation pipeline (run before commits)
make validate              # Full validation pipeline
make check                 # Quick lint + type check
make test                  # Run all tests (85% coverage target)
make lint                  # Code linting
make type-check            # Type checking
make format                # Code formatting
make security              # Security scanning
```

### Plugin Development

```bash
# Development setup
make setup                 # Complete development environment

# Plugin operations (requires CLI implementation)
make plugin-validate       # Validate plugin system
```

## Configuration

### Environment Variables

```bash
# Plugin discovery paths
export FLEXT_PLUGIN_DISCOVERY_PATHS="plugins:~/.flext/plugins"

# Hot reload settings
export FLEXT_PLUGIN_HOT_RELOAD=true
export FLEXT_PLUGIN_WATCH_INTERVAL=2
```

## Quality Standards

### **Quality Targets**

- **Coverage**: 85% target (currently ~33%)
- **Type Safety**: MyPy strict mode adoption
- **Linting**: Ruff with comprehensive rules
- **Security**: Bandit + pip-audit scanning

## Integration with FLEXT Ecosystem

### **FLEXT Core Patterns**

```python
# FlextResult for all operations
def register_plugin(plugin: FlextPlugin) -> FlextResult[FlextPlugin]:
    try:
        # Plugin registration logic
        return FlextResult[None].ok(registered_plugin)
    except Exception as e:
        return FlextResult[None].fail(f"Registration failed: {e}")
```

### **Service Integration**

- **FlexCore (Go)**: Plugin management via gRPC interface
- **FLEXT Service**: Data processing pipeline plugin integration
- **Singer Ecosystem**: Native tap/target/transform plugin support

## Current Status

**Version**: 0.9.0 (Development)

**Completed**:

- ✅ Domain entities (FlextPlugin, FlextPluginRegistry)
- ✅ Clean Architecture implementation
- ✅ Plugin lifecycle management

**In Progress**:

- 🔄 CLI implementation (entry point defined but missing cli.py)
- 🔄 Test coverage improvement (33% → 85%)
- 🔄 Hot reload system completion

**Planned**:

- 📋 Singer/Meltano integration
- 📋 Plugin discovery enhancements
- 📋 Performance optimization

## Contributing

### Development Standards

- **FLEXT Core Integration**: Use established patterns
- **Type Safety**: All code must pass MyPy
- **Testing**: Maintain coverage and ensure tests pass
- **Code Quality**: Follow linting rules

### Development Workflow

```bash
# Setup and validate
make setup
make validate
make test
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Links

- **[flext-core](../flext-core)**: Foundation library
- **[CLAUDE.md](CLAUDE.md)**: Development guidance
- **[Documentation](docs/)**: Complete documentation

---
