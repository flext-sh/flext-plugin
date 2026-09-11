"""Service base for flext-plugin tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s

from flext_plugin import m
from tests.settings import TestsFlextPluginSettings


class TestsFlextPluginServiceBase(tests_s):
    """Plugin test service base with source and test settings namespaces."""

    # NOTE (multi-agent): flext-tests owns fetch_settings; this project
    # declares only its more-specific bootstrap settings type.
    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextPluginSettings)


s = TestsFlextPluginServiceBase

__all__: list[str] = ["TestsFlextPluginServiceBase", "s"]
