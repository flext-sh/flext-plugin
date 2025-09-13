# FLEXT-PLUGIN CLAUDE.MD

**Enterprise Plugin Management System & Extensibility Foundation for FLEXT Ecosystem**  
**Version**: 0.9.0 | **Authority**: PLUGIN SYSTEM AUTHORITY | **Updated**: 2025-01-08  
**Status**: Production-ready plugin management platform with zero errors across all quality gates

## 🎯 FLEXT-PLUGIN MISSION (PLUGIN SYSTEM AUTHORITY)

**CRITICAL ROLE**: flext-plugin is the enterprise-grade plugin management system and extensibility foundation for the entire FLEXT ecosystem.

**ZERO TOLERANCE ENFORCEMENT (PLUGIN SYSTEM AUTHORITY)**:

### ⛔ ABSOLUTELY FORBIDDEN (IMMEDIATE TERMINATION POLICIES)

#### 1. **Plugin System Violations**

- **FORBIDDEN**: Direct plugin loading without FlextPluginPlatform
- **FORBIDDEN**: Custom plugin discovery implementations
- **FORBIDDEN**: Plugin lifecycle management outside domain entities
- **FORBIDDEN**: Manual plugin state management bypassing FlextPluginRegistry
- **MANDATORY**: ALL plugin operations MUST use FlextPluginPlatform

#### 2. **Plugin Architecture Violations**

- **FORBIDDEN**: Plugin business logic mixed with infrastructure code
- **FORBIDDEN**: Direct file system operations outside discovery protocols
- **FORBIDDEN**: Plugin configuration outside FlextPluginConfig entities
- **MANDATORY**: Use Clean Architecture layers for ALL plugin operations

#### 3. **Enterprise Plugin Security Violations**

- **FORBIDDEN**: Plugin execution without validation
- **FORBIDDEN**: Custom plugin isolation mechanisms
- **FORBIDDEN**: Plugin secrets in plain text or unsafe storage
- **MANDATORY**: Use FlextPluginSecurity for ALL plugin validation and execution

## 🏛️ ENTERPRISE PLUGIN ARCHITECTURE (CLEAN ARCHITECTURE + DDD AUTHORITY)

### **Zero Tolerance Plugin Quality Requirements**

```bash
# MANDATORY before ANY plugin development
make validate                   # Complete pipeline: 100% type safety + 85% coverage + zero security issues
make plugin-validate           # Validate complete plugin system integrity
make plugin-discovery          # Verify plugin discovery mechanisms
make test-plugin              # Execute comprehensive plugin test suite
```

### **Production Plugin Management Configuration (MANDATORY)**

#### Enterprise Plugin Platform (FLEXT AUTHORITY)

```python
from flext_plugin import FlextPluginPlatform, FlextPluginConfig
from flext_core import FlextContainer

# MANDATORY: Use enterprise plugin platform patterns
container = FlextContainer()
platform = FlextPluginPlatform(container)

# MANDATORY: Enterprise plugin configuration
plugin_config = FlextPluginConfig(
    name="enterprise-extension",
    version="0.9.0",
    plugin_type=PluginType.EXTENSION,          # Enterprise plugin classification
    author="FLEXT Enterprise",                 # Enterprise attribution
    description="Production enterprise plugin",
    dependencies=["flext-core", "flext-api"],  # FLEXT ecosystem dependencies
    security_level=PluginSecurityLevel.HIGH,   # Enterprise security requirements
    enable_hot_reload=True,                    # Production hot-reload support
    enable_monitoring=True,                    # Enterprise monitoring integration
)

# MANDATORY: Enterprise plugin registration
registration_result = await platform.register_plugin(plugin_config)
if registration_result.success:
    plugin = registration_result.value
    logger.info(f"Plugin {plugin.name} registered successfully")
```

### **Plugin Discovery & Lifecycle Management (PRODUCTION PATTERNS)**

#### Enterprise Plugin Discovery (Clean Architecture)

