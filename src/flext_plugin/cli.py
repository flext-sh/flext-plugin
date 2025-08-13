"""FLEXT Plugin CLI - Command-line interface for plugin management.

Enterprise-grade CLI implementation using Click framework with comprehensive
plugin management capabilities. Follows SOLID principles and integrates
with flext-core patterns for consistent error handling and logging.

Key Commands:
    - create: Create new plugin from template
    - install: Install plugin from registry or file
    - uninstall: Remove plugin from system
    - list: List installed plugins
    - validate: Validate plugin configuration
    - watch: Monitor plugin directory for changes
    - platform: Manage plugin platform

Architecture:
    Built using Click framework with command groups, consistent error handling
    through flext-core FlextResult pattern, and integration with the plugin
    platform for all operations.

Example:
    $ flext-plugin list --format json
    $ flext-plugin create --name my-plugin --type tap
    $ flext-plugin validate --all

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from flext_core import FlextLogger, FlextResult

from flext_plugin import create_flext_plugin_platform
from flext_plugin.core.types import PluginType

# Initialize logger
logger = FlextLogger(__name__)


class PluginCLI:
    """CLI handler with platform integration following SOLID principles."""

    def __init__(self) -> None:
        """Initialize CLI with plugin platform."""
        try:
            self.platform = create_flext_plugin_platform()
        except Exception as e:
            logger.exception("Failed to initialize plugin platform", error=str(e))
            sys.exit(1)


def handle_result(result: FlextResult[object], success_msg: str = "") -> None:
    """Handle FlextResult with consistent error messaging."""
    if result.is_failure:
        click.echo(f"Error: {result.error}", err=True)
        sys.exit(1)
    elif success_msg:
        click.echo(success_msg)


@click.group(name="flext-plugin")
@click.version_option()
@click.option(
    "--verbose/--no-verbose",
    "-v",
    default=False,
    help="Enable verbose output",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format",
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, output_format: str) -> None:  # noqa: FBT001
    """FLEXT Plugin Management CLI - Enterprise plugin management system."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["format"] = output_format
    ctx.obj["cli_handler"] = PluginCLI()

    if verbose:
        logger.info("FLEXT Plugin CLI initialized")


