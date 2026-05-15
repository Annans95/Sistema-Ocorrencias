#rotas flask
from pathlib import Path
from threading import Lock
from urllib.parse import quote_plus
import sys

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from flask import Flask, render_template, jsonify, request
from src.services.sistema import SistemaOcorrencias

#Cria aplicação Flask
app = Flask(__name__)

#Cria instância do sistema
sistema = SistemaOcorrencias()
sistema_lock = Lock()


def _status_para_api(status: str) -> str:
    if status == "em andamento":
        return "em_andamento"
    return status


def _status_para_servico(status: str) -> str:
    if status == "em_andamento":
        return "em andamento"
    return status


def _ocorrencia_para_json(ocorrencia):
    dados = ocorrencia.to_dict()
    dados["status"] = _status_para_api(dados.get("status", ""))
    return dados


def gerar_url_api_qr(url_destino: str, tamanho: str = "110x110") -> str:
    dados_qr = quote_plus(url_destino)
    return (
        "https://api.qrserver.com/v1/create-qr-code/"
        f"?size={tamanho}&data={dados_qr}"
    )

#Cria URL
@app.route("/")
#lógica da página
def index():
    return render_template("index.html")

@app.route("/api/ocorrencias")
def api_ocorrencias():
    with sistema_lock:
        sistema.carregar_dados()
        return jsonify([
            _ocorrencia_para_json(o) for o in sistema.listar_ocorrencias()
        ])


@app.route("/api/ocorrencias", methods=["POST"])
def criar_ocorrencia_api():
    payload = request.get_json(silent=True) or {}
    titulo = (payload.get("titulo") or "").strip()
    descricao = (payload.get("descricao") or "").strip()
    equipamentoId = payload.get("equipamentoId")

    if not titulo or not descricao:
        return jsonify({"erro": "titulo e descricao sao obrigatorios"}), 400

    # Converte equipamentoId para int se fornecido e válido
    if equipamentoId:
        try:
            equipamentoId = int(equipamentoId)
        except (ValueError, TypeError):
            equipamentoId = None

    with sistema_lock:
        ocorrencia = sistema.criar_ocorrencia(titulo, descricao, equipamentoId=equipamentoId)
        return jsonify(_ocorrencia_para_json(ocorrencia)), 201


@app.route("/api/ocorrencias/<int:occ_id>/status", methods=["PUT"])
def atualizar_status_api(occ_id):
    payload = request.get_json(silent=True) or {}
    status_api = payload.get("status")
    status_servico = _status_para_servico(status_api)

    if status_servico not in {"aberta", "em andamento", "resolvida"}:
        return jsonify({"erro": "status invalido"}), 400

    with sistema_lock:
        if not sistema.atualizar_status(occ_id, status_servico):
            return jsonify({"erro": "ocorrencia nao encontrada"}), 404

        ocorrencia = sistema.buscar_ocorrencia_por_id(occ_id)
        return jsonify(_ocorrencia_para_json(ocorrencia))


@app.route("/api/ocorrencias/<int:occ_id>", methods=["PUT"])
def atualizar_ocorrencia_api(occ_id):
    payload = request.get_json(silent=True) or {}
    titulo = payload.get("titulo")
    descricao = payload.get("descricao")
    equipamentoId = payload.get("equipamentoId")

    if titulo is not None:
        titulo = str(titulo).strip()
    if descricao is not None:
        descricao = str(descricao).strip()

    if titulo == "" or descricao == "":
        return jsonify({"erro": "titulo e descricao nao podem ser vazios"}), 400

    # Converte equipamentoId para int se fornecido e válido
    if equipamentoId:
        try:
            equipamentoId = int(equipamentoId)
        except (ValueError, TypeError):
            equipamentoId = None

    with sistema_lock:
        if not sistema.atualizar_ocorrencia(occ_id, titulo=titulo, descricao=descricao, equipamentoId=equipamentoId):
            return jsonify({"erro": "ocorrencia nao encontrada"}), 404

        ocorrencia = sistema.buscar_ocorrencia_por_id(occ_id)
        return jsonify(_ocorrencia_para_json(ocorrencia))


@app.route("/api/ocorrencias/<int:occ_id>", methods=["DELETE"])
def excluir_ocorrencia_api(occ_id):
    with sistema_lock:
        if not sistema.remover_ocorrencia(occ_id):
            return jsonify({"erro": "ocorrencia nao encontrada"}), 404
        return jsonify({"ok": True})

