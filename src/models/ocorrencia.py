from datetime import datetime

class Ocorrencia:
    def __init__(self, id, titulo, descricao, equipamentoId=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = "aberta"
        self.data_criacao = datetime.now()
        self.data_atualizacao = datetime.now()
        self.equipamentoId = equipamentoId

    def __str__(self):
        return f"{self.id} - {self.titulo} ({self.status})"

    def to_dict(self):
        # Converte para um formato simples de salvar em JSON.
        data = {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "data_criacao": self.data_criacao.isoformat(),
            "data_atualizacao": self.data_atualizacao.isoformat(),
        }
        if self.equipamentoId is not None:
            data["equipamentoId"] = self.equipamentoId
        return data

    @classmethod
    def from_dict(cls, data):
        # Reconstrói o objeto vindo do JSON salvo no disco.
        equipamentoId = data.get("equipamentoId")
        ocorrencia = cls(data["id"], data["titulo"], data["descricao"], equipamentoId=equipamentoId)
        ocorrencia.status = data.get("status", "aberta")

        data_criacao = data.get("data_criacao")
        if data_criacao:
            ocorrencia.data_criacao = datetime.fromisoformat(data_criacao)

        data_atualizacao = data.get("data_atualizacao")
        if data_atualizacao:
            ocorrencia.data_atualizacao = datetime.fromisoformat(
                data_atualizacao
            )

        return ocorrencia