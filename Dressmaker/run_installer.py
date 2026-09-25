import sys
import os
import threading
import time
import webbrowser

# Garante importação correta dos módulos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.backend.server import run_server

PORT = 7890
SERVER_URL = f"http://127.0.0.1:{PORT}"

def start_backend():
    server = run_server(port=PORT)
    server.serve_forever()

def main():
    # Inicia o servidor HTTP em background
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    time.sleep(0.5)

    print("Iniciando interface do instalador...")

    # Tenta abrir como aplicativo nativo de desktop usando pywebview (WebView2 / Edge nativo)
    try:
        import webview
        print("Abrindo janela nativa do instalador (WebView2)...")
        window = webview.create_window(
            title="Dressmaker — Tradução PT-BR (Instalador Oficial)",
            url=SERVER_URL,
            width=640,
            height=720,
            resizable=False,
            frameless=False,
            easy_drag=True,
            background_color="#110e13"
        )
        webview.start()
    except Exception as e:
        print(f"Janela nativa não disponível ({e}). Abrindo no navegador...")
        # Tenta abrir em modo aplicativo no Chrome/Edge
        opened = False
        for browser_cmd in ["msedge --app=", "chrome --app="]:
            try:
                os.system(f"start {browser_cmd}{SERVER_URL}")
                opened = True
                break
            except Exception:
                pass
        
        if not opened:
            webbrowser.open(SERVER_URL)

        print(f"Instalador ativo em: {SERVER_URL}")
        print("Pressione Ctrl+C nesta janela para fechar o instalador.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nInstalador finalizado.")

if __name__ == "__main__":
    main()
