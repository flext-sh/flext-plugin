# Triagem SonarCloud — flext-sh/flext-plugin

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead de rastreio: `mro-2wjm.15`

## Resumo

**12 issues** — BLOCKER 0, CRITICAL 1, MAJOR 5, MINOR 6
Tipos: VULNERABILITY 5, BUG 0, CODE_SMELL 7

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

## Issues

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | tipo | regra | componente | linha | Decisão |
|---|---|---|---|---|---|---|
| 1 | CRITICAL | CODE_SMELL | `python:S1192` | `examples/03_docker_integration.py` | 59 | |
| 2 | MAJOR | VULNERABILITY | `githubactions:S8264` | `.github/workflows/docs.yml` | 18 | |
| 3 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 19 | |
| 4 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 20 | |
| 5 | MAJOR | VULNERABILITY | `python:S2068` | `examples/02_plugin_configuration.py` | 53 | |
| 6 | MAJOR | VULNERABILITY | `text:S8565` | `pyproject.toml` | - | |
| 7 | MINOR | CODE_SMELL | `python:S7504` | `conftest.py` | 20 | |
| 8 | MINOR | CODE_SMELL | `python:S5713` | `src/flext_plugin/_utilities/discovery.py` | 43 | |
| 9 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_plugin/_utilities/plugin_platform.py` | 278 | |
| 10 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_plugin/_utilities/plugin_platform.py` | 279 | |
| 11 | MINOR | CODE_SMELL | `python:S116` | `src/flext_plugin/utilities.py` | 59 | |
| 12 | MINOR | CODE_SMELL | `python:S116` | `src/flext_plugin/utilities.py` | 60 | |

## Como triar

1. **BLOCKER e CRITICAL primeiro**, e todo VULNERABILITY independente de severidade.
2. Classificar: **corrigir**, **falso-positivo** (marcar na plataforma SonarCloud com justificativa), **risco-aceito** (com prazo).
3. CODE_SMELL em volume alto sugere padrão — corrigir a causa raiz, não issue a issue.

Dados brutos: `~/sonarqube-violations/by-repo/flext-sh__flext-plugin.json`

