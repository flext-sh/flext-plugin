#!/usr/bin/env python3
"""Basic Plugin Example - Minimal functional plugin demonstration.

This example shows how to create and use a basic plugin with the FLEXT Plugin system.
Demonstrates core functionality without external dependencies.

Usage:
    python examples/basic_plugin_example.py
"""

from __future__ import annotations

from flext_plugin import PluginStatus, create_flext_plugin


def main() -> None:
    """Demonstrate basic plugin creation and usage."""
    print("=== FLEXT Plugin Basic Example ===")

    # Create a basic plugin
    print("\n1. Creating a basic plugin...")
    plugin = create_flext_plugin(
      name="example-plugin",
      version="1.0.0",
      config={
          "description": "A basic example plugin",
          "author": "FLEXT Team",
          "tags": ["example", "demo"],
      },
    )

    print(f"   Plugin created: {plugin.name}")
    print(f"   Version: {plugin.plugin_version}")
    print(f"   Status: {plugin.status}")
    print(f"   Description: {plugin.description}")
    print(f"   Author: {plugin.author}")

    # Demonstrate plugin properties
    print("\n2. Plugin properties:")
    print(f"   ID: {plugin.id}")
    print(f"   Created at: {plugin.created_at}")
    print(f"   Is active: {plugin.is_active()}")

    # Demonstrate domain validation
    print("\n3. Domain validation:")
    validation_result = plugin.validate_business_rules()
    if validation_result.success:
      print("   ✅ Plugin validation passed")
    else:
      print(f"   ❌ Plugin validation failed: {validation_result.error}")

    # Demonstrate status transitions
    print("\n4. Status transitions:")
    if plugin.status == PluginStatus.INACTIVE:
      print(f"   Current status: {plugin.status}")
      activate_result = plugin.activate()
      if activate_result:
          print("   ✅ Plugin activation successful")
          print(f"   New status: {plugin.status}")
      else:
          print("   ❌ Plugin activation failed")

    print("\n=== Example completed successfully ===")


if __name__ == "__main__":
    main()
