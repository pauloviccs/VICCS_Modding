import os
import json
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import subprocess
from .patcher import ModPatcher

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
TRANSLATIONS_FILE = os.path.join(PROJECT_ROOT, "data", "translations_ptbr.json")

patcher = ModPatcher()

class InstallerHTTPHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status_code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/status":
            self.send_json(patcher.get_status())
            return

        # Serve static files from FRONTEND_DIR
        rel_path = path.lstrip("/")
        if not rel_path or rel_path == "":
            rel_path = "index.html"

        norm_frontend = os.path.normcase(os.path.abspath(FRONTEND_DIR))
        norm_file = os.path.normcase(os.path.abspath(os.path.join(FRONTEND_DIR, rel_path)))

        if not norm_file.startswith(norm_frontend) or not os.path.isfile(norm_file):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        file_path = os.path.join(FRONTEND_DIR, rel_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        req_body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(req_body.decode("utf-8")) if req_body else {}
        except Exception:
            payload = {}

        if path == "/api/set_path":
            new_path = payload.get("path")
            if new_path:
                patcher.game_dir = new_path
            self.send_json(patcher.get_status())
            return

        if path == "/api/select_folder":
            # Abre caixa de seleção de pasta nativa do Windows via PowerShell
            ps_cmd = (
                "[System.Reflection.Assembly]::LoadWithPartialName('System.windows.forms') | Out-Null;"
                "$f = New-Object System.Windows.Forms.FolderBrowserDialog;"
                "$f.Description = 'Selecione a pasta onde o Dressmaker está instalado';"
                "if($f.ShowDialog() -eq 'OK'){ Write-Output $f.SelectedPath }"
            )
            try:
                selected = subprocess.check_output(["powershell", "-Command", ps_cmd], text=True).strip()
                if selected and os.path.isdir(selected):
                    patcher.game_dir = selected
            except Exception as e:
                pass
            self.send_json(patcher.get_status())
            return

        if path == "/api/install":
            try:
                if not os.path.isfile(TRANSLATIONS_FILE):
                    self.send_json({"success": False, "error": "Arquivo translations_ptbr.json não encontrado."}, 500)
                    return

                with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as f:
                    translations = json.load(f)

                manifest = patcher.apply_patch(translations)
                self.send_json({"success": True, "manifest": manifest})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, 500)
            return

        if path == "/api/restore":
            try:
                patcher.restore_original()
                self.send_json({"success": True, "message": "Arquivos originais restaurados com sucesso!"})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, 500)
            return

        if path == "/api/launch":
            try:
                patcher.launch_game()
                self.send_json({"success": True, "message": "Jogo iniciado!"})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, 500)
            return

        self.send_response(404)
        self.end_headers()

def run_server(port=7890):
    server = HTTPServer(("127.0.0.1", port), InstallerHTTPHandler)
    print(f"Servidor do Instalador Dressmaker iniciado em http://127.0.0.1:{port}")
    return server

if __name__ == "__main__":
    server = run_server()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
