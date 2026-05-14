import json
import os
from contextlib import contextmanager
from pathlib import Path

from src.models.equipamento import Equipamento
from src.models.ocorrencia import Ocorrencia


class SistemaOcorrencias:
    def __init__(self, arquivo_dados=None):
        self.ocorrencias = []
        self.equipamentos = []
        self.proximo_id = 1
        if arquivo_dados is None:
            # Caminho padrão usado pela aplicação (raiz do projeto).
            self.arquivo_dados = Path(__file__).resolve().parents[2] / "ocorrencias.json"
        else:
            # Permite injetar outro arquivo (ex.: testes com tmp_path).
            self.arquivo_dados = Path(arquivo_dados)
        self.arquivo_lock = self.arquivo_dados.with_suffix(self.arquivo_dados.suffix + ".lock")
        self.carregar_dados()

    def criar_ocorrencia(self, titulo, descricao, equipamentoId=None):
        def _operacao():
            ocorrencia = Ocorrencia(self.proximo_id, titulo, descricao, equipamentoId=equipamentoId)
            self.ocorrencias.append(ocorrencia)
            self.proximo_id += 1
            return ocorrencia
        
        return self._executar_atomicamente(_operacao)

    def listar_ocorrencias(self):
        return self.ocorrencias

    def atualizar_status(self, id, novo_status):
        novo_status_normalizado = self._normalizar_status(novo_status)
        if novo_status_normalizado not in {"aberta", "em andamento", "resolvida"}:
            return False

        def _operacao():
            for o in self.ocorrencias:
                if o.id == id:
                    o.status = novo_status_normalizado
                    return True
            return False
        
        return self._executar_atomicamente(_operacao)

    def atualizar_ocorrencia(self, id, titulo=None, descricao=None, equipamentoId=None):
        def _operacao():
            for o in self.ocorrencias:
                if o.id == id:
                    if titulo is not None:
                        o.titulo = titulo
                    if descricao is not None:
                        o.descricao = descricao
                    if equipamentoId is not None:
                        o.equipamentoId = equipamentoId
                    return True
            return False
        
        return self._executar_atomicamente(_operacao)

    def buscar_ocorrencia_por_id(self, id):
        for o in self.ocorrencias:
            if o.id == id:
                return o
        return None

    def remover_ocorrencia(self, id):
        def _operacao():
            tamanho_antigo = len(self.ocorrencias)
            self.ocorrencias = [
                o for o in self.ocorrencias if o.id != id
            ]
            # Só grava no arquivo se realmente houve alteração.
            if len(self.ocorrencias) != tamanho_antigo:
                return True
            return False
        
        return self._executar_atomicamente(_operacao)

    def salvar_dados(self):
        #Salva dados em memória para o JSON (deve ser chamado dentro de _executar_atomicamente).
        dados = {
            "proximo_id": self.proximo_id,
            "ocorrencias": [ocorrencia.to_dict() for ocorrencia in self.ocorrencias],
        }

        with self.arquivo_dados.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    def carregar_dados(self):
        with self._arquivo_lock_exclusivo():
            if not self.arquivo_dados.exists():
                return

            try:
                with self.arquivo_dados.open("r", encoding="utf-8") as arquivo:
                    dados = json.load(arquivo)

                self.ocorrencias = [
                    Ocorrencia.from_dict(item)
                    for item in dados.get("ocorrencias", [])
                ]
                # Garante que o próximo ID não "ande para trás" mesmo com arquivo editado manualmente.
                self.proximo_id = max(dados.get("proximo_id", 1), self._calcular_proximo_id())
            except (json.JSONDecodeError, OSError, KeyError, TypeError):
                # Se o JSON estiver inválido/corrompido, o sistema inicia limpo para não travar.
                self.ocorrencias = []
                self.proximo_id = 1

    def _calcular_proximo_id(self):
        if not self.ocorrencias:
            return 1

        return max(ocorrencia.id for ocorrencia in self.ocorrencias) + 1

    def _normalizar_status(self, status):
        if not isinstance(status, str):
            return ""

        valor = status.strip().lower()
        if valor == "em_andamento":
            return "em andamento"
        return valor

    def _executar_atomicamente(self, operacao):
        """Padrão read-modify-write atomicamente: relê disco, executa operação, escreve disco.
        
        Isso garante que mesmo com múltiplos processos, cada um tem visão atualizada antes de modificar.
        """
        with self._arquivo_lock_exclusivo():
            self._carregar_dados_unlocked()
            resultado = operacao()
            if resultado is not False:
                self.salvar_dados()
            return resultado

    def _carregar_dados_unlocked(self):
        """Carrega dados sem adquirir lock (deve ser chamado dentro de _arquivo_lock_exclusivo)."""
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

    @contextmanager
    def _arquivo_lock_exclusivo(self):
        self.arquivo_lock.parent.mkdir(parents=True, exist_ok=True)
        with self.arquivo_lock.open("a+b") as lock_file:
            self._bloquear_arquivo(lock_file)
            try:
                yield
            finally:
                self._desbloquear_arquivo(lock_file)

    def _bloquear_arquivo(self, lock_file):
        if os.name == "nt":
            import msvcrt

            lock_file.seek(0)
            if lock_file.tell() == 0:
                lock_file.write(b"0")
                lock_file.flush()
            lock_file.seek(0)
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
            return

        import fcntl

        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)

    def _desbloquear_arquivo(self, lock_file):
        if os.name == "nt":
            import msvcrt

            lock_file.seek(0)
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
            return

        import fcntl

        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

    #métodos de equipamento
    def criar_equipamento(self, nome, codigo, localizacao):
        equipamento = Equipamento(
            self.proximo_id,
            nome,
            codigo,
            localizacao
        )

        self.equipamentos.append(equipamento)
        self.proximo_id += 1
        self.salvar_dados()

        return equipamento

    def listar_equipamentos(self):
        return self.equipamentos

    def buscar_equipamento_por_id(self, id):
        return next(
            (e for e in self.equipamentos if e.id == id),
            None
        )

    def remover_equipamento(self, id):
        def _operacao():
            tamanho_antigo = len(self.equipamentos)
            self.equipamentos = [
                e for e in self.equipamentos if e.id != id
            ]
            if len(self.equipamentos) != tamanho_antigo:
                return True
            return False
        
        return self._executar_atomicamente(_operacao)

    def atualizar_equipamento(self, id, nome=None, codigo=None, localizacao=None):
        def _operacao():
            for e in self.equipamentos:
                if e.id == id:
                    if nome is not None:
                        e.nome = nome
                    if codigo is not None:
                        e.codigo = codigo
                    if localizacao is not None:
                        e.localizacao = localizacao
                        e.localização = localizacao
                    return True
            return False

        return self._executar_atomicamente(_operacao)

    #salvar dados no JSON
    def salvar_dados(self):
        dados = {
            "proximo_id": self.proximo_id,
            "ocorrencias": [
                o.to_dict() for o in self.ocorrencias
            ],
            "equipamentos": [
                e.to_dict() for e in self.equipamentos
            ]
        }

        with self.arquivo_dados.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    #carregar dados de equipamento
    def carregar_dados(self):

        if not self.arquivo_dados.exists():
            self.ocorrencias = []
            self.equipamentos = []
            self.proximo_id = 1
            return

        try:
            with self.arquivo_dados.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            self.ocorrencias = [
                Ocorrencia.from_dict(item)
                for item in dados.get("ocorrencias", [])
            ]

            self.equipamentos = [
                Equipamento.from_dict(item)
                for item in dados.get("equipamentos", [])
            ]

            self.proximo_id = max(
                dados.get("proximo_id", 1),
                self._calcular_proximo_id()
            )

        except (json.JSONDecodeError, OSError, KeyError, TypeError):
            self.ocorrencias = []
            self.equipamentos = []
            self.proximo_id = 1