```python
from flext_plugin import (
    FlextPluginDiscoveryService,
    FlextPluginRegistry,
    PluginDiscovery
)

# MANDATORY: Use discovery patterns for ALL plugin operations
discovery_service = FlextPluginDiscoveryService()

# Production plugin discovery with enterprise patterns
discovery_result = await discovery_service.discover_plugins(
    paths=[
        "/opt/flext/plugins",           # Enterprise plugin directory
        "~/.flext/plugins",             # User plugin directory
        "./plugins"                     # Project plugin directory
    ],
    plugin_types=[
        PluginType.EXTENSION,
        PluginType.SERVICE,
        PluginType.MIDDLEWARE,
        PluginType.TAP,                 # Singer ecosystem integration
        PluginType.TARGET,              # Singer ecosystem integration
    ],
    enable_validation=True,             # Production validation required
    enable_security_scan=True,          # Enterprise security scanning
)

if discovery_result.success:
    # MANDATORY: Process via FlextResult patterns
    plugins = discovery_result.value
    logger.info(f"Discovered {len(plugins)} enterprise plugins")
```

### **Plugin Hot Reload System (ENTERPRISE AUTOMATION)**

#### Production Hot Reload Management

```python
from flext_plugin import FlextPluginHotReloadManager

# MANDATORY: Enterprise hot reload with state management
hot_reload_config = FlextPluginHotReloadConfig(
    watch_paths=["/opt/flext/plugins", "./plugins"],
    reload_interval=2,                  # 2 second reload interval
    enable_rollback=True,               # Enterprise rollback support
    max_reload_attempts=3,              # Production retry policy
    enable_state_persistence=True,      # State persistence for reliability
)

hot_reload_manager = FlextPluginHotReloadManager(
    platform=platform,
    config=hot_reload_config
)

# Start enterprise hot reload monitoring
await hot_reload_manager.start_monitoring()
```

## 🔒 ENTERPRISE PLUGIN SECURITY (ZERO TOLERANCE)

### **Plugin Security Framework (PRODUCTION REQUIREMENTS)**

#### Plugin Validation & Sandboxing

```python
from flext_plugin import FlextPluginSecurity, PluginSecurityLevel

# MANDATORY: Enterprise plugin security patterns
security_manager = FlextPluginSecurity()

# Production plugin validation before execution
security_result = await security_manager.validate_plugin(
    plugin=plugin,
    security_level=PluginSecurityLevel.HIGH,
    enable_sandboxing=True,             # Enterprise sandboxing required
    allowed_imports=ENTERPRISE_ALLOWED_IMPORTS,
    allowed_operations=ENTERPRISE_ALLOWED_OPS,
)

if security_result.success:
    # Plugin is safe for enterprise execution
    execution_result = await platform.execute_plugin(plugin, security_context)
```

### **Plugin Data Protection (ENTERPRISE COMPLIANCE)**

- **Plugin Isolation**: All plugins executed in secure sandboxes
- **Data Encryption**: Plugin data encrypted at rest and in transit
- **Access Control**: Role-based plugin access via FlextAuth integration
- **Audit Logging**: Complete plugin operation audit via FlextObservability patterns

## 🔧 ENTERPRISE PLUGIN DEVELOPMENT COMMANDS (ZERO TOLERANCE WORKFLOWS)

### **Mandatory Plugin Quality Gates (ZERO ERRORS TOLERANCE)**

```bash
# MANDATORY: Complete plugin system validation pipeline
make validate                   # 100% type safety + 85% coverage + zero security vulnerabilities
make plugin-validate           # Enterprise plugin system integrity validation
make plugin-discovery          # Plugin discovery mechanisms verification
make test-plugin               # Production plugin functionality validation
make test-hot-reload           # Hot-reload system validation with real file operations
make security                  # Bandit + pip-audit: zero security vulnerabilities
```

### **Plugin System Quality Standards (PRODUCTION REQUIREMENTS)**

```bash
# Type Safety & Code Quality (ZERO TOLERANCE)
make type-check                # MyPy strict mode: zero errors across all plugin modules
make lint                      # Ruff comprehensive linting: enterprise plugin standards
make format                    # Auto-format with enterprise code standards

# Enterprise Plugin Testing (COMPREHENSIVE COVERAGE)
make test                      # 85% minimum coverage with real plugin operations
make test-unit                 # Isolated plugin unit tests (domain entities, services)
make test-integration          # Cross-layer plugin integration testing
make test-e2e                  # End-to-end plugin lifecycle testing
make coverage-html             # Detailed HTML coverage report generation
```

### **Plugin CLI Operations (ENTERPRISE PLUGIN MANAGEMENT)**

