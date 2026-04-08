from src.services.sistema import SistemaOcorrencias


def criar_sistema_tmp(tmp_path):
    arquivo = tmp_path / "ocorrencias_test.json"
    return SistemaOcorrencias(arquivo_dados=arquivo)


def test_criar_ocorrencia(tmp_path):
    sistema = criar_sistema_tmp(tmp_path)
    sistema.criar_ocorrencia("Teste", "Descricao")

    assert len(sistema.ocorrencias) == 1
    assert sistema.ocorrencias[0].titulo == "Teste"
    assert sistema.ocorrencias[0].status == "aberta"


def test_atualizar_status_quando_encontra(tmp_path):
    sistema = criar_sistema_tmp(tmp_path)
    sistema.criar_ocorrencia("Teste", "Descricao")

    atualizado = sistema.atualizar_status(1, "resolvida")

    assert atualizado is True
    assert sistema.ocorrencias[0].status == "resolvida"


def test_atualizar_status_quando_nao_encontra(tmp_path):
    sistema = criar_sistema_tmp(tmp_path)

    atualizado = sistema.atualizar_status(999, "resolvida")

    assert atualizado is False


def test_buscar_ocorrencia_por_id(tmp_path):
    sistema = criar_sistema_tmp(tmp_path)
    sistema.criar_ocorrencia("Teste", "Descricao")

    ocorrencia = sistema.buscar_ocorrencia_por_id(1)

    assert ocorrencia is not None
    assert ocorrencia.id == 1


def test_remover_ocorrencia(tmp_path):
    sistema = criar_sistema_tmp(tmp_path)
    sistema.criar_ocorrencia("Primeira", "Descricao 1")
    sistema.criar_ocorrencia("Segunda", "Descricao 2")

    removida = sistema.remover_ocorrencia(1)

    assert removida is True
    assert len(sistema.ocorrencias) == 1
    assert sistema.ocorrencias[0].id == 2


def test_persistencia_json_entre_instancias(tmp_path):
    arquivo = tmp_path / "persistencia.json"
    sistema = SistemaOcorrencias(arquivo_dados=arquivo)
    sistema.criar_ocorrencia("Ocorrencia Persistida", "Descricao Persistida")
    sistema.atualizar_status(1, "em andamento")

    novo_sistema = SistemaOcorrencias(arquivo_dados=arquivo)
    ocorrencia = novo_sistema.buscar_ocorrencia_por_id(1)

    assert ocorrencia is not None
    assert ocorrencia.titulo == "Ocorrencia Persistida"
    assert ocorrencia.status == "em andamento"
    assert novo_sistema.proximo_id == 2