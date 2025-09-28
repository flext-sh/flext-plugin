"""FLEXT Plugin CLI - Simplified command-line interface for plugin management.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from typing import override

from Flext_cli import FlextCliApi, FlextCliCommands

from flext_core import FlextContainer, FlextLogger, FlextResult

# Initialize logger
logger = FlextLogger(__name__)


class PluginCLI:
    """Simplified CLI handler."""

    @override
    def __init__(self: object) -> None:
        """Initialize CLI."""
        try:
            self.container = FlextContainer()
        except Exception as e:
            logger.exception("Failed to initialize container", error=str(e))
            sys.exit(1)


class FlextPluginCliService:
    """Simplified FLEXT Plugin CLI service."""

    @override
    def __init__(self) -> None:
        """Initialize plugin CLI service."""
        self._cli_api = FlextCliApi()
        self._config: dict[str, object] = {}
        self._plugin_handler = PluginCLI()

    def handle_result(
        self,
        result: FlextResult[object],
        success_msg: str = "",
    ) -> FlextResult[str]:
        """Handle FlextResult with basic logging."""
        if result.is_failure:
            error_msg = result.error or "Unknown error occurred"
            logger.error(f"Plugin operation failed: {error_msg}")
            return FlextResult[str].fail(error_msg)
        if success_msg:
            logger.info(success_msg)
            return FlextResult[str].ok(success_msg)
        return FlextResult[str].ok("Operation completed")

    def create_plugin_cli_interface(self: object) -> FlextResult[FlextCliCommands]:
        """Create simplified plugin CLI interface."""
        try:
            main_cli = FlextCliCommands()
            return FlextResult[FlextCliCommands].ok(main_cli)
        except Exception as e:
            return FlextResult[FlextCliCommands].fail(f"CLI initialization failed: {e}")

    def handle_create_plugin(
        self,
        name: str,
        plugin_type: str = "EXTENSION",
    ) -> FlextResult[str]:
        """Handle plugin creation command."""
        try:
            if not name or not name.strip():
                return FlextResult[str].fail("Plugin name is required")

            logger.info(f"Creating plugin '{name}' with type '{plugin_type}'")
            return FlextResult[str].ok(f"Plugin '{name}' would be created successfully")

        except Exception as e:
            return FlextResult[str].fail(f"Plugin creation failed: {e}")

    def handle_list_plugins(self: object) -> FlextResult[str]:
        """Handle list plugins command."""
        try:
            logger.info("Listing available plugins")
            return FlextResult[str].ok("Plugins would be listed successfully")
        except Exception as e:
            return FlextResult[str].fail(f"Plugin listing failed: {e}")

    def handle_platform_status(self: object) -> FlextResult[str]:
        """Handle platform status command."""
        try:
            logger.info("Getting platform status")
            return FlextResult[str].ok("Platform status would be retrieved")
        except Exception as e:
            return FlextResult[str].fail(f"Status retrieval failed: {e}")


def main() -> None:
    """Main CLI entry point."""
    try:
        cli_service = FlextPluginCliService()
        cli_result: FlextResult[object] = cli_service.create_plugin_cli_interface()
        if cli_result.is_success:
            cli = cli_result.unwrap()
            cli.execute()
        else:
            error_msg = cli_result.error or "Unknown CLI initialization error"
            logger.error(f"CLI initialization failed: {error_msg}")
            sys.exit(1)
    except Exception as e:
        logger.exception("Plugin CLI execution failed", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
