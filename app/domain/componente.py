from dataclasses import dataclass

from app.domain.excecoes import EstoqueInsuficiente, QuantidadeInvalida


@dataclass
class Componente:
    nome: str
    categoria: str
    quantidade_total: int
    quantidade_disponivel: int | None = None
    id: int | None = None

    def __post_init__(self) -> None:
        if self.quantidade_total < 0:
            raise QuantidadeInvalida("A quantidade total não pode ser negativa.")
        if self.quantidade_disponivel is None:
            self.quantidade_disponivel = self.quantidade_total

    def retirar(self, quantidade: int) -> None:
        """Retira unidades do estoque para um empréstimo."""
        if quantidade <= 0:
            raise QuantidadeInvalida("A quantidade deve ser maior que zero.")
        if quantidade > self.quantidade_disponivel:
            raise EstoqueInsuficiente(
                f"Disponível: {self.quantidade_disponivel}; solicitado: {quantidade}."
            )
        self.quantidade_disponivel -= quantidade

    def repor(self, quantidade: int) -> None:
        """Devolve unidades ao estoque, sem passar do total cadastrado."""
        if quantidade <= 0:
            raise QuantidadeInvalida("A quantidade deve ser maior que zero.")
        self.quantidade_disponivel = min(
            self.quantidade_total, self.quantidade_disponivel + quantidade
        )