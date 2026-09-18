# from flext-plugin_examples/README.md:112
from __future__ import annotations

from flext_plugin import enable_hot_reload

# Enable hot reload for development
enable_hot_reload(watch_paths=["./plugins", "./custom-plugins"], reload_on_change=True)

print("Hot reload enabled - modify plugin files to see changes")
