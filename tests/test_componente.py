import pytest

from app.domain.componente import Componente
from app.domain.excecoes import EstoqueInsuficiente, QuantidadeInvalida


def novo_componente(total: int = 10) -> Componente:
    return Componente(nome="Resistor 10k", categoria="resistor", quantidade_total=total)


def test_disponivel_inicia_igual_ao_total():
    componente = novo_componente(50)
    assert componente.quantidade_disponivel == 50


def test_total_negativo_e_invalido():
    with pytest.raises(QuantidadeInvalida):
        novo_componente(-1)


def test_retirar_reduz_o_estoque_disponivel():
    componente = novo_componente(50)
    componente.retirar(20)
    assert componente.quantidade_disponivel == 30


def test_retirar_mais_que_o_disponivel_falha_e_nao_altera_o_estoque():
    componente = novo_componente(5)
    with pytest.raises(EstoqueInsuficiente):
        componente.retirar(6)
    assert componente.quantidade_disponivel == 5


@pytest.mark.parametrize("quantidade", [0, -1])
def test_retirar_quantidade_invalida_falha(quantidade):
    componente = novo_componente()
    with pytest.raises(QuantidadeInvalida):
        componente.retirar(quantidade)


def test_repor_aumenta_o_estoque_sem_passar_do_total():
    componente = novo_componente(10)
    componente.retirar(4)
    componente.repor(4)
    assert componente.quantidade_disponivel == 10
    componente.repor(3)
    assert componente.quantidade_disponivel == 10
    
@pytest.mark.parametrize("quantidade", [0, -1])
def test_repor_quantidade_invalida_falha(quantidade):
    componente = novo_componente()
    with pytest.raises(QuantidadeInvalida):
        componente.repor(quantidade)