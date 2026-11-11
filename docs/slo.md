# SLO (Service Level Objective, "Objetivo de Nível de Serviço")

Metas de qualidade da API Bancada Componentes, medidas com a métrica
`http_request_duration_seconds`, publicada em `GET /metrics`.

## Indicadores (SLI, Service Level Indicator, "Indicador de Nível de Serviço")

| Indicador | O que mede | Fonte |
|---|---|---|
| Latência | p95 do tempo de resposta (o tempo abaixo do qual ficam 95% das requisições) | Histograma `http_request_duration_seconds` |
| Erros do servidor | Proporção de respostas com código 5xx | Mesmo histograma, filtrando `status` |

## Objetivos

| Objetivo | Meta | Janela |
|---|---|---|
| Latência | p95 menor ou igual a **300 ms** nas rotas `/componentes` e `/emprestimos` | 30 dias |
| Confiabilidade | **99%** ou mais das requisições sem erro 5xx | 30 dias |

Respostas 4xx (como 404 e 409) **não** contam como falha: são o comportamento
correto da API ao recusar um pedido que viola uma regra de negócio.

## Como medir (PromQL, a linguagem de consulta do Prometheus)

p95 de latência:

```
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{rota=~"/componentes|/emprestimos.*"}[5m])))
```

Proporção de erros 5xx:

```
sum(rate(http_request_duration_seconds_count{status=~"5.."}[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))
```

## Verificação

O teste de desempenho com k6 mede o p95 observado e o compara com a meta de
300 ms. O resultado está registrado em `docs/desempenho.md`.