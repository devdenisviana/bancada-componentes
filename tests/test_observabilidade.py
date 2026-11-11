import json
import logging

from app.observabilidade import FormatadorJson


def test_metricas_expoe_a_duracao_das_requisicoes(cliente):
    cliente.get("/health")

    resposta = cliente.get("/metrics")

    assert resposta.status_code == 200
    assert "http_request_duration_seconds_count" in resposta.text
    assert 'rota="/health"' in resposta.text


def test_metrica_usa_o_modelo_da_rota_e_nao_o_endereco_real(cliente):
    cliente.post("/emprestimos/123/devolucao")

    texto = cliente.get("/metrics").text

    assert 'rota="/emprestimos/{emprestimo_id}/devolucao"' in texto
    assert "/emprestimos/123/devolucao" not in texto


def test_formatador_gera_uma_linha_json_com_os_campos():
    registro = logging.LogRecord(
        "bancada", logging.INFO, __file__, 1, "requisicao", None, None
    )
    registro.campos = {"metodo": "GET", "status": 200}

    dados = json.loads(FormatadorJson().format(registro))

    assert dados["evento"] == "requisicao"
    assert dados["nivel"] == "INFO"
    assert dados["metodo"] == "GET"
    assert dados["status"] == 200