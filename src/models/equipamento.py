
class Equipamento:
    def __init__(self, id, nome, codigo, localizacao):
        self.id = id
        self.nome = nome
        self.codigo = codigo
        self._localizacao = localizacao

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
        # Converte para um formato simples de salvar em JSON.
        return {
            "id": self.id,
            "nome": self.nome,
            "codigo": self.codigo,
            "localizacao": self.localizacao
        }
    @classmethod
    def from_dict(cls, data):
        # Reconstrói o objeto vindo do JSON salvo no disco.
        localizacao = data.get("localizacao", data.get("localização"))
        return cls(
            data["id"],
            data["nome"],
            data["codigo"],
            localizacao
        )