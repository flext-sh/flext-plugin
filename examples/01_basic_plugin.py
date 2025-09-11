#!/usr/bin/env python3
"""Basic Plugin Example - Minimal functional plugin demonstration.

This example shows how to create and use a basic plugin with the FLEXT Plugin system.
Demonstrates core functionality without external dependencies.

Usage:
    python examples/01_basic_plugin.py
"""

from __future__ import annotations

from flext_plugin import PluginStatus, create_flext_plugin


def main() -> None:
    """Demonstrate basic plugin creation and usage."""
    print("FLEXT Plugin Basic Example")
    print("=" * 40)

    # Create a basic plugin
    plugin = create_flext_plugin(
        name="example-plugin",
        version="1.0.0",
        config={
            "description": "A basic example plugin",
            "author": "FLEXT Team",
            "tags": ["example", "demo"],
        },
    )

    # Demonstrate plugin properties
    print(f"Plugin created: {plugin.name}")
    print(f"Version: {plugin.plugin_version}")

    # Demonstrate domain validation
    validation_result = plugin.validate_business_rules()
    if validation_result.success:
        print("Plugin validation passed")

    # Demonstrate status transitions
    if plugin.status == PluginStatus.INACTIVE:
        activate_result = plugin.activate()
        if activate_result:
            print("Plugin activation successful")

    print("Example completed successfully")


if __name__ == "__main__":
    main()
