def criar_componente(cliente, total: int = 50) -> dict:
    resposta = cliente.post(
        "/componentes",
        json={"nome": "Resistor 10k", "categoria": "resistor", "quantidade_total": total},
    )
    assert resposta.status_code == 201
    return resposta.json()


def emprestar(cliente, componente_id: int, quantidade: int, responsavel: str = "Denis"):
    return cliente.post(
        "/emprestimos",
        json={
            "componente_id": componente_id,
            "responsavel": responsavel,
            "quantidade": quantidade,
        },
    )


def estoque_disponivel(cliente) -> int:
    return cliente.get("/componentes").json()[0]["quantidade_disponivel"]


def test_health(cliente):
    resposta = cliente.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_fluxo_completo_cadastrar_emprestar_devolver_e_consultar(cliente):
    componente = criar_componente(cliente, 50)

    emprestimo = emprestar(cliente, componente["id"], 3)
    assert emprestimo.status_code == 201
    assert emprestimo.json()["status"] == "ABERTO"
    assert estoque_disponivel(cliente) == 47

    devolucao = cliente.post(f"/emprestimos/{emprestimo.json()['id']}/devolucao")
    assert devolucao.status_code == 200
    assert devolucao.json()["status"] == "DEVOLVIDO"
    assert estoque_disponivel(cliente) == 50

    historico = cliente.get("/emprestimos", params={"responsavel": "Denis"})
    assert historico.status_code == 200
    assert len(historico.json()) == 1
    assert historico.json()[0]["status"] == "DEVOLVIDO"


def test_limite_por_pessoa_retorna_409_e_nao_altera_o_estoque(cliente):
    componente = criar_componente(cliente, 50)
    assert emprestar(cliente, componente["id"], 8).status_code == 201

    resposta = emprestar(cliente, componente["id"], 3)

    assert resposta.status_code == 409
    assert "Limite" in resposta.json()["detalhe"]
    assert estoque_disponivel(cliente) == 42


def test_estoque_insuficiente_retorna_409(cliente):
    componente = criar_componente(cliente, 5)

    resposta = emprestar(cliente, componente["id"], 6)

    assert resposta.status_code == 409
    assert estoque_disponivel(cliente) == 5


def test_componente_inexistente_retorna_404(cliente):
    resposta = emprestar(cliente, componente_id=999, quantidade=1)
    assert resposta.status_code == 404


def test_quantidade_invalida_retorna_422(cliente):
    componente = criar_componente(cliente, 10)
    resposta = emprestar(cliente, componente["id"], 0)
    assert resposta.status_code == 422


def test_devolver_duas_vezes_retorna_409(cliente):
    componente = criar_componente(cliente, 10)
    emprestimo_id = emprestar(cliente, componente["id"], 2).json()["id"]
    assert cliente.post(f"/emprestimos/{emprestimo_id}/devolucao").status_code == 200

    segunda = cliente.post(f"/emprestimos/{emprestimo_id}/devolucao")

    assert segunda.status_code == 409
    assert estoque_disponivel(cliente) == 10


def test_devolver_emprestimo_inexistente_retorna_404(cliente):
    resposta = cliente.post("/emprestimos/999/devolucao")
    assert resposta.status_code == 404


def test_cadastro_com_dados_invalidos_retorna_422(cliente):
    resposta = cliente.post(
        "/componentes",
        json={"nome": "", "categoria": "resistor", "quantidade_total": 10},
    )
    assert resposta.status_code == 422