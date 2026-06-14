from src.models.equipamento import Equipamento
from src.models.ocorrencia import Ocorrencia
from src.database.conexao import conectar


class SistemaOcorrencias:
    def __init__(self):
        self.ocorrencias = []
        self.equipamentos = []
        self.carregar_dados()

    def criar_ocorrencia(self, titulo, descricao, equipamentoId=None):
        
        conn = conectar() #Abre a conexão
        cursor = conn.cursor() #objeto que executa os comandos SQL

        cursor.execute("""
            INSERT INTO ocorrencias 
            (titulo, descricao, status, equipamento_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id, titulo, descricao, status,
            data_criacao, data_atualizacao, equipamento_id;
        """, 
        (
            titulo, 
            descricao, 
            "aberta", 
            equipamentoId
        ))
                       
        linha = cursor.fetchone() #captura dos dados retornados pelo RETURNING

        conn.commit() #salva permanentemente a alteração no bd

        cursor.close()
        conn.close()

        #Mapeamento para Objeto
        ocorrencia = Ocorrencia(
            linha[0],
            linha[1],
            linha[2],
            equipamentoId=linha[6] if len(linha) > 6 else None
        )

        ocorrencia.status = linha[3]
        ocorrencia.data_criacao = linha[4]
        ocorrencia.data_atualizacao = linha[5]

        return ocorrencia

    def listar_ocorrencias(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT id, titulo, descricao, status,
                       data_criacao, data_atualizacao, equipamento_id
                       FROM ocorrencias
                       ORDER BY id;
                       """)
        linhas = cursor.fetchall()

        ocorrencias = []

        for linha in linhas:
            ocorrencia = Ocorrencia(
                linha[0],
                linha[1],
                linha[2],
                equipamentoId=linha[6] if len(linha) > 6 else None
            )

            ocorrencia.status = linha[3]
            ocorrencia.data_criacao = linha[4]
            ocorrencia.data_atualizacao = linha[5]

            ocorrencias.append(ocorrencia)

        cursor.close()
        conn.close()

        return ocorrencias

    def atualizar_status(self, id, novo_status):
        novo_status_normalizado = self._normalizar_status(novo_status)
        if novo_status_normalizado not in {"aberta", "em andamento", "resolvida"}:
            return False

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE ocorrencias
                       SET status = %s,
                       data_atualizacao = CURRENT_TIMESTAMP
                       WHERE id = %s
                       RETURNING id;
                       """,
                       (
                        novo_status_normalizado,
                        id
                       ))
        resultado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return resultado is not None

    def atualizar_ocorrencia(self, id, titulo=None, descricao=None, equipamentoId=None):
        
        campos = []
        valores = []

        if titulo is not None:
            campos.append("titulo = %s")
            valores.append(titulo)
        
        if descricao is not None:
            campos.append("descricao = %s")
            valores.append(descricao)
        
        if equipamentoId is not None:
            campos.append("equipamento_id = %s")
            valores.append(equipamentoId)
        
        if not campos:
            return False
        
        campos.append("data_atualizacao = CURRENT_TIMESTAMP")

        valores.append(id)

        query = f"""
            UPDATE ocorrencias
            SET {", ".join(campos)}
            WHERE id = %s
            RETURNING id;
        """
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(query, valores)

        resultado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return resultado is not None
        
    def buscar_ocorrencia_por_id(self, id):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, titulo, descricao, status,
                data_criacao, data_atualizacao,
                equipamento_id
        FROM ocorrencias
        WHERE id = %s;
                       """,(id,))
        
        linha = cursor.fetchone()

        cursor.close()
        conn.close()

        if linha is None:
            return None
        
        ocorrencia = Ocorrencia(
            linha[0],
            linha[1],
            linha[2],
            equipamentoId=linha[6]
        )

        ocorrencia.status = linha[3]
        ocorrencia.data_criacao = linha[4]
        ocorrencia.data_atualizacao = linha[5]

        return ocorrencia

    def remover_ocorrencia(self, id):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
                    DELETE FROM ocorrencias
                    WHERE id = %s
                    RETURNING id;
                       """, (id,))
        
        resultado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return resultado is not None
    def _normalizar_status(self, status):
        if not isinstance(status, str):
            return ""

        valor = status.strip().lower()
        if valor == "em_andamento":
            return "em andamento"
        return valor

    def carregar_dados(self):
        self.ocorrencias = self.listar_ocorrencias()
        self.equipamentos = self.listar_equipamentos()

    #métodos de equipamento
    def criar_equipamento(self, nome, codigo, localizacao):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO equipamento
            (
                nome,
                codigo,
                localizacao
            )
            VALUES (%s, %s, %s)
            RETURNING id, codigo, nome, descricao,
                    localizacao, data_cadastro, ativo;
        """,
        (
            nome,
            codigo,
            localizacao
        ))

        linha = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        equipamento = Equipamento(
            linha[0],
            linha[2],
            linha[1],
            linha[4]
        )

        equipamento.descricao = linha[3] or ""
        equipamento.data_cadastro = linha[5]
        equipamento.ativo = linha[6]

        return equipamento

    def listar_equipamentos(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome, codigo, descricao,
                    localizacao, data_cadastro, ativo
            FROM equipamento
            WHERE ativo = TRUE
            ORDER BY id;
        """)

        linhas = cursor.fetchall()

        equipamentos = []

        for linha in linhas:
            equipamento = Equipamento(
                linha[0],
                linha[1],
                linha[2],
                linha[4]
            )

            equipamento.descricao = linha[3]
            equipamento.data_cadastro = linha[5]
            equipamento.ativo = linha[6]

            equipamentos.append(equipamento)

        cursor.close()
        conn.close()

        return equipamentos

    def buscar_equipamento_por_id(self, id):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, codigo, nome, descricao,
                localizacao, data_cadastro, ativo
            FROM equipamento
            WHERE id = %s
            AND ativo = TRUE;
            """, (id,))

        linha = cursor.fetchone()

        cursor.close()
        conn.close()

        if linha is None:
            return None
        
        equipamento = Equipamento(
            linha[0],
            linha[2],
            linha[1],
            linha[4]
        )

        equipamento.descricao = linha[3] or ""
        equipamento.data_cadastro = linha[5]
        equipamento.ativo = linha[6]

        return equipamento

    def remover_equipamento(self, id):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE equipamento
            SET ativo = FALSE
            WHERE id = %s
            RETURNING id;
            """, (id,))

        resultado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return resultado is not None

    def atualizar_equipamento(self, id, nome=None, codigo=None, localizacao=None):
        campos = []
        valores = []

        if nome is not None:
            campos.append("nome = %s")
            valores.append(nome)
        
        if codigo is not None:
            campos.append("codigo = %s")
            valores.append(codigo)
        
        if localizacao is not None:
            campos.append("localizacao = %s")
            valores.append(localizacao)
        
        if not campos:
            return False
        
        valores.append(id)

        query = f"""
            UPDATE equipamento
            SET {", ".join(campos)}
            WHERE id = %s
            RETURNING id;
        """

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(query, valores)

        resultado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return resultado is not None

    def buscar_equipamento_por_codigo(self, codigo):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, codigo, nome, descricao,
                localizacao, data_cadastro, ativo
            FROM equipamento
            WHERE codigo = %s
            AND ativo = TRUE;
        """, (codigo,))

        linha = cursor.fetchone()

        cursor.close()
        conn.close()

        if linha is None:
            return None

        equipamento = Equipamento(
            linha[0],
            linha[2],
            linha[1],
            linha[4]
        )

        equipamento.descricao = linha[3] or ""
        equipamento.data_cadastro = linha[5]
        equipamento.ativo = linha[6]

        return equipamento