```bash
# Enterprise Plugin CLI Commands
flext-plugin create --name enterprise-extension --type EXTENSION
flext-plugin install --plugin production-plugin --version 1.0.0
flext-plugin list --format json --filter "status:ACTIVE"
flext-plugin validate --all --security-scan
flext-plugin watch --directory /opt/flext/plugins --hot-reload
flext-plugin platform --status --health-check

# Production Plugin Operations
flext-plugin registry --add-source https://plugins.flext.enterprise
flext-plugin registry --publish-plugin ./my-plugin --version 0.9.0
flext-plugin security --scan-plugin ./suspicious-plugin
flext-plugin backup --plugins-state /backup/plugins-$(date +%Y%m%d)
```

### **Plugin Development Workflow (CLEAN ARCHITECTURE)**

```bash
# Environment Setup
make setup                     # Complete plugin development environment
make install                   # Install all enterprise dependencies
make deps-update               # Update plugin dependencies securely

# Plugin System Operations
make plugin-operations         # Complete plugin system validation
make plugin-test               # Test plugin platform with real scenarios
make diagnose                  # Complete plugin system diagnostics and health check
```

## 🏗️ ENTERPRISE PLUGIN SYSTEM ARCHITECTURE (CLEAN ARCHITECTURE + DDD)

### **Plugin System Integration Layers (PRODUCTION SEPARATION)**

#### 1. **Domain Layer (Plugin Business Logic)**

```python
# Plugin domain entities with business rules
from flext_plugin import (
    FlextPlugin,                    # Core plugin entity
    FlextPluginConfig,              # Plugin configuration entity
    FlextPluginMetadata,            # Plugin metadata entity
    FlextPluginRegistry,            # Plugin registry entity
    PluginStatus,                   # Plugin lifecycle status
    PluginType,                     # Plugin type classification
)
```

#### 2. **Application Layer (Plugin Use Cases)**

```python
# Plugin application services and handlers
from flext_plugin import (
    FlextPluginService,             # Core plugin service
    FlextPluginDiscoveryService,    # Plugin discovery service
    FlextPluginHandler,             # Plugin operation handler
    FlextPluginRegistrationHandler, # Plugin registration handler
)
```

#### 3. **Infrastructure Layer (Plugin Platform)**

```python
# Plugin platform and infrastructure services
from flext_plugin import (
    FlextPluginPlatform,            # Main plugin platform
    FlextPluginHotReloadManager,    # Hot-reload management
    FlextPluginSecurity,            # Plugin security framework
)
```

#### 4. **Interface Layer (CLI & APIs)**

```python
# Plugin interfaces and CLI operations
from flext_plugin import (
    FlextPluginCLI,                 # Command-line interface
    FlextPluginAPI,                 # REST API interface
    FlextPluginSimpleAPI,           # Simplified API
)
```

### **Plugin Configuration Architecture (ENTERPRISE PATTERNS)**

```python
# MANDATORY: Enterprise plugin configuration structure
from flext_plugin import FlextPluginConfig

enterprise_config = FlextPluginConfig(
    name="enterprise-extension",
    version="0.9.0",
    plugin_type=PluginType.EXTENSION,
    author="FLEXT Enterprise",
    dependencies=["flext-core>=0.9.0", "flext-api>=0.9.0"],
    security_requirements={
        "sandboxing": True,
        "network_access": False,
        "file_system_access": "read-only",
        "allowed_modules": ["flext_core", "flext_api"]
    },
    monitoring={
        "enable_metrics": True,
        "enable_tracing": True,
        "enable_health_checks": True
    }
)
```

### **Plugin Exception Architecture (COMPREHENSIVE ERROR HANDLING)**

```python
# Complete plugin system error hierarchy
from flext_plugin import (
    FlextPluginError,                   # Base plugin error
    FlextPluginDiscoveryError,          # Plugin discovery failures
    FlextPluginLoadingError,            # Plugin loading failures
    FlextPluginExecutionError,          # Plugin execution failures
    FlextPluginSecurityError,           # Plugin security violations
    FlextPluginConfigurationError,      # Plugin configuration errors
)
```

## 📦 FLEXT ECOSYSTEM INTEGRATION (MANDATORY PLUGIN DEPENDENCIES)

### **FLEXT Foundation Dependencies (ENTERPRISE PLUGIN INTEGRATION)**

