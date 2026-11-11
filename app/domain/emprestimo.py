from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum

from app.domain.componente import Componente
from app.domain.excecoes import (
    EmprestimoJaDevolvido,
    LimiteExcedido,
    QuantidadeInvalida,
)
from app.domain.politica import PoliticaEmprestimo


class StatusEmprestimo(str, Enum):
    ABERTO = "ABERTO"
    DEVOLVIDO = "DEVOLVIDO"


@dataclass
class Emprestimo:
    componente_id: int | None
    responsavel: str
    quantidade: int
    data_emprestimo: date
    data_prevista_devolucao: date
    status: StatusEmprestimo = StatusEmprestimo.ABERTO
    data_devolucao: date | None = None
    dias_atraso: int = 0
    id: int | None = None

    @classmethod
    def abrir(
        cls,
        componente: Componente,
        responsavel: str,
        quantidade: int,
        unidades_em_aberto: int,
        politica: PoliticaEmprestimo,
        hoje: date,
    ) -> "Emprestimo":
        """Abre um empréstimo aplicando as regras de quantidade, limite e prazo."""
        if quantidade <= 0:
            raise QuantidadeInvalida("A quantidade deve ser maior que zero.")
        if unidades_em_aberto + quantidade > politica.limite_por_pessoa():
            raise LimiteExcedido(
                f"Limite de {politica.limite_por_pessoa()} unidades em aberto por pessoa."
            )
        componente.retirar(quantidade)
        return cls(
            componente_id=componente.id,
            responsavel=responsavel,
            quantidade=quantidade,
            data_emprestimo=hoje,
            data_prevista_devolucao=hoje + timedelta(days=politica.prazo_em_dias()),
        )

    def devolver(self, componente: Componente, hoje: date) -> None:
        """Registra a devolução, repõe o estoque e calcula os dias de atraso."""
        if self.status == StatusEmprestimo.DEVOLVIDO:
            raise EmprestimoJaDevolvido("Este empréstimo já foi devolvido.")
        componente.repor(self.quantidade)
        self.status = StatusEmprestimo.DEVOLVIDO
        self.data_devolucao = hoje
        self.dias_atraso = max(0, (hoje - self.data_prevista_devolucao).days)