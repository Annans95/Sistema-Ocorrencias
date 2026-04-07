from src.models.ocorrencia import Ocorrencia

class SistemaOcorrencias:
    def __init__(self):
        self.ocorrencias = []
        self.proximo_id = 1

    def criar_ocorrencia(self, titulo, descricao):
        ocorrencia = Ocorrencia(self.proximo_id, titulo, descricao)
        self.ocorrencias.append(ocorrencia)
        self.proximo_id += 1

    def listar_ocorrencias(self):
        return self.ocorrencias

    def atualizar_status(self, id, novo_status):
        for o in self.ocorrencias:
            if o.id == id:
                o.status = novo_status
                return True
        return False

    def buscar_ocorrencia_por_id(self, id):
        for o in self.ocorrencias:
            if o.id == id:
                return o
        return None