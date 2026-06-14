import uuid

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
        cursor.execute("DELETE FROM ocorrencias WHERE equipamento_id IN (SELECT id FROM equipamento WHERE codigo = %s);", (codigo,))
        cursor.execute("DELETE FROM equipamento WHERE codigo = %s;", (codigo,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def test_criar_equipamento_e_vincular_ocorrencia_no_banco():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL nao configurada no .env/ambiente")

    sistema = SistemaOcorrencias()
    sufixo = _sufixo_unico()
    codigo = f"IMP-TEST-{sufixo}"
    nome = f"Impressora Financeiro {sufixo}"
    localizacao = "Sala 2"

    equipamento = None
    ocorrencia = None

    try:
        equipamento = sistema.criar_equipamento(nome, codigo, localizacao)
        ocorrencia = sistema.criar_ocorrencia(
            "Papel atolado",
            "Equipamento nao imprime",
            equipamentoId=equipamento.id,
        )

        equipamento_salvo = sistema.buscar_equipamento_por_id(equipamento.id)
        ocorrencia_salva = sistema.buscar_ocorrencia_por_id(ocorrencia.id)

        assert equipamento_salvo is not None
        assert equipamento_salvo.nome == nome
        assert equipamento_salvo.codigo == codigo
        assert ocorrencia_salva is not None
        assert ocorrencia_salva.equipamentoId == equipamento.id
    finally:
        _limpar_equipamento(codigo)


def test_atualizar_e_remover_equipamento_no_banco():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL nao configurada no .env/ambiente")

    sistema = SistemaOcorrencias()
    sufixo = _sufixo_unico()
    codigo = f"PROJ-TEST-{sufixo}"
    equipamento = None

    try:
        equipamento = sistema.criar_equipamento("Projetor", codigo, "Auditorio")

        atualizado = sistema.atualizar_equipamento(
            equipamento.id,
            nome="Projetor principal",
            localizacao="Sala de reuniao",
        )
        equipamento_atualizado = sistema.buscar_equipamento_por_id(equipamento.id)

        assert atualizado is True
        assert equipamento_atualizado.nome == "Projetor principal"
        assert equipamento_atualizado.localizacao == "Sala de reuniao"
        assert sistema.remover_equipamento(equipamento.id) is True
        assert sistema.buscar_equipamento_por_id(equipamento.id) is None
    finally:
        _limpar_equipamento(codigo)
