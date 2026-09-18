# from flext-plugin_docs/architecture/containers.md:223
# REST API delegates to Core
from __future__ import annotations

from flext_plugin import FlextPluginPlatform

platform = FlextPluginPlatform()
# HTTP request → Core API call → Response```
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