@app.route("/api/equipamentos", methods=["GET"])
def listar_equipamentos():
    with sistema_lock:
        sistema.carregar_dados()
        return jsonify([
            e.to_dict() for e in sistema.listar_equipamentos()
        ])

@app.route("/api/equipamentos", methods=["POST"])
def criar_equipamento():
    payload = request.get_json() or {}

    nome = payload.get("nome", "").strip()
    codigo = payload.get("codigo", "").strip()
    localizacao = payload.get("localizacao", "").strip()

    if not nome or not codigo or not localizacao:
        return jsonify({"erro": "campos obrigatorios"}), 400

    with sistema_lock:
        eq = sistema.criar_equipamento(nome, codigo, localizacao)
        return jsonify(eq.to_dict()), 201


@app.route("/api/equipamentos/<int:eq_id>", methods=["GET", "PUT", "DELETE"])
def equipamento_api(eq_id):
    if request.method == "GET":
        with sistema_lock:
            eq = sistema.buscar_equipamento_por_id(eq_id)
            if not eq:
                return jsonify({"erro": "equipamento nao encontrado"}), 404
            return jsonify(eq.to_dict())

    if request.method == "PUT":
        payload = request.get_json() or {}
        nome = payload.get("nome")
        codigo = payload.get("codigo")
        localizacao = payload.get("localizacao")

        if nome is not None:
            nome = str(nome).strip()
        if codigo is not None:
            codigo = str(codigo).strip()
        if localizacao is not None:
            localizacao = str(localizacao).strip()

        with sistema_lock:
            if not sistema.atualizar_equipamento(eq_id, nome=nome, codigo=codigo, localizacao=localizacao):
                return jsonify({"erro": "equipamento nao encontrado"}), 404

            eq = sistema.buscar_equipamento_por_id(eq_id)
            return jsonify(eq.to_dict())

    with sistema_lock:
        if not sistema.remover_equipamento(eq_id):
            return jsonify({"erro": "equipamento nao encontrado"}), 404
        return jsonify({"ok": True})


@app.route("/api/equipamentos/code/<codigo>", methods=["GET"])
def obter_equipamento_por_codigo(codigo):
    with sistema_lock:
        # Busca por codigo textual com correspondencia exata.
        eq = next((e for e in sistema.listar_equipamentos() if e.codigo == codigo), None)
        if not eq:
            return jsonify({"erro": "equipamento nao encontrado"}), 404
        return jsonify(eq.to_dict())


@app.route("/api/equipamentos/<int:eq_id>/url-qr", methods=["GET"])
@app.route("/api/equipamentos/<int:eq_id>/qr-url", methods=["GET"])
def obter_url_qr_equipamento(eq_id):
    """Retorna o caminho e a URL absoluta do equipamento para gerar QR code."""
    with sistema_lock:
        eq = sistema.buscar_equipamento_por_id(eq_id)
        if not eq:
            return jsonify({"erro": "equipamento nao encontrado"}), 404
        caminhoQr = f"/equipamentos/code/{eq.codigo}"
        urlAbsolutaQr = request.host_url.rstrip("/") + caminhoQr
        return jsonify({
            "caminhoQr": caminhoQr,
            "urlAbsolutaQr": urlAbsolutaQr,
            "urlApiQr": gerar_url_api_qr(urlAbsolutaQr),
            "codigo": eq.codigo,
        })


@app.route('/api/reload', methods=['POST'])
def reload_data_api():
    """Recarrega os dados do arquivo JSON em tempo de execução (útil após edição manual)."""
    with sistema_lock:
        try:
            sistema.carregar_dados()
            return jsonify({"ok": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500


# Serve a mesma SPA para rotas de deep-link de equipamento (QR codes apontam aqui)
@app.route('/equipamentos', strict_slashes=False)
def pagina_equipamentos_raiz():
    return render_template('index.html')

@app.route('/equipamentos/code/<codigo>', strict_slashes=False)
def pagina_equipamentos_por_codigo(codigo):
    return render_template('index.html')

@app.route('/equipamentos/<path:caminhoCompleto>', strict_slashes=False)
def pagina_equipamento(caminhoCompleto):
    return render_template('index.html')

#inicia servidor
if __name__ == "__main__":
    app.run(debug=True, port=5003, use_reloader=False)
