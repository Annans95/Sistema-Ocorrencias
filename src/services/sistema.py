from src.models.ocorrencia import Ocorrencia

class SistemaOcorrencias:
    def __init__(self):
        self.ocorrencias = []
        self.proximo_id = 1

    def criar_ocorrencia(self, titulo, descricao):
        ocorrencia = Ocorrencia(self.proximo_id, titulo, descricao)
        self.ocorrencias.append(ocorrencia)
        self.proximo_id += 1
