import json
import logging
import time

from fastapi import Request
from prometheus_client import Histogram

LOGGER = logging.getLogger("bancada")

DURACAO_REQUISICOES = Histogram(
    "http_request_duration_seconds",
    "Duração das requisições HTTP, em segundos.",
    ["metodo", "rota", "status"],
)


class FormatadorJson(logging.Formatter):
    """Escreve cada log como uma linha JSON."""

    def format(self, record: logging.LogRecord) -> str:
        registro = {
            "momento": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "nivel": record.levelname,
            "evento": record.getMessage(),
        }
        registro.update(getattr(record, "campos", {}))
        return json.dumps(registro, ensure_ascii=False)


def configurar_logs() -> None:
    if LOGGER.handlers:
        return
    manipulador = logging.StreamHandler()
    manipulador.setFormatter(FormatadorJson())
    LOGGER.addHandler(manipulador)
    LOGGER.setLevel(logging.INFO)
    LOGGER.propagate = False


async def registrar_requisicao(request: Request, call_next):
    """Mede cada requisição: grava a métrica de duração e um log em JSON."""
    inicio = time.perf_counter()
    status = 500
    try:
        resposta = await call_next(request)
        status = resposta.status_code
        return resposta
    finally:
        duracao = time.perf_counter() - inicio
        rota = request.scope.get("route")
        caminho = rota.path if rota else "desconhecida"
        DURACAO_REQUISICOES.labels(request.method, caminho, str(status)).observe(duracao)
        LOGGER.info(
            "requisicao",
            extra={
                "campos": {
                    "metodo": request.method,
                    "rota": caminho,
                    "status": status,
                    "duracao_ms": round(duracao * 1000, 2),
                }
            },
        )