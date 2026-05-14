
class Equipamento:
    def __init__(self, id, nome, codigo, localização):
        self.id = id
        self.nome = nome
        self.codigo = codigo
        self.localização = localização

    def to_dict(self):
        # Converte para um formato simples de salvar em JSON.
        return {
            "id": self.id,
            "nome": self.nome,
            "codigo": self.codigo,
            "localizacao": self.localização
        }
    @classmethod
    def from_dict(cls, data):
        # Reconstrói o objeto vindo do JSON salvo no disco.
        return cls(
            data["id"],
            data["nome"],
            data["codigo"],
            data["localizacao"]
        )