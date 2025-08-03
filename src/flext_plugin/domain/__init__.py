"""FLEXT Plugin Domain Layer - Rich business entities and domain-driven design patterns.

This package implements the domain layer of the Clean Architecture, containing
rich business entities, domain services, and business logic for plugin management.
Following Domain-Driven Design principles, this layer encapsulates core business
rules and provides the foundation for plugin lifecycle management.

Key Components:
    - entities.py: Rich domain entities (FlextPlugin, FlextPluginConfig, etc.)
    - ports.py: Domain interfaces defining external dependencies

Domain-Driven Design:
    - Rich entities with business logic and validation
    - Domain events for plugin lifecycle changes
    - Business rules enforcement and consistency boundaries
    - Clean separation from infrastructure concerns

Architecture:
    The domain layer forms the heart of the Clean Architecture,
    containing business logic while remaining independent of
    external frameworks, databases, and infrastructure details.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""
