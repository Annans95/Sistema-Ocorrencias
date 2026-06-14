import uuid
from urllib.parse import quote_plus

import pytest

from src.database.conexao import DATABASE_URL, conectar
from src.services.sistema import SistemaOcorrencias


def _sufixo_unico():
    return uuid.uuid4().hex[:8].upper()


def _limpar_equipamento(codigo):
    if not DATABASE_URL:
        return

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM equipamento WHERE codigo = %s;", (codigo,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def _importar_web_app():
    try:
        from src.web import app as web_app
    except Exception as erro:
        pytest.skip(f"Nao foi possivel importar a web app com o banco atual: {erro}")
    return web_app


def test_api_qr_equipamento_retorna_url_da_api_publica(tmp_path):
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL nao configurada no .env/ambiente")

    try:
        conn = conectar()
        conn.close()
    except Exception as erro:
        pytest.skip(f"Banco indisponivel para importar a web app: {erro}")

    web_app = _importar_web_app()
    web_app.sistema = SistemaOcorrencias()
    web_app.app.config["TESTING"] = True

    cliente = web_app.app.test_client()
    sufixo = _sufixo_unico()
    codigo = f"NOTE-TEST-{sufixo}"
    resposta_equipamento = cliente.post(
        "/api/equipamentos",
        json={
            "nome": f"Notebook Recepcao {sufixo}",
            "codigo": codigo,
            "localizacao": "Recepcao",
        },
    )
    equipamento = resposta_equipamento.get_json()

    try:
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
    finally:
        _limpar_equipamento(codigo)


def test_api_busca_equipamento_pelo_codigo():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL nao configurada no .env/ambiente")

    try:
        conn = conectar()
        conn.close()
    except Exception as erro:
        pytest.skip(f"Banco indisponivel para importar a web app: {erro}")

    web_app = _importar_web_app()
    web_app.sistema = SistemaOcorrencias()
    web_app.app.config["TESTING"] = True

    cliente = web_app.app.test_client()
    sufixo = _sufixo_unico()
    codigo = f"AR-TEST-{sufixo}"
    cliente.post(
        "/api/equipamentos",
        json={
            "nome": f"Ar Condicionado {sufixo}",
            "codigo": codigo,
            "localizacao": "Laboratorio",
        },
    )

    try:
        resposta = cliente.get(f"/api/equipamentos/code/{codigo}")
        equipamento = resposta.get_json()

        assert resposta.status_code == 200
        assert equipamento["nome"].startswith("Ar Condicionado")
        assert equipamento["codigo"] == codigo
    finally:
        _limpar_equipamento(codigo)
