from urllib.parse import quote_plus

from src.services.sistema import SistemaOcorrencias
import src.web.app as web_app


def test_api_qr_equipamento_retorna_url_da_api_publica(tmp_path):
    web_app.sistema = SistemaOcorrencias(
        arquivo_dados=tmp_path / "web_ocorrencias.json"
    )
    web_app.app.config["TESTING"] = True

    cliente = web_app.app.test_client()
    resposta_equipamento = cliente.post(
        "/api/equipamentos",
        json={
            "nome": "Notebook Recepcao",
            "codigo": "NOTE-01",
            "localizacao": "Recepcao",
        },
    )
    equipamento = resposta_equipamento.get_json()

    resposta_qr = cliente.get(
        f"/api/equipamentos/{equipamento['id']}/qr-url",
        base_url="https://sistema-ocorrencias.example",
    )
    dados_qr = resposta_qr.get_json()
    url_esperada = (
        "https://sistema-ocorrencias.example"
        f"/equipamentos/code/{equipamento['codigo']}"
    )

    assert resposta_equipamento.status_code == 201
    assert resposta_qr.status_code == 200
    assert dados_qr["urlAbsolutaQr"] == url_esperada
    assert dados_qr["urlApiQr"].startswith(
        "https://api.qrserver.com/v1/create-qr-code/"
    )
    assert f"data={quote_plus(url_esperada)}" in dados_qr["urlApiQr"]


def test_api_busca_equipamento_pelo_codigo(tmp_path):
    web_app.sistema = SistemaOcorrencias(
        arquivo_dados=tmp_path / "web_ocorrencias.json"
    )
    web_app.app.config["TESTING"] = True

    cliente = web_app.app.test_client()
    cliente.post(
        "/api/equipamentos",
        json={
            "nome": "Ar Condicionado",
            "codigo": "AR-09",
            "localizacao": "Laboratorio",
        },
    )

    resposta = cliente.get("/api/equipamentos/code/AR-09")
    equipamento = resposta.get_json()

    assert resposta.status_code == 200
    assert equipamento["nome"] == "Ar Condicionado"
    assert equipamento["codigo"] == "AR-09"
