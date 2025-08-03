"""FLEXT Plugin Application Layer - CQRS application services and use case orchestration.

This package implements the application layer of the Clean Architecture, providing
application services and CQRS handlers that orchestrate domain operations and
coordinate with external systems. The application layer translates between
the presentation layer and domain layer while managing transactions and workflows.

Key Components:
    - services.py: Application services (FlextPluginService, FlextPluginDiscoveryService)
    - handlers.py: CQRS command and event handlers

CQRS Patterns:
    - Command handlers for state-changing operations
    - Event handlers for domain event processing
    - Query handlers for read-only data retrieval
    - Service coordination without business logic

Architecture:
    The application layer orchestrates domain entities and coordinates
    with infrastructure services while maintaining separation of concerns
    and providing transaction boundaries for complex operations.

Use Cases:
    - Plugin discovery and validation workflows
    - Plugin installation and configuration management
    - Plugin lifecycle management and state transitions
    - Cross-cutting concerns like logging and monitoring

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""
