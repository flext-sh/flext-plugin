"""Runtime settings for flext-plugin tests."""

from __future__ import annotations

from flext_tests import FlextTestsSettings

from flext_plugin import FlextPluginSettings


class TestsFlextPluginSettings(FlextPluginSettings, FlextTestsSettings):
    """Plugin settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextPluginSettings"]
