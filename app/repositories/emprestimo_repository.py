from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.emprestimo import Emprestimo, StatusEmprestimo
from app.repositories.models import EmprestimoModel


class EmprestimoRepository:
    """Salva e busca empréstimos, escondendo o banco do resto do sistema."""

    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def adicionar(self, emprestimo: Emprestimo) -> Emprestimo:
        modelo = EmprestimoModel(
            componente_id=emprestimo.componente_id,
            responsavel=emprestimo.responsavel,
            quantidade=emprestimo.quantidade,
            data_emprestimo=emprestimo.data_emprestimo,
            data_prevista_devolucao=emprestimo.data_prevista_devolucao,
            status=emprestimo.status.value,
            data_devolucao=emprestimo.data_devolucao,
            dias_atraso=emprestimo.dias_atraso,
        )
        self._sessao.add(modelo)
        self._sessao.flush()
        emprestimo.id = modelo.id
        return emprestimo

    def buscar_por_id(self, emprestimo_id: int) -> Emprestimo | None:
        modelo = self._sessao.get(EmprestimoModel, emprestimo_id)
        return self._para_dominio(modelo) if modelo else None

    def listar(self, responsavel: str | None = None) -> list[Emprestimo]:
        consulta = select(EmprestimoModel).order_by(EmprestimoModel.id)
        if responsavel:
            consulta = consulta.where(EmprestimoModel.responsavel == responsavel)
        return [self._para_dominio(m) for m in self._sessao.scalars(consulta)]

    def unidades_em_aberto(self, responsavel: str) -> int:
        total = self._sessao.scalar(
            select(func.coalesce(func.sum(EmprestimoModel.quantidade), 0)).where(
                EmprestimoModel.responsavel == responsavel,
                EmprestimoModel.status == StatusEmprestimo.ABERTO.value,
            )
        )
        return int(total)

    def atualizar(self, emprestimo: Emprestimo) -> None:
        modelo = self._sessao.get(EmprestimoModel, emprestimo.id)
        modelo.status = emprestimo.status.value
        modelo.data_devolucao = emprestimo.data_devolucao
        modelo.dias_atraso = emprestimo.dias_atraso

    @staticmethod
    def _para_dominio(modelo: EmprestimoModel) -> Emprestimo:
        return Emprestimo(
            id=modelo.id,
            componente_id=modelo.componente_id,
            responsavel=modelo.responsavel,
            quantidade=modelo.quantidade,
            data_emprestimo=modelo.data_emprestimo,
            data_prevista_devolucao=modelo.data_prevista_devolucao,
            status=StatusEmprestimo(modelo.status),
            data_devolucao=modelo.data_devolucao,
            dias_atraso=modelo.dias_atraso,
        )