```python
# MANDATORY: Core FLEXT patterns for plugin system
from flext_core import (
    FlextResult,              # Railway-oriented programming (ALL plugin operations)
    FlextLogger,              # Enterprise logging patterns for plugins
    FlextContainer,           # Dependency injection container for plugin services
    FlextConfig,             # Configuration management for plugin settings
)

# MANDATORY: Enterprise API patterns for plugin integrations
from flext_api import (
    FlextApiClient,          # Base API client patterns for plugin APIs
    FlextApiAuth,            # Enterprise authentication for plugin access
    FlextApiPlugin,          # Plugin API integration patterns
)

# MANDATORY: Observability integration for plugin monitoring
from flext_observability import (
    FlextMetrics,            # Plugin metrics collection and reporting
    FlextTracing,            # Distributed tracing for plugin operations
    FlextAlerting,           # Plugin health alerting and notifications
)

# MANDATORY: Configuration management for plugin ecosystem
from flext_config import (
    FlextConfigManager,      # Centralized plugin configuration management
    FlextSecretManager,      # Secure plugin credential management
)
```

### **Plugin System Import Standards (ZERO TOLERANCE ENFORCEMENT)**

#### ✅ **MANDATORY: Always Use These Plugin Patterns**

```python
# CORRECT: Root-level plugin imports ONLY
from flext_plugin import FlextPluginPlatform
from flext_plugin import FlextPluginDiscoveryService
from flext_plugin import PluginType, PluginStatus

# CORRECT: flext-core integration for plugin operations
from flext_core import FlextResult, get_logger
plugin_result: FlextResult[FlextPlugin] = await platform.register_plugin(config)
```

#### ❌ **ABSOLUTELY FORBIDDEN: These Plugin Import Patterns**

```python
# FORBIDDEN: Internal plugin module imports
from flext_plugin.domain.entities import FlextPlugin          # ❌ VIOLATION
from flext_plugin.internal.discovery import PluginLoader     # ❌ VIOLATION

# FORBIDDEN: Direct plugin loading mechanisms
import importlib                                             # ❌ VIOLATION (use FlextPluginPlatform)
import sys                                                   # ❌ VIOLATION (use plugin discovery)
import subprocess                                            # ❌ VIOLATION (security risk)

# FORBIDDEN: Custom plugin implementations
class MyPluginManager: pass                                  # ❌ VIOLATION (use FlextPluginPlatform)
```

## 🔍 PLUGIN SYSTEM QUALITY REQUIREMENTS (ENTERPRISE STANDARDS)

### **Plugin Type Safety (100% COMPLIANCE MANDATORY)**

```python
# MANDATORY: All plugin operations must be typed
async def register_plugin(
    self,
    config: FlextPluginConfig,
    security_level: PluginSecurityLevel = PluginSecurityLevel.HIGH,
) -> FlextResult[FlextPlugin]:
    """Register plugin with complete type safety."""

# MANDATORY: Use FlextResult for ALL plugin operations
result = await platform.register_plugin(plugin_config)
if result.success:
    plugin: FlextPlugin = result.value
    logger.info(f"Plugin {plugin.name} registered successfully")
else:
    logger.error(f"Plugin registration failed: {result.error}")
```

### **Plugin Security Framework (COMPREHENSIVE PROTECTION)**

```python
# MANDATORY: Use plugin security framework
from flext_plugin import FlextPluginSecurity, PluginSecurityLevel

try:
    security_result = await security_manager.validate_plugin(plugin, PluginSecurityLevel.HIGH)
    if security_result.is_failure:
        # Handle plugin security violations via FlextResult
        logger.error(f"Plugin security validation failed: {security_result.error}")
except FlextPluginSecurityError as e:
    # Handle plugin security-specific errors
    await handle_plugin_security_error(e)
except FlextPluginExecutionError as e:
    # Handle plugin execution issues
    await handle_plugin_execution_error(e)
```

## 🚀 ENTERPRISE PLUGIN DEVELOPMENT PATTERNS (CLEAN ARCHITECTURE ENFORCEMENT)

### **Domain-Driven Plugin Design (MANDATORY PATTERNS)**

#### Enterprise Plugin Service Layer

