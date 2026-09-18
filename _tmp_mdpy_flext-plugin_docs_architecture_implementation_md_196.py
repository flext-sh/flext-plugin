# from flext-plugin_docs/architecture/implementation.md:196
# flext_plugin/discovery.py - Infrastructure adapters
from __future__ import annotations

from pathlib import Path


class FlextPluginDiscovery:
    """Infrastructure adapter for file-based plugin discovery."""

    def __init__(self, container: FlextContainer) -> None:
        self.container = container
        self.logger = container.resolve("logger").unwrap()

    async def discover_plugins(
        self, paths: t.StringList
    ) -> p.Result[list[dict[str, t.JsonValue]]]:
        """Discover plugins from file system."""
        try:
            discovered_plugins = []

            for path_str in paths:
                path = Path(path_str)

                if not path.exists():
                    self.logger.warning(f"Plugin path does not exist: {path}")
                    continue

                # Scan for plugin files
                plugin_files = self._scan_plugin_files(path)
                self.logger.info(f"Found {len(plugin_files)} plugin files in {path}")

                for plugin_file in plugin_files:
                    try:
                        plugin_config = self._parse_plugin_file(plugin_file)
                        if plugin_config:
                            discovered_plugins.append(plugin_config)
                    except Exception as e:
                        self.logger.error(
                            f"Failed to parse plugin file {plugin_file}: {e}"
                        )
                        continue

            self.logger.info(f"Discovered {len(discovered_plugins)} plugins")
            return r.ok(discovered_plugins)

        except Exception as e:
            self.logger.exception("Plugin discovery failed")
            return r.fail(f"Discovery error: {e!s}")

    def _scan_plugin_files(self, path: Path) -> list[Path]:
        """Scan directory for plugin files."""
        plugin_files = []

        if path.is_file():
            if self._is_plugin_file(path):
                plugin_files.append(path)
        else:
            # Recursive scan
            for file_path in path.rglob("*"):
                if file_path.is_file() and self._is_plugin_file(file_path):
                    plugin_files.append(file_path)

        return plugin_files

    def _is_plugin_file(self, file_path: Path) -> bool:
        """Check if file is a valid plugin file."""
        if file_path.suffix.lower() not in [".py", ".json", ".yaml", ".yml"]:
            return False

        # Additional validation logic...
        return True

    def _parse_plugin_file(self, file_path: Path) -> dict[str, t.JsonValue] | None:
        """Parse plugin configuration from file."""
        try:
            if file_path.suffix.lower() == ".py":
                return self._parse_python_plugin(file_path)
            if file_path.suffix.lower() in [".json"]:
                return self._parse_json_plugin(file_path)
            if file_path.suffix.lower() in [".yaml", ".yml"]:
                return self._parse_yaml_plugin(file_path)
        except Exception as e:
            self.logger.error(f"Failed to parse {file_path}: {e}")

        return None```
### Protocol-Based Architecture Implementation

#### **Protocol Definitions**

