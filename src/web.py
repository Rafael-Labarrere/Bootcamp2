"""TaskTracker - Interface web local (usa somente a biblioteca padrão).

Uso:  python src/web.py   ->  abre http://127.0.0.1:8000 no navegador.
Reaproveita a lista de tarefas e a persistência em JSON do main.py.
"""

import json
import os
import re
import threading
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import main as core  # tarefas, carregar_tarefas() e salvar_tarefas()

HOST = os.environ.get("HOST", "127.0.0.1")  # no Docker use HOST=0.0.0.0
PORT = int(os.environ.get("PORT", "8000"))
PASTA_STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
PRIORIDADES = {"alta": "Alta", "média": "Média", "media": "Média", "baixa": "Baixa"}

STATUS = ("Pendente", "Em andamento", "Concluída")

trava = threading.Lock()  # evita duas gravações simultâneas

TAMANHO_MAX_SUBTAREFA = 120


def buscar_tarefa(id_tarefa):
    """Retorna a tarefa com esse ID (ou None). Chamar dentro de `with trava`."""
    return next((t for t in core.tarefas if t["id"] == id_tarefa), None)


def validar(dados):
    """Aplica as regras de negócio. Retorna (tarefa_limpa, erro)."""
    titulo = str(dados.get("titulo", "")).strip()
    if not titulo:
        return None, "O título é obrigatório."

    prioridade = PRIORIDADES.get(str(dados.get("prioridade", "")).strip().lower())
    if not prioridade:
        return None, "Escolha a prioridade: Alta, Média ou Baixa."

    data_limite = str(dados.get("data_limite", "")).strip()
    if data_limite:
        try:
            datetime.strptime(data_limite, "%d/%m/%Y")
        except ValueError:
            return None, "Data inválida. Use o formato DD/MM/AAAA."

    campos = {
        "titulo": titulo,
        "descricao": str(dados.get("descricao", "")).strip(),
        "prioridade": prioridade,
        "data_limite": data_limite,
    }

    # Status é opcional (usado na edição); no cadastro é sempre "Pendente"
    if "status" in dados:
        if dados["status"] not in STATUS:
            return None, "Status inválido. Use Pendente, Em andamento ou Concluída."
        campos["status"] = dados["status"]

    return campos, None


