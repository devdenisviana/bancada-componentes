# Desempenho

Teste de fumaça (smoke test) com k6 sobre o fluxo principal da API, comparado
com o SLO definido em [`slo.md`](slo.md).

## Ambiente

- API em container Docker (`docker compose up`), um único processo `uvicorn`, banco SQLite em volume.
- Docker Desktop no Windows 11.
- k6 executado em outro container (`grafana/k6`), acessando a API pelo endereço `host.docker.internal:8000`.
- Banco com poucos dados no início do teste.

## Cenário

Script: [`k6/smoke.js`](../k6/smoke.js).

- 5 usuários virtuais (VUs) durante 20 segundos.
- Cada repetição executa o fluxo principal: `POST /emprestimos`, `POST /emprestimos/{id}/devolucao` e `GET /componentes`.
- A preparação (`setup`) cadastra um componente com estoque grande, e cada repetição usa um responsável diferente, para não esbarrar no limite de 10 unidades.

Como reproduzir (com a API no ar via `docker compose up -d --build`):

```
Get-Content k6\smoke.js | docker run --rm -i -e BASE_URL=http://host.docker.internal:8000 grafana/k6 run -
```

## Resultados medidos

| Métrica | Valor |
|---|---|
| Requisições totais | 1.918 (cerca de 95 por segundo) |
| Requisições com falha | 0,00% (0 de 1.918) |
| Verificações (`checks`) aprovadas | 100% (1.917 de 1.917) |
| Tempo de resposta médio | 52,09 ms |
| Mediana | 31,18 ms |
| **p95** | **145,12 ms** |
| p90 | 106,04 ms |
| Máximo | 1,47 s |

## Comparação com o SLO

| Objetivo | Meta | Medido | Situação |
|---|---|---|---|
| Latência (p95) | 300 ms ou menos | 145,12 ms | Atendido |
| Erros 5xx | menos de 1% | 0,00% | Atendido |

O k6 também verificou essas metas automaticamente (`thresholds` no script) e
terminou com todas as marcas de aprovação.

## Observações e limites

- A carga é pequena (5 usuários, 20 s): confirma que o fluxo principal funciona sob uso simultâneo, mas **não** é um teste de capacidade nem de estresse.
- O tempo máximo (1,47 s) é bem maior que o p95. Não investiguei a causa; hipóteses são o aquecimento dos primeiros acessos ou a disputa por escrita no SQLite, que serializa gravações.
- O p95 por repetição completa (três requisições seguidas) foi de 341 ms, mas o SLO é definido por requisição, não por repetição.

## O que eu mudaria

1. Rodar um teste mais longo e com aumento gradual de usuários, para achar o ponto em que a latência piora.
2. Investigar o tempo máximo com a métrica `http_request_duration_seconds` de `/metrics`, separando por rota.
3. Se as gravações simultâneas virarem gargalo, trocar o SQLite por um banco com melhor concorrência de escrita (como o PostgreSQL) e usar mais de um processo da API.