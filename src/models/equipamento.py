from datetime import datetime

class Equipamento:
    def __init__(self, id, nome, codigo, localizacao, descricao="", data_cadastro=None, ativo=True):
        self.id = id
        self.nome = nome
        self.codigo = codigo
        self.descricao = descricao
        self._localizacao = localizacao
        self.data_cadastro = data_cadastro or datetime.now()
        self.ativo = ativo

    @property
    def localizacao(self):
        return self._localizacao

    @localizacao.setter
    def localizacao(self, valor):
        self._localizacao = valor

    @property
    def localização(self):
        return self._localizacao

    @localização.setter
    def localização(self, valor):
        self._localizacao = valor

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "codigo": self.codigo,
            "descricao": self.descricao or "",
            "localizacao": self.localizacao,
            "data_cadastro": self.data_cadastro.isoformat(),
            "ativo": self.ativo
        }

    @classmethod
    def from_dict(cls, data):
        localizacao = data.get("localizacao", data.get("localização"))

        data_cadastro = data.get("data_cadastro")
        if data_cadastro:
            data_cadastro = datetime.fromisoformat(data_cadastro)

        return cls(
            data["id"],
            data["nome"],
            data["codigo"],
            localizacao,
            descricao=data.get("descricao", ""),
            data_cadastro=data_cadastro,
            ativo=data.get("ativo", True)
        )