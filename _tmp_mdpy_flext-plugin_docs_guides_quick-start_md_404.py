# from flext-plugin_docs/guides/quick-start.md:404
from __future__ import annotations

from flext_plugin import enable_hot_reload
from flext_plugin import create_flext_plugin_platform


def development_server():
    """Development server with hot reload."""
    # Enable hot reload
    enable_hot_reload(
        watch_paths=["./"],  # Watch current directory
        reload_on_change=True,
    )

    # Create platform
    platform = create_flext_plugin_platform(
        settings={"hot_reload": True, "debug": True}
    )

    print("🔥 Hot reload enabled!")
    print("Modify plugin files to see live updates...")
    print("Press Ctrl+C to stop")

    try:
        # Keep server running
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down development server...")
        platform.shutdown()


# Run development server
run(development_server())```
## Quality Gates

FLEXT Plugin includes comprehensive quality gates. Set them up for your project:

