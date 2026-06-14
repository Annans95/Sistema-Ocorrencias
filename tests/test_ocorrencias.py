import uuid

import pytest

from src.database.conexao import DATABASE_URL, conectar
from src.services.sistema import SistemaOcorrencias


def _sufixo_unico():
    return uuid.uuid4().hex[:8].upper()


def _limpar_equipamento_e_ocorrencias(codigo, titulo=None):
    if not DATABASE_URL:
        return

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM ocorrencias WHERE equipamento_id IN (SELECT id FROM equipamento WHERE codigo = %s);",
            (codigo,),
        )
        if titulo is not None:
            cursor.execute("DELETE FROM ocorrencias WHERE titulo = %s;", (titulo,))
        cursor.execute("DELETE FROM equipamento WHERE codigo = %s;", (codigo,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def test_criar_ocorrencia_no_banco():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL nao configurada no .env/ambiente")

    sistema = SistemaOcorrencias()
    sufixo = _sufixo_unico()
    codigo = f"EQ-TEST-{sufixo}"
    titulo = f"TEST-OCORR-{sufixo}"
    equipamento = None

    try:
        equipamento = sistema.criar_equipamento(
            f"Equipamento Teste {sufixo}",
            codigo,
            "Laboratorio",
        )
        ocorrencia = sistema.criar_ocorrencia(titulo, "Descricao", equipamentoId=equipamento.id)

        assert ocorrencia.titulo == titulo
        assert ocorrencia.status == "aberta"
        assert ocorrencia.equipamentoId == equipamento.id

        ocorrencia_banco = sistema.buscar_ocorrencia_por_id(ocorrencia.id)
        assert ocorrencia_banco is not None
        assert ocorrencia_banco.titulo == titulo
        assert ocorrencia_banco.equipamentoId == equipamento.id
    finally:
        _limpar_equipamento_e_ocorrencias(codigo, titulo=titulo)


def test_atualizar_status_quando_encontra_no_banco():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL nao configurada no .env/ambiente")

    sistema = SistemaOcorrencias()
    sufixo = _sufixo_unico()
    codigo = f"EQ-STATUS-{sufixo}"
    titulo = f"TEST-STATUS-{sufixo}"
    equipamento = None
    ocorrencia = None

    try:
        equipamento = sistema.criar_equipamento(
            f"Equipamento Status {sufixo}",
            codigo,
            "Sala 1",
        )
        ocorrencia = sistema.criar_ocorrencia(titulo, "Descricao", equipamentoId=equipamento.id)

        atualizado = sistema.atualizar_status(ocorrencia.id, "resolvida")

        assert atualizado is True
        ocorrencia_atualizada = sistema.buscar_ocorrencia_por_id(ocorrencia.id)
        assert ocorrencia_atualizada.status == "resolvida"
    finally:
        _limpar_equipamento_e_ocorrencias(codigo, titulo=titulo)


def test_atualizar_status_quando_nao_encontra_no_banco():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL nao configurada no .env/ambiente")

    sistema = SistemaOcorrencias()

    atualizado = sistema.atualizar_status(999999, "resolvida")

    assert atualizado is False


def test_buscar_ocorrencia_por_id_no_banco():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL nao configurada no .env/ambiente")

    sistema = SistemaOcorrencias()
    sufixo = _sufixo_unico()
    codigo = f"EQ-BUSCA-{sufixo}"
    titulo = f"TEST-BUSCA-{sufixo}"

    try:
        equipamento = sistema.criar_equipamento(
            f"Equipamento Busca {sufixo}",
            codigo,
            "Sala 2",
        )
        ocorrencia = sistema.criar_ocorrencia(titulo, "Descricao", equipamentoId=equipamento.id)

        buscada = sistema.buscar_ocorrencia_por_id(ocorrencia.id)

        assert buscada is not None
        assert buscada.id == ocorrencia.id
        assert buscada.titulo == titulo
    finally:
        _limpar_equipamento_e_ocorrencias(codigo, titulo=titulo)


def test_remover_ocorrencia_no_banco():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL nao configurada no .env/ambiente")

    sistema = SistemaOcorrencias()
    sufixo = _sufixo_unico()
    codigo = f"EQ-REMOVE-{sufixo}"
    titulo = f"TEST-REMOVE-{sufixo}"

    try:
        equipamento = sistema.criar_equipamento(
            f"Equipamento Remove {sufixo}",
            codigo,
            "Sala 3",
        )
        ocorrencia = sistema.criar_ocorrencia(titulo, "Descricao", equipamentoId=equipamento.id)

        removida = sistema.remover_ocorrencia(ocorrencia.id)

        assert removida is True
        assert sistema.buscar_ocorrencia_por_id(ocorrencia.id) is None
    finally:
        _limpar_equipamento_e_ocorrencias(codigo, titulo=titulo)


def test_persistencia_no_banco_entre_instancias():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL nao configurada no .env/ambiente")

    sistema = SistemaOcorrencias()
    sufixo = _sufixo_unico()
    codigo = f"EQ-PERSIST-{sufixo}"
    titulo = f"TEST-PERSIST-{sufixo}"

    try:
        equipamento = sistema.criar_equipamento(
            f"Equipamento Persistencia {sufixo}",
            codigo,
            "Sala 4",
        )
        ocorrencia = sistema.criar_ocorrencia(titulo, "Descricao", equipamentoId=equipamento.id)

        novo_sistema = SistemaOcorrencias()
        ocorrencia_recarregada = novo_sistema.buscar_ocorrencia_por_id(ocorrencia.id)

        assert ocorrencia_recarregada is not None
        assert ocorrencia_recarregada.titulo == titulo
        assert ocorrencia_recarregada.status == "aberta"
    finally:
        _limpar_equipamento_e_ocorrencias(codigo, titulo=titulo)