# Container Architecture (C4 Level 2)

<!-- TOC START -->
- [🏗️ Container Architecture Overview](#container-architecture-overview)
  - [Architecture Principles](#architecture-principles)
- [📦 Container Diagram](#container-diagram)
- [🐳 Container Descriptions](#container-descriptions)
  - [Core Containers](#core-containers)
  - [Data Containers](#data-containers)
- [🔗 Container Communication Patterns](#container-communication-patterns)
  - [Internal Communication](#internal-communication)
  - [External Communication](#external-communication)
- [🚀 Deployment and Technology Choices](#deployment-and-technology-choices)
  - [Technology Stack](#technology-stack)
  - [Deployment Patterns](#deployment-patterns)
  - [Environment Configurations](#environment-configurations)
- [📊 Container Quality Attributes](#container-quality-attributes)
  - [Performance Characteristics](#performance-characteristics)
  - [Reliability Characteristics](#reliability-characteristics)
  - [Security Characteristics](#security-characteristics)
- [🔧 Container Management and Operations](#container-management-and-operations)
  - [Lifecycle Management](#lifecycle-management)
  - [Monitoring and Observability](#monitoring-and-observability)
  - [Scaling and Performance](#scaling-and-performance)
- [🧪 Testing Strategy by Container](#testing-strategy-by-container)
  - [Unit Testing](#unit-testing)
  - [Integration Testing](#integration-testing)
  - [Performance Testing](#performance-testing)
- [📋 Container Interface Contracts](#container-interface-contracts)
  - [FLEXT Plugin Core API](#flext-plugin-core-api)
  - [FLEXT Plugin CLI Interface](#flext-plugin-cli-interface)
  - [FLEXT Plugin API Interface (Planned)](#flext-plugin-api-interface-planned)
<!-- TOC END -->

**C4 Model Level 2**: Containers | **Version**: 0.9.0 | **Last Updated**: October 2025

______________________________________________________________________

## 🏗️ Container Architecture Overview

FLEXT Plugin operates as a **Python library package** with **optional CLI components**, designed for deployment across multiple container environments. The system provides plugin management capabilities to FLEXT ecosystem applications while maintaining clean separation between core functionality and optional interfaces.

### Architecture Principles

- **Library-First Design**: Core functionality as importable Python package
- **Optional CLI**: Command-line interface as separate optional component
- **Container Agnostic**: Deployable in any Python environment (Docker, Podman, Kubernetes, bare metal)
- **Dependency Injection**: Clean separation through FLEXT container patterns

______________________________________________________________________

## 📦 Container Diagram

```plantuml
@startuml Container Diagram
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

title Container Diagram - FLEXT Plugin System

Person(developer, "Plugin Developer", "Creates and tests plugins")
Person(operator, "System Operator", "Deploys FLEXT applications")

System_Boundary(flext_plugin_system, "FLEXT Plugin System") {

    Container(flext_plugin_core, "FLEXT Plugin Core", "Python Library", "Plugin lifecycle management, discovery, execution, security validation")
    Container(flext_plugin_cli, "FLEXT Plugin CLI", "Python CLI Application", "Command-line interface for plugin management (optional)")
    Container(flext_plugin_api, "FLEXT Plugin API", "Python REST API", "REST API for plugin operations (planned)")

    ContainerDb(plugin_registry, "Plugin Registry", "File System / Database", "Plugin metadata, configurations, and state")
    ContainerDb(plugin_cache, "Plugin Cache", "File System", "Compiled plugins and execution artifacts")
}

System_Ext(flext_core, "FLEXT Core", "Python Library", "Foundation patterns: r, FlextContainer, FlextModels")
System_Ext(flext_observability, "FLEXT Observability", "Python Library", "Metrics, tracing, health checks")

System_Ext(pypi, "PyPI", "Package Repository", "Plugin package distribution")
System_Ext(github, "GitHub", "Git Repository", "Source code and CI/CD")

System_Ext(flexcore, "FlexCore", "Go Container", "Runtime container with plugin proxy")
System_Ext(flext_service, "FLEXT Service", "Go/Python Service", "Data platform with Python bridge")

System_Ext(docker_registry, "Docker Registry", "Container Images", "FLEXT application containers")
System_Ext(kubernetes, "Kubernetes", "Container Orchestrator", "Deployment and scaling platform")

Rel(developer, flext_plugin_cli, "Develops plugins using", "Python CLI")
Rel(developer, flext_plugin_core, "Imports and uses", "Python API")
Rel(operator, flext_plugin_cli, "Manages plugins via", "CLI commands")
Rel(operator, flext_plugin_api, "Manages plugins via", "REST API (planned)")

Rel(flext_plugin_core, flext_core, "Depends on", "r[T], FlextContainer")
Rel(flext_plugin_core, flext_observability, "Integrates with", "metrics, tracing")

Rel(flext_plugin_cli, flext_plugin_core, "Uses", "Core plugin APIs")
Rel(flext_plugin_api, flext_plugin_core, "Uses", "Core plugin APIs")

Rel(flext_plugin_core, plugin_registry, "Reads/Writes", "Plugin metadata")
Rel(flext_plugin_core, plugin_cache, "Reads/Writes", "Plugin artifacts")

Rel(flext_plugin_cli, plugin_registry, "Manages", "Plugin configurations")
Rel(flext_plugin_cli, plugin_cache, "Manages", "Cache operations")

Rel(flext_plugin_core, pypi, "Discovers plugins from", "Package metadata")
Rel(flext_plugin_core, github, "Downloads plugins from", "Git repositories")

Rel(flext_plugin_core, flexcore, "Communicates with", "Plugin proxy protocol")
Rel(flext_plugin_core, flext_service, "Integrates with", "Service mesh")

Rel(flexcore, docker_registry, "Pulls images from", "Container deployment")
Rel(flext_service, kubernetes, "Deploys to", "Orchestration platform")

@enduml
```

______________________________________________________________________

## 🐳 Container Descriptions

### Core Containers

#### **FLEXT Plugin Core** (Primary Container)

- **Technology**: Python 3.13+ Library Package
- **Purpose**: Core plugin management functionality
- **Responsibilities**:
  - Plugin discovery, loading, and execution
  - Security validation and sandboxing
  - Lifecycle management and hot reload
  - FLEXT ecosystem integration
- **Key Components**:
  - `FlextPluginPlatform`: Main platform facade
  - `FlextPluginApi`: Unified API interface
  - Plugin discovery and loader services
  - Security and validation services
- **Deployment**: Deployed as Python package in consuming applications

#### **FLEXT Plugin CLI** (Optional Container)

- **Technology**: Python CLI Application (Click framework)
- **Purpose**: Command-line interface for plugin management
- **Responsibilities**:
  - Plugin installation and management
  - Development workflow commands
  - Debugging and troubleshooting tools
  - Batch operations and automation
- **Key Components**:
  - CLI command definitions
  - Interactive prompts and wizards
  - File operations and utilities
- **Deployment**: Optional component, installed separately
- **Status**: Implementation complete but disabled (dependency issues)

#### **FLEXT Plugin API** (Planned Container)

- **Technology**: Python REST API (FastAPI/Flask)
- **Purpose**: REST API for plugin operations
- **Responsibilities**:
  - HTTP endpoints for plugin management
  - Web-based plugin REDACTED_LDAP_BIND_PASSWORDistration
  - API-driven plugin operations
  - Integration with web interfaces
- **Key Components**:
  - REST API endpoints
  - OpenAPI/Swagger documentation
  - Authentication and authorization
- **Deployment**: Optional microservice
- **Status**: Planned for future release

### Data Containers

#### **Plugin Registry** (Data Store)

- **Technology**: File System / SQLite / PostgreSQL
- **Purpose**: Persistent storage for plugin metadata and state
- **Responsibilities**:
  - Plugin configuration storage
  - Execution history and metrics
  - Plugin dependency tracking
  - State persistence across restarts
- **Key Data**:
  - Plugin metadata (name, version, author, description)
  - Configuration settings and parameters
  - Execution statistics and performance metrics
  - Security validation results and certificates

#### **Plugin Cache** (Cache Store)

- **Technology**: File System Cache
- **Purpose**: Performance optimization for plugin operations
- **Responsibilities**:
  - Compiled plugin bytecode storage
  - Plugin artifact caching
  - Temporary execution state
  - Performance optimization data
- **Key Data**:
  - Compiled Python bytecode (.pyc files)
  - Plugin execution artifacts
  - Temporary configuration files
  - Performance optimization metadata

______________________________________________________________________

## 🔗 Container Communication Patterns

### Internal Communication

#### **Core ↔ CLI Communication**

```python
# CLI imports and uses Core APIs
from flext_plugin import FlextPluginApi

api = FlextPluginApi()
result = api.discover_plugins(["./plugins"])
```

#### **Core ↔ API Communication** (Planned)

```python
# REST API delegates to Core
from flext_plugin import FlextPluginPlatform

platform = FlextPluginPlatform()
# HTTP request → Core API call → Response
```

### External Communication

#### **FLEXT Ecosystem Integration**

| Container | External System     | Protocol        | Purpose                           |
| --------- | ------------------- | --------------- | --------------------------------- |
| Core      | flext-core          | Direct Import   | Foundation patterns and utilities |
| Core      | flext-observability | Direct Import   | Monitoring and metrics collection |
| CLI       | flext-cli           | Optional Import | CLI framework integration         |
| Core      | FlexCore            | HTTP/gRPC       | Plugin proxy and Go bridge        |
| Core      | FLEXT Service       | HTTP/REST       | Service mesh integration          |

#### **Plugin Distribution**

| Container | External System | Protocol  | Purpose                                   |
| --------- | --------------- | --------- | ----------------------------------------- |
| Core      | PyPI            | HTTPS/API | Plugin package discovery and installation |
| Core      | GitHub          | HTTPS/Git | Source code repositories and releases     |
| CLI       | PyPI            | CLI/API   | Plugin package management commands        |

#### **Deployment Integration**

| Container | External System | Protocol    | Purpose                          |
| --------- | --------------- | ----------- | -------------------------------- |
| All       | Docker Registry | Docker API  | Container image distribution     |
| All       | Kubernetes      | kubectl/API | Orchestration and deployment     |
| Core      | File System     | POSIX       | Local plugin storage and caching |

______________________________________________________________________

## 🚀 Deployment and Technology Choices

### Technology Stack

#### **Core Runtime**

- **Python Version**: 3.13+ (exclusive, modern typing features)
- **Framework**: Custom library with FLEXT ecosystem patterns
- **Architecture**: Clean Architecture + Domain-Driven Design
- **Concurrency**: AsyncIO for non-blocking operations

#### **Optional Components**

- **CLI Framework**: Click 8.2+ (industry standard Python CLI)
- **Web Framework**: FastAPI/Flask (planned for REST API)
- **Rich Terminal**: Rich library for CLI formatting
- **Tabulate**: Table formatting for CLI output

#### **Data Storage**

- **Primary**: File system for portability and simplicity
- **Cache**: In-memory + file system for performance
- **Optional**: SQLite/PostgreSQL for enterprise deployments

### Deployment Patterns

#### **Library Deployment** (Primary)

```dockerfile
# FLEXT Plugin as library dependency
FROM python:3.13-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
# flext-plugin installed as dependency
RUN pip install flext-plugin
```

#### **CLI Deployment** (Optional)

```dockerfile
# FLEXT Plugin CLI container
FROM python:3.13-slim
RUN pip install flext-plugin[cli]
ENTRYPOINT ["flext-plugin"]
```

#### **API Deployment** (Planned)

```dockerfile
# FLEXT Plugin API microservice
FROM python:3.13-slim
RUN pip install flext-plugin[api]
EXPOSE 8000
CMD ["uvicorn", "flext_plugin.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Configurations

#### **Development Environment**

- **Dependencies**: All dev dependencies installed
- **Debugging**: Full debug logging enabled
- **Hot Reload**: File watching for development
- **Testing**: All test frameworks available

#### **Production Environment**

- **Dependencies**: Minimal runtime dependencies only
- **Security**: Sandboxing and validation enabled
- **Monitoring**: Full observability integration
- **Performance**: Optimized for production workloads

#### **CI/CD Environment**

- **Testing**: Full test suite execution
- **Quality Gates**: Linting, type checking, security scanning
- **Packaging**: Build and publish packages
- **Documentation**: Generate and validate docs

______________________________________________________________________

## 📊 Container Quality Attributes

### Performance Characteristics

#### **FLEXT Plugin Core**

- **Startup Time**: < 500ms (library import time)
- **Plugin Discovery**: < 100ms for 100 plugins
- **Plugin Loading**: < 50ms per plugin
- **Memory Usage**: < 50MB baseline + plugin overhead
- **Concurrent Operations**: Support for 100+ concurrent plugins

#### **FLEXT Plugin CLI**

- **Command Latency**: < 200ms for typical operations
- **Batch Operations**: < 5 seconds for 100 plugins
- **Memory Usage**: < 100MB for CLI operations
- **Disk I/O**: Minimal, primarily for plugin management

#### **Plugin Registry**

- **Read Performance**: < 10ms for plugin metadata
- **Write Performance**: < 50ms for state updates
- **Storage Efficiency**: < 1KB per plugin metadata
- **Concurrent Access**: Thread-safe operations

### Reliability Characteristics

#### **Fault Tolerance**

- **Plugin Failures**: Isolated, don't crash host application
- **Network Issues**: Graceful degradation for external services
- **Disk Space**: Continue operation with reduced caching
- **Memory Pressure**: Automatic cleanup and resource management

#### **Data Durability**

- **Plugin Metadata**: Persistent across restarts
- **Execution State**: Recoverable after failures
- **Cache Consistency**: Automatic cache invalidation
- **Configuration**: Version-controlled and auditable

### Security Characteristics

#### **Container Security**

- **Process Isolation**: Plugins run in separate processes
- **Resource Limits**: CPU and memory restrictions per plugin
- **Network Access**: Configurable network permissions
- **File System**: Restricted file system access

#### **Data Protection**

- **Configuration Security**: Encrypted sensitive plugin data
- **Audit Logging**: Complete audit trail for plugin operations
- **Access Control**: Role-based plugin execution permissions
- **Integrity Checks**: Plugin code and data integrity validation

______________________________________________________________________

## 🔧 Container Management and Operations

### Lifecycle Management

#### **Startup Sequence**

1. **Core Initialization**: Load FLEXT dependencies and configuration
1. **Registry Setup**: Initialize plugin registry and cache
1. **Discovery Phase**: Scan for available plugins
1. **Validation Phase**: Validate plugin security and compatibility
1. **Ready State**: Accept plugin operations

#### **Shutdown Sequence**

1. **Operation Drain**: Complete in-flight plugin operations
1. **State Persistence**: Save plugin state and metrics
1. **Resource Cleanup**: Release resources and connections
1. **Graceful Exit**: Clean shutdown with proper logging

### Monitoring and Observability

#### **Health Checks**

- **Core Health**: Plugin system operational status
- **Registry Health**: Data store accessibility
- **Plugin Health**: Individual plugin operational status
- **Resource Health**: Memory, CPU, disk usage within limits

#### **Metrics Collection**

- **Plugin Metrics**: Load times, execution counts, error rates
- **System Metrics**: Memory usage, CPU utilization, I/O operations
- **Performance Metrics**: Response times, throughput, latency
- **Security Metrics**: Validation failures, security events

### Scaling and Performance

#### **Horizontal Scaling**

- **Stateless Design**: Core containers can be scaled horizontally
- **Shared Registry**: Centralized plugin registry for coordination
- **Load Balancing**: Distribute plugin operations across instances
- **Session Affinity**: Maintain plugin context within sessions

#### **Vertical Scaling**

- **Resource Allocation**: Configurable memory and CPU limits
- **Plugin Isolation**: Per-plugin resource quotas
- **Caching Strategy**: Optimize for available memory
- **Performance Tuning**: Configurable thread pools and timeouts

______________________________________________________________________

## 🧪 Testing Strategy by Container

### Unit Testing

- **Core**: 15+ unit test files covering all modules
- **CLI**: 3+ unit test files for CLI components
- **API**: Planned unit tests for REST endpoints
- **Coverage Target**: 90%+ for all containers

### Integration Testing

- **Container Interactions**: Core ↔ CLI ↔ API integration
- **External Systems**: FLEXT ecosystem integration testing
- **Data Persistence**: Registry and cache testing
- **End-to-End**: Complete plugin lifecycle testing

### Performance Testing

- **Load Testing**: Concurrent plugin operations
- **Stress Testing**: Resource limit testing
- **Scalability Testing**: Multi-container deployments
- **Benchmarking**: Performance regression detection

______________________________________________________________________

## 📋 Container Interface Contracts

### FLEXT Plugin Core API

```python
# Primary interface for all plugin operations
from flext_plugin import FlextPluginApi

api = FlextPluginApi()
plugins = await api.discover_plugins(["./plugins"])
result = await api.execute_plugin("plugin-name", context)
```

### FLEXT Plugin CLI Interface

```bash
# Command-line interface (when enabled)
flext-plugin discover ./plugins
flext-plugin execute plugin-name --context=context.json
flext-plugin list --format=json
```

### FLEXT Plugin API Interface (Planned)

```bash
# REST API endpoints (planned)
GET /api/v1/plugins
POST /api/v1/plugins/{name}/execute
GET /api/v1/plugins/{name}/status
```

______________________________________________________________________

**Container Architecture** - Technology stack, deployment patterns, and container interactions for FLEXT Plugin system.
