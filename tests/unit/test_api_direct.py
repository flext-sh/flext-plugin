"""Public plugin composition, registration, discovery, and loading contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_plugin import (
    FlextPluginApi,
    FlextPluginDiscovery,
    FlextPluginPlatform,
    FlextPluginSettings,
    plugin,
)
from tests import c, m, p, tm, u

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextPluginApi:
    """One explicitly composed graph per independent API instance."""

    @staticmethod
    def test_runtime_bootstrap_and_settings_reuse_core_contracts() -> None:
        """The service base selects its settings owner without copying its API."""
        supplied = FlextPluginSettings()
        api = FlextPluginApi(runtime_settings=supplied)
        options: p.RuntimeBootstrapOptions = api.runtime_bootstrap_options()
        runtime_settings: p.Settings = api.settings
        tm.that(isinstance(options, p.RuntimeBootstrapOptions), truth=True)
        tm.that(options.settings_type is FlextPluginSettings, truth=True)
        tm.that(isinstance(runtime_settings, p.Settings), truth=True)
        tm.that(runtime_settings.model_dump(), eq=supplied.model_dump())

    @staticmethod
    def test_public_instance_exposes_the_structural_lifecycle_contract() -> None:
        """The composed public instance needs no concrete facade annotation."""
        public_api: p.Plugin.PlatformService = plugin
        tm.that(isinstance(public_api, p.Plugin.PlatformService), truth=True)
        tm.ok(public_api.execute())

    @staticmethod
    def test_independent_apis_are_isolated() -> None:
        """Default composition never shares registered payloads implicitly."""
        first = FlextPluginApi()
        second = FlextPluginApi()
        payload = m.Plugin.Entity(name="isolated-plugin")
        tm.ok(first.register_plugin(payload))
        tm.that(first.fetch_plugin(payload.name).value is payload, truth=True)
        tm.fail(second.fetch_plugin(payload.name))
        tm.that(second.list_plugins().value, eq=[])

    @staticmethod
    def test_explicit_registry_sharing_preserves_identity() -> None:
        """Only passing the same registry shares registration ownership."""
        first = FlextPluginApi()
        second = FlextPluginApi(registry=first.registry)
        payload = m.Plugin.Entity(name="shared-plugin", metadata={"origin": "caller"})
        tm.ok(first.register_plugin(payload))
        tm.that(second.fetch_plugin(payload.name).value is payload, truth=True)
        tm.that(second.list_plugins().value[0] is payload, truth=True)
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
        tm.that(api.fetch_plugin(original.name).value is original, truth=True)
        tm.that(len(api.list_plugins().value), eq=1)
        tm.ok(api.unregister_plugin(original.name))
        tm.fail(api.fetch_plugin(original.name))
        tm.that(api.list_plugins().value, eq=[])
        tm.ok(api.register_plugin(conflict))
        tm.that(api.fetch_plugin(conflict.name).value is conflict, truth=True)

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

    @staticmethod
    @pytest.mark.parametrize(
        "field_name", ["registry", "discovery", "loader", "executor"]
    )
    def test_service_port_assignment_is_validated(field_name: str) -> None:
        """Every public collaborator assignment validates before replacing its port."""
        api = FlextPluginApi()
        original = getattr(api, field_name)
        with pytest.raises(c.ValidationError):
            setattr(api, field_name, "invalid")
        tm.that(getattr(api, field_name) is original, truth=True)

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
            tm.that(name not in dumped, truth=True)
            tm.that(name not in properties, truth=True)

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
        tm.that(api.fetch_plugin(payload.name).value is payload, truth=True)
        tm.ok(api.unregister_plugin(payload.name))
        tm.fail(api.fetch_plugin(payload.name))

    @staticmethod
    def test_discovery_failure_does_not_create_entries(tmp_path: Path) -> None:
        """Propagate adapter failure rather than returning an empty success."""
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
        tm.that(loader.plugin_loaded(payload.name), truth=True)
        tm.that(api.fetch_plugin(payload.name).value is payload, truth=True)

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
        tm.that(api.fetch_plugin(original.name).value is original, truth=True)
        tm.that(api.fetch_plugin(original.name).value.metadata, eq=original.metadata)
