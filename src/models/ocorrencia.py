class Ocorrencia:
    def __init__(self, id, titulo, descricao):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = "aberta"

    def __str__(self):
        return f"{self.id} - {self.titulo} ({self.status})"