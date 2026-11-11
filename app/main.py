from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.api.rotas import router
from app.database import Base, engine
from app.domain.excecoes import (
    EmprestimoJaDevolvido,
    ErroDeDominio,
    EstoqueInsuficiente,
    LimiteExcedido,
    QuantidadeInvalida,
    RecursoNaoEncontrado,
)
from app.observabilidade import configurar_logs, registrar_requisicao
from app.repositories import models  # noqa: F401  (registra as tabelas)

STATUS_POR_ERRO = {
    RecursoNaoEncontrado: 404,
    QuantidadeInvalida: 422,
    EstoqueInsuficiente: 409,
    LimiteExcedido: 409,
    EmprestimoJaDevolvido: 409,
}

configurar_logs()


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Bancada Componentes",
    version="0.1.0",
    description="Inventário e empréstimo de componentes eletrônicos de bancada.",
    lifespan=ciclo_de_vida,
)

app.middleware("http")(registrar_requisicao)


@app.exception_handler(ErroDeDominio)
async def tratar_erro_de_dominio(request: Request, erro: ErroDeDominio):
    codigo = STATUS_POR_ERRO.get(type(erro), 400)
    return JSONResponse(status_code=codigo, content={"detalhe": str(erro)})


app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics", include_in_schema=False)
def metricas() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)