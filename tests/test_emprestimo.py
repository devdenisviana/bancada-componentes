from datetime import date

import pytest

from app.domain.componente import Componente
from app.domain.emprestimo import Emprestimo, StatusEmprestimo
from app.domain.excecoes import (
    EmprestimoJaDevolvido,
    EstoqueInsuficiente,
    LimiteExcedido,
    QuantidadeInvalida,
)
from app.domain.politica import PoliticaEmprestimo, PoliticaPadrao

HOJE = date(2026, 11, 11)


def novo_componente(total: int = 20) -> Componente:
    return Componente(
        nome="Capacitor 100nF", categoria="capacitor", quantidade_total=total, id=1
    )


def abrir(
    componente: Componente,
    quantidade: int = 3,
    unidades_em_aberto: int = 0,
    politica: PoliticaEmprestimo | None = None,
) -> Emprestimo:
    return Emprestimo.abrir(
        componente=componente,
        responsavel="Denis",
        quantidade=quantidade,
        unidades_em_aberto=unidades_em_aberto,
        politica=politica or PoliticaPadrao(),
        hoje=HOJE,
    )


def test_abrir_define_prazo_padrao_e_retira_do_estoque():
    componente = novo_componente(20)
    emprestimo = abrir(componente, quantidade=3)

    assert emprestimo.status == StatusEmprestimo.ABERTO
    assert emprestimo.data_prevista_devolucao == date(2026, 11, 18)
    assert emprestimo.componente_id == 1
    assert componente.quantidade_disponivel == 17


@pytest.mark.parametrize("quantidade", [0, -1])
def test_abrir_com_quantidade_invalida_falha(quantidade):
    with pytest.raises(QuantidadeInvalida):
        abrir(novo_componente(), quantidade=quantidade)


def test_abrir_acima_do_estoque_falha():
    with pytest.raises(EstoqueInsuficiente):
        abrir(novo_componente(5), quantidade=6)


def test_abrir_acima_do_limite_falha_e_nao_altera_o_estoque():
    componente = novo_componente(20)
    with pytest.raises(LimiteExcedido):
        abrir(componente, quantidade=3, unidades_em_aberto=8)
    assert componente.quantidade_disponivel == 20


def test_abrir_exatamente_no_limite_e_permitido():
    emprestimo = abrir(novo_componente(20), quantidade=3, unidades_em_aberto=7)
    assert emprestimo.status == StatusEmprestimo.ABERTO


def test_politica_customizada_altera_limite_e_prazo():
    class PoliticaLonga(PoliticaEmprestimo):
        def limite_por_pessoa(self) -> int:
            return 20

        def prazo_em_dias(self) -> int:
            return 30

    emprestimo = abrir(
        novo_componente(50), quantidade=15, unidades_em_aberto=5, politica=PoliticaLonga()
    )
    assert emprestimo.data_prevista_devolucao == date(2026, 12, 11)


def test_devolver_no_prazo_repoe_estoque_sem_atraso():
    componente = novo_componente(20)
    emprestimo = abrir(componente, quantidade=3)

    emprestimo.devolver(componente, hoje=date(2026, 11, 15))

    assert emprestimo.status == StatusEmprestimo.DEVOLVIDO
    assert emprestimo.data_devolucao == date(2026, 11, 15)
    assert emprestimo.dias_atraso == 0
    assert componente.quantidade_disponivel == 20


def test_devolver_com_atraso_calcula_os_dias():
    componente = novo_componente(20)
    emprestimo = abrir(componente, quantidade=3)

    emprestimo.devolver(componente, hoje=date(2026, 11, 21))

    assert emprestimo.dias_atraso == 3


def test_devolver_duas_vezes_falha():
    componente = novo_componente(20)
    emprestimo = abrir(componente, quantidade=3)
    emprestimo.devolver(componente, hoje=date(2026, 11, 15))

    with pytest.raises(EmprestimoJaDevolvido):
        emprestimo.devolver(componente, hoje=date(2026, 11, 16))
    assert componente.quantidade_disponivel == 20