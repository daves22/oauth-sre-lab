# OAuth SRE Lab

Laboratório pessoal de **Site Reliability Engineering** construído do zero:
um pequeno ecossistema de microsserviços (foco em autenticação/autorização)
usado para praticar confiabilidade, observabilidade, resposta a incidentes
e automação.

> Projeto de estudo. Os serviços são fictícios e não representam nenhum
> sistema de produção real.

## Objetivo

Aprender fazendo: construir, instrumentar, medir, quebrar, investigar,
corrigir e documentar um sistema distribuído.

## Arquitetura alvo
Client -> Gateway -> Auth Service -> Database
-> User Service -> Database
Todos os serviços -> OpenTelemetry Collector -> Prometheus / Loki / Tempo -> Grafana

## Stack

Python + FastAPI · Docker · Kubernetes (Kind) · Prometheus · Grafana ·
Alertmanager · OpenTelemetry · Loki · Tempo · k6 · GitHub Actions · Terraform

## Roadmap

- [x] Fase 0: Ambiente local (WSL2, Docker, kubectl, Kind)
- [x] Fase 1: Repositório e estrutura
- [ ] Fase 2: Primeiros microsserviços
- [ ] Fase 3: Containerização (Docker Compose)
- [ ] Fases 4-8: Observabilidade (métricas, logs, traces)
- [ ] Fase 9: SLI, SLO e Error Budget
- [ ] Fase 10: Alertas
- [ ] Fase 11: Kubernetes
- [ ] Fases 12-14: Incidentes, testes de carga e resiliência
- [ ] Fases 15-17: CI/CD, Terraform e segurança
- [ ] Fases 18-20: Runbooks, postmortems e capstone

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `docs/` | Arquitetura (ADRs), SRE, runbooks, incidentes e postmortems |
| `services/` | Código dos microsserviços |
| `scripts/` | Automações auxiliares |

Novas pastas (`infrastructure/`, `observability/`, `tests/`, `.github/`)
surgem conforme as fases avançam.

## Decisões de arquitetura

- [ADR-0001: Linguagem dos serviços](docs/architecture/adr-0001-linguagem-dos-servicos.md)