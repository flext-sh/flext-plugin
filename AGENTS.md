# AGENTS.md — flext-plugin

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the parent raw `AGENTS.md` URL to the same branch/release as this package (never `main`).

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->
**Package:** `flext_plugin` · deps: `flext-cli`, `flext-core`

## Overview

Plugin system for the FLEXT platform — discovery, loading, lifecycle, hot reload.

## Structure

```text
src/flext_plugin/
├── api.py            # FlextPluginApi facade
├── _utilities/
│   ├── discovery.py         # discover_plugins
│   ├── implementations.py
│   └── plugin_platform.py   # platform (delegated to via _build_default_platform / _platform)
├── constants.py typings.py protocols.py models.py utilities.py   # AUTO-GENERATED facets
└── _config.py
```

## Code Map

| Symbol | Kind | Location | Role |
|--------|------|----------|------|
| `FlextPluginApi` | class | `api.py` | facade: `discover_plugins`, `load_plugin`, `register_plugin`, `execute_plugin`, `start/stop_hot_reload` |

## Conventions (specific to this package)

- Plugin lifecycle is **explicit** — discover → load → register → execute → unregister; hot reload is managed through the facade.
- Registration/discovery is protocol-driven (`p.*`); depend on abstractions, not concrete plugin classes.
- Config/settings canonical pattern: ADR-012.
- Codemod governance (ast-grep + make mod): ADR-014.

## Commands

```bash
make check PROJECT=flext-plugin
make test  PROJECT=flext-plugin       # tests/unit
```
<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->
