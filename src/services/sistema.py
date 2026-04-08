import json
from pathlib import Path

from src.models.ocorrencia import Ocorrencia

class SistemaOcorrencias:
    def __init__(self):
        self.ocorrencias = []
        self.proximo_id = 1
        self.arquivo_dados = Path(__file__).resolve().parents[2] / "ocorrencias.json"
        self.carregar_dados()

    def criar_ocorrencia(self, titulo, descricao):
        ocorrencia = Ocorrencia(self.proximo_id, titulo, descricao)
        self.ocorrencias.append(ocorrencia)
        self.proximo_id += 1
        self.salvar_dados()
        return ocorrencia

    def listar_ocorrencias(self):
        return self.ocorrencias

    def atualizar_status(self, id, novo_status):
        for o in self.ocorrencias:
            if o.id == id:
                o.status = novo_status
                self.salvar_dados()
                return True
        return False

    def buscar_ocorrencia_por_id(self, id):
        for o in self.ocorrencias:
            if o.id == id:
                return o
        return None

    def remover_ocorrencia(self, id):
        tamanho_antigo = len(self.ocorrencias)
        self.ocorrencias = [
            o for o in self.ocorrencias if o.id != id
        ]
        if len(self.ocorrencias) != tamanho_antigo:
            self.salvar_dados()
            return True
        return False

    def salvar_dados(self):
        dados = {
            "proximo_id": self.proximo_id,
            "ocorrencias": [ocorrencia.to_dict() for ocorrencia in self.ocorrencias],
        }

        with self.arquivo_dados.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    def carregar_dados(self):
        if not self.arquivo_dados.exists():
            return

        try:
            with self.arquivo_dados.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            self.ocorrencias = [
                Ocorrencia.from_dict(item)
                for item in dados.get("ocorrencias", [])
            ]
            self.proximo_id = max(dados.get("proximo_id", 1), self._calcular_proximo_id())
        except (json.JSONDecodeError, OSError, KeyError, TypeError):
            self.ocorrencias = []
            self.proximo_id = 1

    def _calcular_proximo_id(self):
        if not self.ocorrencias:
            return 1

        return max(ocorrencia.id for ocorrencia in self.ocorrencias) + 1