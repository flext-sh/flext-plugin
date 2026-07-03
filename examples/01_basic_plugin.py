"""Basic Plugin Example - Minimal functional plugin demonstration.

This example shows how to create and use a basic plugin with the FLEXT Plugin system.
Demonstrates core functionality without external dependencies.

Usage:
    python examples/01_basic_plugin.py
"""

from __future__ import annotations

from flext_plugin import FlextPluginApi


def main() -> None:
    """Demonstrate basic plugin creation and usage."""
    api = FlextPluginApi.fetch_global()
    _ = api.list_plugins()


if __name__ == "__main__":
    main()
