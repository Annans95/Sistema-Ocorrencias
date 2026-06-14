import uuid

import pytest

from src.database.conexao import DATABASE_URL, conectar
from src.services.sistema import SistemaOcorrencias


@pytest.fixture()
def sistema_db():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL nao configurada no .env/ambiente")

    return SistemaOcorrencias()


def gerar_sufixo_unico():
    return uuid.uuid4().hex[:8].upper()


def limpar_dados_teste(equipamento_codigo=None, ocorrencia_id=None, ocorrencia_titulo=None):
    if not DATABASE_URL:
        return

    conn = conectar()
    cursor = conn.cursor()

    try:
        if ocorrencia_id is not None:
            cursor.execute("DELETE FROM ocorrencias WHERE id = %s;", (ocorrencia_id,))
        elif ocorrencia_titulo is not None:
            cursor.execute("DELETE FROM ocorrencias WHERE titulo = %s;", (ocorrencia_titulo,))

        if equipamento_codigo is not None:
            cursor.execute("DELETE FROM equipamento WHERE codigo = %s;", (equipamento_codigo,))

        conn.commit()
    finally:
        cursor.close()
        conn.close()


def test_conexao_banco_real():
    assert DATABASE_URL, (
        "DATABASE_URL nao configurada no .env/ambiente. "
        "Configure a conexao para executar os testes reais de banco."
    )

    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT 1;")
        resultado = cursor.fetchone()
        assert resultado == (1,)
    finally:
        cursor.close()
        conn.close()


def test_cadastro_de_equipamento_no_banco(sistema_db):
    sufixo = gerar_sufixo_unico()
    codigo = f"TEST-IMP-{sufixo}"
    nome = f"Impressora Teste {sufixo}"
    localizacao = f"Sala Teste {sufixo}"

    try:
        equipamento = sistema_db.criar_equipamento(nome, codigo, localizacao)

        assert equipamento.id is not None
        assert equipamento.nome == nome
        assert equipamento.codigo == codigo
        assert equipamento.localizacao == localizacao
        assert equipamento.to_dict()["descricao"] == ""

        equipamento_banco = sistema_db.buscar_equipamento_por_codigo(codigo)
        assert equipamento_banco is not None
        assert equipamento_banco.id == equipamento.id
        assert equipamento_banco.nome == nome
        assert equipamento_banco.codigo == codigo
        assert equipamento_banco.localizacao == localizacao
    finally:
        limpar_dados_teste(equipamento_codigo=codigo)


def test_cadastro_de_ocorrencia_no_banco(sistema_db):
    sufixo = gerar_sufixo_unico()
    codigo = f"TEST-EQ-{sufixo}"
    nome = f"Equipamento Base {sufixo}"
    localizacao = f"Almoxarifado {sufixo}"
    titulo = f"TEST-OCORR-{sufixo}"
    descricao = f"Descricao de teste {sufixo}"

    equipamento = None
    ocorrencia = None

    try:
        equipamento = sistema_db.criar_equipamento(nome, codigo, localizacao)
        ocorrencia = sistema_db.criar_ocorrencia(
            titulo,
            descricao,
            equipamentoId=equipamento.id,
        )

        assert ocorrencia.id is not None
        assert ocorrencia.titulo == titulo
        assert ocorrencia.descricao == descricao
        assert ocorrencia.status == "aberta"
        assert ocorrencia.equipamentoId == equipamento.id

        ocorrencia_banco = sistema_db.buscar_ocorrencia_por_id(ocorrencia.id)
        assert ocorrencia_banco is not None
        assert ocorrencia_banco.id == ocorrencia.id
        assert ocorrencia_banco.titulo == titulo
        assert ocorrencia_banco.descricao == descricao
        assert ocorrencia_banco.equipamentoId == equipamento.id
    finally:
        limpar_dados_teste(
            equipamento_codigo=codigo,
            ocorrencia_id=ocorrencia.id if ocorrencia is not None else None,
            ocorrencia_titulo=titulo,
        )
