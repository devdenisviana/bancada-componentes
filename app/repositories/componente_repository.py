from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.componente import Componente
from app.repositories.models import ComponenteModel


class ComponenteRepository:
    """Salva e busca componentes, escondendo o banco do resto do sistema."""

    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def adicionar(self, componente: Componente) -> Componente:
        modelo = ComponenteModel(
            nome=componente.nome,
            categoria=componente.categoria,
            quantidade_total=componente.quantidade_total,
            quantidade_disponivel=componente.quantidade_disponivel,
        )
        self._sessao.add(modelo)
        self._sessao.flush()
        componente.id = modelo.id
        return componente

    def buscar_por_id(self, componente_id: int) -> Componente | None:
        modelo = self._sessao.get(ComponenteModel, componente_id)
        return self._para_dominio(modelo) if modelo else None

    def listar(self) -> list[Componente]:
        modelos = self._sessao.scalars(
            select(ComponenteModel).order_by(ComponenteModel.id)
        )
        return [self._para_dominio(modelo) for modelo in modelos]

    def atualizar(self, componente: Componente) -> None:
        modelo = self._sessao.get(ComponenteModel, componente.id)
        modelo.quantidade_disponivel = componente.quantidade_disponivel

    @staticmethod
    def _para_dominio(modelo: ComponenteModel) -> Componente:
        return Componente(
            id=modelo.id,
            nome=modelo.nome,
            categoria=modelo.categoria,
            quantidade_total=modelo.quantidade_total,
            quantidade_disponivel=modelo.quantidade_disponivel,
        )