**Nível: B (simples)**

# Bancada Componentes

![CI](https://github.com/devdenisviana/bancada-componentes/actions/workflows/ci.yml/badge.svg)

API para controle de inventário e empréstimo de componentes eletrônicos de
bancada (resistores, capacitores, circuitos integrados e similares).

**Fluxo principal:** cadastrar componente → emprestar → devolver → consultar o
histórico.

## Regras de negócio

1. A quantidade emprestada deve ser maior que zero.
2. Não é possível emprestar mais do que a quantidade disponível (o estoque nunca fica negativo).
3. Cada pessoa pode ter no máximo **10 unidades em aberto** ao mesmo tempo, somando todos os componentes.
4. O prazo padrão de devolução é de **7 dias**.
5. Só é possível devolver um empréstimo com status `ABERTO`; a devolução repõe o estoque.
6. Devoluções após a data prevista registram os **dias de atraso**.

As regras 3 e 4 ficam em uma política de empréstimo substituível (padrão
Strategy), justificada em [`docs/adr/`](docs/adr/0001-strategy-para-politicas-de-emprestimo.md).

## Tecnologias

Python 3.14, FastAPI, SQLAlchemy, SQLite, pytest, ruff, Docker Compose e GitHub Actions.

## Como rodar

### Com Docker (recomendado)

Pré-requisito: Docker Desktop (ou Docker Engine) em execução.

```bash
docker compose up --build
```

A API fica em http://127.0.0.1:8000 e a documentação interativa em
http://127.0.0.1:8000/docs. O banco SQLite fica em um volume do Docker, então os
dados sobrevivem a `docker compose down` (para apagá-los, use `docker compose down -v`).

### Sem Docker

```bash
python -m venv .venv
# Windows (PowerShell): .\.venv\Scripts\Activate.ps1
# Linux/macOS:          source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

A variável `DATABASE_URL` é opcional (veja [`.env.example`](.env.example)); sem
ela, o banco é o arquivo `bancada.db` na pasta do projeto.

## Como testar

```bash
pytest
```

O comando roda os testes unitários do domínio e os testes de integração da API
(com banco SQLite em memória) e **falha se a cobertura ficar abaixo de 80%**.
Para o lint:

```bash
ruff check .
```

O CI (GitHub Actions) executa o lint e os testes a cada `push`.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/componentes` | Cadastra um componente |
| GET | `/componentes` | Lista os componentes e o estoque disponível |
| POST | `/emprestimos` | Abre um empréstimo |
| POST | `/emprestimos/{id}/devolucao` | Registra a devolução |
| GET | `/emprestimos?responsavel=...` | Lista empréstimos (filtro opcional por pessoa) |
| GET | `/health` | Verificação de saúde |
| GET | `/metrics` | Métricas no formato Prometheus |

Erros de negócio retornam `{"detalhe": "..."}` com o código HTTP: `404` (não
encontrado), `409` (conflito com o estado atual: estoque, limite ou devolução
repetida) e `422` (dados inválidos).

## Observabilidade

- **Logs estruturados:** cada requisição gera uma linha JSON (método, rota, status e duração em ms).
- **Métrica:** `http_request_duration_seconds` (histograma) em `/metrics`.
- **SLO:** veja [`docs/slo.md`](docs/slo.md).

## Documentação

- [`docs/openapi.yaml`](docs/openapi.yaml): especificação OpenAPI 3.1 da API
- [`docs/adr/`](docs/adr/0001-strategy-para-politicas-de-emprestimo.md): decisão de arquitetura (ADR)
- [`docs/slo.md`](docs/slo.md): objetivos de nível de serviço
- [`docs/desempenho.md`](docs/desempenho.md): teste de desempenho com k6
- [`docs/ia.md`](docs/ia.md): uso de IA no projeto

## Estrutura

```
app/
  domain/        regras de negócio (sem dependência de framework ou banco)
  repositories/  acesso ao banco (SQLAlchemy)
  services/      casos de uso (orquestram domínio e repositórios)
  api/           rotas e esquemas HTTP
tests/           testes unitários e de integração
docs/            documentação
```

## Autoria

Projeto individual de Denis Viana (@devdenisviana). Veja
[`CONTRIBUTORS.md`](CONTRIBUTORS.md).