```python
# MANDATORY: Clean Architecture separation for plugin services
from flext_plugin import (
    FlextPluginPlatform,
    FlextPluginService,
    FlextPluginDiscoveryService,
    FlextPluginHotReloadManager,
)
from flext_core import FlextResult, get_logger

class EnterprisePluginOrchestrator:
    """Domain service orchestrating plugin operations."""

    def __init__(self, platform: FlextPluginPlatform):
        self.platform = platform
        self.plugin_service = FlextPluginService(platform)
        self.discovery_service = FlextPluginDiscoveryService()
        self.hot_reload_mgr = FlextPluginHotReloadManager(platform)
        self.logger = get_logger(__name__)

    async def orchestrate_plugin_lifecycle(
        self,
        plugin_path: str
    ) -> FlextResult[PluginLifecycleResult]:
        """Orchestrate complete plugin lifecycle in enterprise environment."""
        # Step 1: Discover plugin with security validation
        discovery_result = await self.discovery_service.discover_plugin(plugin_path)
        if discovery_result.is_failure:
            return FlextResult.fail(f"Plugin discovery failed: {discovery_result.error}")

        # Step 2: Validate plugin security
        plugin_config = discovery_result.value
        security_result = await self.platform.validate_plugin_security(plugin_config)
        if security_result.is_failure:
            return FlextResult.fail(f"Security validation failed: {security_result.error}")

        # Step 3: Register and activate plugin
        registration_result = await self.platform.register_plugin(plugin_config)
        return registration_result
```

#### Plugin Configuration Patterns (ENTERPRISE SECURITY)

```python
# MANDATORY: Enterprise plugin configuration with secrets management
from flext_plugin import FlextPluginConfig, PluginType, PluginSecurityLevel
from flext_core import FlextSecretManager

class PluginConfigurationService:
    """Enterprise plugin configuration management."""

    @classmethod
    async def create_production_plugin_config(cls, plugin_name: str) -> FlextPluginConfig:
        """Create production plugin configuration."""
        secret_manager = FlextSecretManager()

        return FlextPluginConfig(
            name=plugin_name,
            version="0.9.0",

            # Plugin classification
            plugin_type=PluginType.EXTENSION,

            # Enterprise security requirements
            security_level=PluginSecurityLevel.HIGH,
            security_requirements={
                "sandboxing": True,
                "network_access": False,
                "file_system_access": "read-only",
                "allowed_imports": ["flext_core", "flext_api", "flext_observability"]
            },

            # Enterprise monitoring
            monitoring={
                "enable_metrics": True,
                "enable_tracing": True,
                "enable_health_checks": True,
                "enable_audit_logging": True
            },

            # Production settings
            enable_hot_reload=True,
            enable_rollback=True,
            max_execution_time=300,  # 5 minutes for production operations

            # Dependencies
            dependencies=[
                "flext-core>=0.9.0",
                "flext-api>=0.9.0",
                "flext-observability>=0.9.0"
            ]
        )
```

### **Plugin Testing Patterns (ENTERPRISE VALIDATION)**

#### Integration Testing with Real Plugin Operations

```python
# MANDATORY: Real plugin integration testing
import pytest
from flext_plugin import FlextPluginPlatform, FlextPluginConfig
from flext_core import FlextResult

@pytest.mark.integration
@pytest.mark.plugin
@pytest.mark.enterprise
async def test_plugin_system_integration():
    """Test real plugin system operations."""
    # Use test plugin platform instance
    platform = await PluginTestEnvironment.create_test_platform()

    # Test plugin registration
    plugin_config = await PluginConfigurationService.create_test_plugin_config()
    registration_result = await platform.register_plugin(plugin_config)
    assert registration_result.success
    assert registration_result.value.status == PluginStatus.ACTIVE

    # Test plugin execution
    execution_result = await platform.execute_plugin(registration_result.value)
    assert execution_result.success
```

#### Hot-Reload Testing with Real File Operations

```python
# MANDATORY: Real hot-reload testing without mocks
@pytest.mark.hot_reload
@pytest.mark.real_fs
async def test_plugin_hot_reload_complete_workflow():
    """Test complete hot-reload workflow with real file operations."""
    async with PluginHotReloadTestEnvironment() as test_env:
        platform = test_env.platform
        hot_reload_manager = test_env.hot_reload_manager

        # Create initial plugin file
        plugin_path = await test_env.create_test_plugin("test_plugin.py")

        # Start hot-reload monitoring
        await hot_reload_manager.start_monitoring([plugin_path.parent])

        # Modify plugin file and verify hot-reload
        await test_env.modify_plugin_file(plugin_path)

        # Verify plugin was reloaded automatically
        reload_result = await hot_reload_manager.wait_for_reload(timeout=5)
        assert reload_result.success
        assert reload_result.value.plugin_name == "test_plugin"
```

