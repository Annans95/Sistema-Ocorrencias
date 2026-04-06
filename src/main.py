from src.services.sistema import SistemaOcorrencias

sistema = SistemaOcorrencias()

sistema.criar_ocorrencia(
    "Erro no sistema", "Sistema travando")

for o in sistema.ocorrencias:
    print(o)