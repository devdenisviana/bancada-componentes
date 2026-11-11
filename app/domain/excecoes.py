class ErroDeDominio(Exception):
    """Base de todos os erros das regras de negócio."""


class QuantidadeInvalida(ErroDeDominio):
    """A quantidade informada deve ser maior que zero."""


class EstoqueInsuficiente(ErroDeDominio):
    """Não há unidades disponíveis suficientes para o empréstimo."""


class LimiteExcedido(ErroDeDominio):
    """A pessoa ultrapassaria o limite de unidades em aberto."""


class EmprestimoJaDevolvido(ErroDeDominio):
    """O empréstimo já foi devolvido e não pode ser devolvido de novo."""
    
    

class RecursoNaoEncontrado(ErroDeDominio):
    """O componente ou o empréstimo solicitado não existe."""