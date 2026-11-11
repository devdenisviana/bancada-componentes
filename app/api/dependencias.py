from collections.abc import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.bancada import BancadaService


def obter_sessao() -> Iterator[Session]:
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


def obter_servico(sessao: Session = Depends(obter_sessao)) -> BancadaService:
    return BancadaService(sessao)