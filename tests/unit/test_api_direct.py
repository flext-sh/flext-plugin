"""Public plugin composition, registration, discovery, and loading contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_plugin import FlextPluginApi, FlextPluginDiscovery, FlextPluginPlatform
from tests import c, m, tm, u

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextPluginApi:
    """One explicitly composed graph per independent API instance."""

    @staticmethod
    def test_independent_apis_are_isolated() -> None:
        """Default composition never shares registered payloads implicitly."""
        first = FlextPluginApi()
        second = FlextPluginApi()
        payload = m.Plugin.Entity(name="isolated-plugin")
        tm.ok(first.register_plugin(payload))
        assert first.fetch_plugin(payload.name).value is payload
        tm.fail(second.fetch_plugin(payload.name))
        tm.that(second.list_plugins().value, eq=[])

    @staticmethod
    def test_explicit_registry_sharing_preserves_identity() -> None:
        """Only passing the same registry shares registration ownership."""
        first = FlextPluginApi()
        second = FlextPluginApi(registry=first.registry)
        payload = m.Plugin.Entity(name="shared-plugin", metadata={"origin": "caller"})
        tm.ok(first.register_plugin(payload))
        assert second.fetch_plugin(payload.name).value is payload
        assert second.list_plugins().value[0] is payload
        tm.ok(second.unregister_plugin(payload.name))
        tm.fail(first.fetch_plugin(payload.name))

    @staticmethod
    def test_duplicate_identity_conflict_and_reregistration() -> None:
        """Conflicts cannot replace an entry; real removal makes the key reusable."""
        api = FlextPluginApi()
        original = m.Plugin.Entity(name="identity-plugin")
        conflict = m.Plugin.Entity(name=original.name)
        tm.ok(api.register_plugin(original))
        tm.ok(api.register_plugin(original))
        tm.fail(api.register_plugin(conflict))
        assert api.fetch_plugin(original.name).value is original
        tm.that(len(api.list_plugins().value), eq=1)
        tm.ok(api.unregister_plugin(original.name))
        tm.fail(api.fetch_plugin(original.name))
        tm.that(api.list_plugins().value, eq=[])
        tm.ok(api.register_plugin(conflict))
        assert api.fetch_plugin(conflict.name).value is conflict

    @staticmethod
    def test_unknown_plugin_operations_fail() -> None:
        """Lookup, status, activation, and removal do not hide an absent entry."""
        api = FlextPluginApi()
        tm.fail(api.fetch_plugin("absent-plugin"))
        tm.fail(api.fetch_plugin_status("absent-plugin"))
        tm.fail(api.resolve_plugin_active("absent-plugin"))
        tm.fail(api.unregister_plugin("absent-plugin"))

    @staticmethod
    def test_registry_payload_must_satisfy_plugin_contract() -> None:
        """A scalar stored through the kernel is not silently rebuilt as a plugin."""
        api = FlextPluginApi()
        tm.ok(
            api.registry.register_plugin(
                c.Plugin.REGISTRY_CATEGORY, "invalid-payload", "not a plugin"
            )
        )
        tm.fail(api.fetch_plugin("invalid-payload"))
        tm.fail(api.list_plugins())
        tm.ok(api.unregister_plugin("invalid-payload"))
        tm.that(api.list_plugins().value, eq=[])

    @staticmethod
    def test_service_registry_port_is_required_and_validated() -> None:
        """An uncomposed service cannot construct its missing collaborator."""
        tm.fail(u.validate_value(FlextPluginPlatform.PluginPlatformService, {}))
        tm.fail(
            u.validate_value(
                FlextPluginPlatform.PluginPlatformService, {"registry": "invalid"}
            )
        )
        api = FlextPluginApi()
        original = api.registry
        with pytest.raises(c.ValidationError):
            api.registry = "invalid"
        assert api.registry is original

    @staticmethod
    def test_ports_are_not_transport_payloads() -> None:
        """Collaborators remain excluded from serialization and schema."""
        api = FlextPluginApi(
            discovery=FlextPluginDiscovery(),
            loader=u.Plugin.Tests.FilePluginLoader(),
            executor=u.Plugin.Tests.EchoExecutor(),
        )
        dumped = api.model_dump()
        schema = u.json_mapping_adapter().validate_python(api.model_json_schema())
        properties = u.json_mapping_adapter().validate_python(schema["properties"])
        for name in ("registry", "discovery", "loader", "executor"):
            assert name not in dumped
            assert name not in properties

    @staticmethod
    def test_real_discovery_registers_owned_payload(tmp_path: Path) -> None:
        """Discovery metadata is retained and canonical lookup returns its identity."""
        plugin_file = tmp_path / "found.py"
        plugin_file.write_text('"""Real discoverable plugin."""\n', encoding="utf-8")
        api = FlextPluginApi(discovery=FlextPluginDiscovery())
        discovered = tm.ok(api.discover_plugins([str(tmp_path)]))
        payload = next(
            plugin for plugin in discovered if plugin.name == plugin_file.stem
        )
        tm.that(payload.name, eq=plugin_file.stem)
        tm.that(payload.plugin_version, eq=c.Plugin.DEFAULT_PLUGIN_VERSION)
        assert api.fetch_plugin(payload.name).value is payload
        tm.ok(api.unregister_plugin(payload.name))
        tm.fail(api.fetch_plugin(payload.name))

    @staticmethod
    def test_discovery_failure_does_not_create_entries(tmp_path: Path) -> None:
        """An adapter failure is propagated rather than converted to an empty success."""
        api = FlextPluginApi(discovery=u.Plugin.Tests.FailingDiscovery())
        tm.fail(api.discover_plugins([str(tmp_path / "missing")]))
        tm.that(api.list_plugins().value, eq=[])

    @staticmethod
    def test_real_loader_preserves_domain_metadata(tmp_path: Path) -> None:
        """Loaded metadata and the original registered payload remain available."""
        plugin_file = tmp_path / "loaded.py"
        plugin_file.write_text('"""Real loadable plugin."""\n', encoding="utf-8")
        loader = u.Plugin.Tests.FilePluginLoader()
        api = FlextPluginApi(loader=loader)
        payload = tm.ok(api.load_plugin(str(plugin_file)))
        tm.that(payload.name, eq=plugin_file.stem)
        tm.that(payload.plugin_version, eq=c.Plugin.DEFAULT_PLUGIN_VERSION)
        tm.that(payload.metadata["path"], eq=str(plugin_file))
        assert loader.plugin_loaded(payload.name)
        assert api.fetch_plugin(payload.name).value is payload

    @staticmethod
    def test_loader_failure_does_not_create_entries(tmp_path: Path) -> None:
        """A missing real file fails without leaving an entry in the registry."""
        api = FlextPluginApi(loader=u.Plugin.Tests.FilePluginLoader())
        tm.fail(api.load_plugin(str(tmp_path / "missing.py")))
        tm.that(api.list_plugins().value, eq=[])

    @staticmethod
    def test_loader_conflict_preserves_existing_payload(tmp_path: Path) -> None:
        """Loading another object under an owned name cannot replace its metadata."""
        plugin_file = tmp_path / "existing.py"
        plugin_file.write_text('"""Conflicting plugin file."""\n', encoding="utf-8")
        api = FlextPluginApi(loader=u.Plugin.Tests.FilePluginLoader())
        original = m.Plugin.Entity(name=plugin_file.stem, metadata={"origin": "caller"})
        tm.ok(api.register_plugin(original))
        tm.fail(api.load_plugin(str(plugin_file)))
        assert api.fetch_plugin(original.name).value is original
        tm.that(api.fetch_plugin(original.name).value.metadata, eq=original.metadata)