@cli.command()
@click.option("--name", "-n", required=True, help="Plugin name")
@click.option(
    "--type",
    "plugin_type",
    "-t",
    type=click.Choice([pt.value for pt in PluginType]),
    default="utility",
    help="Plugin type",
)
@click.option("--meta", "-m", help="Plugin metadata as 'description:author'")
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    default=".",
    help="Output directory",
)
@click.pass_context
def create(
    ctx: click.Context,
    name: str,
    plugin_type: str,
    meta: str | None = None,
    output_dir: str = ".",
) -> None:
    """Create a new plugin from template."""
    cli_handler = ctx.obj["cli_handler"]

    try:
        # Parse metadata if provided
        description, author = "Plugin " + name, "Unknown"
        if meta:
            parts = meta.split(":", 1)
            description = parts[0]
            if len(parts) > 1:
                author = parts[1]

        # Create plugin using the platform
        plugin_result = cli_handler.platform.create_plugin(
            name=name,
            plugin_type=PluginType(plugin_type),
            description=description,
            author=author,
            output_dir=output_dir,
        )
        handle_result(
            plugin_result,
            f"Plugin '{name}' created successfully in {output_dir}",
        )

    except Exception as e:
        logger.exception("Failed to create plugin", error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("plugin_name")
@click.option("--registry", "-r", help="Plugin registry URL")
@click.option("--file", "-f", type=click.Path(exists=True), help="Install from file")
@click.pass_context
def install(ctx: click.Context, plugin_name: str, registry: str, file: str) -> None:
    """Install plugin from registry or file."""
    cli_handler = ctx.obj["cli_handler"]

    try:
        if file:
            # Install from file
            result = cli_handler.platform.install_plugin_from_file(Path(file))
        else:
            # Install from registry
            result = cli_handler.platform.install_plugin(plugin_name, registry)

        handle_result(result, f"Plugin '{plugin_name}' installed successfully")

    except Exception as e:
        logger.exception("Failed to install plugin", error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("plugin_name")
@click.option(
    "--force",
    is_flag=True,
    help="Force uninstall without confirmation",
)
@click.pass_context
def uninstall(ctx: click.Context, plugin_name: str, *, force: bool) -> None:  # noqa: FBT001
    """Uninstall plugin from system."""
    cli_handler = ctx.obj["cli_handler"]

    if not force and not click.confirm(
        f"Are you sure you want to uninstall '{plugin_name}'?",
    ):
        click.echo("Uninstall cancelled.")
        return

    try:
        result = cli_handler.platform.uninstall_plugin(plugin_name)
        handle_result(result, f"Plugin '{plugin_name}' uninstalled successfully")

    except Exception as e:
        logger.exception("Failed to uninstall plugin", error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command("list")
@click.option(
    "--installed/--no-installed",
    default=False,
    help="Show only installed plugins",
)
@click.option(
    "--available/--no-available",
    default=False,
    help="Show only available plugins",
)
@click.option(
    "--type",
    "plugin_type",
    "-t",
    type=click.Choice([pt.value for pt in PluginType]),
    help="Filter by plugin type",
)
@click.pass_context
def list_plugins(
    ctx: click.Context,
    installed: bool,
    available: bool,
    plugin_type: str | None,
) -> None:
    """List installed and available plugins."""
    cli_handler = ctx.obj["cli_handler"]
    format_output = ctx.obj["format"]

    try:
        if installed or not available:
            result = cli_handler.platform.list_installed_plugins()
            if result.is_failure:
                handle_result(result)
                return

            plugins = result.data

            # Filter by type if specified
            if plugin_type:
                plugins = [
                    p
                    for p in plugins
                    if getattr(p, "type", None) is not None
                    and getattr(p, "type", None) == plugin_type
                ]

            if format_output == "json":
                plugin_data = [
                    {"name": p.name, "version": p.plugin_version, "status": p.status}
                    for p in plugins
                ]
                click.echo(json.dumps(plugin_data, indent=2))
            elif not plugins:
                click.echo("No plugins found.")
            else:
                click.echo(f"Found {len(plugins)} plugin(s):")
                for plugin in plugins:
                    status = getattr(plugin, "status", "unknown")
                    click.echo(f"  {plugin.name} v{plugin.plugin_version} ({status})")

    except Exception as e:
        logger.exception("Failed to list plugins", error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--plugin", "-p", help="Validate specific plugin")
@click.option(
    "--all/--no-all",
    "validate_all",
    default=False,
    help="Validate all plugins",
)
@click.pass_context
def validate(ctx: click.Context, plugin: str, *, validate_all: bool) -> None:  # noqa: FBT001
    """Validate plugin configuration and dependencies."""
    cli_handler = ctx.obj["cli_handler"]

    try:
        if plugin:
            result = cli_handler.platform.validate_plugin(plugin)
            handle_result(result, f"Plugin '{plugin}' is valid")
        elif validate_all:
            result = cli_handler.platform.validate_all_plugins()
            handle_result(result, "All plugins are valid")
        else:
            click.echo("Please specify --plugin <name> or --all")
            sys.exit(1)

    except Exception as e:
        logger.exception("Failed to validate plugin", error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--directory",
    "-d",
    type=click.Path(exists=True),
    default="./plugins",
    help="Directory to watch",
)
@click.option("--interval", "-i", type=int, default=2, help="Watch interval in seconds")
@click.pass_context
def watch(ctx: click.Context, directory: str, interval: int) -> None:
    """Monitor plugin directory for changes (hot reload)."""
    cli_handler = ctx.obj["cli_handler"]

    try:
        click.echo(
            f"Starting hot reload monitoring on {directory} (interval: {interval}s)",
        )
        click.echo("Press Ctrl+C to stop...")

        result = cli_handler.platform.start_hot_reload(Path(directory), interval)
        handle_result(result, "Hot reload monitoring started")

    except KeyboardInterrupt:
        click.echo("\nHot reload monitoring stopped.")
    except Exception as e:
        logger.exception("Failed to start watching", error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--status", is_flag=True, help="Show platform status")
@click.option("--health", is_flag=True, help="Show platform health")
@click.option("--reset", is_flag=True, help="Reset platform configuration")
@click.pass_context
def platform(ctx: click.Context, *, status: bool, health: bool, reset: bool) -> None:  # noqa: FBT001
    """Manage plugin platform."""
    cli_handler = ctx.obj["cli_handler"]
    format_output = ctx.obj["format"]

    try:
        if status:
            result = cli_handler.platform.get_status()
            if result.is_success:
                if format_output == "json":
                    click.echo(json.dumps(result.data, indent=2))
                else:
                    status_data = result.data
                    click.echo(
                        f"Platform Status: {status_data.get('status', 'unknown')}",
                    )
                    click.echo(
                        f"Plugins Loaded: {status_data.get('plugins_loaded', 0)}",
                    )
                    click.echo(
                        f"Hot Reload: {status_data.get('hot_reload_active', False)}",
                    )
            else:
                handle_result(result)

        elif health:
            result = cli_handler.platform.health_check()
            handle_result(result, "Platform is healthy")

        elif reset:
            if click.confirm(
                "Are you sure you want to reset the platform configuration?",
            ):
                result = cli_handler.platform.reset()
                handle_result(result, "Platform reset successfully")
            else:
                click.echo("Reset cancelled.")
        else:
            click.echo("Please specify --status, --health, or --reset")

    except Exception as e:
        logger.exception("Failed platform operation", error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main() -> None:
    """Provide CLI entry point."""
    try:
        cli()
    except Exception as e:
        logger.exception("CLI error", error=str(e))
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
