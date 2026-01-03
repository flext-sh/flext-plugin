#!/usr/bin/env python3
"""Basic Plugin Example - Minimal functional plugin demonstration.

This example shows how to create and use a basic plugin with the FLEXT Plugin system.
Demonstrates core functionality without external dependencies.

Usage:
    python examples/01_basic_plugin.py
"""

from __future__ import annotations

from flext_core import FlextContainer

from flext_plugin import FlextPluginApi, FlextPluginConstants


def main() -> None:  # EXAMPLE - Acceptable loose function for demonstration
    """Demonstrate basic plugin creation and usage."""
    # Initialize the plugin API
    container = FlextContainer()
    FlextPluginApi(container)

    # Discover plugins (this would normally scan directories)
    # For demo purposes, we'll create a mock plugin result
    print("Plugin API initialized successfully")  # EXAMPLE - Demo output

    # Demonstrate status constants
    print("Available plugin statuses:")  # EXAMPLE - Demo output
    print(
        f"  - Active: {FlextPluginConstants.Plugin.Lifecycle.STATUS_ACTIVE}"
    )  # EXAMPLE - Demo output
    print(
        f"  - Inactive: {FlextPluginConstants.Plugin.Lifecycle.STATUS_INACTIVE}"
    )  # EXAMPLE - Demo output
    print(
        f"  - Loading: {FlextPluginConstants.Plugin.Lifecycle.STATUS_LOADING}"
    )  # EXAMPLE - Demo output

    # Example of how to use the API (commented out since we don't have actual plugins)
    # discovery_result = api.discover_plugins(["./plugins"])
    # if discovery_result.is_success:
    #     plugins = discovery_result.value
    #     print(f"Discovered {len(plugins)} plugins")

    print("✅ Plugin system demonstration complete")  # EXAMPLE - Demo output


if __name__ == "__main__":
    main()
