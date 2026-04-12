"""FLEXT Plugin Domain Entities - Domain-Driven Design patterns for plugin system.

This module provides domain entities following Domain-Driven Design patterns with
Pydantic v2 validation. Entities represent core plugin domain concepts with identity
and lifecycle.

Architecture Layer: 1 (Domain)
=============================
Domain layer with pure business logic, no infrastructure dependencies.

Domain Concepts:
- Plugin: Core plugin entity with identity and lifecycle
- PluginRegistry: Aggregate root managing collection of plugins
- Domain Events: Significant domain occurrences

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations


class FlextPluginEntities:
    """Domain entities for plugin system following Domain-Driven Design patterns.

    Provides core domain entities with Pydantic validation and r error
    handling. All entities follow railway-oriented programming patterns and are
    designed for composition and extensibility.

    Nested Classes:
    ===============
    - Plugin: Core plugin entity with lifecycle (Entity pattern)
    - PluginConfig: Plugin configuration value t.RecursiveContainer (Value pattern)
    - PluginMetadata: Plugin metadata value t.RecursiveContainer (Value pattern)
    - PluginRegistry: Collection aggregate root (AggregateRoot pattern)
    - DomainEvents: Significant plugin domain events (Event pattern)

    Architecture: Layer 1 (Domain)
    =============================
    Pure business logic with no infrastructure dependencies. Uses Pydantic v2
    validation and FlextCore patterns for type safety and error handling.

    Features:
    =========
    - Identity-based equality for entities
    - Immutable value objects with frozen Pydantic models
    - Aggregate root for consistency boundaries
    - Domain events for event sourcing
    - r[T] for composable error handling
    - 100% type safety with Pyrefly strict mode

    """

    class DomainEvents:
        """Significant plugin domain events for event sourcing.

        Contains event classes representing important domain occurrences that can
        be persisted for audit trails and event replay.

        """


__all__: list[str] = ["FlextPluginEntities"]
