"""FLEXT Plugin CLI - Command-line interface for plugin management.

Enterprise-grade CLI implementation using flext-cli framework with comprehensive
plugin management capabilities. Follows SOLID principles and integrates
with flext-core patterns for co

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import sys

from flext_cli import FlextCliApi, FlextCliConfig, FlextCliMain
from flext_core import FlextContainer, FlextLogger, FlextResult

from .flext_plugin_models import PluginType
from .flext_plugin_platform import FlextPluginPlatform

# Initialize logger
logger = FlextLogger(__name__)


class PluginCLI:
    """CLI handler with platform integration."""

    def __init__(self) -> None:
        """Initialize CLI with plugin platform."""
        try:
            container = FlextContainer()
            self.platform = FlextPluginPlatform(container)
        except Exception as e:
            logger.exception("Failed to initialize plugin platform", error=str(e))
            sys.exit(1)


class FlextPluginCliService:
    """FLEXT Plugin CLI service using flext-cli foundation exclusively."""

    def __init__(self) -> None:
        """Initialize plugin CLI service with flext-cli patterns."""
        self._cli_api = FlextCliApi()
        self._config = FlextCliConfig()
        self._plugin_handler = PluginCLI()

    def handle_result(
        self, result: FlextResult[object], success_msg: str = ""
    ) -> FlextResult[str]:
        """Handle FlextResult with flext-cli output patterns."""
        if result.is_failure:
            self._cli_api.display_error(f"Plugin operation failed: {result.error}")
            return FlextResult[str].fail(result.error)
        if success_msg:
            self._cli_api.display_success(success_msg)
            return FlextResult[str].ok(success_msg)
        return FlextResult[str].ok("Operation completed")

    def create_plugin_cli_interface(self) -> FlextResult[FlextCliMain]:
        """Create plugin CLI interface using flext-cli patterns."""
        main_cli = FlextCliMain(
            name="flext-plugin",
            description="FLEXT Plugin Management CLI - Enterprise plugin management system",
        )

        # Register plugin command groups
        create_result = main_cli.register_command_group(
            "create", self._create_plugin_commands
        )
        if create_result.is_failure:
            return FlextResult[FlextCliMain].fail(
                f"Create commands registration failed: {create_result.error}"
            )

        list_result = main_cli.register_command_group(
            "list", self._create_list_commands
        )
        if list_result.is_failure:
            return FlextResult[FlextCliMain].fail(
                f"List commands registration failed: {list_result.error}"
            )

        platform_result = main_cli.register_command_group(
            "platform", self._create_platform_commands
        )
        if platform_result.is_failure:
            return FlextResult[FlextCliMain].fail(
                f"Platform commands registration failed: {platform_result.error}"
            )

        return FlextResult[FlextCliMain].ok(main_cli)

    def _create_plugin_commands(self) -> FlextResult[dict]:
        """Create plugin creation commands using flext-cli patterns."""
        commands = {
            "plugin": self._cli_api.create_command(
                name="plugin",
                description="Create a new plugin from template",
                handler=self._handle_create_plugin,
                arguments=["name", "plugin_type", "meta", "output_dir"],
                output_format="json",
            )
        }
        return FlextResult[dict].ok(commands)

    def _handle_create_plugin(self, args: dict) -> FlextResult[str]:
        """Handle plugin creation command."""
        name = args.get("name")
        if not name:
            return FlextResult[str].fail("Plugin name is required")

        plugin_type = args.get("plugin_type", "utility")
        meta = args.get("meta")
        output_dir = args.get("output_dir", ".")

        # Parse metadata if provided
        description, author = "Plugin " + name, "Unknown"
        if meta:
            parts = meta.split(":", 1)
            description = parts[0]
            if len(parts) > 1:
                author = parts[1]

        # Create plugin using the platform
        plugin_result = self._plugin_handler.platform.create_plugin(
            name=name,
            plugin_type=PluginType(plugin_type),
            description=description,
            author=author,
            output_dir=output_dir,
        )

        return self.handle_result(
            plugin_result,
            f"Plugin '{name}' created successfully in {output_dir}",
        )

    def _create_list_commands(self) -> FlextResult[dict]:
        """Create plugin list commands using flext-cli patterns."""
        commands = {
            "plugins": self._cli_api.create_command(
                name="plugins",
                description="List available plugins",
                handler=self._handle_list_plugins,
                output_format="table",
            )
        }
        return FlextResult[dict].ok(commands)

    def _handle_list_plugins(self, args: dict) -> FlextResult[str]:
        """Handle list plugins command."""
        list_result = self._plugin_handler.platform.list_plugins()
        return self.handle_result(list_result, "Plugins listed successfully")

    def _create_platform_commands(self) -> FlextResult[dict]:
        """Create platform management commands using flext-cli patterns."""
        commands = {
            "status": self._cli_api.create_command(
                name="status",
                description="Show platform status",
                handler=self._handle_platform_status,
                output_format="json",
            )
        }
        return FlextResult[dict].ok(commands)

    def _handle_platform_status(self, args: dict) -> FlextResult[str]:
        """Handle platform status command."""
        status_result = self._plugin_handler.platform.get_platform_status()
        return self.handle_result(status_result, "Platform status retrieved")


# Main CLI entry point using flext-cli patterns
def main() -> None:
    """Main CLI entry point for flext-plugin."""
    cli_service = FlextPluginCliService()
    cli_result = cli_service.create_plugin_cli_interface()

    if cli_result.is_failure:
        sys.exit(1)

    cli = cli_result.unwrap()
    cli.run()


# Legacy functions for compatibility (without Click dependencies)
def install_plugin_legacy(plugin_name: str, registry: str = "", file: str = "") -> None:
    """Legacy plugin installation function."""
    # Implementation would use FlextPluginCliService
    FlextPluginCliService()


__all__ = ["FlextPluginCliService", "PluginCLI", "install_plugin_legacy", "main"]


if __name__ == "__main__":
    main()
