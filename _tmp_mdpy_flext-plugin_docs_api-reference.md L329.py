# from flext-plugin/docs/api-reference.md:329
# Discover plugins in directory
from __future__ import annotations

discovery_result = platform.scan_directory("./plugins")
if discovery_result.success:
    for plugin in discovery_result.value:
        print(f"Found: {plugin.name} v{plugin.plugin_version}")

        # Validate each plugin
        validation = platform.validate_plugin(plugin)
        if validation.success:
            print("  ✓ Valid plugin")
        else:
            print(f"  ✗ Invalid: {validation.error}")```
______________________________________________________________________

For complete examples and usage patterns, see the examples/ directory.

## Related Documentation

**Within Project**:

- Getting Started - Installation and basic usage
- Architecture - Architecture and design patterns
- Examples - Working code examples
- Development - Contributing guidelines

**Across Projects**:

- [flext-core Foundation](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-core/docs/api-reference/foundation.md) - Core APIs and patterns
- [flext-core Railway-Oriented Programming](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-core/docs/guides/railway-oriented-programming.md) - r patterns
- [flext-meltano Pipelines](https://github.com/flext-sh/flext/tree/0.12.0-dev/flext-meltano/AGENTS.md) - Data integration and ELT orchestration

**External Resources**:

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
