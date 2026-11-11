from collections.abc import Callable
from datetime import date

from sqlalchemy.orm import Session

from app.domain.componente import Componente
from app.domain.emprestimo import Emprestimo
from app.domain.excecoes import RecursoNaoEncontrado
from app.domain.politica import PoliticaEmprestimo, PoliticaPadrao
from app.repositories.componente_repository import ComponenteRepository
from app.repositories.emprestimo_repository import EmprestimoRepository


class BancadaService:
    """Casos de uso do sistema: orquestra o domínio e os repositórios."""

    def __init__(
        self,
        sessao: Session,
        politica: PoliticaEmprestimo | None = None,
        relogio: Callable[[], date] = date.today,
    ) -> None:
        self._sessao = sessao
        self._componentes = ComponenteRepository(sessao)
        self._emprestimos = EmprestimoRepository(sessao)
        self._politica = politica or PoliticaPadrao()
        self._relogio = relogio

    def cadastrar_componente(
        self, nome: str, categoria: str, quantidade_total: int
    ) -> Componente:
        componente = Componente(
            nome=nome, categoria=categoria, quantidade_total=quantidade_total
        )
        self._componentes.adicionar(componente)
        self._sessao.commit()
        return componente

    def listar_componentes(self) -> list[Componente]:
        return self._componentes.listar()

    def emprestar(
        self, componente_id: int, responsavel: str, quantidade: int
    ) -> Emprestimo:
        componente = self._buscar_componente(componente_id)
        em_aberto = self._emprestimos.unidades_em_aberto(responsavel)
        emprestimo = Emprestimo.abrir(
            componente=componente,
            responsavel=responsavel,
            quantidade=quantidade,
            unidades_em_aberto=em_aberto,
            politica=self._politica,
            hoje=self._relogio(),
        )
        self._componentes.atualizar(componente)
        self._emprestimos.adicionar(emprestimo)
        self._sessao.commit()
        return emprestimo

    def devolver(self, emprestimo_id: int) -> Emprestimo:
        emprestimo = self._emprestimos.buscar_por_id(emprestimo_id)
        if emprestimo is None:
            raise RecursoNaoEncontrado(f"Empréstimo {emprestimo_id} não encontrado.")
        componente = self._buscar_componente(emprestimo.componente_id)
        emprestimo.devolver(componente, hoje=self._relogio())
        self._componentes.atualizar(componente)
        self._emprestimos.atualizar(emprestimo)
        self._sessao.commit()
        return emprestimo

    def listar_emprestimos(self, responsavel: str | None = None) -> list[Emprestimo]:
        return self._emprestimos.listar(responsavel)

    def _buscar_componente(self, componente_id: int | None) -> Componente:
        componente = self._componentes.buscar_por_id(componente_id)
        if componente is None:
            raise RecursoNaoEncontrado(f"Componente {componente_id} não encontrado.")
        return componente