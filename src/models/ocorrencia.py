from datetime import datetime


class Ocorrencia:
    def __init__(self, id, titulo, descricao):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = "aberta"
        self.data_criacao = datetime.now()

    def __str__(self):
        return f"{self.id} - {self.titulo} ({self.status})"

    def to_dict(self):
        # Converte para um formato simples de salvar em JSON.
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "data_criacao": self.data_criacao.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        # Reconstrói o objeto vindo do JSON salvo no disco.
        ocorrencia = cls(data["id"], data["titulo"], data["descricao"])
        ocorrencia.status = data.get("status", "aberta")

        data_criacao = data.get("data_criacao")
        if data_criacao:
            ocorrencia.data_criacao = datetime.fromisoformat(data_criacao)

        return ocorrencia