## 🎯 PLUGIN SYSTEM CRITICAL SUCCESS METRICS (ENTERPRISE KPIS)

### **Production Readiness Requirements (ZERO TOLERANCE)**

- **Type Safety**: 100% MyPy compliance across all plugin system modules
- **Test Coverage**: 85% minimum with real plugin operations testing
- **Security Compliance**: Zero security vulnerabilities in plugin execution
- **Plugin Isolation**: 100% sandboxing for untrusted plugin execution
- **Hot Reload Performance**: Plugin reloads complete within 2 seconds
- **Error Handling**: 100% of plugin operations handled via FlextResult patterns

### **Plugin System Health Metrics**

```bash
# MANDATORY: Health monitoring commands
make plugin-validate          # Plugin system integrity validation
make plugin-discovery         # Plugin discovery mechanisms health
make test-plugin             # Plugin functionality health validation
make test-hot-reload         # Hot-reload system health validation
```

## ⚡ PERFORMANCE OPTIMIZATION (ENTERPRISE PLUGIN SYSTEM)

### **Plugin System Performance Optimization**

- **Plugin Loading**: Optimized plugin discovery and loading mechanisms
- **Hot Reload Efficiency**: Intelligent file watching with minimal resource usage
- **Plugin Sandboxing**: Efficient security isolation without performance penalties
- **Memory Management**: Proper plugin lifecycle and resource cleanup
- **Monitoring Integration**: Real-time plugin performance metrics via FlextObservability

## 📋 ENTERPRISE PLUGIN INTEGRATION CHECKLIST

### **Pre-Development Validation (MANDATORY)**

```bash
# REQUIRED: Execute BEFORE any plugin development
□ make validate                    # Zero errors across all quality gates
□ make plugin-validate            # Verify plugin system integrity
□ make plugin-discovery           # Validate plugin discovery mechanisms
□ make test-plugin                # Comprehensive plugin functionality validation
□ make security                   # Zero security vulnerabilities
```

### **Development Standards Compliance**

```bash
# REQUIRED: During plugin development
□ 100% type safety (MyPy strict mode)
□ 85% minimum test coverage with real plugin operations
□ All plugin operations via FlextResult patterns
□ Zero custom plugin loading implementations
□ Enterprise security validation for all plugins
□ Complete hot-reload integration testing
```

### **Production Deployment Readiness**

```bash
# REQUIRED: Before production
□ Enterprise plugin platform configuration validated
□ Plugin security framework fully implemented
□ Performance benchmarks met for plugin operations
□ Security audit completed for plugin sandbox
□ Monitoring and alerting configured for plugin health
□ Disaster recovery tested for plugin system
```

---

**FLEXT-PLUGIN AUTHORITY**: This document establishes flext-plugin as the definitive plugin management system and extensibility foundation for the entire FLEXT ecosystem.

**ZERO TOLERANCE ENFORCEMENT**: Any deviation from these patterns requires explicit approval from FLEXT architecture authority.

**ENTERPRISE GRADE**: Production-ready plugin management with comprehensive security, monitoring, and hot-reload capabilities.

**CLEAN ARCHITECTURE**: Strict separation of plugin business logic, application services, and infrastructure concerns.

**EXTENSIBILITY FOUNDATION**: Complete plugin ecosystem supporting Singer/Meltano integration, custom extensions, and enterprise plugin development.

---

## 🔗 RELATED FLEXT ECOSYSTEM PROJECTS

### **Core Dependencies (MANDATORY)**

- **flext-core**: Foundation patterns, FlextResult, logging, DI container
- **flext-api**: Enterprise API client patterns and authentication
- **flext-observability**: Plugin monitoring, tracing, and alerting
- **flext-config**: Centralized plugin configuration management

### **Singer/Meltano Integration Projects**

- **flext-tap-\***: Singer tap plugins (data extraction)
- **flext-target-\***: Singer target plugins (data loading)
- **flext-dbt-\***: dbt transformation plugins
- **flext-meltano**: Meltano project configuration integration

### **Enterprise Platform Integration**

- **flext-auth**: Enterprise authentication for plugin access
- **flext-quality**: Quality gates and plugin validation framework
- **flext-security**: Enterprise security framework for plugin sandboxing

---

**FINAL AUTHORITY**: flext-plugin is the single source of truth for all plugin management, discovery, loading, and execution operations within the FLEXT ecosystem. No custom plugin implementations are permitted.
