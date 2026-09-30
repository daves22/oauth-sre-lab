# ADR-0001: Linguagem dos microsserviços

- **Status:** Aceito
- **Data:** 2026-09-29

## Contexto
O laboratório precisa de serviços simples de ler, fáceis de instrumentar
com OpenTelemetry e Prometheus, e com falhas simples de injetar
(latência, erros, vazamento de memória).

## Decisão
Python 3.12 com FastAPI.

## Alternativas consideradas
- **Go:** mais eficiente e comum em ecossistemas de infraestrutura, mas
  aumenta a curva de aprendizado e o volume de código.

## Consequências
- (+) Foco em SRE, não na linguagem.
- (+) Auto-instrumentação madura do OpenTelemetry.
- (-) Maior consumo de CPU/memória que Go; o GIL limita concorrência.
  Aceitável e até útil para estudar saturação.
- Um serviço poderá ser reescrito em Go futuramente para comparar performance.
