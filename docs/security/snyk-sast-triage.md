# Triagem Snyk Code (SAST) — flext-sh/flext-plugin

Gerado do scan Snyk da org Datacosmos (dump 2026-08-06).

**4 achados** — critical 0, high 0, medium 4, low 0

| categoria | achados |
|---|---|
| Use of Hardcoded Passwords | 4 |

## Achados

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | categoria | arquivo | linha | CWE | Decisão |
|---|---|---|---|---|---|---|
| 1 | medium | Use of Hardcoded Passwords | `examples/02_plugin_configuration.py` | 27 | - | |
| 2 | medium | Use of Hardcoded Passwords | `examples/03_docker_integration.py` | 49 | - | |
| 3 | medium | Use of Hardcoded Passwords | `examples/03_docker_integration.py` | 74 | - | |
| 4 | medium | Use of Hardcoded Passwords | `examples/03_docker_integration.py` | 104 | - | |

## Como triar

1. Abrir `arquivo:linha` e seguir o fluxo de dados até o sink.
2. Classificar: **corrigir** (entrada externa alcança o sink sem sanitização), **falso-positivo** (credencial de fixture, path de constante — registrar em `.snyk` com justificativa), **risco-aceito** (com prazo de revisão).

Dados brutos: `~/snyk-violations/sast/flext-sh__flext-plugin.sast.json`

