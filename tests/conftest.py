import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencias import obter_sessao
from app.database import Base
from app.main import app
from app.repositories import models  # noqa: F401  (registra as tabelas)


@pytest.fixture
def cliente():
    """Cliente HTTP de teste, ligado a um banco SQLite em memória e vazio."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    sessao_de_teste = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def obter_sessao_de_teste():
        sessao = sessao_de_teste()
        try:
            yield sessao
        finally:
            sessao.close()

    app.dependency_overrides[obter_sessao] = obter_sessao_de_teste
    yield TestClient(app)
    app.dependency_overrides.clear()
    engine.dispose()