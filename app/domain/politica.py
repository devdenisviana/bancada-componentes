from abc import ABC, abstractmethod


class PoliticaEmprestimo(ABC):
    """Estratégia: define as regras variáveis de um empréstimo."""

    @abstractmethod
    def limite_por_pessoa(self) -> int:
        """Máximo de unidades em aberto por pessoa."""

    @abstractmethod
    def prazo_em_dias(self) -> int:
        """Prazo de devolução, em dias corridos."""


class PoliticaPadrao(PoliticaEmprestimo):
    """Política padrão: 10 unidades por pessoa, prazo de 7 dias."""

    def limite_por_pessoa(self) -> int:
        return 10

    def prazo_em_dias(self) -> int:
        return 7