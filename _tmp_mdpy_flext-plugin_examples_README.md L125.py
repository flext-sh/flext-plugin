# from flext-plugin/examples/README.md:125
from __future__ import annotations

import pytest
from flext_plugin import create_flext_plugin_platform


@pytest.fixture
def platform():
    """Test platform fixture."""
    platform = create_flext_plugin_platform(settings={"test_mode": True})
    yield platform
    platform.shutdown()


def test_plugin_activation(platform):
    """Test plugin activation."""
    plugin = create_flext_plugin(name="test-plugin", version="0.12.0-dev")
    platform.register_plugin(plugin)

    result = platform.activate_plugin("test-plugin")
    assert result.success
