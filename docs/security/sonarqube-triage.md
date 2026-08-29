# Triagem SonarCloud — flext-sh/flext-plugin

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead: `mro-2wjm.15`

## Resumo

**12 issues** — BLOCKER 0, CRITICAL 1, MAJOR 5, MINOR 6
Tipos: VULNERABILITY 5, BUG 0, CODE_SMELL 7 · **Debt total: 76min**

| regra | issues |
|---|---|
| `githubactions:S8233` | 2 |
| `python:S7498` | 2 |
| `python:S116` | 2 |
| `python:S1192` | 1 |
| `githubactions:S8264` | 1 |
| `python:S2068` | 1 |
| `text:S8565` | 1 |
| `python:S7504` | 1 |
| `python:S5713` | 1 |

## Como usar

Cada issue traz a **mensagem do SonarQube** (descreve o problema e o impacto), o **código real** (linha `>>>`), o tipo e o effort estimado.
**Decisão**: `corrigir` / `falso-positivo` (marcar na plataforma com justificativa) / `risco-aceito`. Ordem: BLOCKER → CRITICAL → VULNERABILITY → MAJOR. CODE_SMELL em volume pede correção de padrão.

## Issues

### 1 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `examples/03_docker_integration.py:59` · **Effort**: 6min

> Define a constant instead of duplicating this literal "FLEXT Team" 3 times.

```python
       55      postgres_plugin = FlextPluginModels.Plugin.Entity(
       56          name="docker-postgres-connector",
       57          plugin_version="1.0.0",
       58          description="PostgreSQL database connector for Docker environment",
>>>    59          author="FLEXT Team",
       60          plugin_type=FlextPluginConstants.Plugin.Type.DATABASE.value,
       61          is_enabled=True,
       62          metadata={"dependencies": ["psycopg2-binary"]},
       63      )
```

**Decisão**: pendente

### 2 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8264`
**Local**: `.github/workflows/docs.yml:18` · **Effort**: 5min

> Move this read permission from workflow level to job level.

```yaml
       14        - ".github/workflows/docs.yml"
       15    workflow_dispatch:
       16  
       17  permissions:
>>>    18    contents: read
       19    pages: write
       20    id-token: write
       21  
       22  concurrency:
```

**Decisão**: pendente

### 3 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:19` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       15    workflow_dispatch:
       16  
       17  permissions:
       18    contents: read
>>>    19    pages: write
       20    id-token: write
       21  
       22  concurrency:
       23    group: pages
```

**Decisão**: pendente

### 4 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:20` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       16  
       17  permissions:
       18    contents: read
       19    pages: write
>>>    20    id-token: write
       21  
       22  concurrency:
       23    group: pages
       24    cancel-in-progress: false
```

**Decisão**: pendente

### 5 · 🟡 MAJOR · VULNERABILITY · `python:S2068`
**Local**: `examples/02_plugin_configuration.py:53` · **Effort**: 30min

> "password" detected here, review this potentially hard-coded credential.

```python
       49              "server": "localhost",
       50              "port": 389,
       51              "base_dn": "dc=flext,dc=dev",
       52              "bind_dn": "cn=readonly,dc=flext,dc=dev",
>>>    53              "bind_password": "readonly",
       54              "use_ssl": False,
       55              "timeout": 30,
       56          },
       57          "search": {
```

**Decisão**: pendente

### 6 · 🟡 MAJOR · VULNERABILITY · `text:S8565`
**Local**: `pyproject.toml:-` · **Effort**: 5min

> Dependency versions are not predictable if the lock file (uv.lock, poetry.lock, pdm.lock or pylock.toml) is missing.


**Decisão**: pendente

### 7 · ⚪ MINOR · CODE_SMELL · `python:S7504`
**Local**: `conftest.py:20` · **Effort**: 5min

> Remove this unnecessary `list()` call on an already iterable object.

```python
       16      if (
       17          existing_package is None
       18          or Path(getattr(existing_package, "__file__", "")).resolve() != init_file
       19      ):
>>>    20          for module_name in list(sys.modules):
       21              if module_name == package_name or module_name.startswith(
       22                  f"{package_name}."
       23              ):
       24                  sys.modules.pop(module_name, None)
```

**Decisão**: pendente

### 8 · ⚪ MINOR · CODE_SMELL · `python:S5713`
**Local**: `src/flext_plugin/_utilities/discovery.py:43` · **Effort**: 1min

> Remove this redundant Exception class; it derives from another which is already caught.

```python
       39          """Discover Python plugins recursively in a directory."""
       40          discovered: MutableSequence[TDiscovery] = []
       41          try:
       42              items = tuple(path.iterdir())
>>>    43          except (OSError, PermissionError):
       44              logger.exception("Failed to discover directory %s", path)
       45              return discovered
       46          for item in items:
       47              if (
```

**Decisão**: pendente

### 9 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_plugin/_utilities/plugin_platform.py:278` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
      274              """Initialize plugin platforFlextPluginModels."""
      275              super().__init__()
      276              if container is not None:
      277                  self._container = container
>>>   278              self._plugins = dict[str, FlextPluginPlatform.Plugin]()
      279              self._executions = dict[str, FlextPluginPlatform.PluginExecution]()
      280              self._registry = FlextPluginPlatform.PluginRegistry.create()
      281              self._discovery = None
      282              self._loader = None
```

**Decisão**: pendente

### 10 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_plugin/_utilities/plugin_platform.py:279` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
      275              super().__init__()
      276              if container is not None:
      277                  self._container = container
      278              self._plugins = dict[str, FlextPluginPlatform.Plugin]()
>>>   279              self._executions = dict[str, FlextPluginPlatform.PluginExecution]()
      280              self._registry = FlextPluginPlatform.PluginRegistry.create()
      281              self._discovery = None
      282              self._loader = None
      283              self._executor = None
```

**Decisão**: pendente

### 11 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_plugin/utilities.py:59` · **Effort**: 2min

> Rename this field "Discovery" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       55              "__import__",
       56              "subprocess",
       57              "os.system",
       58          ]
>>>    59          Discovery: ClassVar[type[FlextPluginDiscovery]]
       60          Platform: ClassVar[type[FlextPluginPlatform]]
       61  
       62          @classmethod
       63          def discover_plugins(
```

**Decisão**: pendente

### 12 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_plugin/utilities.py:60` · **Effort**: 2min

> Rename this field "Platform" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       56              "subprocess",
       57              "os.system",
       58          ]
       59          Discovery: ClassVar[type[FlextPluginDiscovery]]
>>>    60          Platform: ClassVar[type[FlextPluginPlatform]]
       61  
       62          @classmethod
       63          def discover_plugins(
       64              cls, directory: Path | str
```

**Decisão**: pendente