class Handler(BaseHTTPRequestHandler):
    def _responder(self, codigo, corpo, tipo="application/json; charset=utf-8"):
        if not isinstance(corpo, bytes):
            corpo = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def _ler_json(self):
        """Lê o corpo da requisição como objeto JSON (dict). Retorna None se inválido."""
        try:
            tamanho = int(self.headers.get("Content-Length", 0))
            dados = json.loads(self.rfile.read(tamanho) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return None
        return dados if isinstance(dados, dict) else None

    def do_GET(self):
        if self.path == "/api/tarefas":
            with trava:
                return self._responder(200, core.tarefas)
        if self.path in ("/", "/index.html"):
            with open(os.path.join(PASTA_STATIC, "index.html"), "rb") as f:
                return self._responder(200, f.read(), "text/html; charset=utf-8")
        self._responder(404, {"erro": "Não encontrado."})

    def do_POST(self):
        achou = re.fullmatch(r"/api/tarefas/(\d+)/subtarefas", self.path)
        if achou:
            return self._adicionar_subtarefa(int(achou.group(1)))
        if self.path != "/api/tarefas":
            return self._responder(404, {"erro": "Não encontrado."})
        try:
            tamanho = int(self.headers.get("Content-Length", 0))
            dados = json.loads(self.rfile.read(tamanho) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._responder(400, {"erro": "Requisição inválida."})

        tarefa, erro = validar(dados)
        if erro:
            return self._responder(400, {"erro": erro})

        with trava:
            tarefa["id"] = core.proximo_id
            tarefa["status"] = "Pendente"
            tarefa["subtarefas"] = []
            core.tarefas.append(tarefa)
            core.proximo_id += 1
            core.salvar_tarefas()
        self._responder(201, tarefa)

    def do_PUT(self):
        achou = re.fullmatch(r"/api/tarefas/(\d+)", self.path)
        if not achou:
            return self._responder(404, {"erro": "Não encontrado."})
        id_tarefa = int(achou.group(1))
        try:
            tamanho = int(self.headers.get("Content-Length", 0))
            dados = json.loads(self.rfile.read(tamanho) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._responder(400, {"erro": "Requisição inválida."})

        campos, erro = validar(dados)
        if erro:
            return self._responder(400, {"erro": erro})

        with trava:
            tarefa = next((t for t in core.tarefas if t["id"] == id_tarefa), None)
            if tarefa is None:
                return self._responder(404, {"erro": "Tarefa não encontrada."})
            tarefa.update(campos)  # o ID nunca muda
            core.salvar_tarefas()
        self._responder(200, tarefa)

    def do_DELETE(self):
        achou = re.fullmatch(r"/api/tarefas/(\d+)/subtarefas/(\d+)", self.path)
        if achou:
            return self._remover_subtarefa(int(achou.group(1)), int(achou.group(2)))
        achou = re.fullmatch(r"/api/tarefas/(\d+)", self.path)
        if not achou:
            return self._responder(404, {"erro": "Não encontrado."})
        id_tarefa = int(achou.group(1))

        with trava:
            tarefa = next((t for t in core.tarefas if t["id"] == id_tarefa), None)
            if tarefa is None:
                return self._responder(404, {"erro": "Tarefa não encontrada."})
            core.tarefas.remove(tarefa)
            core.salvar_tarefas()
        self._responder(200, {"id": id_tarefa, "excluida": True})

    def do_PATCH(self):
        achou = re.fullmatch(r"/api/tarefas/(\d+)/subtarefas/(\d+)", self.path)
        if not achou:
            return self._responder(404, {"erro": "Não encontrado."})
        return self._marcar_subtarefa(int(achou.group(1)), int(achou.group(2)))

    # ---------- subtasks ----------
    def _adicionar_subtarefa(self, id_tarefa):
        dados = self._ler_json()
        if dados is None:
            return self._responder(400, {"erro": "Requisição inválida."})
        titulo = str(dados.get("titulo", "")).strip()
        if not titulo:
            return self._responder(400, {"erro": "O título da subtask é obrigatório."})
        if len(titulo) > TAMANHO_MAX_SUBTAREFA:
            return self._responder(
                400, {"erro": f"A subtask pode ter no máximo {TAMANHO_MAX_SUBTAREFA} caracteres."})

        with trava:
            tarefa = buscar_tarefa(id_tarefa)
            if tarefa is None:
                return self._responder(404, {"erro": "Tarefa não encontrada."})
            # setdefault: tarefas antigas (sem o campo) passam a ter a lista
            subtarefas = tarefa.setdefault("subtarefas", [])
            novo_id = max((s["id"] for s in subtarefas), default=0) + 1
            subtarefas.append({"id": novo_id, "titulo": titulo, "concluida": False})
            core.salvar_tarefas()
        self._responder(201, tarefa)

    def _marcar_subtarefa(self, id_tarefa, id_sub):
        dados = self._ler_json()
        if dados is None or not isinstance(dados.get("concluida"), bool):
            return self._responder(400, {"erro": "Informe concluida como true ou false."})

        with trava:
            tarefa = buscar_tarefa(id_tarefa)
            sub = next((x for x in (tarefa or {}).get("subtarefas", []) if x["id"] == id_sub), None)
            if sub is None:
                return self._responder(404, {"erro": "Subtask não encontrada."})
            sub["concluida"] = dados["concluida"]
            core.salvar_tarefas()
        self._responder(200, tarefa)

    def _remover_subtarefa(self, id_tarefa, id_sub):
        with trava:
            tarefa = buscar_tarefa(id_tarefa)
            sub = next((x for x in (tarefa or {}).get("subtarefas", []) if x["id"] == id_sub), None)
            if sub is None:
                return self._responder(404, {"erro": "Subtask não encontrada."})
            tarefa["subtarefas"].remove(sub)
            core.salvar_tarefas()
        self._responder(200, tarefa)

    def log_message(self, *args):  # silencia o log de cada requisição
        pass


def main():
    core.carregar_tarefas()
    servidor = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{'127.0.0.1' if HOST == '0.0.0.0' else HOST}:{PORT}"
    print(f"TaskTracker rodando em {url}  (Ctrl+C para encerrar)")
    if HOST != "0.0.0.0":
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando o TaskTracker. Até logo!")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()