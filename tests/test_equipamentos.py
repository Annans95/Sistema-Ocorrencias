from src.services.sistema import SistemaOcorrencias


def test_criar_equipamento_e_vincular_ocorrencia_com_persistencia(tmp_path):
    arquivo = tmp_path / "equipamentos.json"
    sistema = SistemaOcorrencias(arquivo_dados=arquivo)

    equipamento = sistema.criar_equipamento(
        "Impressora Financeiro",
        "IMP-001",
        "Sala 2",
    )
    ocorrencia = sistema.criar_ocorrencia(
        "Papel atolado",
        "Equipamento nao imprime",
        equipamentoId=equipamento.id,
    )

    novo_sistema = SistemaOcorrencias(arquivo_dados=arquivo)
    equipamento_salvo = novo_sistema.buscar_equipamento_por_id(equipamento.id)
    ocorrencia_salva = novo_sistema.buscar_ocorrencia_por_id(ocorrencia.id)

    assert equipamento_salvo is not None
    assert equipamento_salvo.nome == "Impressora Financeiro"
    assert ocorrencia_salva is not None
    assert ocorrencia_salva.equipamentoId == equipamento.id
    assert novo_sistema.proximo_id == 3


def test_atualizar_e_remover_equipamento(tmp_path):
    sistema = SistemaOcorrencias(arquivo_dados=tmp_path / "equipamentos.json")
    equipamento = sistema.criar_equipamento("Projetor", "PROJ-01", "Auditorio")

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
