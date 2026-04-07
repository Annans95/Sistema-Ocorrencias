from src.services.sistema import SistemaOcorrencias

def test_criar_ocorrencia():
    sistema = SistemaOcorrencias()
    sistema.criar_ocorrencia("Teste", "Descrição")

    assert len(sistema.ocorrencias) == 1
    assert sistema.ocorrencias[0].titulo == "Teste"


def test_status_inicial():
    sistema = SistemaOcorrencias()
    sistema.criar_ocorrencia("Teste", "Descrição")

    assert sistema.ocorrencias[0].status == "aberta"


def test_atualizar_status():
    sistema = SistemaOcorrencias()
    sistema.criar_ocorrencia("Teste", "Descrição")

    sistema.atualizar_status(1, "resolvida")

    assert sistema.ocorrencias[0].status == "resolvida"


def test_buscar_ocorrencia():
    sistema = SistemaOcorrencias()
    sistema.criar_ocorrencia("Teste", "Descrição")

    o = sistema.buscar_ocorrencia_por_id(1)

    assert o is not None
    assert o.id == 1